"""Lista as webcams conectadas com o caminho físico USB (device path).

Resolve o problema de todas as câmeras terem o mesmo nome: o DevicePath do
DirectShow contém a rota da porta USB e é estável enquanto a câmera ficar na
mesma porta. A ordem da lista é a mesma que o OpenCV usa em
cv2.VideoCapture(indice, cv2.CAP_DSHOW).

Uso:
    python tools/list_devices.py            # lista legível
    python tools/list_devices.py --json     # JSON (usado pela calibração)
"""
import json
import re
import sys

from comtypes import GUID, client
from comtypes.persist import IPropertyBag
from pygrabber.dshow_core import ICreateDevEnum
from pygrabber.dshow_ids import DeviceCategories, clsids


def listar():
    enum = client.CreateObject(clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
    it = enum.CreateClassEnumerator(GUID(DeviceCategories.VideoInputDevice), dwFlags=0)
    dispositivos = []
    try:
        moniker, count = it.Next(1)
    except ValueError:
        return dispositivos
    i = 0
    while count > 0:
        bag = moniker.BindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
        nome = bag.Read("FriendlyName", pErrorLog=None)
        try:
            caminho = bag.Read("DevicePath", pErrorLog=None) or ""
        except Exception:
            caminho = ""
        m = re.search(r"vid_([0-9a-f]{4})&pid_([0-9a-f]{4})", caminho, re.I)
        rota = re.search(r"#([^#]+)#\{", caminho)
        dispositivos.append(
            {
                "indice": i,
                "nome": nome,
                "device_path": caminho,
                "vid": (m.group(1) if m else "").lower(),
                "pid": (m.group(2) if m else "").lower(),
                "rota_usb": rota.group(1) if rota else "",
                "usb": "usb#" in caminho.lower(),
            }
        )
        i += 1
        moniker, count = it.Next(1)
    return dispositivos


def main():
    disp = listar()
    if "--json" in sys.argv:
        print(json.dumps(disp, ensure_ascii=False, indent=2))
        return
    print(f"{len(disp)} dispositivo(s) de video encontrados\n")
    for d in disp:
        tipo = "USB" if d["usb"] else "virtual"
        print(f"[{d['indice']:2}] {d['nome']:<24} {tipo:<7} vid={d['vid'] or '----'} pid={d['pid'] or '----'} rota={d['rota_usb'] or '-'}")


if __name__ == "__main__":
    main()
