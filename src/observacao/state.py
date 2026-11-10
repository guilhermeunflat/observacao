"""Quem está na frente, quem vê quem, e qual tela é de quem.

Regras (plano, decisões de 28/10 e 05/11):
    0 pessoas  -> "vazio": as telas mostram a última pessoa que passou, com o olho à deriva.
    1 pessoa   -> vê a anterior (a última sessão fechada do banco).
    2 pessoas  -> A vê B e B vê A (o que está sendo gravado agora).
    3 pessoas  -> anel, ordenado da esquerda para a direita: 1 vê 2, 2 vê 3, 3 vê 1.
    4+ pessoas -> "arquivo": sem 3D, texto grande e mural de todo mundo que passou.
                  Volta ao normal quando ficam 3 ou menos por `saida_arquivo_s`.

Telas: cada tela é de quem está mais de frente para ela (ângulo entre a
normal da tela e a direção da pessoa). Tela que ninguém está de frente vira
tela de texto. Uma tela só troca de dono se o outro estiver claramente mais
de frente (histerese), para não piscar.
"""
import math
import time

import numpy as np

from .render.projection import cantos_tela

ANGULO_MAX = 72.0         # graus: mais de lado que isso, a tela não é de ninguém
HISTERESE = 0.12          # diferença de cosseno para uma tela mudar de dono
MIN_QUADROS_OUTRO = 8     # sessão em andamento com menos que isso ainda não serve para mostrar


class Estado:
    def __init__(self, cfg, banco, telas):
        t = cfg["app"].get("estado", {})
        self.entrada_arquivo = t.get("pessoas_arquivo", 4)
        self.saida_arquivo_s = t.get("saida_arquivo_s", 3.0)
        self.banco = banco
        self.telas = []
        for tela in telas:
            pa, pb, pc = cantos_tela(tela)
            n = np.cross(pb - pa, pc - pa)
            self.telas.append((tela["id"], (pb + pc) / 2, n / np.linalg.norm(n)))
        self.dono = {tid: None for tid, _, _ in self.telas}
        self.slots = {}                 # pessoa id -> 0..2 (qual cena 3D ela usa)
        self.modo = "vazio"
        self._t_poucos = None
        self.quantas = 0

    def _slot(self, pid, vivos):
        for p in list(self.slots):
            if p not in vivos:
                del self.slots[p]
        if pid not in self.slots:
            livres = [s for s in range(3) if s not in self.slots.values()]
            self.slots[pid] = livres[0] if livres else 0
        return self.slots[pid]

    def _modo(self, n, agora):
        if n >= self.entrada_arquivo:
            self._t_poucos = None
            return "arquivo"
        if self.modo == "arquivo":
            if self._t_poucos is None:
                self._t_poucos = agora
            if agora - self._t_poucos < self.saida_arquivo_s:
                return "arquivo"
        self._t_poucos = None
        return "pessoas" if n else "vazio"

    def atualizar(self, pessoas):
        """pessoas = Tracker.estado(). Devolve o que cada tela deve mostrar."""
        agora = time.time()
        vivos = {p["id"] for p in pessoas}
        # banco: abre sessão para quem chegou, fecha para quem saiu
        for p in pessoas:
            self.banco.abrir(p["id"])
        for pid in list(self.banco.gravando):
            if pid not in vivos:
                self.banco.encerrar(pid)
        self.quantas = len(pessoas)
        self.modo = self._modo(len(pessoas), agora)

        if self.modo == "arquivo":
            self.dono = {tid: None for tid in self.dono}
            return {"modo": "arquivo", "pessoas": [], "telas": dict(self.dono)}

        # quem vê quem
        ordem = sorted(pessoas, key=lambda p: p["x"])
        n = len(ordem)
        vistas = []
        for i, p in enumerate(ordem):
            propria = self.banco.gravando.get(p["id"])
            alvo = None
            if n >= 2:
                outro = self.banco.gravando.get(ordem[(i + 1) % n]["id"])
                if outro is not None and outro.total() >= MIN_QUADROS_OUTRO:
                    alvo = outro
            if alvo is None:
                alvo = self.banco.anterior(excluir=[propria])
            vistas.append({**p, "alvo": alvo, "propria": propria, "slot": self._slot(p["id"], vivos)})

        # dono de cada tela
        cos_max = math.cos(math.radians(ANGULO_MAX))
        for tid, c, nrm in self.telas:
            notas = {}
            for p in vistas:
                v = np.array([p["x"], p["y"], p["z"]]) - c
                d = float(v @ nrm)
                if d > 15:
                    notas[p["id"]] = d / float(np.linalg.norm(v))
            atual = self.dono.get(tid)
            if not notas:
                self.dono[tid] = None
                continue
            melhor = max(notas, key=notas.get)
            if notas[melhor] < cos_max:
                self.dono[tid] = None
            elif atual in notas and notas[atual] >= cos_max and notas[melhor] - notas[atual] < HISTERESE:
                pass
            else:
                self.dono[tid] = melhor
        if self.modo == "vazio":
            self.dono = {tid: "vazio" for tid in self.dono}
        return {"modo": self.modo, "pessoas": vistas, "telas": dict(self.dono)}
