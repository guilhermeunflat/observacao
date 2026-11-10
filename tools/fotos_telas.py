"""Mede a montagem das 5 telas a partir de fotos de celular.

Com o app mostrando os marcadores ArUco (tecla M ou --marcadores), tire 4 a 8
fotos do lugar onde o público fica, de ângulos diferentes (roteiro em
docs/fotos_medicao.md). Este script acha os marcadores, estima a lente do
celular, calcula a posição e o ângulo de cada tela em relação à TV 32 do
centro e propõe os valores de centro_cm / yaw / pitch para screens.json.

A escala vem de largura_cm/altura_cm de cada tela (medidas da área de imagem
com trena: nas TVs de tubo, só o que aparece, sem a borda escondida).
A altura vem do marcador impresso no chão (tools/fotos_telas.py --imprimir-chao)
ou, sem ele, de --altura-centro (centro da TV 32 até o chão, em cm).

Uso:
    python tools/fotos_telas.py docs/fotos/2026-11-07_casa/medicao
    python tools/fotos_telas.py docs/fotos/2026-11-07_casa/medicao --escrever
    python tools/fotos_telas.py --imprimir-chao docs/fotos/marcador_chao.pdf
Saída: tabela no terminal + pasta _resultado/ ao lado das fotos (marcadores
detectados em cada foto e vista de cima: cinza = screens.json atual, verde = medido).
"""
import argparse
import json
import math
import shutil
import sys
import time
from pathlib import Path

import _caminho  # noqa: F401
import cv2
import numpy as np

from observacao import config
from observacao.render import marcadores as mk

EXT = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
ORDEM = ["tubo_esq", "esq_21", "centro_32", "dir_21_touch", "tubo_dir"]


# ---------- poses ----------
def T(R, t):
    m = np.eye(4)
    m[:3, :3], m[:3, 3] = R, np.ravel(t)
    return m


def inv(m):
    R, t = m[:3, :3], m[:3, 3]
    return T(R.T, -R.T @ t)


def media_poses(lista):
    """Média de matrizes 4x4: translação pela média, rotação projetada de volta (SVD)."""
    t = np.mean([m[:3, 3] for m in lista], axis=0)
    U, _, Vt = np.linalg.svd(np.sum([m[:3, :3] for m in lista], axis=0))
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    espalho = max(float(np.linalg.norm(m[:3, 3] - t)) for m in lista)
    return T(R, t), espalho


# ---------- fotos ----------
def ler_fotos(caminhos):
    arqs = []
    for c in caminhos:
        p = Path(c)
        arqs += sorted(q for q in p.iterdir() if q.suffix.lower() in EXT) if p.is_dir() else [p]
    return arqs


def detectar(img, detector, telas, chao_cm):
    """{chave: (pontos_obj Nx3, pontos_img Nx2, n_marcadores)}; chave = id da tela ou 'chao'."""
    mapa = {}
    for i, t in enumerate(telas):
        for item in mk.layout(t, i):
            mapa[item[0]] = (t["id"], mk.cantos_cm(t, item))
    s = chao_cm / 2
    mapa[mk.ID_CHAO] = ("chao", np.array([[-s, s, 0], [s, s, 0], [s, -s, 0], [-s, -s, 0]], np.float32))
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cantos, ids, _ = detector.detectMarkers(cinza)
    out = {}
    if ids is None:
        return out, cantos, ids
    for c, i in zip(cantos, ids.ravel()):
        if int(i) not in mapa:
            continue
        chave, obj = mapa[int(i)]
        o, im, n = out.get(chave, ([], [], 0))
        out[chave] = (o + [obj], im + [c.reshape(4, 2)], n + 1)
    return {k: (np.concatenate(o).astype(np.float32), np.concatenate(im).astype(np.float32), n)
            for k, (o, im, n) in out.items()}, cantos, ids


