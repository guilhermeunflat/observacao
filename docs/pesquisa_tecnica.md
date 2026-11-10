# Pesquisa técnica — instalação OBSERVAÇÃO

Contexto: Windows 11, Python 3.11, RTX 2070 Super, 15–20 webcams USB idênticas, 5 telas, tracking de cabeça e projeção off-axis.
Data da pesquisa: 2026-10-28. Só constam URLs abertas ou que apareceram nos resultados de busca. Onde não foi possível abrir a página, isso está indicado.

---

## 1. Webcam Mercado Livre MLB24564760 (VID 1BCF / PID 2281)

**O anúncio não pôde ser aberto** (Mercado Livre devolve HTTP 403 para fetch automático em `produto.mercadolivre.com.br/MLB-24564760` e `mercadolivre.com.br/p/MLB24564760`). Abra manualmente no navegador para confirmar fotos da base/rosca e a seção "Perguntas".

O que se sabe pelo VID:PID:

- `USB\VID_1BCF&PID_2281` = **Sunplus Innovation Technology SPCA2281 Web Camera**, classe USB 0e-01-00 (UVC). É um chipset genérico de webcam de baixo custo, usado por dezenas de marcas "white label".
  - Fonte: https://devicehunt.com/view/type/usb/vendor/1BCF/device/2281
  - Fonte: https://linux-hardware.org/index.php?id=usb:1bcf-2281
  - Fonte: https://www.devicekb.com/hardware/usb-vendors/vid_1bcf-pid_2281
- É UVC padrão: no Linux usa `uvcvideo` (kernel ≥ 2.6.26); no Windows aparece como "USB Camera"/"USB Video Device" com o driver `usbvideo.sys` da Microsoft. Sem driver proprietário.
  - Fonte: https://linux-hardware.org/index.php?id=usb:1bcf-2281
- Um review no webcamtests.com de um exemplar com o mesmo ID (vendido como "WN FullHD Camera", modelo WN-L2204k326L / "1080OPF") mediu: 1920×1080, **~20 fps reais** no navegador, bitrate 32 MB/s. Ou seja: "Full HD 30 fps" do anúncio costuma ser 1080p MJPEG com fps real menor.
  - Fonte: https://webcamtests.com/reviews/168782
- **Formatos**: a família Sunplus SPCA22xx em UVC expõe tipicamente MJPEG (até 1080p) e YUY2 (raw, em resoluções baixas). Não encontrei a lista `v4l2-ctl --list-formats-ext` publicada para o 2281; confirme na sua unidade (comando abaixo).
  - Fonte (padrão YUYV+MJPG em webcams UVC genéricas): https://www.mikrocontroller.net/topic/539146
- **Rosca 1/4"**: não foi possível confirmar no anúncio. Modelos "com tripé" desse tipo costumam trazer rosca 1/4" na base dobrável; verifique nas fotos/perguntas do anúncio.
- **Relatos de várias iguais no mesmo PC**: nada específico para o 1BCF:2281. O problema genérico (banda/endpoints por controlador) está na seção 2–3.

Como obter a lista real de formatos/resoluções/fps no Windows (sem Linux):

```python
# pip install cv2-enumerate-cameras opencv-python
import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640); cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
print(cap.get(cv2.CAP_PROP_FOURCC), cap.get(cv2.CAP_PROP_FPS))
```

Alternativa mais completa: `ffmpeg -f dshow -list_options true -i video="USB Camera"` lista todos os pares formato/resolução/fps que o driver UVC anuncia (pacote `capture-devices` usa a mesma abordagem).
- Fonte: https://pypi.org/project/capture-devices

**Recomendação**: comprar 1 unidade antes do lote, rodar `ffmpeg -list_options`, confirmar MJPEG 640×480 @ 30 e @ 15 fps e medir o fps real por 5 min. Só então comprar as outras 19.

---

## 2. Muitas webcams idênticas no Windows: identificador estável e mapeamento de índices

### 2.1 Identificadores estáveis

- **DirectShow**: cada moniker de `CLSID_VideoInputDeviceCategory` tem no `IPropertyBag` a propriedade `DevicePath`. A Microsoft documenta que "não é legível, mas é garantidamente único por dispositivo" e serve para distinguir duas instâncias do mesmo modelo.
  - Fonte: https://learn.microsoft.com/fi-fi/windows/win32/directshow/selecting-a-capture-device
  - Fonte: https://learn.microsoft.com/en-ie/Windows/Win32/directshow/using-the-system-device-enumerator
- **Media Foundation**: `MFEnumDeviceSources` devolve `IMFActivate[]`; de cada um lê-se `MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_SYMBOLIC_LINK` (único no sistema) e `MF_DEVSOURCE_ATTRIBUTE_FRIENDLY_NAME` (não único). Com o symbolic link em mãos, pode-se criar a fonte diretamente com `MFCreateDeviceSource`/`MFCreateDeviceSourceActivate`.
  - Fonte: https://learn.microsoft.com/en-us/windows/win32/medfound/enumerating-video-capture-devices
  - Fonte: https://learn.microsoft.com/en-us/windows/win32/medfound/handling-video-device-loss
  - Fonte: https://learn.microsoft.com/en-za/windows/win32/api/mfidl/nf-mfidl-mfenumdevicesources
- O formato do symbolic link/device path é `\\?\usb#vid_1bcf&pid_2281&mi_00#<instância>#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global`. O trecho `<instância>` (ex.: `6&153a3df0&0&0000`) é a *Device Instance ID* gerada pelo PnP: para dispositivos **sem número de série USB** (caso das webcams baratas) ela deriva da **porta física** (hub + número da porta), então muda se você trocar a câmera de porta, e permanece se a mesma porta for usada. Isso é exatamente o que você quer: identidade = porta.
  - Fonte (exemplos reais do formato): https://hero.handmade.network/forums/code-discussion/t/7031/p/21540
  - Fonte: https://windows-hexerror.linestarve.com/q/so58201892-how-to-get-hardware-id-when-enumerating-with-windows-media-foundation
  - Relato de usuário com 2 câmeras idênticas: ao trocar as portas, as câmeras "invertem" — ou seja, o DevicePath segue a porta, não a unidade física.
    - Fonte: https://forum.xojo.com/t/directshowpropertybagmbs-read-what-parameter/67096
