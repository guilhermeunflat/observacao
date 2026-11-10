# USB: o que limita, e dá para ligar 15 webcams com o que já existe em casa?

> **CORREÇÃO (05/11, teste real com 4 webcams):** o limite é **por controlador, não por porta**. Três webcams 1bcf:2281 em três portas azuis diferentes (mesmo controlador da CPU) → a terceira não abre. O mesmo vale com hub, em MJPEG ou YUY2, em 640×480, 424×240 ou 352×288: **2 câmeras abertas por controlador**, sempre. O firmware reserva a banda máxima em qualquer modo.
> Também descoberto: (1) no DirectShow a resolução precisa ser definida **antes** do FOURCC e **não** se pode pedir fps, senão a câmera volta para YUY2; (2) a câmera só oferece MJPEG a 30 fps; (3) uma das webcams do lote é de outro modelo, "DV20 USB CAMERA" (VID 4c4a, PID 4a55); (4) abrir uma câmera e receber o primeiro quadro leva ~1,9 s.
> Capacidade real deste PC: 3 controladores com porta física × 2 = **6 câmeras ao vivo**. A placa tem 2 slots PCIe livres (SMBIOS: x8 e x4 do chipset). As seções abaixo, que supõem um tubo por porta, ficam como histórico.


Levantado em 28/10/2026 direto do PC (Gigabyte **X570 AORUS ELITE WIFI**, Ryzen 7 3800X), com `Get-PnpDevice`. A resposta curta: **sim, dá para chegar a 15 câmeras sem comprar nada de USB**, com três condições que só o teste de carga confirma (seção 5).

## 1. O que limita de verdade (não é o número de portas)

Uma webcam USB 2.0 fala em *High Speed*: 480 Mb/s brutos num "tubo". Quem define quantas câmeras cabem num tubo não é o fluxo real de vídeo (MJPEG 640×480 a 15 fps usa 10–30 Mb/s), e sim a **reserva** que o driver faz quando a câmera começa a transmitir:

1. **Reserva isócrona por alt-setting.** O firmware da câmera anuncia vários tamanhos de pacote (ex.: 1024, 2048, 3072 bytes por microquadro). Ao abrir o vídeo, a câmera diz quanto quer (`dwMaxPayloadTransferSize`) e o driver `usbvideo.sys` **bloqueia** essa fatia do tubo, usada ou não. 3072 B/µframe ≈ 196 Mb/s. A norma só deixa 80 % do tubo para isócrono (≈ 384 Mb/s). Logo, uma câmera "gulosa" que pede 196 Mb/s cabe só **2 por tubo**; uma que pede proporcional à resolução cabe 5 ou 6. Webcams baratas de chipset Sunplus costumam pedir muito mesmo em resolução baixa. **Isso é a incógnita nº 1 e só o teste resolve.**
2. **Tubos por controlador.** Em controladores xHCI (todos os USB 3.x), **cada porta raiz tem o seu próprio tubo de 480 Mb/s** para dispositivos USB 2.0 (é assim que o driver do Linux calcula banda, por porta raiz; o Windows segue a mesma lógica). O que se compartilha é a capacidade interna total do chip, que costuma ser folgada mas não é publicada. A nota antiga em `docs/pesquisa_tecnica.md` dizia que todas as portas de um controlador dividiam um único tubo: isso vale para controladores EHCI antigos (até ~2012), não para esta placa.
3. **Hub = um tubo só.** Tudo que pendura num hub (3.0 ou 2.0) divide o tubo da porta onde o hub está. Hub não cria banda; só multiplica tomadas.
4. **Energia.** Porta USB 3.x entrega 900 mA; porta 2.0, 500 mA. Cada webcam puxa 150–250 mA. Hub **sem fonte** numa porta 3.x repassa ~900 mA no total → 3 câmeras com folga, 4 no limite. Hub sem fonte numa porta 2.0 → 2 câmeras.
5. **Recursos do controlador.** Cada câmera ocupa endpoints/slots; controladores xHCI aguentam dezenas, mas o Windows dá "Not enough USB controller resources" quando um chip estoura. Com 5 a 6 câmeras por controlador não chega perto.

## 2. Mapa real desta placa (lido do Windows em 28/10)

| Controlador | Onde | Portas que ele atende | O que está plugado hoje |
|---|---|---|---|
| AMD xHCI **da CPU** (bus 12) | 4 USB 3.2 Gen1 **azuis** traseiras | 4 portas raiz = 4 tubos | **4 discos externos** (Seagate, 2× SanDisk) nas portas 5, 6, 7, 8 |
| AMD xHCI **chipset A** (bus 7, fn 1) | 2 USB 3.2 Gen2 **vermelhas** traseiras + hub interno Genesys (GL850) com os **4 USB 2.0 pretos** + controlador de LED da placa | 2 tubos + 1 tubo compartilhado pelos 4 USB 2.0 | 2 discos externos nas vermelhas (portas 7 e 8); receptores Logitech (mouse/teclado) e um conversor USB‑serial nos USB 2.0 |
| AMD xHCI **chipset B** (bus 7, fn 3) | Bluetooth da placa Wi‑Fi + um 2º hub Genesys **sem nada ligado** (os 2 headers USB 2.0 internos F_USB1/F_USB2) + os **2 headers USB 3.2 Gen1 de 19 pinos** (4 portas) e o header Type‑C Gen2, conforme o manual da Gigabyte | 1 tubo (hub 2.0) + **4 tubos** nos headers 3.0 (precisam de bracket, ~R$ 35 cada um com 2 portas) | nada |
| NVIDIA xHCI (RTX 2070 Super) | sem conector físico | 0 | nada |

