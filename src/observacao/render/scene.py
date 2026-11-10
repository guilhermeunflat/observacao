"""Cena 3D: nuvem de cacos de câmera flutuando atrás das telas.

Cada caco é um retângulo no espaço (cm) com um recorte da imagem de uma
câmera. Todos ficam num volume atrás do U de telas, então cada tela mostra a
mesma nuvem de um ângulo diferente, e a paralaxe muda com a cabeça.
Há também uma grade de linhas ao fundo e no chão para dar profundidade.

OpenGL 3.3 core via pyglet.gl, com um VBO para todos os cacos (desenhados
um a um, cada um com a textura da sua câmera) e outro para as linhas.
"""
import ctypes
import math
import random

import cv2
import numpy as np
from pyglet import gl
from pyglet.graphics.shader import Shader, ShaderProgram

VS_CACO = """#version 330 core
in vec3 posicao;
in vec2 uv;
uniform mat4 mvp;
out vec2 v_uv;
out vec3 v_mundo;
void main() {
    gl_Position = mvp * vec4(posicao, 1.0);
    v_uv = uv;
    v_mundo = posicao;
}
"""

FS_CACO = """#version 330 core
in vec2 v_uv;
in vec3 v_mundo;
uniform sampler2D tex;
uniform float alfa;
uniform float tempo;
uniform vec3 olho;
uniform vec4 recorte;        // u0, v0, u1, v1 do caco
out vec4 cor;
void main() {
    vec3 c = texture(tex, v_uv).rgb;
    float cinza = dot(c, vec3(0.299, 0.587, 0.114));
    c = mix(vec3(cinza), c, 0.55);                       // meio dessaturado, cara de CCTV
    float linha = 0.88 + 0.12 * sin(v_uv.y * 900.0 + tempo * 6.0);   // scanline
    float dist = length(v_mundo - olho);
    float nevoa = clamp(1.25 - dist / 700.0, 0.28, 1.0);  // mais longe do olho = mais escuro
    // moldura fina: separa um caco do outro mesmo quando se cruzam
    vec2 l = (v_uv - recorte.xy) / (recorte.zw - recorte.xy);
    float borda = min(min(l.x, 1.0 - l.x), min(l.y, 1.0 - l.y));
    float moldura = 1.0 - smoothstep(0.0, 0.025, borda);
    vec3 final = mix(c * linha * nevoa, vec3(0.55, 0.85, 0.6) * nevoa, moldura * 0.7);
    cor = vec4(final, alfa);
}
"""

VS_LINHA = """#version 330 core
in vec3 posicao;
uniform mat4 mvp;
void main() { gl_Position = mvp * vec4(posicao, 1.0); }
"""

FS_LINHA = """#version 330 core
uniform vec4 cor_linha;
out vec4 cor;
void main() { cor = cor_linha; }
"""


class Caco:
    __slots__ = ("cam", "uv", "centro", "tam", "yaw", "vida", "duracao", "deriva")

    def __init__(self, cam, uv, centro, tam, yaw, duracao, deriva):
        self.cam, self.uv, self.centro, self.tam, self.yaw = cam, uv, centro, tam, yaw
        self.vida, self.duracao, self.deriva = 0.0, duracao, deriva

    def alfa(self):
        f = 1.2                                        # segundos de fade
        return max(0.0, min(1.0, self.vida / f, (self.duracao - self.vida) / f))

    def vertices(self):
        cx, cy, cz = self.centro
        w, h = self.tam
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        dx, dz = c * w / 2, -s * w / 2
        u0, v0, u1, v1 = self.uv
        # (x, y, z, u, v) — v invertido: a imagem do OpenCV vem de cima para baixo
        bl = (cx - dx, cy - h / 2, cz - dz, u0, v1)
        br = (cx + dx, cy - h / 2, cz + dz, u1, v1)
        tl = (cx - dx, cy + h / 2, cz - dz, u0, v0)
        tr = (cx + dx, cy + h / 2, cz + dz, u1, v0)
        return [*bl, *br, *tr, *bl, *tr, *tl]


class Volume:
    """Onde os cacos vivem: caixa atrás das telas, em cm."""

    def __init__(self, x=(-140, 140), y=(40, 220), z=(-620, -15)):
        self.x, self.y, self.z = x, y, z