- Para mapear device path → porta/hub de forma legível, use **USB Device Tree Viewer** (Uwe Sieber) ou USBView: ambos mostram controlador → hub → porta → dispositivo, com endpoints.
  - Fonte: https://borncity.com/win/2019/09/06/windows-10-not-enough-usb-controller-resources/
  - Fonte: https://obsproject.com/forum/threads/2-usb-cameras-work-but-not-3.124695/

### 2.2 Ordem dos índices do OpenCV

- **CAP_DSHOW**: `videoInput::listDevices()` em `cap_dshow.cpp` cria `ICreateDevEnum` → `CreateClassEnumerator(CLSID_VideoInputDeviceCategory)` → percorre `pEnum->Next()` incrementando um contador; **o índice é a posição nessa enumeração, sem ordenação**, e só lê `FriendlyName`. Não há como abrir por DevicePath.
  - Fonte: https://raw.githubusercontent.com/opencv/opencv/4.x/modules/videoio/src/cap_dshow.cpp
- **pygrabber** (`FilterGraph.get_input_devices()`) usa o mesmo `ICreateDevEnum`/`CLSID_VideoInputDeviceCategory` do DirectShow, portanto **a ordem coincide com a do CAP_DSHOW** (mesma API do sistema, chamada no mesmo processo). Não há documentação oficial afirmando isso; é consequência de ambos usarem o mesmo enumerador. Valide uma vez no seu PC (procedimento no 2.4). pygrabber v0.2 (out/2023) está pouco mantido.
  - Fonte: https://pypi.org/project/pygrabber
  - Fonte: https://forum.opencv.org/t/cant-open-2-camera-ps3-eye/23374/5
- **CAP_MSMF**: `CvCapture_MSMF::open(int index)` chama `DeviceList::read()` → `MFEnumDeviceSources` e ativa `devices[index]`. O índice é a posição no array devolvido por `MFEnumDeviceSources`. Não há abertura por symbolic link no OpenCV.
  - Fonte: https://raw.githubusercontent.com/opencv/opencv/4.x/modules/videoio/src/cap_msmf.cpp
- A ordem de `MFEnumDeviceSources` e do enumerador DirectShow **não é documentada e não é estável entre reboots/replug** (depende da topologia USB e da ordem de inicialização). Vários relatos de índice "pulando" de câmera.
  - Fonte: https://forum.opencv.org/t/unclear-and-unstable-meaning-of-videocapture-camera-index-on-windows-msmf-when-multiple-cameras-are-present/24262
  - Fonte: https://github.com/bpawletz/Aalaapi-Sky/issues/181
- OpenCV codifica o backend no índice: `cv2.VideoCapture(701)` = câmera 1 no DSHOW (700); 1401 = câmera 1 no MSMF (1400).
  - Fonte: https://pypi.org/project/cv2-enumerate-cameras/

### 2.3 Bibliotecas Python que expõem device path

| Biblioteca | Backend | Expõe path? | Observação |
|---|---|---|---|
| **cv2-enumerate-cameras** (`pip install cv2-enumerate-cameras`) | MSMF e DSHOW (Windows), V4L2/GStreamer, AVFoundation | **Sim** (`CameraInfo.path`, `.vid`, `.pid`, `.index`, `.backend`) | Mantido (2025), enumera **com a mesma API que o OpenCV usa**, então `index` já é o índice correto para `cv2.VideoCapture(info.index, info.backend)`. **Recomendado.** |
| pyusbcameraindex | DSHOW | Sim (index, name, vid, pid, path) | Windows only; site do PyPI não abriu no fetch. |
| windows-capture-device-list | DSHOW | Não (só nomes + resoluções) | Extensão C++. |
| pygrabber | DSHOW | Não (só nomes) | Útil para grafo DirectShow; pouco mantido. |
| capture-devices | ffmpeg dshow | "alternative name" (= device path) | Depende de ffmpeg. |
| pymf | — | não encontrado no PyPI | |

- Fonte: https://pypi.org/project/cv2-enumerate-cameras/
- Fonte: https://github.com/chinaheyu/cv2_enumerate_cameras
- Fonte: https://pypi.org/project/pyusbcameraindex/1.0.1
- Fonte: https://pypi.org/project/windows-capture-device-list/
- Fonte: https://pypi.org/project/capture-devices

```python
from cv2_enumerate_cameras import enumerate_cameras
import cv2
for info in enumerate_cameras(cv2.CAP_MSMF):   # ou cv2.CAP_DSHOW
    print(info.index, info.name, hex(info.vid or 0), hex(info.pid or 0), info.path)
# abrir pelo path estável:
PATHS = {"tela1_esq": r"\\?\usb#vid_1bcf&pid_2281&mi_00#7&2a1b3c4d&0&0000#{65e8773d-...}\global", ...}
by_path = {i.path.lower(): i for i in enumerate_cameras(cv2.CAP_MSMF)}
cap = cv2.VideoCapture(by_path[PATHS["tela1_esq"].lower()].index, cv2.CAP_MSMF)
```

### 2.4 Limite de dispositivos UVC por controlador ("Not enough USB controller resources")

- O erro é de **endpoints**, não de energia: controladores xHCI Intel têm limite de **96 endpoints por controlador**; AMD chega a **254**. Cada webcam UVC consome tipicamente 3–5 endpoints (controle, vídeo isócrono, interrupção, áudio se tiver microfone). Em xHCI Intel, 20 webcams com microfone (≈5 endpoints cada = 100) podem estourar o limite num só controlador; em AMD B450/X570 (Ryzen) o teto de 254 é folgado.
  - Fonte: https://borncity.com/win/2019/09/06/windows-10-not-enough-usb-controller-resources/
  - Fonte: https://www.lention.com/blogs/news/not-enough-usb-controller-resources-usb-c-hub
  - Fonte: https://appuals.com/fix-not-enough-usb-controller-resources/
  - Fonte (caso real em X570, mensagem exata no Windows): https://learn.microsoft.com/en-us/answers/questions/4195485/not-enough-usb-controller-resources
