# Compras — versão 2 (28/10/2026, festa em 14/11 → 17 dias)

Refeita a partir do que **já existe em casa**. A versão anterior, com 90 links, está em `compras_v1_28-10.md`; 38 links do Mercado Livre e 15 da Leroy Merlin recusam robô (abrem no navegador, mas não pude confirmar preço) e 4 estavam quebrados. Aqui só entram links que abriram em 28/10 com preço visto, ou páginas de busca do Mercado Livre (`lista.mercadolivre.com.br/...`, que abrem no navegador). "Não visto" = a página abre mas esconde o preço do robô.

**Regra de prazo:** nada de "Envio da China". Pedidos eletrônicos até **03/11**. Material de construção: retirar na loja (a Telhanorte mostrou os PVCs só com estoque online).

## 0. O que já existe e o que isso resolve

| Item em casa | Resolve | Falta |
|---|---|---|
| Controlador de video wall 2×2 (**comprado 28/10**, MLB22145200) | 5ª tela: as 2 TVs de tubo com imagens diferentes | 2 cabos HDMI curtos até os conversores HDMI→AV, se não tiver |
| Conversores HDMI→AV e tudo das TVs de tubo | pontas do U | nada |
| PC: 10 portas USB traseiras (4 azuis da CPU, 2 vermelhas, 4 pretas) + 2 headers USB 3.0 internos | 7 "tubos" USB 2.0 independentes (`docs/usb.md`) | bracket de header só se o teste de carga reprovar |
| 3 hubs USB 3.0 de 4 portas **sem fonte** | 3 câmeras por hub nas portas azuis (900 mA) | nada; hub com fonte **não** é mais necessário |
| ~20 webcams, extensores USB, régua | olhos; cabos até ~3 m sem extensor ativo | fixação (sem rosca) e varas |
| Suporte duplo pivotante + pés dos monitores | os 2 monitores 21" | nada |
| Tripé de câmera | TV 32" vertical | amarrar com abraçadeira e pôr peso na coluna |
| Mesa de cavaletes 1,20×0,60 | base do PC/hubs ou das pontas do U (estudo da Fase 2) | nada |
| Notebook extra | plano B de 5ª tela; terminal do operador | nada |

**Não comprar:** placa PCIe USB, hubs com fonte, splitter HDMI, extensores USB 3.0.

## 1. Fixar a webcam sem rosca (essencial)

A webcam (Sunplus, ~80×85×32 mm, 70–110 g) tem clipe dobrável que vira pezinho. Duas soluções, por função:

| Uso | Método | Material e preço (28/10) | Ângulo | Firmeza |
|---|---|---|---|---|
| **Câmeras que precisam de ajuste fino** (masters do tracking e as mais perto do público): 5–6 un. | **Pinça de celular com rosca 1/4"** (a webcam entra na pinça de 55–85 mm) rosqueada numa **barra roscada 1/4"-20** enfiada no topo do cano; ballhead opcional | Pinça R$ 17,90 https://www.amazon.com.br/dp/B07T3SY4NV · Kit ballhead + pinça R$ 29,90 https://www.amazon.com.br/dp/B0FRCY9LCX · Barra roscada 1/4" 1 m: loja de ferragens R$ 4–8 (ML: https://lista.mercadolivre.com.br/barra-roscada-1-4) + 12 porcas e arruelas 1/4" | Solta, aponta, trava: segundos | Alta (metal) |
| **Todas as outras**: 10 un. + reservas | **Abraçadeira de nylon** atravessando a boca do clipe e abraçando o cano; fita isolante no cano para não girar | HellermannTyton 4,6×200 mm, 100 un, R$ 44,90 (35,92 PIX) https://www.telhanorte.com.br/abracadeira-t50r-200x4-6mm-100un-branco-hellermanntyton-1489186/p | Inclinação do clipe ajusta ~30°; mais que isso = cortar e refazer; giro = girar o cano | Alta |
| Em borda de móvel/TV/monitor (sem vara) | **Gooseneck de celular com garra de mesa** (braço ≤ 35 cm) ou **binder clip 51 mm** | Gooseneck R$ 14,99 (Amazon via Buscapé; avaliações reclamam da garra) · braço de metal R$ 69,89 https://www.extra.com.br/suporte-celular-tablet-braco-metal-longo-flexivel-para-mesa/p/1576065337 · binder 51 mm, 12 un, R$ 20,28 https://www.amazon.com.br/dp/B0DNN9WXQ9 | Muito rápido | Média |
| Reforço/alternativa em cano | **Braçadeira metálica rosca sem fim 3/4"×1"** com tira de EVA | 2 un R$ 24,90 https://www.telhanorte.com.br/abracadeira-rosca-sem-fim-34-x-1-fixtil-243353/p | 30 s com chave de fenda | Muito alta |

