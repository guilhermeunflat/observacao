"""Letreiros: o texto de cada tela, com troca a cada N segundos e fade.

Três estilos:
    "tela"     tela que ninguém está olhando de frente: frase grande, centralizada.
    "legenda"  tela 3D: faixa estreita embaixo, como legenda de câmera de segurança.
    "arquivo"  modo 4+: frase enorme sobre o mural, com faixa escura atrás.

Fonte e cores são provisórias (Consolas, verde CCTV) até a identidade visual.
"""
import pyglet

FONTE = "Consolas"
COR = (150, 255, 170)
COR_FONTE = (110, 160, 120)
FADE = 0.7
PT_POR_PX = 72 / 96


class Letreiro:
    def __init__(self, intervalo=8.0, atraso=0.0):
        self.intervalo = intervalo
        self.texto, self.fonte = "", ""
        self.t = -1e9
        self.atraso = atraso                      # telas não trocam todas ao mesmo tempo
        self.estilo = None
        self.lbl = pyglet.text.Label("", font_name=FONTE, multiline=True, width=100,
                                     anchor_x="center", anchor_y="center", align="center")
        self.lbl_fonte = pyglet.text.Label("", font_name=FONTE, anchor_x="center", anchor_y="top")
        self.faixa = pyglet.shapes.Rectangle(0, 0, 1, 1, color=(0, 0, 0, 200))

    def talvez_trocar(self, agora, escolher, estilo):
        if estilo != self.estilo:                 # mudou de papel: troca já
            self.estilo = estilo
            self.t = -1e9
        if agora - self.t >= self.intervalo:
            self.texto, self.fonte = escolher()
            primeira = self.t < 0
            self.t = agora - (self.atraso if primeira else 0.0)   # desencontra as telas

    def _alfa(self, agora):
        v = agora - self.t
        return max(0.0, min(1.0, v / FADE, (self.intervalo - v) / FADE))

    def desenhar(self, x, y, w, h, agora):
        """x, y, w, h em coordenadas da janela (não do framebuffer)."""
        if not self.texto:
            return
        a = int(255 * self._alfa(agora))
        L, F = self.lbl, self.lbl_fonte
        if self.estilo == "legenda":
            px = max(9, h * 0.032)
            L.font_size = px * PT_POR_PX
            L.width = int(w * 0.92)
            L.x, L.y = x + w // 2, y + int(px * 2.2)
            self.faixa.x, self.faixa.y, self.faixa.width, self.faixa.height = x, y, w, int(px * 4.4)
            self.faixa.opacity = int(170 * a / 255)
            self.faixa.draw()
            L.text, L.color = self.texto, (*COR, a)
            L.draw()
            return
        grande = self.estilo == "arquivo"
        px = max(12, min(w, h) * (0.085 if grande else 0.06))
        L.font_size = px * PT_POR_PX
        L.width = int(w * 0.86)
        L.x, L.y = x + w // 2, y + h // 2
        L.text, L.color = self.texto, (*COR, a)
        if grande:
            alt = min(h, L.content_height + px * 2.5)
            self.faixa.x, self.faixa.y, self.faixa.width, self.faixa.height = x, y + (h - alt) / 2, w, alt
            self.faixa.opacity = int(210 * a / 255)
            self.faixa.draw()
        L.draw()
        if self.fonte and self.fonte != "sistema":
            F.font_size = max(7, px * 0.38) * PT_POR_PX
            F.text, F.color = self.fonte, (*COR_FONTE, a)
            F.x, F.y = x + w // 2, L.y - L.content_height / 2 - px * 0.5
            F.draw()