- Relato: 12 câmeras funcionaram num PC Windows; a 13ª deu "Not Enough USB Controller Resources".
  - Fonte: https://www.agisoft.com/forum/index.php?topic=1920.0
- O outro limite é **banda isócrona** (seção 3). Ao abrir o stream, o Windows pode falhar silenciosamente (frame preto/`cap.read()` False) ou com erro de "bandwidth" no Gerenciador de Dispositivos; antigamente o Gerenciador mostrava a aba "Avançado" com % de banda por controlador (ex.: "20% reservado + 48% por câmera").
  - Fonte: https://forums.tomshardware.com/threads/trying-to-run-8-usb-webcams-on-single-computer.1329901/
- Como contar endpoints e banda no Windows: **USB Device Tree Viewer** (mostra soma de endpoints por root hub e, em cada interface de vídeo, os *alternate settings* com `wMaxPacketSize` do endpoint isócrono — a banda reservada por câmera = `wMaxPacketSize × transações/µframe × 8000 µframes/s`).
  - Fonte: https://borncity.com/win/2019/09/06/windows-10-not-enough-usb-controller-resources/
- O quirk `usbvideo.sys` do Windows não permite forçar "bandwidth cap" como o `uvcvideo.bandwidth_cap` do Linux; a única alavanca é escolher formato/resolução/fps que selecione um alt-setting menor (MJPEG 640×480 em vez de 1080p) e **espalhar por controladores**.
  - Fonte: https://www.thegoodpenguin.co.uk/blog/multiple-uvc-cameras-on-linux/

### 2.5 Solução recomendada, passo a passo

1. **Inventário**: instale USB Device Tree Viewer; anote quantos controladores xHCI (`USB xHCI Compliant Host Controller`) o PC tem e quais portas traseiras/frontais caem em cada um (plugue uma câmera e veja onde aparece).
2. **Hardware**: cada controlador USB 2.0 (480 Mb/s) comporta com segurança **2–3 câmeras a 640×480 MJPEG 30 fps** e **até ~6 a 15 fps** se o firmware não super-reservar (ver §3). Para 15–20 câmeras planeje **6–8 controladores independentes**: 2–3 da placa-mãe + placas PCIe com controladores dedicados por porta (§3.3).
3. **Cabeamento fixo**: cada câmera numa porta fixa; nunca use hubs sem necessidade (um hub concentra tudo no mesmo controlador). Etiquete porta ↔ posição na instalação.
4. **Enumerar por path**: `cv2-enumerate-cameras` com `CAP_MSMF`; grave num `cameras.json` o mapa `nome_lógico → device_path` (uma vez, com utilitário de calibração que abre cada câmera e mostra a imagem para você nomear).
5. **Abrir**: resolva path → índice **a cada inicialização** (nunca grave índices) e abra com `cv2.VideoCapture(index, cv2.CAP_MSMF)`; force `CAP_PROP_FOURCC = MJPG`, 640×480, fps desejado, `CAP_PROP_BUFFERSIZE = 1`. Abra as câmeras **sequencialmente** com ~0,5 s de intervalo (o UVC serializa a inicialização).
   - Fonte (inicialização serializada 0,5–1 s/câmera): https://github.com/mastduki/uvc-multicam
6. **Threads**: uma thread por câmera (`cap.grab()`/`retrieve()`) guardando só o último frame; com 20 câmeras × 640×480 × 15 fps o decode MJPEG em CPU é leve (~2 MB/s por câmera).
7. **Watchdog**: se `read()` falhar por N frames, release + reabrir pelo path; se a enumeração não encontrar o path, logar "câmera X desconectada" (porta errada).
8. **Teste de carga**: script que abre N câmeras incrementalmente e reporta fps real por câmera e qual falhou — assim você descobre empiricamente o limite por controlador antes da montagem.

---

## 3. Limite prático de webcams por controlador xHCI (USB 2.0) e placas PCIe

### 3.1 Números

- USB 2.0 High Speed = 480 Mb/s; a norma reserva no máximo **80 % de cada microquadro** para isócrono → **~384 Mb/s** para todas as câmeras do controlador; alguns textos citam 196 Mb/s por dispositivo.
  - Fonte: https://www.thegoodpenguin.co.uk/blog/multiple-uvc-cameras-on-linux/
  - Fonte: https://www.96boards.org/documentation/consumer/guides/multi-usb-camera.md.html
- O que conta é a **banda reservada pelo alt-setting** que o firmware pede (`dwMaxPayloadTransferSize`), **não** o fluxo real. Webcams baratas pedem o mesmo valor alto para qualquer resolução (ex.: 3060 B/µframe ≈ 195 Mb/s → só 1–2 câmeras por barramento, mesmo a 320×240). Esse é o motivo nº 1 de "a 3ª câmera fica preta".
  - Fonte: https://www.thegoodpenguin.co.uk/blog/multiple-uvc-cameras-on-linux/
  - Fonte: https://github.com/AgRoboticsResearch/uvc_multi_cam_patch
  - Fonte: https://forum.arducam.com/t/linux-uvc-driver-bandwidth-issues/6731
- Dados reais 640×480 MJPEG, um hub USB 2.0 / um controlador:
  - 30 fps: **2 câmeras**; 15 fps: **até 3**; raw (YUY2) na resolução padrão: nem 2 cabem.
    - Fonte: https://www.96boards.org/documentation/consumer/guides/multi-usb-camera.md.html
  - **6 câmeras** 640×480 MJPEG @ 30 fps contínuas num único barramento USB 2.0 (Raspberry Pi, V4L2), com câmeras cujo firmware reserva banda proporcional.
    - Fonte: https://github.com/mastduki/uvc-multicam
  - 8 câmeras 1280×720 MJPEG @ 30 fps (4 por controlador) só com patch do driver Linux.
    - Fonte: https://github.com/AgRoboticsResearch/uvc_multi_cam_patch
