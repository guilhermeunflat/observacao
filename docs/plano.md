# OBSERVAÇÃO — plano da ativação artística sobre vigilância

## Contexto

Festa em 14/11/2026. Instalação com 5 telas em U, 15 webcams ativas em varas ("olhos") + 5 de reserva, um PC (RTX 2070 Super sem USB-C, Ryzen 7 3800X, 48 GB RAM, 3 DP + 1 HDMI; placa-mãe com 2 USB 3.1 + 4 USB 3.0 + 4 USB 2.0 traseiras e headers USB internos livres) e um notebook extra. A obra mostra a quem observa as imagens fragmentadas da pessoa **anterior**, num espaço 3D que acompanha o movimento da cabeça (perspectiva off-axis, como o exemplo do Reddit em TouchDesigner), e nas telas que a pessoa não está olhando exibe frases sobre os danos da vigilância e descrições inferidas da própria pessoa (idade, altura, humor).

Decisões já tomadas com o usuário:
- **Stack:** Python + OpenCV + motor 3D próprio (sem TouchDesigner).
- **Ritmo:** sem datas por fase; avançar o mais rápido possível e fechar cada fase quando estiver pronta. Única data fixa: a festa.
- **Gastos:** o mínimo; controlador de video wall liberado; placa PCIe USB liberada se barata; compras que deixem a obra "mais saudável" são aceitas.
- **TVs de tubo:** conversores já existem.
- **Câmeras:** obra dimensionada para **15**; 5 de reserva já calibradas e trocáveis.
- **Pesquisa:** Markdown no projeto + doc Claude Docs compartilhável para o amigo. Foco: **danos da vigilância e do monitoramento exacerbado, com dados**, além dos dossiês de empresas.
- **Consentimento:** placa na entrada do evento ("tudo será gravado; permanecer no evento autoriza o uso das imagens"). Sem termo na tela touch.
- **Touch:** um dos monitores de 21" é touch; vira "terminal do dossiê" (toque → o que o sistema inferiu sobre você).
- **4+ pessoas:** o tracking de uma cabeça só não faz sentido, então o espaço 3D é desligado: as telas mostram **texto grande** (frases do banco) e o mural de fotos e vídeos de todo mundo que já passou. Volta ao 3D com ≤ 3.
- **TVs de tubo mostram imagens diferentes** (controlador de video wall 2×2 **já comprado** em 28/10, anúncio MLB22145200): cada tela é uma janela/portal própria para quem a olha, como no vídeo do Reddit. Nada de espelhar.
- **Webcam não tem rosca 1/4"**: fixação pelo clipe + abraçadeira/velcro/garra (opções em `docs/compras.md`).
- **USB:** não comprar placa PCIe nem hubs por enquanto; a placa-mãe tem 7 "tubos" USB 2.0 independentes e os 3 hubs sem fonte já existentes bastam para 15 câmeras na premissa conservadora. Mapa e distribuição em `docs/usb.md`; `bench_usb.py` confirma.
- **Pesquisa:** refeita em 28/10 com leitura integral das fontes, resumo por fonte, ensaio de compreensão e conclusões por dossiê, mais `docs/pesquisa/00_sintese.md`. As frases serão refeitas a partir dessa compreensão (as 42 anteriores foram descartadas).
- **Posicionamento físico é parte da obra** e ainda está em aberto: a mesa de cavaletes (1,20 × 0,60) é opcional, a fixação das webcams precisa ser melhor pensada, e **a montagem do evento não vai replicar o teste de casa**. Logo o software precisa ser totalmente parametrizado e ter uma rotina de recalibração rápida no local.
- **Mobiliário existente:** mesa de cavaletes; suporte duplo pivotante de mesa (base única) e pés originais dos monitores; tripé de câmera para a TV 32".
- **Moodboard** (investigação, observação, espionagem) antes da identidade; identidade construída em conjunto, mais para frente.
- Nome da obra: o usuário vai pensar.

Idioma de tudo: português.

---

## Princípio de projeto: "calibra em 15 minutos no local"

