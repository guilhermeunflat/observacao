"""Teste de carga USB: quantas webcams cabem por porta/hub.

Abre as webcams USB uma a uma, em sequência, e mede o fps real de TODAS as que
já estão abertas depois de cada nova. Para quando uma câmera não abre ou o fps
de alguma cai abaixo de metade do pedido. Salva o resultado em docs/bench/.

Uso (com as webcams plugadas):
    python tools/bench_usb.py                       # 640x480 @ 15, todas as USB
    python tools/bench_usb.py --res 320x240 --fps 15
    python tools/bench_usb.py --vid 1bcf --segundos 15
    python tools/bench_usb.py --final 600          # 10 min com todas abertas (aceite da Fase 1)
"""
import argparse
import json
import time
from pathlib import Path

import _caminho  # noqa: F401
from observacao import devices
from observacao.capture import Camera


def medir(cams, segundos):
    for c in cams:
        c._contagem, c._t_contagem = 0, time.time()
    time.sleep(segundos)
    return {c.nome: (round(c.fps_real, 1), c.status, c.quedas) for c in cams}


def formato(cams):
    return " ".join(f"{c.nome}={getattr(c, 'fourcc_real', '?')}" for c in cams)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default="640x480")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--vid", default=None, help="filtra pelo VID (ex.: 1bcf)")
    ap.add_argument("--fourcc", default="MJPG", help="MJPG ou YUY2")
    ap.add_argument("--segundos", type=float, default=10)
    ap.add_argument("--final", type=float, default=0, help="segundos do teste longo com todas abertas")
    ap.add_argument("--continuar", action="store_true", help="não para na primeira queda; testa todas")
    a = ap.parse_args()
    w, h = map(int, a.res.lower().split("x"))

    webcams = devices.webcams_usb(vid=a.vid)
    if not webcams:
        print("Nenhuma webcam USB encontrada. Plugue as câmeras e rode de novo.")
        return
    print(f"{len(webcams)} webcam(s) USB. Teste em {w}x{h} @ {a.fps} fps {a.fourcc}, {a.segundos:.0f} s por etapa.\n")

    abertas, etapas = [], []
    limite = a.fps * 0.5
    for d in webcams:
        nome = f"i{d['indice']:02d}" + ("" if d["vid"] == "1bcf" else f"[{d['vid']}]")
        cam = Camera(nome, rota_usb=d["rota_usb"], largura=w, altura=h, fps=a.fps, fourcc=a.fourcc).iniciar()
        t0 = time.time()
        while cam.quadro()[0] is None and time.time() - t0 < 8:
            time.sleep(0.2)
        abertas.append(cam)
        res = medir(abertas, a.segundos)
        ruins = [n for n, (f, s, q) in res.items() if f < limite]
        linha = "  ".join(f"{n}:{f:>4}" for n, (f, s, q) in res.items())
        print(f"{len(abertas):2} abertas | {linha}" + ("   <-- QUEDA" if ruins else ""))
        if len(abertas) == 1:
            print(f"   formato: {formato(abertas)}")
        etapas.append({"n": len(abertas), "nova": nome, "rota_usb": d["rota_usb"], "fps": res, "ruins": ruins})
        if ruins and not a.continuar:
            print(f"\nLimite atingido com {len(abertas)} câmeras: {', '.join(ruins)} abaixo de {limite:.0f} fps.")
            print("Anote em que porta/hub está a última câmera; esse é o teto daquele tubo.")
            break

    final = None
    if a.final and (a.continuar or not etapas[-1]["ruins"]):
        print(f"\nTeste longo: {len(abertas)} câmeras por {a.final:.0f} s...")
        final = medir(abertas, a.final)
        for n, (f, s, q) in final.items():
            print(f"  {n}: {f} fps, {s}, quedas={q}")

    for c in abertas:
        c.parar()
    pasta = Path(__file__).resolve().parents[1] / "docs" / "bench"
    pasta.mkdir(parents=True, exist_ok=True)
    arq = pasta / f"bench_{time.strftime('%Y%m%d_%H%M%S')}_{w}x{h}_{a.fourcc}.json"
    arq.write_text(json.dumps({"res": [w, h], "fps": a.fps, "webcams": webcams, "etapas": etapas, "final": final},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResultado salvo em {arq}")


if __name__ == "__main__":
    main()
