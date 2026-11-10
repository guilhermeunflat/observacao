"""Teste das saídas de vídeo e do controlador de video wall 2x2.

Lista os monitores que o Windows enxerga e abre, em cada um, uma tela cheia
com cor e nome. Na saída do video wall (a que mede 1920x1080 e está no HDMI),
desenha os 4 quadrantes com cores e letras diferentes: A (sup. esq.),
B (sup. dir.), C (inf. esq.), D (inf. dir.). Assim você vê qual quadrante
chegou em cada TV de tubo.

Uso:
    python tools/test_screens.py --listar
    python tools/test_screens.py                 # todas as telas
    python tools/test_screens.py --videowall 3   # trata a tela 3 como video wall
Esc fecha.
"""
import argparse

import _caminho  # noqa: F401
import pyglet
from pyglet import shapes

CORES = [(200, 40, 40), (40, 160, 60), (40, 80, 200), (200, 160, 30), (150, 50, 170), (30, 160, 170)]
QUAD = [("A", (220, 30, 30)), ("B", (30, 180, 60)), ("C", (40, 90, 220)), ("D", (230, 190, 20))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--videowall", type=int, default=None, help="índice da tela do video wall")
    a = ap.parse_args()

    telas = pyglet.display.get_display().get_screens()
    for i, s in enumerate(telas):
        print(f"[{i}] {s.width}x{s.height} em ({s.x},{s.y})")
    if a.listar:
        return

    janelas = []
    for i, s in enumerate(telas):
        w = pyglet.window.Window(fullscreen=True, screen=s)
        lote = pyglet.graphics.Batch()
        itens = []
        if i == a.videowall:
            hw, hh = s.width // 2, s.height // 2
            pos = [(0, hh), (hw, hh), (0, 0), (hw, 0)]
            for (letra, cor), (x, y) in zip(QUAD, pos):
                itens.append(shapes.Rectangle(x, y, hw, hh, color=cor, batch=lote))
                itens.append(pyglet.text.Label(letra, font_size=min(hw, hh) // 2, x=x + hw // 2, y=y + hh // 2,
                                               anchor_x="center", anchor_y="center", batch=lote))
            titulo = f"tela {i}: VIDEO WALL"
        else:
            itens.append(shapes.Rectangle(0, 0, s.width, s.height, color=CORES[i % len(CORES)], batch=lote))
            titulo = f"tela {i}"
        itens.append(pyglet.text.Label(f"{titulo}  {s.width}x{s.height}", font_size=28, x=20, y=s.height - 50,
                                       batch=lote))

        def desenhar(w=w, lote=lote):
            w.clear()
            lote.draw()

        def tecla(simbolo, mod):
            if simbolo == pyglet.window.key.ESCAPE:
                pyglet.app.exit()

        w.on_draw = desenhar
        w.on_key_press = tecla
        janelas.append((w, lote, itens))
    pyglet.app.run()


if __name__ == "__main__":
    main()
