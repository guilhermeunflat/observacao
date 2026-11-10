"""Enumeração DirectShow com DevicePath (identidade = porta USB física).

A ordem da lista é a mesma usada por cv2.VideoCapture(indice, cv2.CAP_DSHOW).
Nunca guardar índices: resolver rota_usb -> índice a cada inicialização.
"""
import re

from comtypes import GUID, client, CoInitialize
from comtypes.persist import IPropertyBag
from pygrabber.dshow_core import ICreateDevEnum
from pygrabber.dshow_ids import DeviceCategories, clsids


def listar():
    try:
        CoInitialize()
    except OSError:
        pass
    enum = client.CreateObject(clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
    it = enum.CreateClassEnumerator(GUID(DeviceCategories.VideoInputDevice), dwFlags=0)
    out = []
    try:
        moniker, count = it.Next(1)
    except ValueError:
        return out
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
        out.append({
            "indice": i,
            "nome": nome,
            "device_path": caminho,
            "vid": (m.group(1) if m else "").lower(),
            "pid": (m.group(2) if m else "").lower(),
            "rota_usb": rota.group(1) if rota else "",
            "usb": "usb#" in caminho.lower(),
        })
        i += 1
        moniker, count = it.Next(1)
    return out


def webcams_usb(vid=None, pid=None):
    d = [x for x in listar() if x["usb"]]
    if vid:
        d = [x for x in d if x["vid"] == vid.lower()]
    if pid:
        d = [x for x in d if x["pid"] == pid.lower()]
    return d


# ---------- controlador USB de cada câmera ----------
_PS = r"""
$o = @()
Get-PnpDevice -PresentOnly -Class Camera,Image | ForEach-Object {
  $id = $_.InstanceId; $cur = $id; $ctrl = ''
  for ($i = 0; $i -lt 8; $i++) {
    $cur = (Get-PnpDeviceProperty -InstanceId $cur -KeyName DEVPKEY_Device_Parent -ErrorAction SilentlyContinue).Data
    if (-not $cur) { break }
    if ($cur -like 'PCI\*') { $ctrl = $cur; break }
  }
  $o += [pscustomobject]@{ interface = $id; controlador = $ctrl }
}
$o | ConvertTo-Json -Compress
"""


def controladores():
    """{rota_usb (minúsculo): instance id PCI do controlador xHCI}."""
    import json
    import subprocess
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", _PS],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        dados = json.loads(out) if out else []
    except Exception:
        return {}
    if isinstance(dados, dict):
        dados = [dados]
    res = {}
    for d in dados:
        inst = d["interface"].split("\\")[-1].lower()
        res[inst] = d["controlador"]
    return res


def nome_controlador(pci_id, mapa):
    for chave, nome in mapa.items():
        if chave.lower() in (pci_id or "").lower():
            return nome
    return pci_id or "?"
