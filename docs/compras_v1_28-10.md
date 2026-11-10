# Lista de compras — instalação OBSERVAÇÃO

Pesquisa feita em 28/10/2026 (festa em 14/11/2026 → **17 dias**). Preços são capturas de páginas de busca/anúncios e mudam diariamente; onde não achei preço exato, marquei **(estimativa)**. Links: só os que apareceram nos resultados de busca. Páginas de produto do Mercado Livre e Leroy Merlin bloquearam a abertura direta, então os preços delas vêm do que a busca mostrou.

**Regra de prazo (vale para tudo):** com 17 dias, descarte qualquer anúncio marcado "Compra internacional / Envio da China" (2 a 6 semanas). Priorize Mercado Livre "Full"/frete grátis (2–7 dias úteis), Amazon Prime (1–5 dias úteis) e retirada na loja (Leroy Merlin, Telhanorte, lojas de material de construção do bairro). Faça os pedidos eletrônicos **até 03/11** para ter margem de troca.

**Legenda:** ESSENCIAL = sem isso a instalação não funciona. OPCIONAL = melhora, mas dá para improvisar.

---

## A. Controlador de video wall 1 HDMI → 4 HDMI — ESSENCIAL

**Como funciona:** o PC manda uma única imagem 1080p pela porta HDMI. O controlador recorta essa imagem em 4 pedaços e entrega cada pedaço, reescalado para 1080p, numa saída HDMI. Dois modos interessam aqui:
- **2×2:** recorta em quadrantes (superior-esq, superior-dir, inferior-esq, inferior-dir). Cada tela mostra 1/4 da imagem ampliado 2×.
- **1×4 (ou 4×1):** recorta em 4 faixas verticais (ou horizontais) lado a lado; cada tela recebe uma faixa de 480×1080 esticada para 1920×1080 (a imagem fica distorcida se o conteúdo não for preparado para isso).
- Quase todos têm também "1×1" (espelha a mesma imagem nas 4 saídas), "1×2", "1×3", "3×1". Mudança de modo por botão no painel ou controle remoto IR.

**Implicação para o projeto:** com 3 DP + 1 HDMI você já alimenta 4 telas diretamente do PC. O controlador vai no HDMI e alimenta até 4 telas com *uma* imagem recortada. Combinação sugerida: 2 monitores + TV 32" direto nas DP (3 telas independentes), e o controlador no HDMI alimentando as 2 TVs de tubo (modo 1×2 ou 1×1) — sobra uma saída DP livre como reserva. Se você quiser que as TVs de tubo apenas **espelhem** a mesma imagem, um splitter HDMI 1×2 (R$ 30–60, "Divisor HDMI 1 entrada 2 saídas") resolve por muito menos; o controlador só vale a pena se você quer *recortar* a imagem entre telas.

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Video Wall Controlador 2x2/1x3/1x4/3x1/4x1 HDMI 4K (entrada 4K30, saídas 1080p) | Mercado Livre | ~R$ 300–370 (um anúncio semelhante a R$ 345, frete grátis) | https://produto.mercadolivre.com.br/MLB-3659120228-video-wall-controlador-2x2-1x3-1x4-2x2-3x1-4x1-hdmi-4k-_JM | Suporta os modos 1×4 e 2×2 no título. Confirme que o vendedor é nacional (não "Envio da China"). |
| Controlador de Vídeo Wall 2x2 1080p HDMI (Solução, mod. 9188) | Mercado Livre (catálogo) | R$ 478 (3 anúncios a partir desse valor) | https://www.mercadolivre.com.br/controlador-de-video-wall-2x2-1080p-hdmi/p/MLB27773971 | Marca nacional com suporte; entrada HDMI ou DVI, 4 saídas HDMI. |
| Controlador 2x2 4K2K HDVW2X2 | Mercado Livre | ~R$ 1.000+ (estimativa pelos anúncios "profissionais") | https://produto.mercadolivre.com.br/MLB-1436821940-controlador-de-video-wall-2x2-4k2k-hdvw2x2-_JM | Exagero para 1080p; só se o resto esgotar. |
| Referência de preço internacional (não comprar: não chega a tempo) | AliExpress | US$ 28–50 | https://www.aliexpress.us/item/3256803502996715.html | Mesmo hardware genérico vendido no ML por ~R$ 350. |

Listagens úteis: https://lista.mercadolivre.com.br/hdmi-1x4-video-wall · https://lista.mercadolivre.com.br/video-wall-2x2

**Recomendação:** o genérico de ~R$ 345 (MLB-3659120228) de vendedor nacional; peça já, é o item com menos oferta no país.

---

## B. Placa PCIe x1 USB 3.0 (4+ portas) + adaptador de header interno 19 pinos → bracket — ESSENCIAL

