"""Captura de N webcams em threads, com identidade estável por porta USB.

Cada câmera roda numa thread que guarda só o último quadro (sem fila: o render
sempre quer o mais recente). Se a câmera cai, a thread tenta reabrir a cada
poucos segundos, resolvendo de novo rota_usb -> índice, então trocar uma câmera
por uma reserva na mesma porta não exige reiniciar nada.

Modo simulado (`fake=True`) gera quadros sintéticos: serve para desenvolver e
testar o render sem webcams plugadas.
"""
import threading
import time

import cv2
import numpy as np

from . import devices

# Trava única para tudo que mexe no DirectShow (enumerar, abrir, fechar).
# Em 05/11 o servidor do notebook caiu com corrupção de heap (ntdll 0xc0000374)
# quando várias câmeras reabriram ao mesmo tempo, em threads diferentes,
# enquanto cabos USB eram tirados e recolocados. Ler quadros fica fora da trava.
# Enumerar e abrir sob a mesma trava também evita abrir a câmera errada quando
# a ordem dos índices muda no meio.
DSHOW_LOCK = threading.RLock()


class Camera:
    FPS_MINIMO = 5.0
    SEGUNDOS_LENTA = 5.0
    def __init__(self, nome, rota_usb=None, largura=640, altura=480, fps=15,
                 fourcc="MJPG", fake=False, seed=0):
        self.nome = nome
        self.rota_usb = rota_usb
        self.largura, self.altura, self.fps_pedido = largura, altura, fps
        self.fourcc = fourcc
        self.fake = fake
        self.seed = seed
        self.indice = None
        self._cap = None
        self._lock = threading.Lock()
        self._frame = None
        self._t_frame = 0.0
        self._contagem = 0
        self._t_contagem = time.time()
        self.fps_real = 0.0
        self.status = "parada"
        self.quedas = 0
        self._t_aberta = 0.0
        self._lenta_desde = None
        self._rodando = False
        self._thread = None
        self.exposicao = None  # None = automática
        self.ganho = None
        self._ajustes_pendentes = False

    # ---------- API pública ----------
    def iniciar(self):
        self._rodando = True
        self._thread = threading.Thread(target=self._loop, name=f"cam-{self.nome}", daemon=True)
        self._thread.start()
        return self

    def parar(self):
        self._rodando = False
        if self._thread:
            self._thread.join(timeout=2)
        self._fechar()

    def quadro(self):
        """(frame BGR ou None, idade em segundos)."""
        with self._lock:
            if self._frame is None:
                return None, float("inf")
            return self._frame, time.time() - self._t_frame

    def ajustar(self, exposicao=None, ganho=None):
        self.exposicao, self.ganho = exposicao, ganho
        self._ajustes_pendentes = True

    # ---------- interno ----------
    def _resolver_indice(self):
        if self.rota_usb is None:
            return self.indice
        for d in devices.listar():
            if d["rota_usb"] == self.rota_usb:
                return d["indice"]
        return None

    def _abrir(self):
        if self.fake:
            self.status = "ok (simulada)"
            return True
        with DSHOW_LOCK:
            return self._abrir_travado()

    def _abrir_travado(self):
        idx = self._resolver_indice()
        if idx is None:
            self.status = "não encontrada"
            return False
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            self.status = "falha ao abrir"
            return False
        # Ordem importa no DSHOW: resolução ANTES do FOURCC, senão a câmera
        # fica em YUY2 (sem compressão, ~147 Mb/s a 640x480) e só cabem 2 por tubo.
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.largura)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.altura)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.fourcc))
        # NÃO pedir CAP_PROP_FPS: no DSHOW isso reverte o formato para YUY2.
        # A webcam Sunplus 1bcf:2281 só oferece MJPEG a 30 fps de qualquer jeito.
        f = int(cap.get(cv2.CAP_PROP_FOURCC)) & 0xFFFFFFFF
        self.fourcc_real = f.to_bytes(4, "little").decode("ascii", "replace")
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self._cap, self.indice = cap, idx
        self._t_aberta = time.time()
        self._lenta_desde = None
        self._aplicar_ajustes()
        self.status = "ok"
        return True

    def _aplicar_ajustes(self):
        self._ajustes_pendentes = False
        if self._cap is None:
            return
        with DSHOW_LOCK:
            self._aplicar_ajustes_travado()

    def _aplicar_ajustes_travado(self):
        if self.exposicao is None:
            self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # DSHOW: 0.75 = auto
        else:
            self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            self._cap.set(cv2.CAP_PROP_EXPOSURE, float(self.exposicao))
        if self.ganho is not None:
            self._cap.set(cv2.CAP_PROP_GAIN, float(self.ganho))

    def _fechar(self):
        if self._cap is not None:
            with DSHOW_LOCK:
                self._cap.release()
            self._cap = None

    def _ler_fake(self):
        t = time.time()
        rng = np.random.default_rng(self.seed)
        base = rng.integers(40, 200, size=3).tolist()
        img = np.full((self.altura, self.largura, 3), base, np.uint8)
        cx = int(self.largura / 2 + np.sin(t * 0.7 + self.seed) * self.largura * 0.3)
        cy = int(self.altura / 2 + np.cos(t * 0.5 + self.seed) * self.altura * 0.2)
        cv2.circle(img, (cx, cy), self.altura // 5, (230, 230, 230), -1)
        cv2.putText(img, self.nome, (12, 36), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        cv2.putText(img, time.strftime("%H:%M:%S"), (12, self.altura - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        time.sleep(1.0 / self.fps_pedido)
        return True, img

    def _loop(self):
        falhas_seguidas = 0
        while self._rodando:
            if self._cap is None and not self.fake:
                if not self._abrir():
                    time.sleep(3)
                    continue
            elif self.fake and self.status == "parada":
                self._abrir()
            if self._ajustes_pendentes:
                self._aplicar_ajustes()
            ok, img = self._ler_fake() if self.fake else self._cap.read()
            if not ok or img is None:
                falhas_seguidas += 1
                if falhas_seguidas > 30:
                    self.quedas += 1
                    self.status = "caiu, reabrindo"
                    self._fechar()
                    falhas_seguidas = 0
                    time.sleep(1)
                continue
            falhas_seguidas = 0
            agora = time.time()
            with self._lock:
                self._frame, self._t_frame = img, agora
            self._contagem += 1
            if agora - self._t_contagem >= 1.0:
                self.fps_real = self._contagem / (agora - self._t_contagem)
                self._contagem, self._t_contagem = 0, agora
                if self.status.startswith("caiu") or self.status.startswith("lenta"):
                    self.status = "ok"
                # Vigia: quando outra câmera entra ou sai do mesmo controlador,
                # as que estavam transmitindo podem travar em ~1 fps sem dar erro
                # (visto no notebook em 05/11). Pouca luz derruba no máximo para
                # ~16 fps, então abaixo de FPS_MINIMO por SEGUNDOS_LENTA = reabrir.
                if not self.fake and agora - self._t_aberta > 8:
                    if self.fps_real < self.FPS_MINIMO:
                        if self._lenta_desde is None:
                            self._lenta_desde = agora
                        elif agora - self._lenta_desde > self.SEGUNDOS_LENTA:
                            self.quedas += 1
                            self.status = f"lenta ({self.fps_real:.1f} fps), reabrindo"
                            self._fechar()
                            self._lenta_desde = None
                            time.sleep(1)
                    else:
                        self._lenta_desde = None


def _abrir_dshow(indice, largura, altura, fourcc="MJPG"):
    cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        return None
    # resolução ANTES do FOURCC, e nunca pedir fps (volta para YUY2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
    return cap


class CameraFoto:
    """Câmera do rodízio: não fica aberta; guarda as últimas fotos que tirou.

    Tem a mesma interface de leitura de Camera (nome, quadro(), status,
    fps_real, exposicao), para a grade do operador e o render tratarem igual.
    Aqui fps_real = visitas no último minuto.
    """

    def __init__(self, nome, rota_usb, largura, altura, papel="foto"):
        self.nome, self.rota_usb = nome, rota_usb
        self.largura, self.altura = largura, altura
        self.papel = papel
        self._lock = threading.Lock()
        self.fotos = []          # [(t, frame)] da última visita
        self._t = 0.0
        self.visitas = 0
        self.falhas = 0
        self.status = "aguardando"
        self.exposicao = None
        self.ganho = None
        self.fps_real = 0.0
        self._t_visitas = []

    def quadro(self):
        with self._lock:
            if not self.fotos:
                return None, float("inf")
            return self.fotos[-1][1], time.time() - self._t

    def ultimas_fotos(self):
        with self._lock:
            return list(self.fotos)

    def ajustar(self, exposicao=None, ganho=None):
        self.exposicao, self.ganho = exposicao, ganho

    def _registrar(self, fotos):
        agora = time.time()
        with self._lock:
            self.fotos, self._t = fotos, agora
        self.visitas += 1
        self._t_visitas = [t for t in self._t_visitas if agora - t < 60] + [agora]
        self.fps_real = float(len(self._t_visitas))

    def iniciar(self):
        return self

    def parar(self):
        pass


class Rodizio:
    """N vagas abertas por vez, revezando um grupo de CameraFoto.

    Cada vaga: abre a próxima câmera da fila, descarta alguns quadros (a
    exposição automática precisa assentar), tira uma rajada de fotos, fecha.
    Todas as câmeras do grupo devem estar no MESMO controlador USB, e as vagas
    não podem passar do limite dele (2 webcams abertas por controlador).
    """

    def __init__(self, cams, vagas=2, descartar=12, fotos=3, intervalo=0.15, fourcc="MJPG"):
        self.cams = cams
        self.vagas = vagas
        self.descartar, self.n_fotos, self.intervalo = descartar, fotos, intervalo
        self.fourcc = fourcc
        self._fila_lock = threading.Lock()
        self._fila_i = 0
        self._ocupadas = set()
        self._rodando = False
        self._threads = []
        self.ciclo_s = 0.0       # tempo médio para revisitar a mesma câmera

    def _proxima(self):
        with self._fila_lock:
            for _ in range(len(self.cams)):
                c = self.cams[self._fila_i % len(self.cams)]
                self._fila_i += 1
                if c.nome not in self._ocupadas:
                    self._ocupadas.add(c.nome)
                    return c
        return None

    def _liberar(self, c):
        with self._fila_lock:
            self._ocupadas.discard(c.nome)

    def _visitar(self, c):
        t0 = time.time()
        with DSHOW_LOCK:
            idx = None
            for d in devices.listar():
                if d["rota_usb"] == c.rota_usb:
                    idx = d["indice"]
                    break
            cap = None if idx is None else _abrir_dshow(idx, c.largura, c.altura, self.fourcc)
            if cap is not None and c.exposicao is not None:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
                cap.set(cv2.CAP_PROP_EXPOSURE, float(c.exposicao))
        if idx is None:
            c.status = "não encontrada"
            c.falhas += 1
            time.sleep(1)
            return
        if cap is None:
            c.status = "falha ao abrir"
            c.falhas += 1
            time.sleep(1)
            return
        try:
            lidos = 0
            while lidos < self.descartar and time.time() - t0 < 6:
                ok, _ = cap.read()
                lidos += bool(ok)
            fotos = []
            for _ in range(self.n_fotos):
                ok, f = cap.read()
                if ok and f is not None:
                    fotos.append((time.time(), f))
                time.sleep(self.intervalo)
            if fotos:
                c._registrar(fotos)
                c.status = f"ok ({time.time() - t0:.1f} s/visita)"
            else:
                c.status = "sem imagem"
                c.falhas += 1
        finally:
            with DSHOW_LOCK:
                cap.release()

    def _loop(self):
        while self._rodando:
            c = self._proxima()
            if c is None:
                time.sleep(0.2)
                continue
            try:
                self._visitar(c)
            finally:
                self._liberar(c)
            vpm = sum(x.fps_real for x in self.cams)
            if vpm:
                self.ciclo_s = 60.0 * len(self.cams) / vpm

    def iniciar(self):
        self._rodando = True
        for i in range(self.vagas):
            t = threading.Thread(target=self._loop, name=f"rodizio-{i}", daemon=True)
            t.start()
            self._threads.append(t)
            time.sleep(0.5)
        return self

    def parar(self):
        self._rodando = False
        for t in self._threads:
            t.join(timeout=8)


class CameraRemota:
    """Lê uma câmera servida pelo notebook (observacao.servidor) via HTTP MJPEG."""

    SOI, EOI = bytes([0xFF, 0xD8]), bytes([0xFF, 0xD9])

    def __init__(self, nome, url, papel="olho"):
        self.nome, self.url, self.papel = nome, url, papel
        self._lock = threading.Lock()
        self._frame, self._t = None, 0.0
        self.status = "parada"
        self.fps_real = 0.0
        self.exposicao = None
        self.ganho = None
        self.quedas = 0
        self._rodando = False

    def quadro(self):
        with self._lock:
            if self._frame is None:
                return None, float("inf")
            return self._frame, time.time() - self._t

    def ajustar(self, exposicao=None, ganho=None):
        self.exposicao, self.ganho = exposicao, ganho

    def iniciar(self):
        self._rodando = True
        threading.Thread(target=self._loop, name=f"remota-{self.nome}", daemon=True).start()
        return self

    def parar(self):
        self._rodando = False

    def _loop(self):
        import urllib.request
        while self._rodando:
            try:
                with urllib.request.urlopen(self.url, timeout=5) as r:
                    self.status = "ok (remota)"
                    buf = b""
                    n, t_n = 0, time.time()
                    while self._rodando:
                        pedaco = r.read(16384)
                        if not pedaco:
                            raise ConnectionError("fim do stream")
                        buf += pedaco
                        while True:
                            a = buf.find(self.SOI)
                            if a == -1:
                                buf = b""
                                break
                            b = buf.find(self.EOI, a + 2)
                            if b == -1:
                                buf = buf[a:]
                                break
                            jpg, buf = buf[a:b + 2], buf[b + 2:]
                            img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
                            if img is not None:
                                with self._lock:
                                    self._frame, self._t = img, time.time()
                                n += 1
                        if time.time() - t_n >= 1:
                            self.fps_real, n, t_n = n / (time.time() - t_n), 0, time.time()
            except Exception as e:
                self.quedas += 1
                self.status = f"sem conexão ({type(e).__name__})"
                time.sleep(2)


class Captura:
    """Conjunto de câmeras montado a partir de config/cameras.json.

    Papéis: master (tracking, fixa), video (fixa), olho (fixa), foto (rodízio),
    reserva (ignorada). Câmera com campo "remota" (URL) vem do notebook.
    """

    def __init__(self, cfg, fake=0, incluir_reservas=False):
        cap = cfg["app"]["captura"]
        rod = cfg["app"].get("rodizio", {})
        self.cameras = []
        self.rodizios = []
        if fake:
            for i in range(fake):
                self.cameras.append(Camera(f"sim{i:02d}", largura=cap["largura"], altura=cap["altura"],
                                           fps=cap["fps"], fake=True, seed=i))
            return
        fotos = []
        for c in cfg["cameras"].get("cameras", []):
            papel = c.get("papel", "olho")
            if papel == "reserva" and not incluir_reservas:
                continue
            larg, alt = c.get("largura", cap["largura"]), c.get("altura", cap["altura"])
            if c.get("remota"):
                cam = CameraRemota(c["nome"], c["remota"], papel)
            elif papel == "foto":
                cam = CameraFoto(c["nome"], c["rota_usb"], larg, alt)
                fotos.append(cam)
            else:
                cam = Camera(c["nome"], rota_usb=c["rota_usb"], largura=larg, altura=alt,
                             fps=c.get("fps", cap["fps"]), fourcc=cap.get("fourcc", "MJPG"))
                cam.papel = papel
            cam.ajustar(c.get("exposicao"), c.get("ganho"))
            self.cameras.append(cam)
        if fotos:
            self.rodizios.append(Rodizio(fotos, vagas=rod.get("vagas", 2),
                                         descartar=rod.get("quadros_descartados", 12),
                                         fotos=rod.get("fotos_por_visita", 3),
                                         intervalo=rod.get("intervalo_fotos_s", 0.15),
                                         fourcc=cap.get("fourcc", "MJPG")))

    def iniciar(self, intervalo=0.3):
        # Abrir em sequência, com intervalo: abrir várias UVC ao mesmo tempo
        # costuma travar o driver.
        for c in self.cameras:
            c.iniciar()
            if isinstance(c, Camera):
                time.sleep(intervalo)
        for r in self.rodizios:
            r.iniciar()
        return self

    def parar(self):
        for r in self.rodizios:
            r.parar()
        for c in self.cameras:
            c.parar()

    def por_nome(self, nome):
        return next((c for c in self.cameras if c.nome == nome), None)

    def por_papel(self, papel):
        return [c for c in self.cameras if getattr(c, "papel", "olho") == papel]
