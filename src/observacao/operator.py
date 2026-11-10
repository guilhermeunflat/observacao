"""Janela do operador: grade de todas as câmeras com fps/status, ajuste de
exposição por câmera e o mosaico 2D de teste.

Uso:
    python -m observacao.operator                # câmeras de config/cameras.json
    python -m observacao.operator --fake 15      # 15 câmeras simuladas
    python -m observacao.operator --reservas     # inclui as reservas

Teclas:
    Tab / Shift+Tab ou [ ]   seleciona câmera
    + / -                    exposição da selecionada (manual)
    a                        exposição automática na selecionada
    s                        salva exposições em cameras.json
    m                        alterna grade / mosaico
    q ou Esc                 sai
"""
import argparse
import math
import time

import cv2
import numpy as np

from . import config
from .capture import Captura
from .mosaico import Mosaico

W, H = 1600, 900


def grade(cams, sel):
    n = max(len(cams), 1)
    cols = math.ceil(math.sqrt(n * W / H))
    rows = math.ceil(n / cols)
    cw, ch = W // cols, H // rows
    canvas = np.zeros((H, W, 3), np.uint8)
    for i, c in enumerate(cams):
        r, k = divmod(i, cols)
        x, y = k * cw, r * ch
        f, idade = c.quadro()
        if f is not None:
            canvas[y:y + ch, x:x + cw] = cv2.resize(f, (cw, ch))
        foto = getattr(c, "papel", "") == "foto"
        velha = idade > (30 if foto else 2)
        if f is None or velha:
            cv2.rectangle(canvas, (x, y), (x + cw - 1, y + ch - 1), (0, 0, 160), -1 if f is None else 3)
        cor = (0, 255, 255) if i == sel else (255, 255, 255)
        exp = "auto" if c.exposicao is None else f"exp {c.exposicao:g}"
        papel = getattr(c, "papel", "")
        if foto:
            txt = f"{c.nome}  FOTO  ha {idade:3.0f} s  {c.fps_real:.0f}/min"
        else:
            txt = f"{c.nome}  {papel}  {c.fps_real:4.1f} fps  {exp}"
        cv2.rectangle(canvas, (x, y), (x + cw - 1, y + 22), (0, 0, 0), -1)
        cv2.putText(canvas, txt, (x + 6, y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, cor, 1)
        if not c.status.startswith("ok"):
            cv2.putText(canvas, c.status, (x + 6, y + ch // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        if i == sel:
            cv2.rectangle(canvas, (x, y), (x + cw - 1, y + ch - 1), (0, 255, 255), 2)
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil", default="casa")
    ap.add_argument("--fake", type=int, default=0)
    ap.add_argument("--reservas", action="store_true")
    a = ap.parse_args()

    cfg = config.carregar(a.perfil)
    cap = Captura(cfg, fake=a.fake, incluir_reservas=a.reservas)
    if not cap.cameras:
        print("Nenhuma câmera cadastrada. Rode tools/calibrate_cameras.py ou use --fake 15.")
        return
    cap.iniciar()
    cams = cap.cameras
    mos = Mosaico(len(cams), W, H)
    sel, modo, t_ant = 0, "grade", time.time()
    cv2.namedWindow("operador", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("operador", W, H)
    try:
        while True:
            agora = time.time()
            dt, t_ant = agora - t_ant, agora
            if modo == "grade":
                img = grade(cams, sel)
            else:
                img = mos.desenhar([c.quadro()[0] for c in cams], dt)
            vivas = sum(1 for c in cams if getattr(c, "papel", "") != "foto" and c.quadro()[1] < 2)
            n_vivas = sum(1 for c in cams if getattr(c, "papel", "") != "foto")
            ciclo = "  ".join(f"rodizio {len(r.cams)} cams / {r.vagas} vagas, ciclo {r.ciclo_s:.1f} s" for r in cap.rodizios)
            rodape = f"{vivas}/{n_vivas} ao vivo | {ciclo} | perfil {cfg['perfil']} | Tab sel  +/- exp  a auto  s salva  m modo  q sai"
            cv2.putText(img, rodape, (10, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.imshow("operador", img)
            k = cv2.waitKeyEx(15)
            if k in (ord("q"), 27):
                break
            if k in (9, ord("]")):
                sel = (sel + 1) % len(cams)
            elif k in (ord("["), 0x10000 | 9):
                sel = (sel - 1) % len(cams)
            elif k in (ord("+"), ord("=")):
                c = cams[sel]
                c.ajustar(min((c.exposicao if c.exposicao is not None else -6) + 1, 0), c.ganho)
            elif k == ord("-"):
                c = cams[sel]
                c.ajustar(max((c.exposicao if c.exposicao is not None else -6) - 1, -13), c.ganho)
            elif k == ord("a"):
                cams[sel].ajustar(None, cams[sel].ganho)
            elif k == ord("m"):
                modo = "mosaico" if modo == "grade" else "grade"
            elif k == ord("s") and not a.fake:
                por_nome = {c.nome: c for c in cams}
                for e in cfg["cameras"]["cameras"]:
                    if e["nome"] in por_nome:
                        e["exposicao"] = por_nome[e["nome"]].exposicao
                config.salvar_cameras(cfg)
                print("exposições salvas")
    finally:
        cap.parar()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