Motivo: 15–20 webcams 1080p saturam facilmente um único controlador USB da placa-mãe. Uma placa PCIe com controlador próprio cria um barramento USB independente (mais ~2,5 Gbit/s úteis). O header interno USB 3.0 (19 pinos) da placa-mãe geralmente fica sem uso; um bracket transforma ele em 2 portas traseiras.

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Placa PCI-e x1 4 portas USB 3.0 chip **VL805** (genérica) | Mercado Livre | R$ 98,44 | https://produto.mercadolivre.com.br/MLB-3585720297-placa-adaptadora-vl805-pci-express-pci-e-x1-4-portas-usb-30-_JM | Único anúncio que confirma o chip VL805. Anunciado como "frete internacional grátis" → **risco de prazo**; confira a origem antes. |
| Placa PCIe USB 3.0 4 portas DEX DP-43 | Amazon.com.br | R$ 84,89 (Prime) | https://www.amazon.com.br/Placa-Pci-Express-5gbps-Portas/dp/B07CZPBV3X | Chip não declarado (geralmente VL805 nesse formato). Entrega rápida. |
| Placa PCI-e 4 portas USB 3.0 F3 JC-PCI 3.0 | Amazon.com.br | R$ 104,99 | https://www.amazon.com.br/PLACA-PCI-PORTAS-USB-JC-PCI/dp/B08Q863286 | Marca nacional com garantia. |
| Placa Comtac 9349 4 portas USB 3.0 | Kabum / Amazon | R$ 99,90 (Kabum, **esgotada**) / R$ 119,90 (Amazon) | https://www.kabum.com.br/produto/81442/placa-comtac-pci-express-usb-3-0-4-portas-9349 · https://www.amazon.com.br/Placa-Pci-Express-Portas-Comtac/dp/B076HXNHYZ | Marca conhecida; chip não declarado na página. |
| Placas genéricas 4 portas | Mercado Livre (lista) | R$ 48–80 | https://lista.mercadolivre.com.br/placa-pci-e-usb-3.0-5gbps-com-4-portas | Chip raramente informado; muitas são "Envio da China". |
| **Header:** divisor interno 19/20 pinos → 2 portas USB 3.0 (Engmax) | Mercado Livre | R$ 44,99 (frete grátis) | https://lista.mercadolivre.com.br/adaptador-usb-3.0-19-pinos | Verifique se o anúncio vem com bracket de painel traseiro ("espelho"). |
| **Header:** adaptador 19 pinos → 2 portas + Type-E/USB-C (Engmax) | Engmax / Mercado Livre | R$ 170,99–179,99 | https://www.engmaxinformatica.com.br/hardware/placa-usb-tipo-c/usb-3-1/adaptador-header-placa-mae-2-portas-19-pinos-type-e-tipo-c-preto | Caro; só se a placa-mãe tiver 2 headers. |

Listagem Kabum: https://www.kabum.com.br/hardware/placas-interfaces/placa-usb (tem uma placa 4 saídas por R$ 69,90 sem chip declarado).

**Recomendação:** DEX DP-43 na Amazon (R$ 84,89, chega rápido) + divisor Engmax 19 pinos → 2 portas (R$ 44,99). Total ≈ R$ 130. Se a placa-mãe tiver um 2º header USB 2.0 (9 pinos), um bracket USB 2.0 (R$ 15–25) rende mais 2 portas para as webcams — elas são USB 2.0 e funcionam bem em portas 2.0.

---

## C. Hub USB 3.0 alimentado (com fonte), 4–7 portas — 3 unidades — ESSENCIAL

Regra prática: cada webcam 1080p MJPEG usa ~100–200 Mbit/s e até 250 mA. Coloque **no máximo 4 webcams por hub** e cada hub numa porta de controlador diferente (placa-mãe USB 3.0, placa-mãe USB 2.0, placa PCIe). Hub **sem fonte** não serve: as webcams somadas passam de 500 mA.

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Orico H7013-U3-AD, 7 portas, com fonte 12 V | Amazon.com.br | R$ 171,30–199,90 | https://www.amazon.com.br/hub-usb-3-0-com-fonte/s?k=hub+usb+3.0+com+fonte | Modelo mais comum e confiável nessa faixa. |
| Orico H7013-U3-AD | Kabum | R$ 229,08 (PIX), 9x R$ 25,45 | https://www.kabum.com.br/produto/237942/hub-orico-usb-3-0-com-fonte-7-portas-preto-h7013-u3-ad | Vendido por loja parceira (FAST CHARGER). |
| TP-Link UH700, 7 portas, fonte 12 V/2 A | Amazon / Mercado Livre / Shopee | R$ 209,99–263,85 | https://lista.mercadolivre.com.br/hub-usb-3.0-7-portas-com-fonte | Fonte generosa (24 W), bom para 4–5 webcams por hub. |
| Hub HRebos 7 portas com fonte, botões individuais | Shopee (via comparador) | R$ 184,90 | https://escorregaopreco.com.br/ofertas/shopee/8205161 | Botão por porta ajuda a reiniciar uma webcam travada. |
| "Régua hub USB 3.0 com fonte 5 V, 7 portas" (genérico) | Shopee (via comparador) | R$ 30–56 | https://www.melhoraopreco.com.br/ofertas/shopee/7506853 | Barato, mas fonte fraca (5 V/2 A ≈ 4 webcams no limite) e sem marca. Só como 3º hub de reserva. |
| Hub 7 portas com fonte, sem marca | Mercado Livre | ~R$ 140 | https://lista.mercadolivre.com.br/hub-usb-3.0-com-7-portas | Confirme "USB 3.0" e fonte inclusa na descrição. |
| Comtac 7 portas com interruptor e fonte | Kabum | R$ 339,90 | https://www.kabum.com.br/produto/943439/hub-comtac-power-switch-usb-a-3-0-para-7x-usb-a-3-0-aluminio-24129450 | Caro demais para o uso. |

