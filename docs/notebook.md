# Notebook como 2º servidor de câmeras

O PC mantém só 6 webcams abertas ao mesmo tempo (2 por controlador USB, medido em 05/11). O notebook recebe mais algumas câmeras e manda as imagens ao PC pela rede local. No PC elas aparecem como qualquer outra câmera.

## Distribuição combinada (05/11)

| Onde | Controlador | Papel | Câmeras |
|---|---|---|---|
| PC, azuis de trás | CPU | tracking (master), abertas sempre | 2 |
| PC, azuis da frente | chipset B | vídeo ao vivo, abertas sempre | 2 |
| PC, vermelhas + pretas (+ hub numa vermelha) | chipset A | rodízio de fotos: 2 vagas | 6 |
| Notebook | o que o teste mostrar | a definir | 2 a 4 |

Rodízio medido: cada visita a uma câmera de foto leva ~2,5 a 3 s (abrir + assentar exposição + 3 fotos). Com 6 câmeras e 2 vagas, cada uma tira fotos a cada ~8 a 9 s.

## Instalação no notebook (uma vez, ~15 min)

1. Instale o Python 3.10 (python.org, marque "Add python.exe to PATH").
2. Copie a pasta inteira `OBSERVACAO` para o notebook (pen drive serve), **sem** a pasta `.venv`.
3. No notebook, dentro da pasta `OBSERVACAO`, abra o PowerShell e rode:

```
py -3.10 -m venv .venv
.venv\Scripts\python -m pip install -r requirements_notebook.txt
```

## Descobrir quantas câmeras o notebook aguenta (~10 min)

1. Plugue uma webcam em cada porta do notebook (2 azuis, 1 preta, USB-C com adaptador se tiver).
2. Rode o teste de carga. Ele abre uma a uma e diz quando alguma cai:

```
.venv\Scripts\python tools\bench_usb.py --continuar
```

3. Se todas abrirem, teste mais uma num hub. O número que ficar estável é quantas o notebook recebe.

## Cadastrar e servir

```
.venv\Scripts\python tools\calibrate_cameras.py --perfil notebook
servidor_notebook.bat
```

Na primeira vez o Windows pergunta sobre o firewall: permita em **rede privada**. A janela do servidor mostra o endereço, por exemplo `http://192.168.0.20:8765`.

## No PC

Com o servidor do notebook rodando, importe as câmeras dele (troque pelo endereço que apareceu):

```
.venv/Scripts/python tools/calibrate_cameras.py --remota http://192.168.0.20:8765
```

## Rede

**Teste em casa (Wi-Fi):** o PC fica no cabo (192.168.0.74, roteador 192.168.0.1) e o notebook no Wi-Fi do **mesmo roteador**. O endereço do notebook precisa começar com 192.168.0. Se vier diferente, ele está numa rede de convidados ou em outro roteador, e um não enxerga o outro. Na rede Wi-Fi do notebook, marque o perfil como **Privado** (Configurações > Rede > Wi-Fi > propriedades), senão o firewall bloqueia. O envio sai a 15 fps com JPEG 70, cerca de 6 Mb/s por câmera.
Plano B: o PC tem Tailscale; com Tailscale no notebook também, use o endereço 100.x dele, que funciona em qualquer rede.

**Evento:**

- PC e notebook na mesma rede. No evento, o mais seguro é um **cabo de rede direto** entre os dois, ou um roteador só da obra; Wi-Fi de festa costuma cair.
- Com cabo direto sem roteador, os dois pegam endereço automático (169.254.x.x) em ~1 minuto; funciona igual.
- O IP do notebook pode mudar no evento: rode o `--remota` de novo lá (leva segundos).