class Cena:
    TEX_W, TEX_H = 320, 240
    CAMADAS = (35, 90, 170, 280, 420, 600)    # cm atrás da tela
    ANGULO_CACO = (3.0, 8.5)                   # graus de largura aparente
    FOLGA = 0.9                                # 1 = nenhum caco cobre outro

    def __init__(self, n_cams, telas, n_cacos=70, volume=None, seed=None, olho_ref=(0.0, 155.0, 160.0)):
        self.rng = random.Random(seed)
        self.n_cams = max(1, n_cams)
        self.vol = volume or Volume()
        self.olho_ref = np.asarray(olho_ref, dtype=np.float64)
        # cacos nascem atrás de cada tela, na direção para onde ela olha, para
        # que todas as telas (inclusive as das pontas do U) tenham o que mostrar
        from .projection import cantos_tela
        self.bases = []
        for t in telas:
            pa, pb, pc = cantos_tela(t)
            r, u = pb - pa, pc - pa
            n = np.cross(r / np.linalg.norm(r), u / np.linalg.norm(u))
            self.bases.append({"c": (pb + pc) / 2, "r": r / np.linalg.norm(r), "u": u / np.linalg.norm(u),
                               "n": n, "w": np.linalg.norm(r), "h": np.linalg.norm(u),
                               "yaw": math.radians(t.get("yaw", 0)),
                               "peso": math.sqrt(t["largura_cm"] * t["altura_cm"])})
        self._pesos = [b["peso"] for b in self.bases]
        self.cacos = []
        for _ in range(n_cacos):
            self.cacos.append(self._novo_caco(espalhar=True))
        self.tempo = 0.0
        self.prog_caco = ShaderProgram(Shader(VS_CACO, "vertex"), Shader(FS_CACO, "fragment"))
        self.prog_linha = ShaderProgram(Shader(VS_LINHA, "vertex"), Shader(FS_LINHA, "fragment"))
        self._criar_buffers()
        self._criar_texturas()
        self._linhas = self._grade()
        self._subir_linhas()

    # ---------------------------------------------------------- cacos
    def _candidato(self):
        r = self.rng
        b = r.choices(self.bases, weights=self._pesos)[0]
        prof = r.choice(self.CAMADAS) + r.uniform(-18, 18)  # camadas: o espaço se lê em planos
        d_olho = float(np.linalg.norm(b["c"] - self.olho_ref))
        abre = 1.25 * (1 + prof / d_olho)                  # acompanha o cone de visão da tela
        pos = (b["c"] - b["n"] * prof
               + b["r"] * r.uniform(-0.5, 0.5) * b["w"] * abre
               + b["u"] * r.uniform(-0.5, 0.5) * b["h"] * abre)
        dist = float(np.linalg.norm(pos - self.olho_ref))
        ang = math.radians(r.uniform(*self.ANGULO_CACO))    # tamanho aparente, não absoluto
        largura = 2 * dist * math.tan(ang / 2)
        return b, pos, largura, dist

    def _livre(self, pos, raio_ang, ignorar=None):
        """Quanto o candidato fica longe (em ângulo, visto do olho de referência) dos cacos vivos."""
        o = self.olho_ref
        d = (pos - o) / np.linalg.norm(pos - o)
        pior = 1e9
        for c in getattr(self, "cacos", []):
            if c is ignorar:
                continue
            pc = np.asarray(c.centro) - o
            dc = float(np.linalg.norm(pc))
            rc = max(c.tam) / 2 / dc
            sep = math.acos(max(-1.0, min(1.0, float(d @ (pc / dc)))))
            pior = min(pior, sep - (raio_ang + rc) * self.FOLGA)
        return pior

    def _novo_caco(self, espalhar=False, ignorar=None):
        r = self.rng
        melhor = None
        for _ in range(30):                                 # tenta achar um lugar vazio
            b, pos, largura, dist = self._candidato()
            folga = self._livre(pos, largura / 2 / dist, ignorar)
            if melhor is None or folga > melhor[0]:
                melhor = (folga, b, pos, largura)
            if folga > 0:
                break
        _, b, pos, largura = melhor
        w = r.uniform(0.12, 0.35)                           # recorte da imagem da câmera
        h = min(0.95, w * r.uniform(0.6, 1.4))
        u0, v0 = r.uniform(0, 1 - w), r.uniform(0, 1 - h)
        tam = (largura, largura * (h / w) * 0.75)
        centro = [float(pos[0]), float(pos[1]), float(pos[2])]
        c = Caco(r.randrange(self.n_cams), (u0, v0, u0 + w, v0 + h), centro, tam,
                 b["yaw"] + math.radians(r.uniform(-20, 20)), r.uniform(6, 15),
                 (r.uniform(-1, 1), r.uniform(-0.6, 0.6), r.uniform(-1.5, 1.5)))
        if espalhar:
            c.vida = r.uniform(0, c.duracao)
        return c

    def atualizar(self, dt):
        self.tempo += dt
        for i, c in enumerate(self.cacos):
            c.vida += dt
            c.centro[0] += c.deriva[0] * dt
            c.centro[1] += c.deriva[1] * dt
            c.centro[2] += c.deriva[2] * dt
            if c.vida >= c.duracao:
                self.cacos[i] = self._novo_caco(ignorar=c)
        dados = []
        for c in self.cacos:
            dados += c.vertices()
        arr = np.asarray(dados, dtype=np.float32)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, arr.nbytes, arr.ctypes.data_as(ctypes.c_void_p))

    # ---------------------------------------------------------- GL
    def _vao(self, prog, componentes):
        vao, vbo = gl.GLuint(), gl.GLuint()
        gl.glGenVertexArrays(1, ctypes.byref(vao))
        gl.glGenBuffers(1, ctypes.byref(vbo))
        gl.glBindVertexArray(vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        passo = sum(n for _, n in componentes) * 4
        desloc = 0
        for nome, n in componentes:
            loc = gl.glGetAttribLocation(prog.id, nome.encode())
            gl.glEnableVertexAttribArray(loc)
            gl.glVertexAttribPointer(loc, n, gl.GL_FLOAT, gl.GL_FALSE, passo, ctypes.c_void_p(desloc))
            desloc += n * 4
        gl.glBindVertexArray(0)
        return vao, vbo

    def _criar_buffers(self):
        self.vao, self.vbo = self._vao(self.prog_caco, [("posicao", 3), ("uv", 2)])
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        tamanho = len(self.cacos) * 6 * 5 * 4
        gl.glBufferData(gl.GL_ARRAY_BUFFER, tamanho, None, gl.GL_DYNAMIC_DRAW)
        self.vao_l, self.vbo_l = self._vao(self.prog_linha, [("posicao", 3)])

    def _criar_texturas(self):
        self.tex = []
        preto = np.zeros((self.TEX_H, self.TEX_W, 3), np.uint8)
        for _ in range(self.n_cams):
            t = gl.GLuint()
            gl.glGenTextures(1, ctypes.byref(t))
            gl.glBindTexture(gl.GL_TEXTURE_2D, t)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB8, self.TEX_W, self.TEX_H, 0, gl.GL_BGR,
                            gl.GL_UNSIGNED_BYTE, preto.ctypes.data_as(ctypes.c_void_p))
            self.tex.append(t)
        self._enviado = [None] * self.n_cams

    def subir_quadro(self, i, frame):
        """Envia o quadro da câmera i para a textura dela (só se mudou)."""
        if frame is None or frame is self._enviado[i]:
            return False
        self._enviado[i] = frame
        f = cv2.resize(frame, (self.TEX_W, self.TEX_H), interpolation=cv2.INTER_AREA)
        f = np.ascontiguousarray(f)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex[i])
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, 0, 0, self.TEX_W, self.TEX_H, gl.GL_BGR, gl.GL_UNSIGNED_BYTE,
                           f.ctypes.data_as(ctypes.c_void_p))
        return True

    def _grade(self):
        v = self.vol
        L = []
        zf = v.z[0] - 30
        X = 700
        for x in range(-X, X + 1, 50):            # parede do fundo: verticais
            L += [x, 0, zf, x, 320, zf]
        for y in range(0, 321, 50):               # parede do fundo: horizontais
            L += [-X, y, zf, X, y, zf]
        for x in range(-X, X + 1, 50):            # chão: linhas para o fundo
            L += [x, 0, 60, x, 0, zf]
        for z in range(int(zf), 61, 50):          # chão: linhas transversais
            L += [-X, 0, z, X, 0, z]
        return np.asarray(L, dtype=np.float32)

    def _subir_linhas(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_l)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._linhas.nbytes, self._linhas.ctypes.data_as(ctypes.c_void_p),
                        gl.GL_STATIC_DRAW)

    def desenhar(self, mvp_gl, grade=True, olho=None):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDisable(gl.GL_DEPTH_TEST)
        if grade:
            self.prog_linha.use()
            self.prog_linha["mvp"] = mvp_gl
            self.prog_linha["cor_linha"] = (0.25, 0.55, 0.35, 0.35)
            gl.glBindVertexArray(self.vao_l)
            gl.glDrawArrays(gl.GL_LINES, 0, len(self._linhas) // 3)
        # cacos, do mais fundo para o mais perto (transparência correta)
        self.prog_caco.use()
        self.prog_caco["mvp"] = mvp_gl
        self.prog_caco["tempo"] = self.tempo
        self.prog_caco["tex"] = 0
        self.prog_caco["olho"] = tuple(float(v) for v in (olho if olho is not None else self.olho_ref))
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindVertexArray(self.vao)
        if olho is None:
            ordem = sorted(range(len(self.cacos)), key=lambda i: self.cacos[i].centro[2])
        else:
            o = np.asarray(olho)
            ordem = sorted(range(len(self.cacos)), key=lambda i: -float(np.sum((np.asarray(self.cacos[i].centro) - o) ** 2)))
        for i in ordem:
            c = self.cacos[i]
            a = c.alfa()
            if a <= 0.01:
                continue
            self.prog_caco["alfa"] = a
            self.prog_caco["recorte"] = c.uv
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex[c.cam % len(self.tex)])
            gl.glDrawArrays(gl.GL_TRIANGLES, i * 6, 6)
        gl.glBindVertexArray(0)
        self.prog_caco.stop()