**Recomendação:** 3× Orico H7013 (Amazon, ~R$ 200 cada) ≈ R$ 600. Cenário mínimo: 2× Orico + 1× régua genérica Shopee ≈ R$ 460, ou 3× genérico com fonte ≈ R$ 180 (risco maior de queda de webcam).

---

## D. Extensor USB ativo 5 m e 10 m — OPCIONAL (compre 1–2 só se alguma webcam ficar a mais de 3 m do hub)

Webcams USB 2.0 toleram cabo passivo até ~3–5 m. Acima disso, extensor **ativo/amplificado** (tem chip repetidor no conector fêmea). Para webcam, extensor USB 2.0 basta (o 3.0 custa 3–4× mais e não ajuda).

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Extensor USB 2.0 ativo 5 m (ex.: mod. UB-19) | Mercado Livre | R$ 28–65 (vários a R$ 31–35, frete grátis) | https://lista.mercadolivre.com.br/cabo-extensor-usb-2.0-ativo%2C-amplificado%2C-5-metros%2C-promo%C3%A7%C3%A3o | Checar "amplificado/ativo" no título. |
| Extensor USB 2.0 ativo 10 m | Mercado Livre | R$ 34–70 (ex.: R$ 63,31 frete grátis) | https://lista.mercadolivre.com.br/cabo-extensor-usb-2.0-10-metros | |
| Extensor USB 2.0 ativo 10 m MCB-026 | Central Cabos | R$ 28,40 (PIX) | https://www.centralcabos.com.br/extensor-amplificado-usb-2-0-10mts---mcb-026/p | Loja de SP; some frete. |
| Extensor USB 2.0 ativo 10 m | Oficina dos Bits | R$ 58,99 (PIX) | https://www.oficinadosbits.com.br/produto/cabo-extensor-usb-2-0-ativo-10-metros-a-macho-a-femea/ | |
| Extensor USB 3.0 ativo 10 m | Mercado Livre (catálogo) | R$ 150–360 | https://www.mercadolivre.com.br/cabo-extensor-usb-verso-30-amplificado-ativo-10-metros-cor-preto/p/MLB20325807 | Desnecessário para webcam. |

**Recomendação:** 2× 5 m (≈ R$ 70) + 1× 10 m (≈ R$ 60) só no cenário confortável; no mínimo, aproxime os hubs das webcams e use cabos passivos de 1,5–3 m (R$ 8–15 cada).

---

## E. Hastes/varas para as webcams (20 unidades: 15 + 5 reservas) — ESSENCIAL