- **YUY2** 640×480 @ 30 fps = 640×480×2 B×30 = 147 Mb/s *reais* por câmera → no máximo 2 por controlador USB 2.0; @ 15 fps = 74 Mb/s → 4–5 teóricas. MJPEG 640×480 fica em 10–30 Mb/s reais, mas a *reserva* pode ser bem maior (ver acima). Use **MJPEG sempre**.
- Relatos de fóruns:
  - 8 webcams num PC (2013): máximo 6 funcionando; ~150 Mb/s por câmera; "máx. 2 câmeras por controlador USB 2.0".
    - Fonte: https://forums.tomshardware.com/threads/trying-to-run-8-usb-webcams-on-single-computer.1329901/
  - OBS: 2 câmeras OK, 3ª preta — limite por controlador; solução: USBView para distribuir entre controladores, hub alimentado para energia (hub **não** resolve banda).
    - Fonte: https://obsproject.com/forum/threads/2-usb-cameras-work-but-not-3.124695/
  - 12 câmeras OK, 13ª "Not enough USB controller resources" (Windows 8).
    - Fonte: https://www.agisoft.com/forum/index.php?topic=1920.0
  - NVIDIA Jetson: USB 2.0 e USB 3.0 têm root hubs separados; dispositivos USB 2.0 caem no controlador 2.0 mesmo ligados numa porta azul.
    - Fonte: https://forums.developer.nvidia.com/t/insufficient-bandwidth-when-using-multiple-usb-cameras/232422
  - Não encontrei thread específica de 10–20 webcams em r/TouchDesigner ou forum.opencv.org (buscas feitas sem resultado); as fontes acima são Tom's Hardware, OBS, Agisoft, NVIDIA e GitHub.

**Nota sobre xHCI (corrigida em 28/10 após mapear a placa-mãe):** em controladores xHCI cada **porta raiz** tem o seu próprio tubo USB 2.0 de 480 Mb/s (o driver xhci do Linux contabiliza banda por porta raiz; o Windows segue a mesma lógica). O que se compartilha entre as portas é a capacidade interna do chip, não publicada mas normalmente folgada. A ideia de "um tubo por controlador" vale para EHCI (USB 2.0 puro, placas antigas). Um **hub** continua sendo um tubo só para tudo que está nele. Mapa real das portas deste PC e a distribuição proposta: `docs/usb.md`.

### 3.2 Planejamento para 15–20 câmeras

- Regra conservadora: **3 câmeras (640×480 MJPEG, 15 fps) por controlador** → 20 câmeras = 7 controladores. Regra otimista (firmware bem comportado, medido): 5–6 por controlador → 4 controladores.
- Teste com 1 unidade antes de comprar as placas: abra N cópias numa só porta/hub até falhar; isso dá o limite real deste chipset.

### 3.3 Placas PCIe com controladores independentes

- **StarTech PEXUSB3S44V** (PCIe x4, 4 portas, **4 controladores Renesas/NEC independentes**, alimentação SATA/LP4 opcional, 900 mA/porta): cada porta é um xHCI próprio → 4 "barramentos" USB 2.0 de 480 Mb/s cada. É a escolha clássica para câmeras.
  - Fonte: https://www.pbtech.com/pacific/product/ADPSTT2552329/StarTechcom-PEXUSB3S44V-4-Port-Quad-Bus-PCIe-USB-3
  - Fonte: https://store.cmsdistribution.com/startech-com-pexusb3s44v-interface-cards-adapter-internal-usb-3-2-gen-1-3-1-gen-1-v209453
  - Fonte: https://coastipc.com/4x-usb-3-1-expansion-card-with-dedicated-controllers
- Placas **ASM3142** "4 portas": normalmente **2 controladores** (2 portas por chip), não 4. Verifique a ficha: "dual ASM3142" = 2 controladores.
  - Fonte: https://www.newegg.com/p/N82E16812400546
  - Fonte: https://uk.rs-online.com/web/p/usb-cards/1863259
- Placas **FL1100 (Fresco) e VL805 (VIA)** baratas de 4 portas: 1 chip = **1 controlador** compartilhado pelas 4 portas → só 1 "barramento" de 480 Mb/s. Servem como +1 controlador cada (uma por slot PCIe x1), mas não como 4. Não encontrei fonte abrindo isso especificamente; é a arquitetura desses chips (um xHCI por chip).
- Há placas de 8 portas com 4 controladores + bridge PCIe (marcadas para câmeras/servidores) em marketplaces; confirme o chipset antes de comprar.
  - Fonte: https://www.ebay.de/itm/335572796345
  - Fonte: https://linustechtips.com/topic/1503601-looking-for-usb-pcie-expansion-card-with-separate-controllers/

### 3.4 Portas da placa-mãe B450/X570

- **Não existe mapa universal**: depende do modelo. Em AM4 as portas vêm de dois lugares: xHCI **da CPU** (Ryzen 3000 "Matisse": 4× USB 3.x) e xHCI **do chipset** (B450: até 2× USB 3.1 Gen1 + 6× USB 2.0; X570: 2–3 controladores Matisse/Starship separados). Relatos mostram X570 com 3 controladores xHCI (`lsusb -t` → Bus 04/06/08) e B450 com 2 (CPU + chipset).
  - Fonte: https://forum.level1techs.com/t/usb-3-2-gen2-surprise-on-am4/191742
  - Fonte: https://www.t2linux.com/hardware/board/Asus/Pro%20WS%20X570-ACE/
  - Fonte: https://www.eatyourbytes.com/chipset-comparison/amd_b450&amd_x570/
  - Fonte: https://elevenforum.com/t/question-about-rear-usb-ports.32937
- Como descobrir no seu PC: HWiNFO ou USB Device Tree Viewer → plugue um pendrive em cada porta e veja sob qual "USB xHCI Compliant Host Controller" ele aparece; anote o mapa. Em geral, as portas USB 3.1 Gen2 traseiras vão para a CPU e os headers internos/USB 2.0 para o chipset.
  - Fonte: https://forum.level1techs.com/t/asrock-x570d4i-2t/154306/197
  - Fonte: https://forums.guru3d.com/goto/post?id=6091791

**Recomendação**: placa-mãe (2–3 controladores) + 1× PEXUSB3S44V (4 controladores) = 6–7 controladores → 18–21 câmeras a 3 por controlador. Se faltar slot, 2× placas VL805/FL1100 x1 (1 controlador cada).

---

