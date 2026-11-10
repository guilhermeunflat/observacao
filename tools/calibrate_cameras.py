"""Cadastra cada webcam pela porta USB (rota_usb) em config/cameras.json.

Câmeras já cadastradas são reconhecidas sozinhas. Para cada câmera nova, abre
uma janela com a imagem dela: você olha qual vara ela é (tape a lente se
precisar) e digita o nome e o papel no terminal. No fim, confere o limite de
2 webcams abertas por controlador USB e avisa se a distribuição não cabe.

Papéis:
    m = master  (tracking da cabeça, fica aberta)
    v = video   (vídeo ao vivo, fica aberta)
    o = olho    (fica aberta)
    f = foto    (rodízio: abre, tira fotos, fecha)
    r = reserva (ignorada até trocar o papel)

Uso:
    python tools/calibrate_cameras.py                 # pergunta só as novas
    python tools/calibrate_cameras.py --auto          # novas viram foto_NN, papel foto
    python tools/calibrate_cameras.py --revisar       # pergunta de novo nome/papel de todas
    python tools/calibrate_cameras.py --remota http://192.168.0.20:8765
                                                      # importa as câmeras do notebook
    python tools/calibrate_cameras.py --perfil notebook   # no notebook
Na pergunta do nome: Enter = sugestão; "-" = ignorar esta câmera.
"""
import argparse
import json
import time
import urllib.request
from collections import defaultdict

import cv2

import _caminho  # noqa: F401
from observacao import config, devices
from observacao.capture import Camera

PAPEIS = {"m": "master", "v": "video", "o": "olho", "f": "foto", "r": "reserva"}
ABERTAS = {"master", "video", "olho"}


def mostrar(rota):
    cam = Camera("nova", rota_usb=rota).iniciar()
    t0 = time.time()
    while time.time() - t0 < 2.5:
        f, _ = cam.quadro()
        if f is not None:
            cv2.imshow("camera", f)
        cv2.waitKey(30)
    return cam


def perguntar(sug_nome, sug_papel):
    nome = input(f"  nome [{sug_nome}] (- ignora): ").strip() or sug_nome
    if nome == "-":
        return None, None
    p = input(f"  papel m/v/o/f/r [{sug_papel[0]}]: ").strip().lower() or sug_papel[0]
    return nome, PAPEIS.get(p, sug_papel)


