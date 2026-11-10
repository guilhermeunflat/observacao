"""Banco de sessões: cada pessoa que passa vira uma pasta com quadros de todas as câmeras.

Enquanto uma pessoa confirmada está na frente das telas, uma thread guarda a
cada `intervalo_s` um quadro de cada câmera (JPEG 320x240) na pasta da sessão.
Quando a pessoa sai, a sessão é fechada (meta.json) e passa a ser "a anterior",
que é o que a próxima pessoa vai ver. Sessões curtas demais são descartadas.

Estrutura em disco:
    bank/sessao_0007/meta.json
    bank/sessao_0007/<camera>/0000.jpg ...

Dados ficam só neste PC. Limpeza manual (apagar a pasta bank/) quando quiser.
"""
import json
import shutil
import threading
import time
from collections import OrderedDict
from pathlib import Path

import cv2

from .config import RAIZ

TAM = (320, 240)


class Sessao:
    def __init__(self, pasta, numero, pessoa=None, inicio=None):
        self.pasta = Path(pasta)
        self.numero = numero
        self.pessoa = pessoa
        self.inicio = inicio or time.time()
        self.fim = None
        self.quadros = OrderedDict()          # camera -> [Path, ...]
        self._lock = threading.Lock()

    @property
    def rotulo(self):
        return f"#{self.numero:03d}"

    def cameras(self):
        with self._lock:
            return [c for c, q in self.quadros.items() if q]

    def lista(self, cam):
        with self._lock:
            return list(self.quadros.get(cam, ()))

    def total(self):
        with self._lock:
            return sum(len(q) for q in self.quadros.values())

    def duracao(self):
        return (self.fim or time.time()) - self.inicio

    def _adicionar(self, cam, caminho):
        with self._lock:
            self.quadros.setdefault(cam, []).append(caminho)

    def salvar_meta(self):
        meta = {"numero": self.numero, "inicio": self.inicio, "fim": self.fim,
                "quadros": {c: [p.name for p in q] for c, q in self.quadros.items()}}
        with open(self.pasta / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f)

    @classmethod
    def ler(cls, pasta):
        with open(pasta / "meta.json", encoding="utf-8") as f:
            m = json.load(f)
        s = cls(pasta, m["numero"], inicio=m["inicio"])
        s.fim = m.get("fim") or m["inicio"]
        for c, nomes in m["quadros"].items():
            s.quadros[c] = [pasta / c / n for n in nomes if (pasta / c / n).exists()]
        return s


class Banco:
    def __init__(self, cfg, cameras, pasta=None):
        b = cfg["app"].get("banco", {})
        self.pasta = Path(pasta) if pasta else RAIZ / b.get("pasta", "bank")
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.intervalo = b.get("intervalo_s", 0.5)
        self.max_quadros = b.get("quadros_por_camera", 40)
        self.min_quadros = b.get("min_quadros", 15)
        self.qualidade = b.get("qualidade_jpeg", 80)
        self.cameras = cameras
        self.sessoes = self._carregar()           # fechadas, mais antiga primeiro
        self.gravando = {}                        # pessoa id -> Sessao
        self._lock = threading.Lock()
        self._rodando = False
        self._ultimo = {}                         # camera -> objeto do último quadro gravado
        self._cache = OrderedDict()               # Path -> frame decodificado

    # ---------- disco ----------
    def _carregar(self):
        ss = []
        for p in sorted(self.pasta.glob("sessao_*")):
            if (p / "meta.json").exists():
                try:
                    s = Sessao.ler(p)
                    if s.total():
                        ss.append(s)
                except (OSError, ValueError, KeyError):
                    pass
            else:
                shutil.rmtree(p, ignore_errors=True)   # sessão interrompida (app fechado no meio)
        return sorted(ss, key=lambda s: s.numero)

    def _proximo_numero(self):
        nums = [s.numero for s in self.sessoes] + [s.numero for s in self.gravando.values()]
        return max(nums, default=0) + 1

    # ---------- API ----------
    def iniciar(self):
        self._rodando = True
        threading.Thread(target=self._loop, name="banco", daemon=True).start()
        return self

    def parar(self):
        self._rodando = False
        with self._lock:
            ids = list(self.gravando)
        for i in ids:
            self.encerrar(i)

    def abrir(self, pessoa_id):
        with self._lock:
            if pessoa_id in self.gravando:
                return self.gravando[pessoa_id]
            n = self._proximo_numero()
            s = Sessao(self.pasta / f"sessao_{n:04d}", n, pessoa=pessoa_id)
            s.pasta.mkdir(parents=True, exist_ok=True)
            self.gravando[pessoa_id] = s
            return s

    def encerrar(self, pessoa_id):
        with self._lock:
            s = self.gravando.pop(pessoa_id, None)
        if s is None:
            return None
        s.fim = time.time()
        if s.total() < self.min_quadros:
            shutil.rmtree(s.pasta, ignore_errors=True)
            return None
        s.salvar_meta()
        with self._lock:
            self.sessoes.append(s)
        return s

    def anterior(self, excluir=()):
        """Última sessão fechada (a pessoa que acabou de sair)."""
        with self._lock:
            for s in reversed(self.sessoes):
                if s not in excluir:
                    return s
        return None

    def todas(self):
        with self._lock:
            return list(self.sessoes)

    def total_pessoas(self):
        with self._lock:
            return len(self.sessoes) + len(self.gravando)

    def ler(self, caminho):
        """Quadro BGR decodificado (com cache pequeno). Mesmo objeto para o mesmo arquivo."""
        f = self._cache.get(caminho)
        if f is not None:
            self._cache.move_to_end(caminho)
            return f
        f = cv2.imread(str(caminho))
        if f is None:
            return None
        self._cache[caminho] = f
        if len(self._cache) > 600:
            self._cache.popitem(last=False)
        return f

    def quadro(self, sessao, cam_i, t, fps=2.0):
        """Quadro da câmera de índice cam_i (circular) da sessão, tocando em loop."""
        cams = sessao.cameras()
        if not cams:
            return None
        lista = sessao.lista(cams[cam_i % len(cams)])
        if not lista:
            return None
        return self.ler(lista[int(t * fps + cam_i * 7) % len(lista)])

    # ---------- gravação ----------
    def _loop(self):
        while self._rodando:
            t0 = time.time()
            with self._lock:
                ativas = list(self.gravando.values())
            if ativas:
                for c in self.cameras:
                    f, idade = c.quadro()
                    if f is None or idade > 2 or f is self._ultimo.get(c.nome):
                        continue
                    self._ultimo[c.nome] = f
                    jpg = None
                    for s in ativas:
                        q = s.lista(c.nome)
                        if len(q) >= self.max_quadros:
                            continue
                        if jpg is None:
                            ok, jpg = cv2.imencode(".jpg", cv2.resize(f, TAM, interpolation=cv2.INTER_AREA),
                                                   [cv2.IMWRITE_JPEG_QUALITY, self.qualidade])
                            if not ok:
                                break
                        d = s.pasta / c.nome
                        d.mkdir(exist_ok=True)
                        p = d / f"{len(q):04d}.jpg"
                        p.write_bytes(jpg.tobytes())
                        s._adicionar(c.nome, p)
            time.sleep(max(0.05, self.intervalo - (time.time() - t0)))
