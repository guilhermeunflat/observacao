"""Carrega app.json, screens.json e cameras.json, com sobrescrita pelo perfil."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CONFIG = RAIZ / "config"


def _ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _mesclar(base, extra):
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _mesclar(base[k], v)
        else:
            base[k] = v
    return base


def carregar(perfil="casa"):
    app = _ler(CONFIG / "app.json")
    p = CONFIG / "profiles" / f"{perfil}.json"
    prof = _ler(p) if p.exists() else {}
    _mesclar(app, prof.get("app", {}))
    telas = _ler(RAIZ / prof.get("screens", "config/screens.json"))
    cam_path = RAIZ / prof.get("cameras", "config/cameras.json")
    cams = _ler(cam_path) if cam_path.exists() else {"cameras": []}
    return {"perfil": perfil, "app": app, "telas": telas, "cameras": cams, "cameras_path": cam_path}


def salvar_cameras(cfg):
    with open(cfg["cameras_path"], "w", encoding="utf-8") as f:
        json.dump(cfg["cameras"], f, ensure_ascii=False, indent=2)