Descartados: velcro e VHB (pouca área de contato no cano; servem só em superfície plana), cola quente (emergência: pistola R$ 19,90 + bastões R$ 18,90 na Telhanorte).

## 2. Varas e bases (essencial; quantidades saem do estudo da Fase 2)

| Item | Qtd para 15 + reservas | Preço visto 28/10 | Link que abre |
|---|---|---|---|
| Tubo PVC soldável 25 mm × 3 m Tigre (rígido até 2 m; 20 mm só para hastes ≤ 1,2 m) | 8 barras (24 m, altura média 1,2 m) | R$ 18,90 (15,03 PIX) | https://www.telhanorte.com.br/tubo-soldavel-nbr-5648-3-00m-25mm-tigre-170208/p (loja física do bairro costuma ser mais barata) |
| Cap 25 mm (topo: furo de 6,5 mm para a barra roscada) | 20 | ~R$ 3 (cap 20 mm visto a R$ 3,79) | https://www.telhanorte.com.br/cap-soldavel-20mm-tigre-23523/p |
| Luva 25 mm (emendas/altura) | 6 | R$ 0,90 | https://www.ferreiracosta.com/produto/356785/luva-soldavel-pvc-marrom-25-mm-krona |
| Alternativa: cabo de vassoura 1,2 m Ø 23 mm (o clipe morde direto) | até 20 | R$ 6–12 em loja de bairro | — |
| Spray preto fosco 400 ml | 3 | R$ 28,50–29,00 | https://www.mundografite.com.br/uso-geral-preto-fosco |
| Base: saco de areia 20 kg → garrafas PET de 2 L (3 kg cada) amarradas no pé da vara, ou balde/vaso com areia | 3 sacos | ~R$ 5 cada em loja de construção | — |
| Base em cruz: 2 sarrafos 2,5×5 cm × 40 cm + abraçadeira "D" de PVC 25 mm parafusada | 10 bases | ~R$ 12/base (sarrafo 3 m ~R$ 12) | loja de madeira |
| Caixote de feira (TV de tubo em cima, virado) | 2 | R$ 10–20 na feira; R$ 42 no ML | https://lista.mercadolivre.com.br/caixote-madeira |
| Banquinho plástico dobrável (webcams baixas, pontas do U) | 2 | ~R$ 26 | https://lista.mercadolivre.com.br/banquinho-dobravel |

## 3. Cabos e energia (essencial)