Ou seja: **6 portas USB 3.x traseiras, todas ocupadas por discos externos**, e os 4 USB 2.0 passam por um único hub interno (um tubo para os quatro). Manual da Gigabyte (trecho literal): CPU: 4× USB 3.2 Gen1 traseiras; Chipset: 2× Gen2 traseiras, 4× Gen1 por 2 headers de 19 pinos, 1 header Type‑C; "Chipset + 2 USB 2.0 Hubs: 8 × USB 2.0 (4 traseiras, 4 em headers internos)". Isso bate com o que o Windows mostra (2 hubs Genesys VID_05E3).

Diagnóstico próprio, sem instalar nada:

```bash
powershell -Command "Get-PnpDevice -PresentOnly | ? { $_.InstanceId -like 'USB\*' } | % { $p=(Get-PnpDeviceProperty -InstanceId $_.InstanceId -KeyName DEVPKEY_Device_Parent).Data; $l=(Get-PnpDeviceProperty -InstanceId $_.InstanceId -KeyName DEVPKEY_Device_LocationInfo).Data; \"$($_.FriendlyName) | $l | pai=$p\" }"
```

Para ver os alt-settings e o `MaxPacketSize` de uma webcam (incógnita nº 1), use o **USB Device Tree Viewer** (Uwe Sieber, grátis, sem instalação): selecione a câmera e procure "wMaxPacketSize" nos endpoints isócronos da interface `mi_01`.

## 3. Distribuição proposta para 15 câmeras com o que existe

Material em casa: 10 portas traseiras, 3 hubs USB 3.0 de 4 portas **sem fonte**, extensores. Premissa conservadora: 3 câmeras por tubo em 640×480 MJPEG 15 fps.

| Tubo | Porta | Câmeras | Observação |
|---|---|---|---|
| CPU azul 1 | hub A | 3 | hub alimentado pela porta (900 mA): 3 câmeras ≈ 600 mA, ok |
| CPU azul 2 | hub B | 3 | idem |
| CPU azul 3 | hub C | 3 | idem; 4ª porta do hub recebe os 2 receptores Logitech (tráfego mínimo) |
| CPU azul 4 | direto | 1 | |
| Chipset A vermelha 1 | direto | 1 | |
| Chipset A vermelha 2 | direto | 1 | |
| Chipset A 4× USB 2.0 (1 tubo) | direto | 3 | 4ª porta USB 2.0 → USB do monitor touch |
| **Total** | | **15** | 5 reservas ficam na caixa, já cadastradas |

Se o teste mostrar que a câmera é "gulosa" (2 por tubo), com 320×240 ou com o header de 19 pinos (2 tubos a mais, bracket de ~R$ 35) ainda chega a 15; só se nada disso bastar entra a placa PCIe (1 chip = 1 tubo para 4 portas; placas de "4 controladores" custam caro). Se mostrar 5 por tubo, os hubs podem ter 4 câmeras cada e sobra porta.

**Consequência prática para os testes em casa:** os 6 discos externos precisam sair das portas traseiras durante os testes (ou ficar em um único hub numa porta vermelha, se forem discos com fonte própria). No evento, nenhum disco vai.

## 4. Por que não comprar placa PCIe ainda

- Uma placa VL805/FL1100 de 4 portas adiciona **1 tubo**, não 4 (um chip xHCI por placa). Equivale a ganhar uma porta azul.
- A placa de 4 controladores (StarTech PEXUSB3S44V) custa mais de R$ 1.000 no Brasil e não chega em 17 dias com segurança.
- Os **2 headers USB 3.0 de 19 pinos** dão até **4 tubos** por ~R$ 35 cada bracket de 2 portas, se não estiverem em uso pelo painel frontal do gabinete. É a primeira expansão, bem antes de placa PCIe.

## 5. O teste que decide (`tools/bench_usb.py`, Fase 1)

1. Com **1 câmera** no USB Device Tree Viewer: anotar os `wMaxPacketSize` dos alt-settings e o que ela pede em 640×480/15, 640×480/30 e 320×240/15 (o viewer mostra o alt-setting ativo enquanto `bench_usb.py` captura).
2. Num **único hub** numa porta azul: abrir 1, 2, 3, 4 câmeras em 640×480 MJPEG 15 fps; registrar fps real de cada uma por 60 s e quando a última "fica preta". Repetir em 320×240. → **N por tubo**.
3. **3 câmeras em 3 portas azuis diferentes** sem hub, depois 4, depois somar as vermelhas: se todas mantêm fps, confirma que cada porta é um tubo e que o chip da CPU aguenta a soma.
4. Montar a tabela da seção 3 com os números reais e rodar 15 câmeras por 10 minutos (critério de aceite da Fase 1).