Nada no código depende de posições fixas. Tudo que muda entre o teste em casa e o evento vive em `config/` e é ajustado por ferramentas visuais:

| O que muda no evento | Onde vive | Como recalibrar |
|---|---|---|
| Posição/altura/ângulo das 5 telas | `config/screens.json` | `calibrate_screens.py`: digita medidas em cm (ou arrasta num esquema 2D visto de cima) e vê o resultado da paralaxe ao vivo |
| Posição/ângulo das câmeras master (tracking) | `config/cameras.json` | `calibrate_tracking.py`: a pessoa fica em 2 marcas no chão (1 m e 2 m), clica, pronto |
| Posição das câmeras "olho" | `config/cameras.json` (aproximada) | não precisa de precisão: só altura e lado (esq/centro/dir) para o mosaico ordenar os cacos de forma coerente |
| Qual câmera está em qual porta/vara | `config/cameras.json` | `calibrate_cameras.py` reconhece pelo device path e pergunta só sobre as desconhecidas |
| Luz, exposição | `config/app.json` | ajuste de exposição/ganho por câmera na grade de visualização |
| Limites de "pessoa presente", distância de interação | `config/app.json` | sliders na janela de operador |

Perfis em `config/profiles/`: `casa.json`, `casa_amigo.json`, `evento.json`. `start.bat --profile evento`.

---

## Arquitetura (resumo para executar)

### Vídeo: 5 telas em 4 saídas
| Tela | Saída do PC | Observação |
|---|---|---|
| TV LED 32" vertical (centro, tripé) | DP 1 | rotacionada 90° no Windows |
| Monitor 21" (esq.) | DP 2 | |
| Monitor 21" touch (dir.) | DP 3 + USB do touch | terminal do dossiê |
| TV de tubo 1 | HDMI → controlador video wall (saída A) → conversor HDMI→AV | |
| TV de tubo 2 | controlador video wall (saída B) → conversor HDMI→AV | |

Controlador 1×4 em modo 2×2: o Windows vê um 1920×1080; o software desenha as TVs de tubo nos quadrantes superiores. **Plano B** sem controlador: notebook como 5ª tela via cliente WebSocket.

### USB: 15 câmeras + touch
- Ver `docs/usb.md` (mapa real da X570 AORUS ELITE WIFI). Resumo: em xHCI cada porta raiz é um tubo USB 2.0 de 480 Mb/s; hub não cria banda; o que limita é a reserva isócrona que a câmera pede (incógnita que `bench_usb.py` mede).
- Distribuição sem compras: 3 hubs sem fonte nas portas azuis (3 câmeras cada), 1 câmera na 4ª azul, 1 em cada vermelha, 3 nos USB 2.0 traseiros (1 tubo) + touch na 4ª USB 2.0 = 15.
- Os 6 discos externos saem das portas traseiras nos testes. Compra só se o teste reprovar: bracket do header USB 3.0 (~R$ 35) antes de placa PCIe.
- Identificação estável: enumeração DirectShow (`comtypes`/`pygrabber`) expõe o device path com a rota física USB; o índice de `cv2.VideoCapture(i, cv2.CAP_DSHOW)` segue a mesma ordem → `índice → device path → "vara 07"`.

