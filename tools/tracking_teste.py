"""Janela de teste do tracking: imagens das masters + mapa visto de cima.

Verde = rosto aceito; vermelho = ignorado (fora da distância ou estático,
como estampa ou cartaz). No mapa: as telas de screens.json em cinza e cada
pessoa com número, posição (x, y, z) em cm e há quanto tempo está ali.
Cinza claro = candidata (ainda não completou o tempo de entrada).

Uso:
    python tools/tracking_teste.py
Teclas: q sai.
"""
import argparse
import math

import cv2
import numpy as np

import _caminho  # noqa: F401
from observacao import config
from observacao.capture import Captura
from observacao.tracker import Tracker

MAPA_W, MAPA_H = 560, 480
CORES = [(0, 200, 255), (255, 120, 0), (180, 0, 255), (0, 255, 120), (255, 0, 120)]


def para_mapa(x, z):
    # x -200..200 cm -> 0..W ; z 0..320 cm -> topo..baixo (tela no topo)
    return int(MAPA_W / 2 + x * (MAPA_W / 400)), int(30 + z * ((MAPA_H - 50) / 320))


def mapa(tracker, telas):
    img = np.full((MAPA_H, MAPA_W, 3), 25, np.uint8)
    for z in range(0, 321, 50):
        cv2.line(img, para_mapa(-200, z), para_mapa(200, z), (45, 45, 45), 1)
        cv2.putText(img, f"{z}", (4, para_mapa(0, z)[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (90, 90, 90), 1)
    for t in telas:
        cx, _, cz = t["centro_cm"]
        meia = t["largura_cm"] / 2
        if t.get("rotacao") in (90, 270):
            meia = min(t["largura_cm"], t["altura_cm"]) / 2
        yaw = math.radians(t.get("yaw", 0))
        dx, dz = math.cos(yaw) * meia, -math.sin(yaw) * meia
        cv2.line(img, para_mapa(cx - dx, cz - dz), para_mapa(cx + dx, cz + dz), (150, 150, 150), 3)
        cv2.putText(img, t["id"], para_mapa(cx - dx, cz - dz - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
    for m in tracker.modelos.values():
        p = para_mapa(m.pos[0], m.pos[2])
        cv2.circle(img, p, 4, (255, 255, 255), -1)
        fim = m.pos + m.f * 40
        cv2.line(img, p, para_mapa(fim[0], fim[2]), (255, 255, 255), 1)
        cv2.putText(img, m.nome, (p[0] + 5, p[1] + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
    for pe in tracker.todas():
        cor = CORES[pe["id"] % len(CORES)] if pe["confirmada"] else (110, 110, 110)
        p = para_mapa(pe["x"], pe["z"])
        cv2.circle(img, p, 10, cor, -1)
        cv2.putText(img, str(pe["id"]), (p[0] - 5, p[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(img, f"x{pe['x']:.0f} y{pe['y']:.0f} z{pe['z']:.0f}  {pe['segundos']:.0f}s",
                    (p[0] + 14, p[1] + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, cor, 1)
    n = len(tracker.estado())
    cv2.putText(img, f"pessoas: {n}   tracker {tracker.hz:.0f} Hz", (10, MAPA_H - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil", default="casa")
    a = ap.parse_args()
    cfg = config.carregar(a.perfil)
    cap = Captura(cfg)
    masters = cap.por_papel("master")
    if not masters:
        print("Nenhuma câmera com papel master em cameras.json.")
        return
    cap.cameras, cap.rodizios = masters, []
    cap.iniciar()
    tracker = Tracker(cfg, masters).iniciar()
    cv2.namedWindow("tracking", cv2.WINDOW_NORMAL)
    try:
        while True:
            vistas = []
            for m in masters:
                f, _ = m.quadro()
                f = np.zeros((480, 640, 3), np.uint8) if f is None else f.copy()
                for d in tracker.ultimas_deteccoes.get(m.nome, []):
                    x, y, w, h = d.caixa
                    cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(f, f"{d.dist:.0f}cm", (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                for d in tracker.ignoradas.get(m.nome, []):
                    x, y, w, h = d.caixa
                    cv2.rectangle(f, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(f, m.nome, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                vistas.append(cv2.resize(f, (480, 360)))
            col = np.vstack(vistas) if len(vistas) > 1 else vistas[0]
            m = mapa(tracker, cfg["telas"]["telas"])
            h = max(col.shape[0], m.shape[0])
            col = cv2.copyMakeBorder(col, 0, h - col.shape[0], 0, 0, cv2.BORDER_CONSTANT)
            m = cv2.copyMakeBorder(m, 0, h - m.shape[0], 0, 0, cv2.BORDER_CONSTANT)
            cv2.imshow("tracking", np.hstack([col, m]))
            if cv2.waitKey(15) & 0xFF in (ord("q"), 27):
                break
    finally:
        tracker.parar()
        cap.parar()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
