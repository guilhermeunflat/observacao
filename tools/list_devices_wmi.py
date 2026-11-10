"""Alternativa via PowerShell/PnP: lista câmeras com InstanceId (rota USB).

Não dá o índice do OpenCV, mas mostra todas as câmeras que o Windows conhece,
inclusive as desconectadas (Status != OK).
"""
import json
import subprocess

CMD = (
    "Get-PnpDevice -Class Camera,Image | "
    "Select-Object FriendlyName, InstanceId, Status | ConvertTo-Json"
)

def main():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", CMD], capture_output=True, text=True)
    dados = json.loads(out.stdout or "[]")
    if isinstance(dados, dict):
        dados = [dados]
    for d in dados:
        print(f"{d.get('Status','?'):<8} {d.get('FriendlyName',''):<24} {d.get('InstanceId','')}")

if __name__ == "__main__":
    main()
