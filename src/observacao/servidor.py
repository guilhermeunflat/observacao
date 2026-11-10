"""Servidor de câmeras do notebook: entrega as webcams dele ao PC pela rede.

Roda no notebook, com a mesma pasta do projeto. Usa o perfil "notebook"
(config/profiles/notebook.json -> config/cameras_notebook.json), então as
câmeras do notebook são cadastradas lá com tools/calibrate_cameras.py
--perfil notebook, como no PC. Fixas e rodízio funcionam igual.

Endereços:
    http://<ip-do-notebook>:8765/lista          JSON com as câmeras
    http://<ip-do-notebook>:8765/cam/<nome>     stream MJPEG da câmera

No PC, cada câmera remota entra em config/cameras.json assim:
    {"nome": "nb_01", "papel": "olho", "remota": "http://192.168.0.20:8765/cam/nb_01"}

Uso (no notebook):
    python -m observacao.servidor
    python -m observacao.servidor --fake 3      # teste sem webcams
"""
import argparse
import json
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cv2

from . import config
from .capture import Captura

FRONTEIRA = b"quadro"


def ips_locais():
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ips.add(info[4][0])
    except OSError:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    return sorted(i for i in ips if not i.startswith("127."))


def criar_handler(captura, qualidade, fps_envio=15):
    por_nome = {c.nome: c for c in captura.cameras}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path in ("/", "/lista"):
                corpo = json.dumps([{"nome": c.nome, "papel": getattr(c, "papel", "olho"),
                                     "status": c.status, "fps": round(c.fps_real, 1)}
                                    for c in captura.cameras], ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
                return
            if self.path.startswith("/cam/"):
                cam = por_nome.get(self.path[5:])
                if cam is None:
                    self.send_error(404, "câmera desconhecida")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=" + FRONTEIRA.decode())
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                ultimo = None
                try:
                    while True:
                        f, idade = cam.quadro()
                        if f is not None and f is not ultimo:
                            ultimo = f
                            ok, jpg = cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, qualidade])
                            if ok:
                                dados = jpg.tobytes()
                                self.wfile.write(b"--" + FRONTEIRA + b"\r\nContent-Type: image/jpeg\r\n"
                                                 + f"Content-Length: {len(dados)}\r\n\r\n".encode() + dados + b"\r\n")
                        time.sleep(1 / fps_envio)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    return
            self.send_error(404)

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil", default="notebook")
    ap.add_argument("--fake", type=int, default=0)
    ap.add_argument("--porta", type=int, default=None)
    a = ap.parse_args()

    cfg = config.carregar(a.perfil)
    rem = cfg["app"].get("remotas", {})
    porta = a.porta or rem.get("porta", 8765)
    captura = Captura(cfg, fake=a.fake)
    if not captura.cameras:
        print("Nenhuma câmera cadastrada neste perfil. Rode tools/calibrate_cameras.py --perfil notebook.")
        return
    captura.iniciar()
    srv = ThreadingHTTPServer(("0.0.0.0", porta), criar_handler(captura, rem.get("qualidade_jpeg", 70),
                                                                rem.get("fps_envio", 15)))
    print(f"Servindo {len(captura.cameras)} câmera(s) na porta {porta}.")
    for ip in ips_locais():
        print(f"  no PC, use: http://{ip}:{porta}/cam/<nome>   (lista: http://{ip}:{porta}/lista)")
    for c in captura.cameras:
        print(f"  - {c.nome} ({getattr(c, 'papel', 'olho')})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        captura.parar()


if __name__ == "__main__":
    main()
