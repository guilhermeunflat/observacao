"""Projeção off-axis (Kooima, "Generalized Perspective Projection").

Cada tela física é uma janela para o mesmo espaço 3D. Dados os cantos da tela
em cm e a posição do olho, devolve a matriz que o OpenGL usa para desenhar o
que se veria através daquela janela. Mesmo sistema de coordenadas de
screens.json e do tracker: x para a direita de quem observa, y para cima,
z para a frente (na direção da pessoa); yaw positivo vira a face da tela
para +x.
"""
import math

import numpy as np


def cantos_tela(t):
    """(pa, pb, pc) = inferior esquerdo, inferior direito, superior esquerdo, em cm.

    "esquerdo/direito" do ponto de vista de quem olha a tela de frente.
    largura_cm/altura_cm já são as medidas como a tela está montada (a 32"
    vertical tem largura < altura).
    """
    c = np.array(t["centro_cm"], dtype=float)
    yaw = math.radians(t.get("yaw", 0.0))
    pitch = math.radians(t.get("pitch", 0.0))      # positivo = tela inclinada olhando para cima
    direita = np.array([math.cos(yaw), 0.0, -math.sin(yaw)])
    normal0 = np.array([math.sin(yaw), 0.0, math.cos(yaw)])
    cima = np.array([0.0, 1.0, 0.0]) * math.cos(pitch) - normal0 * math.sin(pitch)
    w, h = t["largura_cm"] / 2, t["altura_cm"] / 2
    pa = c - direita * w - cima * h
    pb = c + direita * w - cima * h
    pc = c - direita * w + cima * h
    return pa, pb, pc


def frustum(l, r, b, t, n, f):
    return np.array([
        [2 * n / (r - l), 0, (r + l) / (r - l), 0],
        [0, 2 * n / (t - b), (t + b) / (t - b), 0],
        [0, 0, -(f + n) / (f - n), -2 * f * n / (f - n)],
        [0, 0, -1, 0],
    ], dtype=np.float64)


def matriz_off_axis(pa, pb, pc, olho, perto=5.0, longe=2000.0):
    """Matriz 4x4 (projeção x vista) para a tela pa/pb/pc vista do olho."""
    pa, pb, pc, pe = (np.asarray(v, dtype=np.float64) for v in (pa, pb, pc, olho))
    vr = pb - pa
    vr /= np.linalg.norm(vr)
    vu = pc - pa
    vu /= np.linalg.norm(vu)
    vn = np.cross(vr, vu)
    vn /= np.linalg.norm(vn)

    va, vb, vc = pa - pe, pb - pe, pc - pe
    d = -float(va @ vn)                 # distância do olho ao plano da tela
    if d < 1.0:                         # olho atrás ou colado na tela: evita explosão
        d = 1.0
    l = float(vr @ va) * perto / d
    r = float(vr @ vb) * perto / d
    b = float(vu @ va) * perto / d
    t = float(vu @ vc) * perto / d
    P = frustum(l, r, b, t, perto, longe)

    M = np.eye(4)
    M[0, :3], M[1, :3], M[2, :3] = vr, vu, vn
    T = np.eye(4)
    T[:3, 3] = -pe
    return P @ M @ T


def para_gl(m):
    """numpy 4x4 (linha) -> tupla de 16 floats em ordem de coluna (OpenGL)."""
    return tuple(float(x) for x in np.asarray(m, dtype=np.float32).T.flatten())


def limitar_olho(olho, cantos, folga=40.0, iteracoes=4):
    """Mantém o olho na frente de todas as telas, a pelo menos `folga` cm do plano de cada uma.

    Atrás (ou rente) ao plano de uma tela a projeção off-axis degenera: a
    imagem estica e vira. Isso acontecia ao levar o mouse para as pontas,
    onde o olho passava para trás das TVs de tubo.
    """
    o = np.asarray(olho, dtype=np.float64).copy()
    normais = []
    for pa, pb, pc in cantos:
        vr, vu = pb - pa, pc - pa
        n = np.cross(vr, vu)
        normais.append((np.asarray(pa, dtype=np.float64), n / np.linalg.norm(n)))
    for _ in range(iteracoes):
        mexeu = False
        for p, n in normais:
            d = float((o - p) @ n)
            if d < folga:
                o += n * (folga - d)
                mexeu = True
        if not mexeu:
            break
    return o