## 4. Projeção off-axis (Kooima) com várias telas e tracking de cabeça por webcam

### 4.1 Fórmula (Kooima, "Generalized Perspective Projection", 2008/2009)

Entrada: cantos da tela em coordenadas do mundo `pa` (inferior-esquerdo), `pb` (inferior-direito), `pc` (superior-esquerdo); posição do olho `pe`; near `n`, far `f`.

```
vr = normalize(pb - pa)          # eixo "direita" da tela
vu = normalize(pc - pa)          # eixo "cima"
vn = normalize(cross(vr, vu))    # normal (aponta para o espectador)
va = pa - pe;  vb = pb - pe;  vc = pc - pe
d  = -dot(va, vn)                # distância olho→plano da tela
l  = dot(vr, va) * n / d
r  = dot(vr, vb) * n / d
b  = dot(vu, va) * n / d
t  = dot(vu, vc) * n / d
P  = frustum(l, r, b, t, n, f)   # = glFrustum
M^T = [[vr.x, vr.y, vr.z, 0],
       [vu.x, vu.y, vu.z, 0],
       [vn.x, vn.y, vn.z, 0],
       [0,0,0,1]]
T  = translate(-pe)
Projeção final = P · M^T · T
```

- Fonte (paper original; a página `csc.lsu.edu/~kooima/articles/genperspective/` devolveu 404 no fetch; o paper está indexado aqui): https://www.semanticscholar.org/paper/Generalized-Perspective-Projection-Kooima/14d1b312aba825bcce17edd67e3fdc139f1a76a2
- Fonte (fórmula completa + código, Wikibooks): https://en.wikibooks.org/wiki/Cg_Programming/Unity/Projection_for_Virtual_Reality
- Fonte (biblioteca C++ do mesmo cálculo): https://github.com/DisplayXR/displayxr-common
- Fonte (explicação Unity): https://medium.com/try-creative-tech/off-axis-projection-in-unity-1572d826541e

**Várias telas**: uma tela = um trio `(pa, pb, pc)` medido em metros no mesmo sistema de coordenadas (origem = um ponto fixo da instalação). O mesmo `pe` vindo do tracker gera 5 matrizes diferentes (uma por tela) a cada frame; a cena 3D é uma só. Telas não precisam ser coplanares nem do mesmo tamanho. É o que o CAVE/ImmersaDesk faz.
- Fonte: https://www.evl.uic.edu/pape/CAVE/idesk/paper
- Fonte: https://www.evl.uic.edu/pape/CAVE/ConfigTricks.html

### 4.2 Python (numpy) — matriz pronta para OpenGL (column-major)

```python
import numpy as np
def off_axis(pa, pb, pc, pe, n=0.05, f=50.0):
    pa, pb, pc, pe = map(np.asarray, (pa, pb, pc, pe))
    vr = pb - pa; vr /= np.linalg.norm(vr)
    vu = pc - pa; vu /= np.linalg.norm(vu)
    vn = np.cross(vr, vu); vn /= np.linalg.norm(vn)
    va, vb, vc = pa - pe, pb - pe, pc - pe
    d = -va @ vn
    l, r = (vr @ va) * n / d, (vr @ vb) * n / d
    b, t = (vu @ va) * n / d, (vu @ vc) * n / d
    P = np.array([[2*n/(r-l), 0, (r+l)/(r-l), 0],
                  [0, 2*n/(t-b), (t+b)/(t-b), 0],
                  [0, 0, -(f+n)/(f-n), -2*f*n/(f-n)],
                  [0, 0, -1, 0]])
    Mt = np.eye(4); Mt[0,:3], Mt[1,:3], Mt[2,:3] = vr, vu, vn
    T = np.eye(4); T[:3,3] = -pe
    return (P @ Mt @ T).astype('f4')          # row-major; use .T.tobytes() ou transpose=True no glUniformMatrix4fv
```

Uso em pyglet 2 / moderngl: `prog['mvp'].write(off_axis(...).T.tobytes())` (moderngl) ou `shader['mvp'] = pyglet.math.Mat4(*off_axis(...).T.flatten())` (pyglet). Em pyglet 2 a matriz de projeção da janela é `window.projection` (Mat4); substitua a cada frame.
- Fonte: https://pyglet.readthedocs.io/en/latest/programming_guide/gl.html

Exemplos existentes (não Python, mas a mesma matemática): three.js + MediaPipe Face Landmarker (com calibração de FOV e IPD) e um demo WebGL.
- Fonte: https://github.com/VintagePhebe/head-tracked-3d-display
- Fonte: https://github.com/saint2706/off-axis-experiments
- Fonte: https://cass-e.net/2021/03/p5js-off-axis-projection/

### 4.3 Tracking de cabeça por webcam (posição 3D do olho)

- Modelo pinhole: `Z = f_px × tamanho_real / tamanho_px`, com `f_px = (largura_px/2) / tan(HFOV/2)`; `X = (u − cx) × Z / f_px`, `Y = (v − cy) × Z / f_px`. Depois aplique a pose da câmera (posição + inclinação) para levar ao sistema de coordenadas das telas.
  - Fonte: https://github.com/VintagePhebe/head-tracked-3d-display
- Referências de tamanho:
  - **Distância interpupilar (IPD)** ≈ 63 mm (média adulta). Erro cresce com yaw da cabeça; corrija usando a `facial_transformation_matrix` do Face Landmarker (primeira coluna = eixo interocular 3D) ou use a projeção do vetor olho-olho.
    - Fonte: https://github.com/VintagePhebe/head-tracked-3d-display
    - Fonte (IPD medido com Face Mesh + curva de calibração polinomial, 20–240 cm): https://www.mdpi.com/2673-9909/5/3/118
  - **Diâmetro da íris** ≈ 11,7 ± 0,5 mm (quase constante na população) → MediaPipe Iris estima distância com erro médio 4,3 % sem sensor de profundidade; precisa de olho com ≥ ~20–30 px, ou seja, câmera a < 1 m em 640×480 ou 1080p.
    - Fonte: https://research.google/blog/mediapipe-iris-real-time-iris-tracking-depth-estimation/
  - **Largura do rosto/bounding box** (Face Detection, BlazeFace): mais ruidoso (±15 %), mas funciona a 2–4 m com 640×480. Bom para "zona" e para fallback.
