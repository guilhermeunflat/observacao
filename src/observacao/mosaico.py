"""Mosaico 2D de cacos: recortes de câmeras diferentes espalhados numa tela.

É o teste visual da Fase 1 e o gerador de "cacos" que o render 3D vai usar
(cada caco = câmera de origem + retângulo de recorte + posição + escala).
"""
import random

import cv2
import numpy as np


class Caco:
    def __init__(self, cam_i, recorte, destino, vida):
        self.cam_i = cam_i          # índice da câmera
        self.recorte = recorte      # (x, y, w, h) normalizados 0..1 no quadro de origem
        self.destino = destino      # (x, y, w, h) em pixels no canvas
        self.vida = vida            # segundos até ser trocado


def novo_caco(n_cams, W, H, rng):
    w = rng.uniform(0.15, 0.45)
    h = w * rng.uniform(0.5, 1.4)
    h = min(h, 0.9)
    rec = (rng.uniform(0, 1 - w), rng.uniform(0, 1 - h), w, h)
    escala = rng.uniform(0.6, 1.6)
    dw = int(W * w * 0.6 * escala)
    dh = int(dw * (h / w) * (H / W) * 1.3)
    dw, dh = max(dw, 24), max(dh, 24)
    dst = (rng.randint(-dw // 4, W - dw * 3 // 4), rng.randint(-dh // 4, H - dh * 3 // 4), dw, dh)
    return Caco(rng.randrange(n_cams), rec, dst, rng.uniform(1.5, 6.0))


class Mosaico:
    def __init__(self, n_cams, W=1280, H=720, n_cacos=28, seed=None):
        self.W, self.H = W, H
        self.rng = random.Random(seed)
        self.n_cams = max(n_cams, 1)
        self.cacos = [novo_caco(self.n_cams, W, H, self.rng) for _ in range(n_cacos)]

    def desenhar(self, quadros, dt):
        canvas = np.zeros((self.H, self.W, 3), np.uint8)
        for i, c in enumerate(self.cacos):
            c.vida -= dt
            if c.vida <= 0:
                self.cacos[i] = c = novo_caco(self.n_cams, self.W, self.H, self.rng)
            f = quadros[c.cam_i] if c.cam_i < len(quadros) else None
            if f is None:
                continue
            fh, fw = f.shape[:2]
            x, y, w, h = c.recorte
            pedaco = f[int(y * fh):int((y + h) * fh), int(x * fw):int((x + w) * fw)]
            if pedaco.size == 0:
                continue
            dx, dy, dw, dh = c.destino
            pedaco = cv2.resize(pedaco, (dw, dh), interpolation=cv2.INTER_LINEAR)
            x0, y0 = max(dx, 0), max(dy, 0)
            x1, y1 = min(dx + dw, self.W), min(dy + dh, self.H)
            if x1 <= x0 or y1 <= y0:
                continue
            canvas[y0:y1, x0:x1] = pedaco[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
            cv2.rectangle(canvas, (x0, y0), (x1 - 1, y1 - 1), (40, 40, 40), 1)
        return canvas