### Software (pacote `observacao/`)
```
OBSERVACAO/
  docs/
    pesquisa/            # danos da vigilância + dossiês de empresas
    compras.md           # preços e links
    posicionamento.md    # estudo de ângulos, alturas, fixação; fotos dos testes; o que mudar no evento
    moodboard/           # imagens de referência + moodboard.md
    identidade.md        # (depois do moodboard)
    montagem.md          # guia físico para o amigo
  config/
    screens.json, cameras.json, app.json
    profiles/casa.json, casa_amigo.json, evento.json
    frases/              # danos.md, descritivas.md, seguranca.md, easter_egg.md
  src/observacao/
    capture.py           # threads, mapeamento estável, hot-swap de reserva
    tracker.py           # rostos nas masters, posição 3D da cabeça, até 3 pessoas
    analyzer.py          # idade/gênero/emoção/altura (insightface + FER)
    bank.py              # sessões, cacos, fotos, clipes, metadados
    state.py             # quem está na frente, quem vê quem, modo arquivo (4+)
    phrases.py           # bancos + templates
    operator.py          # janela do operador: grade das câmeras, fps, sliders, status
    render/
      app.py             # pyglet, uma janela por tela, contexto GL compartilhado
      projection.py      # projeção off-axis (Kooima)
      scene.py           # nuvem de cacos
      text.py            # telas de texto / overlay CCTV
      touch.py           # dossiê
      archive.py         # mural de todos (4+)
    main.py
  tools/
    list_devices.py, calibrate_cameras.py, calibrate_screens.py, calibrate_tracking.py,
    bench_usb.py, record_person0.py, cleanup.py
  bank/                  # runtime
  start.bat, requirements.txt, README.md
```
Dependências: Python 3.11, opencv-python, pygrabber, numpy, mediapipe, insightface + onnxruntime-gpu, fer, pyglet 2.x, pillow, websockets.

### Lógica central
- **Tracking:** 2–3 câmeras master com posição calibrada; MediaPipe; profundidade por tamanho do rosto; IDs de até 3 pessoas. Rosto > 2 s inicia sessão; ausente > 5 s encerra.
- **Mosaico:** nuvem de cacos em profundidades diferentes; cada caco é um recorte de uma webcam diferente (ao vivo na gravação, do banco na exibição). Projeção off-axis por tela a partir da cabeça.
- **Quem vê quem:** 1 → vê a anterior (pessoa 0 = usuário). 2 → A↔B. 3 → anel. Tela de frente mostra a nuvem; as outras, texto. **4+ → modo arquivo:** mural de todas as sessões da noite com carimbos e frases coletivas; volta ao normal com ≤ 3.
- **Frases:** (1) danos da vigilância e dossiês, com fonte; (2) templates descritivos ("cerca de {idade} anos", "parece {humor}", "{n}ª vez registrado hoje"); (3) "segurança" irônica.
- **Touch:** padrão igual às outras telas; ao toque, dossiê da pessoa mais próxima; volta após 20 s.
- **Dados:** placa na entrada; `cleanup.py` para limpeza manual quando o usuário quiser.

---

## Estudo de posicionamento (fase própria, antes do 3D)