- API Python atual: `mediapipe.tasks.python.vision.FaceLandmarker` (modelo `face_landmarker.task`), `running_mode=LIVE_STREAM` com callback ou `VIDEO` com `detect_for_video(img, ts)`; devolve 478 landmarks (inclui íris: índices 468–477) e `facial_transformation_matrixes` (ative com `output_facial_transformation_matrixes=True`). Suavização só é aplicada com `num_faces=1`.
  - Fonte: https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python
- Calibração prática (1 ou 2 fotos): com a pessoa a distância conhecida (ex.: 1,0 m) resolva `f_px`; uma segunda captura a +20 cm permite estimar também a inclinação da webcam.
  - Fonte: https://github.com/VintagePhebe/head-tracked-3d-display
- Suavize `pe` com filtro One-Euro ou EMA (α ≈ 0,3) e limite a velocidade; mantenha a orientação da câmera virtual fixa (nada de `lookAt`), só `pe` muda — senão a cena "descola" das telas.
  - Fonte: https://github.com/VintagePhebe/head-tracked-3d-display
- Multi-câmera: várias webcams de tracking cobrindo zonas diferentes; escolha a que vê o rosto maior e converta para o sistema global com a pose de cada câmera.

### 4.4 Post do Reddit r/TouchDesigner "Perspective tracking on a 12 CRT video wall"

- Link: https://www.reddit.com/r/TouchDesigner/comments/1rvonan/
- **Não foi possível abrir** (reddit.com e old.reddit.com bloqueados para o fetch automático; buscas por título não retornaram o thread). Abra no navegador. Pelo contexto da técnica, o padrão em TouchDesigner é: uma Camera COMP por tela com `Projection = Off-Axis`/matriz customizada (`Projection Matrix` via Script), posição do olho vinda de um CHOP (Kinect/MediaPipe), e um Window COMP por saída — mesma matemática da seção 4.1. Confirme lendo o post.
- Referência de off-axis multi-superfície com CRTs (patente Sun, cada CRT como "patch" com matriz própria): https://patents.justia.com/patent/5446834

---

## 5. pyglet 2.x com várias janelas fullscreen / moderngl-window / upload rápido de texturas

### 5.1 pyglet 2.x

- Cada `Window` tem contexto próprio, mas **por padrão todos compartilham o mesmo object space** (texturas, shaders, VBOs, FBOs) com o "shadow context" criado ao importar `pyglet.gl`. Logo, uma textura criada uma vez serve para as 5 janelas sem fazer nada especial. Pode-se forçar com `Window(context=primary.context)`.
  - Fonte: https://pyglet.readthedocs.io/en/latest/programming_guide/context.html
  - Fonte: https://pythonhosted.org/pyglet/programming_guide/sharing_objects_between_contexts.html
- Uma janela fullscreen **não pode abranger vários monitores**; crie uma janela `fullscreen=True, screen=screens[i]` por monitor e ligue os mesmos handlers. Compartilhamento pode falhar se monitores estiverem em **GPUs diferentes** — mantenha todas as saídas na RTX 2070 Super.
  - Fonte: https://pyglet.readthedocs.io/en/latest/programming_guide/windowing.html
  - Fonte: https://pythonhosted.org/pyglet/programming_guide/using_multiple_windows.html

```python
import pyglet
display = pyglet.display.get_display()
screens = display.get_screens()
wins = [pyglet.window.Window(fullscreen=True, screen=s, vsync=True) for s in screens[:5]]
tex = pyglet.image.Texture.create(640, 480)      # compartilhada
for i, w in enumerate(wins):
    @w.event
    def on_draw(w=w, i=i):
        w.switch_to(); w.clear()
        w.projection = pyglet.math.Mat4(*off_axis(*SCREENS[i], pe).T.flatten())
        # desenhar cena
pyglet.app.run(1/60)
```

- Cuidado com vsync × 5 janelas: com `vsync=True` em cada uma, o `flip()` de cada janela pode bloquear ~16 ms sequencialmente (até ~80 ms/frame). Soluções: vsync só na primeira janela e `vsync=False` nas outras; ou NVIDIA Control Panel → "G-Sync/compatível" off e usar o loop com `pyglet.clock.schedule_interval` fixo; ou usar o Mosaic/Surround da NVIDIA para fundir as 5 telas numa única superfície e **uma só janela** (elimina o problema e dá swap sincronizado). Esta última é a mais robusta para instalação.
  - Fonte (vsync e flip por janela): https://pyglet.readthedocs.io/en/latest/programming_guide/windowing.html

### 5.2 Alternativa: moderngl + glfw (sem moderngl-window)

- `moderngl-window` é feito para **uma** janela; para várias, use `glfw` direto: `glfw.create_window(w, h, title, monitor, share)` — o 5º argumento `share` compartilha objetos com a primeira janela; `glfw.get_monitors()` dá os monitores para fullscreen. Crie um único `moderngl.create_context()` após tornar a primeira janela atual; para cada janela: `glfw.make_context_current(win)` → `ctx.screen` muda? Não: use `ctx.detect_framebuffer()` por janela ou simplesmente renderize com o contexto atual (os objetos são compartilhados).
  - Fonte: https://discourse.glfw.org/t/sharing-the-objects-created-at-first-window-by-all-other-windows/2185
  - Fonte: https://moderngl.readthedocs.io/en/stable/the_guide/functionality_expansion/window_using.html
  - Fonte: https://moderngl-window.readthedocs.io/
- Vantagem do moderngl: `texture.write(frame_bytes)` é um `glTexSubImage2D` direto e `ctx.buffer()` + `texture.write(buffer)` faz upload via PBO sem glue em C.

### 5.3 Frames OpenCV → textura (15 texturas 640×480 @ 15 fps)