def lente(vistas, tamanho):
    """Estima a lente do celular com todas as telas de todas as fotos (cada tela é um alvo plano)."""
    w, h = tamanho
    K = np.array([[0.75 * max(w, h), 0, w / 2], [0, 0.75 * max(w, h), h / 2], [0, 0, 1]], np.float64)
    dist = np.zeros(5)
    usaveis = [(o, im) for o, im in vistas if len(o) >= 8]
    if len(usaveis) < 3:
        return K, dist, None
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_FIX_ASPECT_RATIO | cv2.CALIB_ZERO_TANGENT_DIST |
             cv2.CALIB_FIX_K3 | cv2.CALIB_FIX_PRINCIPAL_POINT)
    rms, K2, d2, _, _ = cv2.calibrateCamera([o for o, _ in usaveis], [im for _, im in usaveis], (w, h), K.copy(),
                                            dist.copy(), flags=flags)
    if not (0.4 * max(w, h) < K2[0, 0] < 1.6 * max(w, h)):    # resultado absurdo: fica com o palpite
        return K, dist, None
    return K2, d2.ravel(), rms


def pnp(o, im, K, dist):
    ok, rv, tv = cv2.solvePnP(o, im, K, dist, flags=cv2.SOLVEPNP_IPPE)
    if not ok:
        return None, None
    rv, tv = cv2.solvePnPRefineLM(o, im, K, dist, rv, tv)
    proj, _ = cv2.projectPoints(o, rv, tv, K, dist)
    erro = float(np.sqrt(np.mean(np.sum((proj.reshape(-1, 2) - im) ** 2, axis=1))))
    return T(cv2.Rodrigues(rv)[0], tv), erro


# ---------- montagem ----------
def montar(poses_por_foto, ref):
    """Junta as fotos num referencial só: o da tela ref. Fotos sem a ref entram por outra tela em comum."""
    medidas = {}                                   # chave -> [T_ref_chave]
    cams = {}                                      # foto -> T_ref_cam
    pendentes = dict(poses_por_foto)
    while pendentes:
        avancou = False
        for foto, poses in list(pendentes.items()):
            base = None
            if ref in poses:
                base = inv(poses[ref])
            else:
                for k in poses:
                    if k in medidas:
                        base = media_poses(medidas[k])[0] @ inv(poses[k])
                        break
            if base is None:
                continue
            cams[foto] = base
            for k, Tk in poses.items():
                medidas.setdefault(k, []).append(base @ Tk)
            del pendentes[foto]
            avancou = True
        if not avancou:
            break
    return medidas, cams, list(pendentes)


def referencial_mundo(medidas, ref_altura):
    """Matriz 3x3 (linhas = eixos x, y, z do mundo) e origem, tudo no referencial da TV central."""
    if "chao" in medidas:
        Tc, _ = media_poses(medidas["chao"])
        Y = Tc[:3, 2]                              # normal do papel no chão = para cima
        if Y[1] < 0:
            Y = -Y
        h = float(-Tc[:3, 3] @ Y)                  # altura do centro da TV acima do plano do chão
        fonte_h = "marcador no chão"
    else:
        Y = np.array([0.0, 1.0, 0.0])              # TV central em pé
        h = ref_altura
        fonte_h = "--altura-centro"
    Z = np.array([0.0, 0.0, 1.0]) - Y * Y[2]
    Z /= np.linalg.norm(Z)
    X = np.cross(Y, Z)
    M = np.stack([X, Y, Z])
    return M, -Y * h, h, fonte_h


def em_mundo(Tr, M, O):
    R = M @ Tr[:3, :3]
    return M @ (Tr[:3, 3] - O), R[:, 0], R[:, 1], R[:, 2]


def angulos(direita, cima, normal):
    yaw = math.degrees(math.atan2(normal[0], normal[2]))
    n0 = np.array([math.sin(math.radians(yaw)), 0, math.cos(math.radians(yaw))])
    pitch = math.degrees(math.asin(float(np.clip(-cima @ n0, -1, 1))))
    roll = math.degrees(math.asin(float(np.clip(direita[1], -1, 1))))
    return yaw, pitch, roll


