"""Marcadores ArUco nas telas, para medir a montagem com fotos de celular.

Cada tela mostra uma grade de marcadores com IDs próprios (bloco de 10 por
tela, na ordem de screens.json). Como sabemos o tamanho de cada tela em cm,
cada canto de marcador tem posição conhecida no plano da tela; o
tools/fotos_telas.py usa isso para achar onde cada tela está no espaço.

As posições ficam em coordenadas normalizadas (0..1) da área desenhada: vale
para qualquer resolução e também para as TVs de tubo, onde o pixel não é
quadrado (o canto continua no lugar certo em cm).
"""
import cv2
import numpy as np

DICIONARIO = cv2.aruco.DICT_4X4_100
BLOCO = 10            # tela i usa IDs i*10 .. i*10+9
ID_CHAO = 99          # marcador impresso que vai no chão (opcional)
GRADES = {"crt": (3, 2), "led": (2, 4), "monitor": (4, 2)}   # (colunas, linhas): marcadores maiores nas telas pequenas


def dicionario():
    return cv2.aruco.getPredefinedDictionary(DICIONARIO)


def layout(tela, i_tela):
    """[(id, u0, v0, du, dv)] com u da esquerda para a direita e v de CIMA para baixo, 0..1."""
    cols, rows = GRADES.get(tela.get("tipo"), (3, 2))
    W, H = tela["largura_cm"], tela["altura_cm"]
    lado = 0.8 * min(W / cols, H / rows)           # marcador quadrado em cm, com folga branca
    out = []
    for r in range(rows):
        for c in range(cols):
            cx, cy = (c + 0.5) * W / cols, (r + 0.5) * H / rows
            out.append((i_tela * BLOCO + r * cols + c, (cx - lado / 2) / W, (cy - lado / 2) / H, lado / W, lado / H))
    return out


def cantos_cm(tela, item):
    """Cantos do marcador (TL, TR, BR, BL, como o ArUco devolve) no plano da tela, em cm.

    Origem no centro da tela, x para a direita, y para cima, z para fora (para quem olha)."""
    _, u0, v0, du, dv = item
    W, H = tela["largura_cm"], tela["altura_cm"]
    uv = [(u0, v0), (u0 + du, v0), (u0 + du, v0 + dv), (u0, v0 + dv)]
    return np.array([[(u - 0.5) * W, (0.5 - v) * H, 0.0] for u, v in uv], np.float32)


def imagem(tela, i_tela, w_px, h_px):
    """Imagem BGR (h_px x w_px) com a grade da tela: fundo branco, marcadores pretos."""
    img = np.full((h_px, w_px, 3), 255, np.uint8)
    d = dicionario()
    for mid, u0, v0, du, dv in layout(tela, i_tela):
        x0, y0 = int(round(u0 * w_px)), int(round(v0 * h_px))
        x1, y1 = int(round((u0 + du) * w_px)), int(round((v0 + dv) * h_px))
        n = max(x1 - x0, y1 - y0)
        m = cv2.aruco.generateImageMarker(d, mid, n, borderBits=1)
        img[y0:y1, x0:x1] = cv2.cvtColor(cv2.resize(m, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST),
                                         cv2.COLOR_GRAY2BGR)
    cv2.putText(img, tela["id"], (8, h_px - 10), cv2.FONT_HERSHEY_SIMPLEX, max(0.4, h_px / 900), (120, 120, 120), 1,
                cv2.LINE_AA)
    return img