- Carga total: 15 × 640×480×3 B × 15 fps ≈ **207 MB/s**. Isso é pequeno para PCIe 3.0 x16 (~12 GB/s) e para `glTexSubImage2D` simples; PBO só vale se o profiler mostrar stall na chamada.
  - Fonte (glTexSubImage2D direto pode ser até 2× mais rápido que PBO para texturas pequenas; o que importa é formato casado com o storage interno): https://community.khronos.org/t/fast-texture-uploads-pbo-threads/106829
  - Fonte: https://community.khronos.org/t/performance-of-texture-upload-with-pbo/61565
- Receita que evita conversões:
  1. Crie a textura **uma vez** (`GL_RGB8`, 640×480) com `glTexImage2D(..., None)`; nunca recrie.
  2. Envie o frame BGR do OpenCV como `GL_BGR` + `GL_UNSIGNED_BYTE` (evita `cvtColor`); ou troque canais no shader.
  3. `glPixelStorei(GL_UNPACK_ALIGNMENT, 1)` (linhas de 640×3 = 1920 B já são múltiplas de 4, mas fique seguro).
  4. Só faça upload quando houver frame novo (flag na thread da câmera); 15 fps de câmera vs 60 fps de render = 1 upload a cada 4 frames por câmera.
  5. Se precisar de PBO: 2 PBOs por textura (ping-pong) — `glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pbo[i]); glTexSubImage2D(..., 0); glBindBuffer(..., pbo[j]); glBufferData(..., None, GL_STREAM_DRAW); ptr = glMapBuffer(...); memcpy; glUnmapBuffer`.
     - Fonte: https://www.songho.ca/opengl/gl_pbo.html
     - Fonte: https://community.khronos.org/t/the-fastest-way-to-upload-large-textures/54268

```python
# pyglet 2 (PyOpenGL-style via pyglet.gl)
from pyglet.gl import *
tex = pyglet.image.Texture.create(640, 480, internalformat=GL_RGB8)
def upload(tex, frame_bgr):            # frame_bgr: numpy (480,640,3) uint8 contíguo
    glBindTexture(GL_TEXTURE_2D, tex.id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 640, 480, GL_BGR, GL_UNSIGNED_BYTE, frame_bgr.ctypes.data)
```

```python
# moderngl
tex = ctx.texture((640, 480), 3)          # RGB8
tex.write(np.ascontiguousarray(frame_bgr[..., ::-1]))   # ou escreva BGR e troque no shader
```

- Primeira `glTexSubImage2D` numa textura nova é lenta (alocação); faça um upload de aquecimento na inicialização.
  - Fonte: https://community.khronos.org/t/first-gltexsubimage2d-on-a-new-texture-is-slow/107239

**Recomendação**: pyglet 2.x, 5 janelas fullscreen com contexto compartilhado (ou 1 janela sobre NVIDIA Mosaic), `glTexSubImage2D` direto com `GL_BGR`; medir; só então PBO.

---

## 6. Idade / gênero / emoção em Python no Windows com GPU

| Pacote | Modelos | GPU no Windows | Atrito | Velocidade (ordem de grandeza) |
|---|---|---|---|---|
| **insightface** `buffalo_l` (SCRFD-10GF det + ResNet50 rec + `genderage`) | ONNX | `onnxruntime-gpu` (CUDA 11/12 + cuDNN) nativo no Windows | **Baixo**: `pip install insightface onnxruntime-gpu`, `FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider','CPUExecutionProvider'])`, `app.prepare(ctx_id=0, det_size=(640,640))`. Precisa de compilador C++ (Build Tools) para o pip do insightface. **Sem emoção.** | Det 640×640 + genderage em GPU: dezenas de fps numa RTX 2070 S (CPU 8 threads do pipeline completo: ~100 ms/img; GB10 ref.). Use `buffalo_s`/`det_size=(320,320)` para ~2–3× mais rápido. |
| **DeepFace** (`actions=['age','gender','emotion']`) | TensorFlow/Keras (VGG-Face age/gender, mini-Xception emotion) | TensorFlow ≥ 2.11 **não tem GPU nativo no Windows** (só WSL2 ou TF 2.10); na prática roda em CPU | Médio/alto: pesos baixam no 1º uso, detector padrão lento; escolha `detector_backend='opencv'`/`'ssd'` ou passe o crop já detectado com `detector_backend='skip'`. | ~0,3–1 s/rosto em CPU com todas as ações; RetinaFace/MTCNN "muito mais lentos". |
| **FER** (`fer` de justinshenk) | TF/Keras mini-Xception emoção (+ MTCNN opcional) | Mesmo problema do TF no Windows | Baixo, mas só **emoção**; pouco mantido. | Rápido em CPU para 48×48 crops (~ms por rosto). |
| **py-feat** | PyTorch (img2pose/RetinaFace det, AUs, emoção, pose) | `device='cuda'` funciona no Windows (PyTorch CUDA) | Médio: pesado (vários modelos), foco em pesquisa/vídeo offline, API baseada em DataFrames. Sem idade/gênero. | Mais lento que insightface; não há benchmark publicado. |

- Fonte (model zoo, quais packs têm genderage): https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md
- Fonte (forçar CUDAExecutionProvider; senão cai em CPU silenciosamente): https://github.com/deepinsight/insightface/issues/2394
- Fonte (versão CUDA × onnxruntime-gpu): https://discuss.huggingface.co/t/run-onnxruntime-for-insightface-model/74338
- Fonte (CPU ~100 ms/img pipeline buffalo_l; números GPU por hardware): https://github.com/mudler/face-detect.cpp/blob/master/benchmarks/RESULTS.md
- Fonte (guia prático insightface): https://agentbus.sh/posts/how-to-build-a-face-recognition-system-with-insightface/
- Fonte (DeepFace: detectores lentos, `stream` só analisa após 5 frames; GPU exige TF com CUDA): https://awesome.ecosyste.ms/projects/301673
- Fonte (DeepFace lento, MediaPipe 3–5× mais rápido, comparação anedótica): https://book.st-hakky.com/purpose/real-time-emotion-recognition-using-python
- Fonte (FER usa TF GPU se disponível): https://github.com/AlekseyKorshuk/fer
- Fonte (py-feat: `device=` cuda/mps/cpu): https://raw.githubusercontent.com/cosanlab/py-feat/main/docs/basic_tutorials/Performance.py
- Licença: modelos do insightface são "non-commercial research only" — relevante para obra exposta; verifique.
  - Fonte: https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md