| Item | Qtd | Preço visto | Link |
|---|---|---|---|
| Filtro de linha 6 tomadas, cabo 5 m | 2 (TVs + monitores + PC + conversores + video wall = 8–9 plugues) | não visto (Amazon) / R$ 76,99 (Fiolux slim 6+1) | https://www.amazon.com.br/dp/B0FKZF9VWM · https://loja.fiolux.com.br/filtro-de-linha/slim/filtro-de-linha-slim-fiolux-6-tomadas-1-tomada-espacada-com-cabo-de-5-metros · https://lista.mercadolivre.com.br/filtro-de-linha-6-tomadas-5m |
| Abraçadeira curta 3×100 mm, 100 un (só cabos) | 1 | R$ 5,90 PIX (resta 1) | https://www.kabum.com.br/produto/79067/abracadeira-md9-de-nylon-3x100mm-100-unidades-preto-3572 |
| Velcro organizador de cabo (cabo USB ao longo do cano) | 2 rolos | não visto | https://lista.mercadolivre.com.br/velcro-dupla-face-para-organizacao-de-cabos-rolo-5m-x-20mm |
| Cabo HDMI 1 m (video wall → conversores) | 2, se faltar | ~R$ 15 | https://lista.mercadolivre.com.br/cabo-hdmi-1-metro |

## 4. Só se o teste de carga USB reprovar

| Item | Para quê | Preço | Link |
|---|---|---|---|
| Bracket header USB 3.0 19 pinos → 2 portas traseiras | +2 tubos USB por bracket (a placa tem 2 headers) | R$ 45 (ML, não visto) / R$ 179,99 (Engmax, com Type-C, exagero) | https://lista.mercadolivre.com.br/adaptador-usb-3.0-19-pinos |
| Placa PCIe x1 USB 3.0 4 portas (1 chip = **1** tubo) | último recurso | R$ 85–105 | https://www.amazon.com.br/dp/B07CZPBV3X · https://www.amazon.com.br/dp/B08Q863286 |

## 5. Opcional

| Item | Por quê | Preço | Link |
|---|---|---|---|
| Ring light 10" com tripé 2,1 m, USB | webcams genéricas ficam ruidosas no escuro; o tripé serve de vara extra | R$ 37–54 | https://lista.mercadolivre.com.br/ring-light-10-polegadas (o link da Amazon deu erro 500 em 28/10) |
| Super Clamp 1/4"–3/8" | prender pinça/gooseneck em mesa, cano, encosto | R$ 59,90 | https://eshop10.com.br/produto/super-clamp-garra-com-entradas-1-4-e-3-8/ |
| Extensor USB 2.0 **ativo** 10 m | só se alguma câmera ficar a mais de 3 m do hub | R$ 28,40 (Central Cabos) / R$ 58,99 (Oficina dos Bits) | https://www.centralcabos.com.br/extensor-amplificado-usb-2-0-10mts---mcb-026/p · https://www.oficinadosbits.com.br/produto/cabo-extensor-usb-2-0-ativo-10-metros-a-macho-a-femea/ |

## Resumo

| Bloco | Mínimo | Confortável |
|---|---|---|
| 1. Fixação (100 abraçadeiras + 5 pinças + barra/porcas) | R$ 150 | R$ 230 (+ 2 kits ballhead, 2 braçadeiras metálicas) |
| 2. Varas e bases (PVC, caps, luvas, spray, areia, sarrafo, caixotes na feira) | R$ 420 | R$ 520 (+ 2 banquinhos, cabos de vassoura extras) |
| 3. Cabos e energia | R$ 110 | R$ 160 |
| 4. USB (só se reprovar) | R$ 0 | R$ 90 (2 brackets) |
| 5. Opcional | R$ 0 | R$ 150 (ring light + super clamp + 1 extensor) |
| **Total** | **≈ R$ 680** | **≈ R$ 1.150** |

Comparado com a versão 1 (R$ 1.480–3.160): saíram o video wall (comprado), os hubs com fonte e a placa PCIe (não são necessários). Fretes fora da conta.

### Ordem
1. **Agora:** pinças 1/4" (Amazon) e abraçadeiras HellermannTyton (Telhanorte): destravam as Fases 1 e 2.
2. **Depois do estudo de posicionamento (Fase 2):** PVC ou cabos de vassoura, caps, spray, areia, sarrafo, caixotes, na quantidade que o estudo definir.
3. **Depois do `bench_usb.py`:** brackets, se precisar.
4. **Até 03/11:** filtros de linha, velcro, HDMI, ring light.