Perguntas que o estudo responde, com testes rápidos e fotos em `docs/posicionamento.md`:
1. **Altura das telas:** centro das telas na altura dos olhos de alguém em pé (~150–160 cm) ou mais baixo, forçando a pessoa a se inclinar? Testar os dois com a 32" no tripé e um monitor no pé.
2. **Raio e abertura do U:** distância ideal entre a pessoa e a 32" (1,0–1,5 m) para o tracking funcionar e a paralaxe ser forte; ângulo das pontas (60–90°).
3. **Câmeras master:** onde ficam (topo da 32" + topos das pontas) e com que inclinação para enxergar rostos de 1,50 a 1,90 m a 1–2 m.
4. **Câmeras olho:** quais alturas/ângulos geram cacos interessantes (de baixo para cima, de lado, de muito perto); quantas atrás das telas vs. ao redor da pessoa; testar 3 posições por câmera e anotar.
5. **Fixação:** opções a pesquisar com preço e testar com 2–3 câmeras: cano PVC 20 mm em base de sarrafo/MDF pesada; barra roscada em bloco de madeira; hastes gooseneck; mini tripés; garras de mesa; pedestal de microfone usado; fita dupla-face + abraçadeira nas telas/tripé. Critério: aguenta a webcam sem balançar, muda de ângulo rápido, cabe no carro.
6. **Base:** mesa de cavaletes vs. sem mesa (telas em tripé/pés/banquinhos direto no chão) vs. combinação. Decidir pelo que é mais fácil de replicar no evento.
7. **Luz:** uma luz frontal suave; testar com a luz de festa simulada (baixa).
Saída: `config/profiles/casa.json` com o que foi testado e uma lista "o que vai mudar no evento e como recalibrar" em `docs/montagem.md`.

---

## Fases. Ao fim de cada uma: checklist + perguntas de revisão ao usuário.

### Fase 0 — Pesquisa, compras, scaffold
1. `docs/pesquisa/`: danos da vigilância (chilling effect, autocensura, viés/falsos positivos, prisões injustas BR/EUA, saúde mental, eficácia duvidosa, custo público) + dossiês (Gabriel, Flock, Clearview, Smart Sampa/Córtex, corretores de dados, vazamentos, LGPD). Fatos, números, citações, fontes.
2. `docs/pesquisa/frases_extraidas.md` (60–100 frases com fonte).
3. Doc Claude Docs compartilhável + link.
4. `docs/compras.md`: controlador video wall, placa PCIe USB, hubs alimentados, opções de fixação/varas, banquinhos/bases, luz; essencial vs. opcional; pedir cedo o que tem frete longo.
5. Scaffold, venv, `list_devices.py` com as câmeras plugadas.
**Revisão:** pesquisa cobre o discurso? Compras aprovadas? Nome?

### Fase 1 — Olhos: captura
1. `capture.py`, `calibrate_cameras.py`, `bench_usb.py`, `operator.py` (grade + fps + exposição).
2. Mosaico 2D de teste.
**Revisão:** 15 estáveis? Subir para 20? Cacos agradam?

### Fase 2 — Posicionamento físico (estudo acima)
**Revisão:** mesa ou não? Alturas e ângulos escolhidos? Fixação escolhida e quantidade a comprar/fabricar? O que vai ser diferente no evento?

### Fase 3 — Telas e espaço 3D
1. `render/app.py`, `projection.py`, `calibrate_screens.py`, `calibrate_tracking.py`, tracker, nuvem de cacos ao vivo, perfil `casa_amigo`.
2. Windows: saídas, rotação, controlador 2×2.
**Revisão:** a "janela" convence? Onde perde a pessoa? Recalibração leva quanto tempo?

### Fase 4 — Memória: banco, rotação, frases, análise, touch, modo arquivo
1. `bank.py`, `state.py`, `analyzer.py`, `phrases.py`, `text.py`, `touch.py`, `archive.py`, `record_person0.py`.
**Revisão:** troca de pessoa clara? Frases invasivas demais? Mural funciona?

### Fase 5 — Moodboard e identidade (em conjunto)
1. `docs/moodboard/`: referências de investigação, observação, espionagem, CCTV, arquivos policiais, redações de jornal, salas de controle, fotografia de vigilância (Sophie Calle, Trevor Paglen, Hasan Elahi, Dries Depoorter, Harun Farocki), tipografias monoespaçadas/OCR, carimbos, mapas de evidência. Com legendas do porquê de cada referência.
2. Sessão de decisão com o usuário → `docs/identidade.md` (nome, paleta, tipografia, movimento, som).
3. Aplicar nas telas de texto, dossiê, mural, placa de entrada, legenda.
**Revisão:** identidade aprovada?

### Fase 6 — Montagem, ensaio, pacote, festa
1. `start.bat --profile evento`, checagem de câmeras com sugestão de reserva.
2. Contingências: tracking cai → modo deriva; faltam câmeras → mosaico com as que há; sem controlador → plano B.
3. `docs/montagem.md` final com fotos e roteiro de recalibração de 15 min; pacote para o amigo.
4. Ensaio de 1 h com 2–3 pessoas; checklist do dia; backup do `bank/`.
**Revisão (pós-festa):** o que funcionou, o que mudar.

---

## Verificação
- Fase 1: 15 câmeras por ≥ 10 min sem queda; varas reconhecidas após reboot; troca por reserva < 2 min.
- Fase 2: `docs/posicionamento.md` com fotos e decisões; perfil `casa.json` preenchido.
- Fase 3: paralaxe coerente nas 5 telas ao andar; 3 IDs mantidos por 2 min; recalibrar telas + tracking do zero em < 15 min.
- Fase 4: João → Marcos → Júlia executado; 4ª pessoa dispara o mural; touch mostra o dossiê certo.
- Fase 6: `start.bat` sobe tudo em < 2 min; ensaio de 1 h sem travar.

## Riscos
- Banda USB (640×480 MJPEG, distribuir por controlador, placa PCIe, cair para 12).
- Compras atrasarem (pedir na fase 0; plano B do notebook).
- Montagem do evento diferente do teste (mitigado pelo princípio "calibra em 15 min").
- Profundidade por rosto é grosseira; aceitar paralaxe só horizontal se incomodar.
- Modelos de idade/emoção erram; frases em tom de "palpite do sistema".
- Luz da festa: prever luz frontal.
- Prazo: fases 3 e 4 são o coração; se apertar, cortar altura estimada, depois emoção, nunca tracking e rotação de pessoas.


---

## Descobertas da Fase 0 que alteram o plano (28/10/2026)

Fonte: `docs/pesquisa_tecnica.md` e `docs/compras.md`.

1. **Banda USB (revisto em 28/10, ver `docs/usb.md`).** A limitação é por *tubo* (porta raiz ou hub), não por controlador; a placa-mãe tem 7 tubos úteis e os hubs existentes bastam para 15 câmeras a 3 por tubo. Texto original mantido abaixo como histórico: O driver UVC reserva banda pelo alt-setting, não pelo fluxo real; a regra segura é **~3 câmeras MJPEG 640×480@15 fps por controlador xHCI** (relatos de 2 a 6). Com 15 câmeras isso pede 5+ controladores. Consequências:
   - `bench_usb.py` (Fase 1) vira o teste decisivo: medir quantas câmeras cada grupo de portas da placa-mãe aguenta de verdade, em 640×480 e em 320×240.
   - Opções em ordem de preferência: (a) baixar para 320×240@15 ou 640×480@10 (cacos são pequenos, não precisa de resolução); (b) placa PCIe com **vários controladores independentes** (ex.: StarTech PEXUSB3S44V, 4 controladores, cara) em vez de uma VL805 (1 controlador só); (c) reduzir para 12 câmeras.
   - Mapear portas → controlador com o USB Device Tree Viewer antes de comprar hubs.
2. **Controlador de video wall: comprado (2×2, MLB22145200).** As TVs de tubo mostram imagens diferentes; a opção de splitter foi descartada. Texto original: A RTX 2070 Super aciona no máximo 4 telas simultâneas, então hub DP-MST não dá a 5ª tela. Alternativa mais barata (R$ 30–60): **splitter HDMI 1×2** se as duas TVs de tubo puderem mostrar a mesma imagem; o software renderizaria 1 conteúdo para as duas pontas. Decidir com o usuário.
3. **Identificação estável das câmeras:** o DevicePath DirectShow já funciona em `tools/list_devices.py`; alternativa `cv2-enumerate-cameras` (MSMF). Nunca gravar índices: resolver path → índice a cada boot.
4. **Webcam MLB24564760:** chipset Sunplus SPCA2281, UVC genérica (MJPEG + YUY2). **Sem rosca 1/4"** (confirmado pelo usuário): fixação pelo clipe, ver `docs/compras.md`.
5. **Atributos (idade/gênero/emoção):** insightface buffalo_l + onnxruntime-gpu é o caminho de menor atrito no Windows com CUDA; DeepFace/FER dependem de TensorFlow sem GPU nativa. Licença do insightface é não-comercial (ok para obra de arte sem venda).
6. **Render:** pyglet 2.x com uma janela por tela compartilha contexto por padrão; vsync em 5 janelas pode travar o loop → testar e, se preciso, 1 janela gigante com viewports.
7. **Compras:** cenário mínimo ≈ R$ 1.480, confortável ≈ R$ 3.160 (sem frete). Risco principal: itens baratos com envio da China não chegam até 14/11; confirmar vendedor nacional.