**Recomendação**: **insightface + onnxruntime-gpu** para detecção + idade/gênero (menor atrito no Windows, tudo ONNX/CUDA). Para **emoção**, adicione um modelo ONNX leve rodando no mesmo onnxruntime (ex.: exportar o mini-Xception do FER/DeepFace para ONNX, ou HSEmotion/`emotion-ferplus` do ONNX model zoo) alimentado com o crop alinhado do insightface — evita instalar TensorFlow no Windows. Rode a análise de atributos a 2–5 Hz por rosto (não por frame), em uma thread separada, e cacheie por track ID.

---

## 7. Controladores de video wall 1×4 baratos

- O que são: 1 entrada HDMI (até 4K@30 nos baratos, 4K@60 nos melhores) → 4 saídas 1080p; modos 1×4, 4×1, 2×2 etc. O PC/Windows **vê um único monitor** com a EDID que o controlador emula (normalmente 3840×2160 ou 1920×1080 "esticado"); o aparelho recorta/escala cada quadrante. Sem driver.
  - Fonte: https://www.amazon.com/Controller-Splicing-Professional-Processor-Display/dp/B0CG1LXRR7
  - Fonte: https://www.amazon.com/Controller-Processor-Splicing-Extractor-3x1x4x1/dp/B0D2RD3FF4
  - Fonte: https://www.port-ta.com/products/n14vw
  - Fonte: https://assets.tripplite.com/product-pdfs/en/b1191x44k6vw.pdf
- Modelos de referência: Port-TA N14VW (~US$130, 4K30 in / 1080p60 out, RS232), AV Access 4KVW14 (~US$500, Web UI), Gefen EXT-UHD600A-VWC-14 (pro), StarTech ST124HDVW (2×2, ~US$900, 4K60 in).
  - Fonte: https://www.port-ta.com/products/n14vw
  - Fonte: https://www.avaccess.com/products/4kvw14/
  - Fonte: https://gefen.com/products/4k-ultra-hd-600-mhz-1x4-video-wall-controller-with-audio-de-embedder-ext-uhd600a-vwc-14
  - Fonte: https://www.cdw.com/product/startech-2x2-hdmi-video-wall-controller-4k-60hz-input-to-4x-1080p-output-m/6065118
- **Lag**: nenhum fabricante barato publica latência. Esses aparelhos usam scaler com frame buffer: espere **1–3 frames (16–50 ms)** de atraso, e mais se a entrada for 4K30 e a saída 1080p60 (conversão de taxa). A DigiBird afirma "frame lock" com latência de 1 frame quando as 4 saídas têm o mesmo timing. Para a obra (tracking de cabeça) 30–50 ms somados ao tracking é perceptível mas aceitável; prefira entrada **4K60** e saídas 1080p60.
  - Fonte: https://conferenceroomav.com/p/digibird-db-vrc4h
  - Fonte: https://www.staples.ca/products/2981267-en-startech-2x2-4k-video-wall-controller
- **Conteúdo diferente por quadrante**: trate o monitor virtual como uma tela 3840×2160 (ou 7680×1080 se o aparelho suportar EDID custom 1×4) e **renderize os 4 viewports você mesmo** na mesma janela: `glViewport(x, y, 1920, 1080)` com a matriz off-axis de cada tela física. Com 2×2 em 4K, quadrante (col, row) = `glViewport(col*1920, (1-row)*1080, 1920, 1080)`. Modo "1×4" nos baratos normalmente **corta a imagem 4K em 4 faixas** (960×2160 cada, escaladas para 1080p) ou em 2×2; leia o manual do modelo para saber que recorte ele faz e ajuste os viewports. Isso elimina a necessidade de 4 saídas na GPU e sincroniza as 4 telas (1 swap).
- Alternativa sem lag e sem caixa: a RTX 2070 Super tem 4 saídas (3× DP + 1× HDMI, + USB-C VirtualLink em alguns modelos) → 4 telas direto; para a 5ª tela use adaptador DP-MST hub (1 DP → 2–3 monitores 1080p60 sem lag) ou o controlador 1×4 só para um subconjunto.
- Se usar o controlador 1×4 em Windows, ative no NVIDIA Control Panel "Perform scaling on: Display" e resolução nativa anunciada pela EDID para evitar duplo scaling.

**Recomendação**: evitar o controlador barato se der para ligar as 5 telas direto na GPU (4 saídas + 1 MST hub); se usar, 2×2 em 4K60 → 1 janela 3840×2160 com 4 viewports, lag estimado 1–3 frames, medir com câmera de alta velocidade/telefone a 240 fps.

---

## Resumo das recomendações

1. **Webcam MLB24564760**: Sunplus SPCA2281 (UVC genérica, MJPEG+YUY2, ~20 fps reais em 1080p); compre 1, meça com `ffmpeg -list_options`, depois o lote.
2. **Identificação**: `cv2-enumerate-cameras` (CAP_MSMF) → device path (segue a porta física) → índice resolvido a cada boot; nunca gravar índices.
3. **USB**: 3 câmeras MJPEG 640×480@15 fps por controlador (regra segura); 6–7 controladores = placa-mãe + StarTech PEXUSB3S44V (4 controladores); evitar hubs; endpoints: Intel 96 / AMD 254.
4. **Off-axis**: fórmula de Kooima por tela (pa, pb, pc) com `pe` do MediaPipe Face Landmarker (IPD 63 mm / íris 11,7 mm → Z); suavizar; orientação fixa.
5. **Render**: pyglet 2 com 5 janelas fullscreen (contexto compartilhado por padrão) ou 1 janela sobre NVIDIA Mosaic; `glTexSubImage2D` direto com `GL_BGR`, PBO só se medir stall.
6. **Atributos**: insightface buffalo_l + onnxruntime-gpu (idade/gênero), emoção via modelo ONNX leve no mesmo runtime; evitar TensorFlow no Windows.
7. **Video wall 1×4**: Windows vê 1 monitor (EDID do aparelho); lag 1–3 frames não documentado; conteúdo por quadrante = 4 viewports numa janela 4K; melhor ligar as telas direto na GPU (+ DP-MST).