### Como fixar a webcam (importante ler antes de comprar)
- Não consegui abrir o anúncio MLB24564760 (bloqueado para leitura automática) e a busca não retornou esse código. **Confirme você mesmo** na ficha do anúncio se há "rosca para tripé" / "furo 1/4"". As webcams genéricas 1080p de ~R$ 35–50 no ML (CIETEC, GoodVision, Dr. Hank — https://lista.mercadolivre.com.br/webcam-1080p) normalmente têm o clipe dobrável para monitor **e** um furo de rosca 1/4"-20 na base do clipe; algumas das mais baratas vêm só com o clipe.
- **Se tiver rosca 1/4":** qualquer solução com parafuso 1/4"-20 funciona (barra roscada 1/4", parafuso 1/4" x 3/4" com porca atravessando um cap de PVC, gooseneck com pino 1/4", mini tripé, garra clamp). Todas as hastes de câmera no Brasil usam esse padrão.
- **Se tiver só o clipe:** o clipe abre ~2–3 cm e aperta em qualquer coisa chata ou redonda: topo de cano PVC 25 mm com cap, cabo de vassoura (23–25 mm), borda de sarrafo. Reforce com uma abraçadeira de nylon atravessando o clipe ou um pedaço de velcro/dupla-face — o clipe sozinho solta se alguém esbarrar.
- **Montagem recomendada (barata e sólida):** cano PVC 25 mm cortado no comprimento desejado (40 cm a 2 m) → cap 25 mm no topo → furo de 6,5 mm no centro do cap → parafuso sextavado 1/4"-20 x 3/4" (ou 20 mm de barra roscada 1/4") com porca por dentro e arruela → rosca da webcam por cima. Gira para ajustar o ângulo e trava com a porca. Pinte tudo de preto fosco. O cabo USB desce por dentro do cano (fure uma janela lateral perto do topo).

### E1. Cano PVC

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Cano PVC marrom soldável 25 mm, barra 3 m, Tigre | Leroy Merlin | R$ 15,99 à vista | https://www.leroymerlin.com.br/cano-pvc-marrom-soldavel-3m-3-4-25mm-tigre_85949885 | Diâmetro ideal: rígido até 2 m e cabe o clipe. Retire na loja. |
| Tubo soldável 25 mm 3 m Tigre | Telhanorte | R$ 15,03 (PIX) / R$ 18,90 | https://www.telhanorte.com.br/tubo-soldavel-nbr-5648-3-00m-25mm-tigre-170208/p | |
| Tubo soldável 20 mm 3 m Tigre | Telhanorte | R$ 16,91 (PIX) / R$ 21,90 | https://www.telhanorte.com.br/tubo-soldavel-3-00m-20mm-tigre-170194/p | 20 mm flexiona acima de 1,2 m; use só nas hastes baixas. |
| Tubo soldável 20 mm 3 m Krona | Telhanorte | R$ 11,61 (PIX) / R$ 12,90 | https://www.telhanorte.com.br/tubo-pvc-soldavel-3-metros-20mm-krona-2386666/p | Mais barato. |
| Cap soldável 20 mm Tigre | Telhanorte | R$ 3,03 (PIX) / R$ 3,79 | https://www.telhanorte.com.br/cap-soldavel-20mm-tigre-23523/p | Cap 25 mm: ~R$ 2–4 (estimativa; citado a R$ 2,04 na Tradição Agrícola). |
| Luva soldável 25 mm (Krona) | Ferreira Costa / Hidrauconex | R$ 0,90–1,25 a unidade | https://www.ferreiracosta.com/produto/356785/luva-soldavel-pvc-marrom-25-mm-krona | Para emendar pedaços e regular altura. Luva 20 mm Tigre: https://www.telhanorte.com.br/luva-soldavel-20mm-tigre-22110/p |
| Tinta spray uso geral preto fosco 400 ml Colorgin (54001) | Mundo Grafite / Bela Tintas / Normatel | R$ 24,78–36,55 (ex.: R$ 28,50 PIX) | https://www.mundografite.com.br/uso-geral-preto-fosco · https://www.belatintas.com.br/19896-spray-preto-fosco-uso-geral-400ml---colorgin/p | 1 lata pinta ~3–4 barras de 3 m. Na loja física costuma sair R$ 25–35. Lixe o PVC levemente antes. |

**Conta para 20 hastes (altura média 1,2 m = 24 m de cano):** 8 barras de 25 mm (R$ 128) + 20 caps (R$ 60) + 6 luvas (R$ 7) + 3 sprays (R$ 90) + 20 parafusos 1/4" c/ porca e arruela (R$ 20, estimativa) ≈ **R$ 305**.

### E2. Barra roscada 1/4" e 3/8"

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Barra roscada 1/4" zincada 1 m, kit 10 | Mercado Livre | R$ 43,90 (≈ R$ 4,39/m) | https://lista.mercadolivre.com.br/barra-roscada-1-4 | Rosca 1/4"-20 = a mesma da webcam. 1 kit serve para os 20 pinos de topo (corte pedaços de 3 cm) e sobra. |
| Barra roscada 1/4" Mister zincada 1 m | Leroy Merlin | R$ 3,72 | (resultado de busca Leroy, sem link direto) | Compre junto com porcas e arruelas 1/4". |
| Barra roscada 3/8" Ciser 1 m | Leroy Merlin | R$ 6,49 | https://www.leroymerlin.com.br/barra-roscada-3-8-1m-ciser-89400_1570435661 | 3/8" é a rosca de pedestal de iluminação; só compre se usar adaptador 3/8→1/4. Não serve como "vara": flexiona demais. |
| Barra roscada 3/8" polida 1 m, 10 peças | Leroy Merlin | R$ 68,90 (≈ R$ 6,89/m) | https://www.leroymerlin.com.br/barra-roscada-polida-1-metro-3-8-10-pecas_1570125760 | |

**Fixação:** a barra 1/4" entra direto na rosca da webcam; a outra ponta atravessa o cap do PVC ou um bloco de madeira com porca dos dois lados.

### E3. Cabo de vassoura / madeira redonda

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Cabo de madeira vassoura/ancinho 1,20 m, Ø 2,3 cm, Volpato | Leroy Merlin | R$ 9,15 (kit 2: R$ 16,50; kit 12: ver página) | https://www.leroymerlin.com.br/cabo-madeira-vassoura-e-ancinho-1,20-metros-volpato_1568031510 · https://www.leroymerlin.com.br/kit-12-cabo-de-madeira-para-vassoura-e-ancinho-1,20-metros_1569336141 | Já vem com ponta rosqueada (rosca de vassoura, não serve para câmera). |
| Cabo de vassoura em loja de bairro/mercado | Loja física | R$ 6–12 (estimativa) | — | |

**Fixação:** o clipe da webcam morde o topo do cabo (Ø 23 mm) direto; ou fure o topo com broca 5,5 mm e rosqueie um parafuso 1/4"-20 (a madeira segura a rosca). Pinte de preto. Limite de 1,2 m; para 2 m emende com luva ou use PVC.

### E4. Haste flexível gooseneck com rosca 1/4"

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Haste flexível 28 cm c/ pino 1/4" Sou Foto SFA-002 | Fotolux (site e ML) | R$ 19,99–32,99 | https://www.fotolux.com.br/cameras-e-acessorios/acessorios/extensores-e-hastes/haste-flexivel-28cm-c-pino-14-suporte-para-iluminadores-e-ring-light-sou-foto | Pino 1/4" em cima (entra na webcam), base com rosca 1/4" fêmea/pino para tripé. Peso 195 g. Uma das páginas cita 5/8" — confirme. |
| Haste flexível 50 cm c/ pino 1/4" e clamp C, Sou Foto SFA-001 | Fotolux | ~R$ 50–70 (estimativa; página sem preço na busca) | https://www.fotolux.com.br/cameras-e-acessorios/acessorios/extensores-e-hastes/haste-flexivel-50cm-c-clamp-e-pino-14-suporte-para-iluminadores-microfones-e-leds-sou-foto | Já vem com garra de mesa: solução completa para pontas do U e mesas. |
| Suporte celular haste flexível ring light encaixe rosca 1/4 | Rede Open | a partir de R$ 34,10 | https://www.redeopen.com/suporte-celular-haste-flexivel-ring-light-encaixe-rosca-1-4/ | |
| Haste metal flexível 28 cm p/ ring light | Mercado Livre | R$ 53,99–55,49 | https://lista.mercadolivre.com.br/haste-para-camera | Confirme a rosca. |
| Gooseneck de microfone (rosca 5/8") | Mercado Livre | R$ 30–60 | https://produto.mercadolivre.com.br/MLB-1074707884-suporte-de-mesaflexivelbracohaste-gooseneck-pmicrofone-_JM | **Não serve** sem adaptador 5/8"→1/4" (R$ 10–15). |
| Suporte gooseneck celular braço longo (Kumprohu 33 cm / licheers 110 cm) | Amazon.com.br | R$ 56,09 / R$ 128,15 | https://www.amazon.com.br/Suporte-para-telefone-Gooseneck-microfone/dp/B0C48KBFPJ · https://www.amazon.com.br/Gooseneck-pregui%C3%A7oso-dispositivos-polegadas-Comprimento/dp/B07HMWW1KX | Garra de celular, sem rosca 1/4": a webcam prende pelo clipe na garra. Funciona, mas é gambiarra. |

**Fixação:** pino 1/4" direto na rosca da webcam; a base da haste rosqueia num pedaço de barra roscada 1/4" fixado no topo do PVC. Dá o efeito "olho que se vira" sem precisar de rótula.

### E5. Mini tripé, garra/clamp, pedestal, luminária de chão

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Mini tripé de mesa rosca 1/4" (metal) | Mercado Livre | R$ 14–22 (frete grátis) | https://lista.mercadolivre.com.br/mini-tripe-mesa | Para webcams baixas (40–60 cm) sobre banquinho/caixote. |
| Mini tripé flexível (tipo gorillapod) | Mercado Livre | R$ 44,61 | https://lista.mercadolivre.com.br/tripe-com-rosca-1-4 | Enrola no cano PVC ou na haste do pedestal. |
| Garra Super Clamp com rosca 1/4" e 3/8" (carga 2 kg) | Eshop10 | R$ 59,90 | https://eshop10.com.br/produto/super-clamp-garra-com-entradas-1-4-e-3-8/ | Prende em mesa, cano, encosto de cadeira. Webcam rosqueia direto ou via haste flexível. |
| Garra clamp de mesa (Rede Open) | Mercado Livre | R$ 78,90 | https://lista.mercadolivre.com.br/clamp-camera | |
| Garra clamp + braço Magic Arm 1/4"-3/8" | Mercado Livre | R$ 115–146 | https://lista.mercadolivre.com.br/clamp-camera | Kit 2 garras: R$ 123,49. |
| Clamp pegador YA405 rosca 1/4" | Shopee (via comparador) | ~R$ 25–40 (estimativa) | https://escorregaopreco.com.br/ofertas/shopee/5983795 | |
| Pedestal girafa microfone c/ cachimbo, novo | Mercado Livre | R$ 78,10 | https://www.mercadolivre.com.br/pedestal-suporte-microfone-girafa-c-cachimbo-com-regulagem-cor-preto/p/MLB24727929 | Altura 0,9–2 m, base tripé dobrável. Rosca de topo 5/8": precisa adaptador 5/8"→1/4" (R$ 10–15) ou abraçadeira. |
| Pedestal girafa Visão PE-04, novo | Mercado Livre | R$ 169,10 | https://www.mercadolivre.com.br/pedestal-girafa-para-microfone-c-pes-dobraveis-e-braco-articulado-viso-musical-cor-preto/p/MLB38027434 | Mais robusto. |
| Pedestal microfone **usado** | Mercado Livre | R$ 126–200 (kit 3 Vector: R$ 160) | https://lista.mercadolivre.com.br/pedestal-microfone-usado | Usado **não** está mais barato que novo genérico; vale olhar OLX/grupos locais (R$ 40–80, estimativa) ou emprestar de igreja/banda. |
| Luminária de chão articulada 1,6–1,9 m (Dapon/YASO) | Mercado Livre | R$ 117–178 | https://lista.mercadolivre.com.br/luminaria-de-chao | Retira a cúpula e prende a webcam no braço com clipe + abraçadeira. Caro para o que faz; só se já tiver uma em casa. |
| Luminária pedestal articulada 1,72–1,90 m | Leroy Merlin | R$ 199,90–338,49 | https://www.leroymerlin.com.br/luminarias-de-chao/tonalidade/Preto | Idem. |

**Recomendação E (geral):** base da frota = PVC 25 mm + cap + parafuso 1/4" (≈ R$ 15 por haste). Complemente com 4–5 hastes flexíveis Sou Foto 28 cm (R$ 32) nas webcams que ficam mais perto do público e 2–3 garras Super Clamp (R$ 60) para prender em móveis/telas. Pedestal de microfone só se conseguir emprestado ou por < R$ 60.

---

## F. Bases pesadas para as varas — ESSENCIAL (uma vara de 2 m de PVC sem base cai com um esbarrão)

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Saco de areia média/grossa lavada 20 kg | Leroy Merlin | R$ 4,90–5,31 | https://www.leroymerlin.com.br/areia-media-lavada-saco-20kg-areiao-brasil_92223005 | **Melhor custo.** Encha garrafas PET 2 L (≈ 3 kg cada) ou sacos pretos duplos e amarre na base do cano; ou enterre 15 cm do cano num balde/vaso com areia. 1 saco = 6–7 garrafas. |
| Sarrafo/MDF: base em cruz 40×40 cm (2 sarrafos 2,5×5 cm cruzados + abraçadeira de cano) | Loja de madeira / Leroy | R$ 8–15 por base (estimativa: sarrafo 3 m ~R$ 12, retalho MDF 15 mm ~R$ 20) | — | Fixe o cano com abraçadeira tipo "D" de PVC 25 mm (R$ 1–2) parafusada na cruz. Pinte de preto. Fica estável até ~1,5 m; para 2 m, some uma garrafa de areia. |
| Base guarda-sol concreto 12 kg MOR | Mercado Livre | R$ 217,17 (frete grátis) | https://lista.mercadolivre.com.br/base-para-guarda-sol-de-concreto | Tubo central aceita cano 25 mm com calço. Caro: só para 1–2 varas de 2 m em ponto de passagem. |
| Base guarda-sol concreto 22–25 kg (MOR/Bel) | Mercado Livre | R$ 464–480 | idem | Exagero. |
| Base guarda-sol de enchimento (água/areia), plástico | Mercado Livre | R$ 88,91 | idem | Leve de transportar; enche com areia na hora. Boa opção intermediária. |
| Base octogonal concreto 30 kg | Leroy Merlin | página com preço inválido (R$ 9.999,90, de 2023) | https://www.leroymerlin.com.br/base-para-guarda-sol-octa-concreto-30-kg_1566882290 | Pergunte na loja física (estimativa R$ 90–150). |
| Pé de pedestal de microfone (base redonda ferro) | Mercado Livre | R$ 155–370 | https://lista.mercadolivre.com.br/pedestal-base-redonda-microfone | Só vem junto com pedestal; não compensa avulso. |

**Recomendação:** 3 sacos de areia (R$ 15) + 10 bases em cruz de sarrafo (≈ R$ 120 com abraçadeiras e parafusos) ≈ R$ 135. Confortável: + 2 bases de enchimento (R$ 178) para as varas de 2 m.

---

## G. Bases para as TVs de tubo e pontas do U — ESSENCIAL (TV de tubo 14–20" pesa 10–20 kg: a base precisa aguentar)

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Caixote de feira madeira pinus 60 cm | Mercado Livre | R$ 42 | https://lista.mercadolivre.com.br/caixote-madeira | Virado de boca para baixo aguenta a TV de tubo; estética combina com a instalação. Em feira/CEASA sai por R$ 10–20 (estimativa). |
| Banquinho plástico dobrável até 100 kg | Mercado Livre | R$ 25,49–26,98 | https://lista.mercadolivre.com.br/banquinho-dobravel | Para webcams baixas e para a ponta do U; **não** para TV de tubo (topo pequeno, balança). |
| Banqueta plástica dobrável Vonder | Leroy Merlin | R$ 72,90–96,90 | https://www.leroymerlin.com.br/banqueta-dobravel-p.html | |
| Cavalete madeira eucalipto reforçado 69×69 cm Neonx | Leroy Merlin | R$ 69,90 | https://www.leroymerlin.com.br/cavalete-para-mesa--decoracao-madeira-de-eucalipto-reforcado-69x69-cm-neonx_1568100421 | 2 cavaletes + tábua/porta velha = mesa longa para as pontas do U e para o PC. |
| Mesa dobrável MDF 60×40 cm (de parede) | Mercado Livre | R$ 75–195 (ex.: R$ 122,68 c/ cupom) | https://lista.mercadolivre.com.br/mesa-dobravel-em-mdf-60-cm-x-40-cm | A maioria é de parede; mesa dobrável de plástico 60 cm de pé: R$ 150–180 (https://lista.mercadolivre.com.br/mesa-de-plastico-dobravel). |
| Estante aço 3 prateleiras EAF007 (90×80×28 cm) | Leroy Merlin | R$ 175,88 (PIX) / R$ 204,51 | https://www.leroymerlin.com.br/estante-aco-3-prateleiras-eaf007-cinza_1567197618 | TV de tubo na prateleira do meio e hub/fonte embaixo; esconde cabos. Fundo 28 cm é pouco para TV de tubo grande (precisa de 35–45 cm). |
| Estante aço/madeira Stronger 98×68×30,5 cm, 180 kg | Leroy Merlin | ver página (estimativa R$ 200–250) | https://www.leroymerlin.com.br/estante-de-aco-e-madeira-com-3-prateleiras-preta-stronger-98x68x30,5cm-180kg-multivisao_91706580 | |

**Recomendação:** 2 caixotes de feira (R$ 84, ou R$ 30 na feira) para as TVs de tubo + 2 banquinhos plásticos (R$ 52) para as pontas do U/webcams baixas. Confortável: + 2 cavaletes Neonx (R$ 140) com uma tábua para a mesa do PC/hubs.

---

## H. Luz frontal suave — OPCIONAL (mas melhora muito a imagem das webcams genéricas, que ficam ruidosas com pouca luz)

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Ring light 10" (26 cm) com tripé 2,10 m, 3 tons, USB | Amazon.com.br | R$ 49,90–53,90 | https://www.amazon.com.br/Light-Iluminador-Polegadas-Trip%C3%A9-Metro/dp/B0CZ7MPQYN | Tripé serve de haste extra para webcam (rosca 1/4" no topo!). Alimenta por USB (ligue num carregador, não no hub das webcams). |
| Ring light 10" com tripé | Mercado Livre | R$ 36,79–50,99 | https://lista.mercadolivre.com.br/ring-light-10-polegadas | Anúncios mais baratos têm poucas avaliações. |
| Ring light 10" Vivitar | Amazon.com.br | R$ 142,78 | https://www.amazon.com.br/Iluminador-Filmagem-Light-Polegadas-MC9000/dp/B08T6H3W1W | |
| Luminária de mesa LED touch 3 níveis | Amazon.com.br | R$ 53,90–68,90 | https://www.amazon.com.br/abajur-de-mesa/s?k=abajur+de+mesa | Luz difusa com papel manteiga por cima. |
| Luminária LED de mesa básica (UNYHOME / ART HOUSE) | via comparadores (Zoom/my-best) | R$ 20–30 | https://www.zoom.com.br/busca/luminaria+abajur+led | |
| Luminária de chão articulada | Mercado Livre | R$ 117–178 | https://lista.mercadolivre.com.br/luminaria-de-chao | Com lâmpada LED fosca 2700 K apontada para a parede = luz rebatida suave. |

**Recomendação:** 1 ring light 10" com tripé (≈ R$ 50) apontada para o rosto de quem observa, intensidade baixa, tom quente. Confortável: 2 ring lights + 1 luminária de chão com lâmpada fosca rebatida na parede.

---

## I. Fixação, cabos e energia — ESSENCIAL

| Opção | Loja | Preço | Link | Observação |
|---|---|---|---|---|
| Abraçadeira nylon preta 3,5×280 mm, 100 un. | Leroy Merlin | R$ 17,90 | https://www.leroymerlin.com.br/abracadeira-de-nylon-3,5x280mm-100-unidades-preto_1571474857 | Tamanho bom para prender cabo + webcam no cano. |
| Abraçadeira nylon 3,5×300 mm, 100 un. | Leroy Merlin | R$ 32,90 | https://www.leroymerlin.com.br/abracadeira-de-nylon-preta-100-unidades-3,5x300mm_1571926285 | |
| Abraçadeira MD9 3×100 mm, 100 un. | Kabum | R$ 7,90 (PIX) | https://kabum.com.br/produto/79067/abracadeira-md9-nylon-3x100mm-com-100-preto-3572 | Pequena: só para cabos. |
| Fita dupla face VHB 19 mm × 20 m (tipo 3M) | Mercado Livre | R$ 43,95 | https://lista.mercadolivre.com.br/fita-dupla-face-3m-vhb | Segura hub/fonte embaixo da mesa e webcam em superfície lisa. |
| Fita dupla face 3M Scotch Fixa Forte 19 mm × 2 m | Leroy Merlin | R$ 20,90 | https://www.leroymerlin.com.br/fita-dupla-face-3m-scotch-fixa-forte-transparente-19mmxm_87917725 | Pouca metragem. |
| Velcro dupla face organizador de cabos 20 mm × 3 m | Mercado Livre | R$ 16,99–19,99 (kit 5 rolos: R$ 74,50) | https://lista.mercadolivre.com.br/velcro-dupla-face-para-organizacao-de-cabos-rolo-5m-x-20mm | Reutilizável; prende o cabo USB ao longo do cano. |
| Velcro adesivo 20 mm, 2–3 m | Mercado Livre | R$ 23,49–27,50 | https://lista.mercadolivre.com.br/velcro-adesivo-20mm | |
| Filtro de linha 6 tomadas, cabo 5 m | Amazon.com.br | R$ 48,21 | https://www.amazon.com.br/Filtro-Metros-Protetor-El%C3%A9trico-Tomadas/dp/B0FKZF9VWM | Compre 2 (TVs + monitores + 3 fontes de hub + PC = 8–9 plugues). |
| Filtro de linha 6 tomadas 5 m | Mercado Livre | R$ 34,59–44,89 (frete grátis) | https://lista.mercadolivre.com.br/filtro-de-linha-6-tomadas-5m | |
| Filtro de linha 6 tomadas 5 m | Magazine Luiza | R$ 30,09 (PIX) | https://www.magazineluiza.com.br/busca/filtro+de+linha+6+tomadas+5+metros/ | |
| Filtro de linha Fiolux slim 6+1 tomadas 5 m | Fiolux | R$ 76,99 | https://loja.fiolux.com.br/filtro-de-linha/slim/filtro-de-linha-slim-fiolux-6-tomadas-1-tomada-espacada-com-cabo-de-5-metros | Tomada espaçada para fontes grandes. |

**Recomendação:** 2 pacotes de abraçadeira 280 mm (R$ 36) + 1 VHB 19 mm × 20 m (R$ 44) + 2 rolos velcro 3 m (R$ 34) + 2 filtros de linha 5 m (R$ 70–96) ≈ **R$ 200**. Fita isolante preta e fita crepe você provavelmente já tem (R$ 5–8 cada).

---

## Itens que você já tem (só referência de preço, caso quebre)

- Suporte duplo articulado para 2 monitores 17–27": R$ 185–260 (Amazon https://www.amazon.com.br/Articulado-Monitores-Adequado-Polegadas-Suportar/dp/B0DK9151LZ ; ML https://lista.mercadolivre.com.br/suporte-monitor-duplo).
- Tripé para TV 32–55" (pedestal de chão): R$ 337–487 (Kabum CTP400 https://www.kabum.com.br/produto/615671/suporte-tripe-para-tv-32-a-55-ctp400). Tripé fotográfico 1,80 m comum **não** aguenta TV 32" (6–8 kg) com segurança — se for usar o de câmera, amarre a TV com abraçadeira e coloque areia na coluna.
- Webcam genérica 1080p USB 2.0 (reposição): R$ 34–39 (CIETEC / GoodVision / Dr. Hank, https://lista.mercadolivre.com.br/webcam-1080p).

---

## Resumo — cenário mínimo × cenário confortável

| Item | Cenário mínimo | Cenário confortável |
|---|---|---|
| A. Video wall 1→4 | R$ 345 (genérico ML) | R$ 478 (Solução 9188) |
| B. Placa PCIe USB 3.0 + header bracket | R$ 130 (DEX + Engmax) | R$ 150 (F3/Comtac + Engmax) |
| C. 3 hubs com fonte | R$ 180 (3× genérico 5 V) | R$ 600 (3× Orico H7013) |
| D. Extensores USB ativos | R$ 0 (cabos passivos curtos) | R$ 130 (2× 5 m + 1× 10 m) |
| E. 20 hastes (PVC + caps + parafusos + spray + barra roscada) | R$ 305 | R$ 305 + 5 gooseneck (R$ 160) + 3 Super Clamp (R$ 180) + 3 mini tripés (R$ 60) = R$ 705 |
| F. Bases pesadas | R$ 135 (areia + cruz de sarrafo) | R$ 313 (+ 2 bases de enchimento) |
| G. Bases TVs de tubo / pontas do U | R$ 136 (2 caixotes + 2 banquinhos) | R$ 276 (+ 2 cavaletes Neonx) |
| H. Luz | R$ 50 (1 ring light) | R$ 260 (2 ring lights + luminária de chão) |
| I. Abraçadeiras, fitas, velcro, 2 filtros de linha | R$ 200 | R$ 250 |
| **TOTAL** | **≈ R$ 1.480** | **≈ R$ 3.160** |

Fretes não incluídos (estimativa de R$ 60–150 no total para o que não for frete grátis/retirada). Margem recomendada de 10–15 % para variação de preço.

### Ordem de compra sugerida (pelo prazo)
1. **Hoje/amanhã (eletrônicos, maior risco de prazo):** controlador video wall, placa PCIe + header, 3 hubs, hastes flexíveis Sou Foto, Super Clamps.
2. **Até 03/11:** filtros de linha, abraçadeiras, VHB, velcro, extensores, ring light.
3. **Qualquer dia, retirada em loja:** cano PVC, caps, luvas, spray, barra roscada e porcas 1/4", areia, sarrafo, caixotes, banquinhos.
4. **Teste de carga USB** assim que a placa e os hubs chegarem: ligue as 15 webcams, abra todas em 1080p e veja se alguma cai. Se cair, reduza para 720p nas webcams mais distantes ou redistribua entre controladores.