def bordas(t, c, direita):
    w = t["largura_cm"] / 2
    return c - direita * w, c + direita * w


# ---------- saída ----------
def vista_de_cima(telas, medido, cams_mundo, caminho):
    S, W, H = 2.2, 900, 700                       # px por cm
    ox, oz = W / 2, 120
    img = np.full((H, W, 3), 18, np.uint8)
    pt = lambda x, z: (int(ox + x * S), int(oz + z * S))
    for g in range(-200, 201, 50):
        cv2.line(img, pt(g, -40), pt(g, 250), (40, 40, 40), 1)
    for g in range(-40, 251, 50):
        cv2.line(img, pt(-200, g), pt(200, g), (40, 40, 40), 1)
    cv2.putText(img, "grade 50 cm   cinza: screens.json   verde: medido   azul: onde a foto foi tirada",
                (10, H - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)
    from observacao.render.projection import cantos_tela
    for t in telas:
        pa, pb, _ = cantos_tela(t)
        cv2.line(img, pt(pa[0], pa[2]), pt(pb[0], pb[2]), (110, 110, 110), 3)
        if t["id"] in medido:
            m = medido[t["id"]]
            a, b = bordas(t, m["c"], m["direita"])
            cv2.line(img, pt(a[0], a[2]), pt(b[0], b[2]), (120, 255, 140), 3)
            n = m["c"] + m["normal"] * 15
            cv2.arrowedLine(img, pt(m["c"][0], m["c"][2]), pt(n[0], n[2]), (120, 255, 140), 1)
            cv2.putText(img, t["id"], pt(m["c"][0] - 20, m["c"][2] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (120, 255, 140), 1, cv2.LINE_AA)
    for p in cams_mundo:
        cv2.circle(img, pt(p[0], p[2]), 4, (255, 150, 60), -1)
    cv2.imwrite(str(caminho), img)


def imprimir_chao(caminho, cm):
    px = int(cm / 2.54 * 300)                     # 300 dpi
    m = mk.cv2.aruco.generateImageMarker(mk.dicionario(), mk.ID_CHAO, px, borderBits=1)
    a4 = np.full((3508, 2480), 255, np.uint8)
    y0, x0 = (3508 - px) // 2, (2480 - px) // 2
    a4[y0:y0 + px, x0:x0 + px] = m
    linhas = [f"OBSERVACAO - marcador do chao (ID {mk.ID_CHAO})", "Imprimir em A4, tamanho real (100%).",
              f"O quadrado preto deve medir {cm:.0f} cm.", "Se medir diferente, use --chao-cm."]
    for i, l in enumerate(linhas):
        cv2.putText(a4, l, (150, 180 + i * 75), cv2.FONT_HERSHEY_SIMPLEX, 1.6, 0, 3, cv2.LINE_AA)
    cv2.putText(a4, "Deitado no chao, no meio do U, em pelo menos 2 fotos.", (150, 3300),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, 0, 3, cv2.LINE_AA)
    try:                                           # PDF com tamanho físico certo; PNG se não houver Pillow
        from PIL import Image
        Image.fromarray(a4).save(caminho.with_suffix(".pdf"), resolution=300)
        caminho = caminho.with_suffix(".pdf")
    except ImportError:
        cv2.imwrite(str(caminho), a4)
    print(f"marcador salvo em {caminho} ({cm:.0f} cm a 300 dpi)")


def caminho_screens(perfil):
    p = config.CONFIG / "profiles" / f"{perfil}.json"
    prof = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return config.RAIZ / prof.get("screens", "config/screens.json")


def escrever(arq, dados, medido):
    if arq.exists():
        bak = arq.with_name(arq.stem + time.strftime("_%Y%m%d-%H%M") + ".bak.json")
        shutil.copy(arq, bak)
        print(f"cópia de segurança: {bak.name}")
    for t in dados["telas"]:
        if t["id"] in medido:
            m = medido[t["id"]]
            t["centro_cm"] = [round(float(v) * 2) / 2 for v in m["c"]]
            t["yaw"] = round(m["yaw"], 1)
            t["pitch"] = round(m["pitch"], 1)
    linhas = ",\n".join("    " + json.dumps(t, ensure_ascii=False) for t in dados["telas"])
    doc = json.dumps(dados.get("_doc", ""), ensure_ascii=False)
    arq.write_text(f'{{\n  "_doc": {doc},\n  "telas": [\n{linhas}\n  ]\n}}\n', encoding="utf-8")
    print(f"gravado: {arq}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fotos", nargs="*", help="pasta(s) ou arquivos de foto")
    ap.add_argument("--perfil", default="casa")
    ap.add_argument("--chao-cm", type=float, default=15.0, help="lado do quadrado preto do marcador do chão")
    ap.add_argument("--altura-centro", type=float, default=None, help="cm do chão ao centro da TV 32 (sem marcador)")
    ap.add_argument("--escrever", action="store_true", help="grava centro_cm/yaw/pitch no screens.json do perfil")
    ap.add_argument("--imprimir-chao", default=None, help="gera o PNG A4 do marcador do chão e sai")
    a = ap.parse_args()

    if a.imprimir_chao:
        imprimir_chao(Path(a.imprimir_chao), a.chao_cm)
        return
    arqs = ler_fotos(a.fotos)
    if not arqs:
        sys.exit("nenhuma foto encontrada")

    arq_screens = caminho_screens(a.perfil)
    dados = json.loads((arq_screens if arq_screens.exists() else config.CONFIG / "screens.json").read_text(encoding="utf-8"))
    telas = dados["telas"]
    por_id = {t["id"]: t for t in telas}
    ref = "centro_32" if "centro_32" in por_id else telas[0]["id"]
    alt_ref = a.altura_centro if a.altura_centro is not None else por_id[ref]["centro_cm"][1]

    params = cv2.aruco.DetectorParameters()
    params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    detector = cv2.aruco.ArucoDetector(mk.dicionario(), params)
    saida = (arqs[0].parent / "_resultado")
    saida.mkdir(exist_ok=True)

    deteccoes, tamanho = {}, None
    for f in arqs:
        img = cv2.imread(str(f))
        if img is None:
            print(f"  {f.name}: não abriu (HEIC? exporte como JPG)")
            continue
        esc = 1.0
        if max(img.shape[:2]) > 4200:                     # fotos de 48-200 MP: reduz para detectar rápido
            esc = 4000 / max(img.shape[:2])
            img = cv2.resize(img, None, fx=esc, fy=esc, interpolation=cv2.INTER_AREA)
        if tamanho is None:
            tamanho = (img.shape[1], img.shape[0])
        elif (img.shape[1], img.shape[0]) != tamanho:
            if (img.shape[0], img.shape[1]) == tamanho:
                print(f"  {f.name}: foto em outra orientação; use todas na mesma (deitadas ou em pé). Ignorada.")
            else:
                print(f"  {f.name}: tamanho diferente (outro celular ou zoom?). Ignorada.")
            continue
        det, cantos, ids = detectar(img, detector, telas, a.chao_cm)
        vis = img.copy()
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(vis, cantos, ids)
        cv2.imwrite(str(saida / f"{f.stem}_marcadores.jpg"), vis)
        det = {k: v for k, v in det.items() if v[2] >= (1 if k == "chao" else 2)}
        print(f"  {f.name}: " + (", ".join(f"{k} ({v[2]})" for k, v in det.items()) or "nada"))
        if det:
            deteccoes[f.name] = det
    if not deteccoes:
        sys.exit("nenhum marcador reconhecido. O app estava com a tecla M ligada?")

    K, dist, rms = lente([(o, im) for d in deteccoes.values() for k, (o, im, _) in d.items() if k != "chao"], tamanho)
    print(f"\nlente: f = {K[0, 0]:.0f} px" + (f" (estimada, erro {rms:.2f} px)" if rms else " (palpite: poucas fotos)"))

    poses, erros = {}, []
    for foto, d in deteccoes.items():
        for k, (o, im, _) in d.items():
            Tk, e = pnp(o, im, K, dist)
            if Tk is not None and e < 8:
                poses.setdefault(foto, {})[k] = Tk
                erros.append(e)
    medidas, cams, soltas = montar(poses, ref)
    for f in soltas:
        print(f"  {f}: nenhuma tela em comum com as outras fotos; ignorada")
    if ref not in medidas:
        sys.exit(f"a tela {ref} não aparece em nenhuma foto: ela é a referência, precisa aparecer")

    M, O, h, fonte_h = referencial_mundo(medidas, alt_ref)
    print(f"altura do centro da {ref}: {h:.1f} cm ({fonte_h})")
    medido = {}
    for tid in [i for i in ORDEM if i in medidas] + [i for i in medidas if i not in ORDEM and i != "chao"]:
        Tm, esp = media_poses(medidas[tid])
        c, direita, cima, normal = em_mundo(Tm, M, O)
        yaw, pitch, roll = angulos(direita, cima, normal)
        medido[tid] = {"c": c, "direita": direita, "normal": normal, "yaw": yaw, "pitch": pitch, "roll": roll,
                       "espalho": esp, "n": len(medidas[tid])}

    print(f"\n{'tela':14} {'centro_cm (x, y, z)':>24} {'yaw':>6} {'pitch':>6}   {'antes':>24} {'yaw':>6}   fotos  variação")
    for tid, m in medido.items():
        t = por_id[tid]
        c0 = t["centro_cm"]
        aviso = "  <- tela torta (roll %.0f°)" % m["roll"] if abs(m["roll"]) > 3 else ""
        print(f"{tid:14} {m['c'][0]:7.1f} {m['c'][1]:7.1f} {m['c'][2]:7.1f}  {m['yaw']:6.1f} {m['pitch']:6.1f}   "
              f"{c0[0]:7.1f} {c0[1]:7.1f} {c0[2]:7.1f}  {t.get('yaw', 0):6.1f}   {m['n']:4d}  {m['espalho']:5.1f} cm{aviso}")
    faltam = [t["id"] for t in telas if t["id"] not in medido]
    if faltam:
        print("sem medida (não apareceram com marcadores suficientes): " + ", ".join(faltam))

    print("\nvãos entre telas vizinhas (borda a borda):")
    seq = [i for i in ORDEM if i in medido]
    for a_, b_ in zip(seq, seq[1:]):
        _, dir_a = bordas(por_id[a_], medido[a_]["c"], medido[a_]["direita"])
        esq_b, _ = bordas(por_id[b_], medido[b_]["c"], medido[b_]["direita"])
        ang = abs(medido[a_]["yaw"] - medido[b_]["yaw"])
        print(f"  {a_} -> {b_}: {np.linalg.norm(esq_b - dir_a):5.1f} cm, ângulo entre elas {ang:4.0f}°")
    print(f"erro médio dos marcadores: {np.mean(erros):.2f} px")

    cams_mundo = [M @ (Tc[:3, 3] - O) for Tc in cams.values()]
    for f, p in zip(cams, cams_mundo):
        print(f"  {f}: foto tirada de x={p[0]:.0f} y={p[1]:.0f} z={p[2]:.0f} cm")
    vista_de_cima(telas, medido, cams_mundo, saida / "vista_de_cima.png")
    print(f"\nimagens em {saida}")
    if a.escrever:
        escrever(arq_screens, dados, medido)
    else:
        print("nada gravado. Rode de novo com --escrever para gravar em " + arq_screens.name)


if __name__ == "__main__":
    main()