def checar_limites(cfg, lista, presentes_ctrl):
    lim = cfg["app"].get("controladores", {}).get("limite_por_controlador", 2)
    vagas = cfg["app"].get("rodizio", {}).get("vagas", 2)
    mapa = cfg["app"].get("controladores", {})
    abertas, fotos = defaultdict(list), defaultdict(list)
    for c in lista:
        if c.get("remota"):
            continue
        ctrl = presentes_ctrl.get(c["rota_usb"].lower())
        if not ctrl:
            continue
        nome = devices.nome_controlador(ctrl, mapa)
        if c.get("papel") in ABERTAS:
            abertas[nome].append(c["nome"])
        elif c.get("papel") == "foto":
            fotos[nome].append(c["nome"])
    print("\nDistribuição por controlador (limite medido: %d abertas):" % lim)
    ok = True
    ctrl_fotos = [k for k, v in fotos.items() if v]
    for nome in sorted(set(abertas) | set(fotos)):
        a, f = abertas[nome], fotos[nome]
        uso = len(a) + (min(vagas, len(f)) if f else 0)
        marca = "ok" if uso <= lim else "EXCEDE"
        ok &= uso <= lim
        print(f"  {nome:<32} abertas={len(a)} {a}  fotos={len(f)} (vagas {min(vagas, len(f)) if f else 0})  -> {uso}/{lim} {marca}")
    if len(ctrl_fotos) > 1:
        print("  AVISO: as câmeras de foto estão em mais de um controlador; o rodízio pode abrir duas no mesmo.")
        ok = False
    if not ok:
        print("  Reorganize as portas ou os papéis: a distribuição não cabe.")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil", default="casa")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--revisar", action="store_true")
    ap.add_argument("--remota", default=None, help="URL do servidor do notebook, ex.: http://192.168.0.20:8765")
    ap.add_argument("--vid", default=None)
    a = ap.parse_args()

    cfg = config.carregar(a.perfil)
    lista = cfg["cameras"].setdefault("cameras", [])

    if a.remota:
        base = a.remota.rstrip("/")
        with urllib.request.urlopen(base + "/lista", timeout=5) as r:
            remotas = json.loads(r.read().decode("utf-8"))
        existentes = {c["nome"] for c in lista}
        for rc in remotas:
            if rc["nome"] in existentes:
                print(f"  já cadastrada: {rc['nome']}")
                continue
            lista.append({"nome": rc["nome"], "papel": "olho" if rc["papel"] == "foto" else rc["papel"],
                          "remota": f"{base}/cam/{rc['nome']}"})
            print(f"  + remota {rc['nome']} ({rc['papel']})")
        config.salvar_cameras(cfg)
        print(f"\nSalvo: {cfg['cameras_path']}")
        return

    print("Lendo portas e controladores USB...")
    webcams = devices.webcams_usb(vid=a.vid)
    ctrl = devices.controladores()
    mapa = cfg["app"].get("controladores", {})
    conhecidas = {c["rota_usb"]: c for c in lista if c.get("rota_usb")}
    print(f"{len(webcams)} webcam(s) USB plugada(s); {len(lista)} cadastrada(s) em {cfg['cameras_path'].name}.\n")

    presentes, novas = set(), []
    for d in webcams:
        presentes.add(d["rota_usb"])
        cn = devices.nome_controlador(ctrl.get(d["rota_usb"].lower(), ""), mapa)
        d["controlador"] = cn
        if d["rota_usb"] in conhecidas and not a.revisar:
            c = conhecidas[d["rota_usb"]]
            print(f"  reconhecida: {c['nome']:<10} {c.get('papel', 'olho'):<8} {cn}")
        else:
            novas.append(d)
    for c in lista:
        if c.get("rota_usb") and c["rota_usb"] not in presentes:
            print(f"  AUSENTE:     {c['nome']:<10} {c.get('papel', 'olho'):<8} (cadastrada, não plugada)")

    usados = {c["nome"] for c in lista}

    def sugestao(prefixo):
        n = 1
        while f"{prefixo}_{n:02d}" in usados:
            n += 1
        return f"{prefixo}_{n:02d}"

    for d in novas:
        antiga = conhecidas.get(d["rota_usb"])
        sug_papel = antiga["papel"] if antiga else "foto"
        sug_nome = antiga["nome"] if antiga else sugestao(sug_papel if sug_papel != "olho" else "vara")
        if a.auto:
            nome, papel = sug_nome, sug_papel
        else:
            print(f"\nCâmera {'já cadastrada' if antiga else 'nova'} ({d['vid']}:{d['pid']}) no {d['controlador']}: veja a janela 'camera'.")
            cam = mostrar(d["rota_usb"])
            nome, papel = perguntar(sug_nome, sug_papel)
            cam.parar()
            cv2.destroyAllWindows()
            if nome is None:
                continue
        if antiga:
            usados.discard(antiga["nome"])
            antiga.update({"nome": nome, "papel": papel})
        else:
            lista.append({"nome": nome, "rota_usb": d["rota_usb"], "papel": papel, "vid": d["vid"], "pid": d["pid"],
                          "posicao_cm": None, "exposicao": None, "ganho": None})
        usados.add(nome)
        print(f"  = {nome} ({papel})")

    checar_limites(cfg, lista, ctrl)
    config.salvar_cameras(cfg)
    print(f"\nSalvo: {cfg['cameras_path']}  ({len(lista)} câmeras)")


if __name__ == "__main__":
    main()
