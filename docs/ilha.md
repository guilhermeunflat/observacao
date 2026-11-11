# Montagem em ILHA (desde 11/11)

A montagem em U foi trocada por uma ilha. Este arquivo diz como ela funciona no código e como configurar no local.

## Layout

```
                 parede do fundo (lisa, mesa quase encostada)
   parede      M3 ->  |  <- M4          câmeras de tracking nas pontas da vara
   c/ janela  [CRT esq | CRT dir]
   (de frente [LED esq | LED dir]       telas costas com costas
    p/ telas   M1 ->  |  <- M2          vara: 14 câmeras numa fila, alternando esq/dir
    da esq)        [ 32" ]              de pé, virada para quem chega        cortinas (de frente p/ telas da dir)
                  ENTRADA
```

- O público chega pela frente, em direção à 32", e circula **só pelas laterais**.
- Cada lateral tem duas zonas, medidas a partir da borda da mesa:
  - **perto** (até a fita no chão, ~1,2 m): quem está ali pode virar "dono" daquele lado, e as telas do lado viram uma janela 3D para ele;
  - **longe** (até ~3 m): só registro, entra nas fotos e no mural.
- A **32"** é um painel 2D (mural). Não tem dono nem tracking.

## Quem vê o quê (por lado)

| Situação no lado | Telas daquele lado |
|---|---|
| ninguém na zona perto | grade das câmeras ao vivo, como parede de monitores de segurança: de longe, o público se vê |
| dono, primeiros `ver_se_s` (10 s) | ele mesmo, ao vivo |
| dono, depois | quem é dono do **outro lado da mesa**; se não houver, a pessoa anterior, trocando a cada `troca_s` (35 s) |
| dono há `alerta_s` (300 s) | flag `alerta` no estado (o aviso e a falha visual entram na camada de conteúdo) |
| `lotacao` (4) ou mais na zona perto | mural |

As sessões do banco abrem só para quem entra na zona perto e fecham `sair_s` (3 s) depois de a pessoa sair dela.

## Configurar no local (sexta)

Tudo em cm, com trena. O referencial é a origem no chão, no centro da mesa; x para a direita de quem chega; z para a frente (a entrada).

1. **Medir e digitar.** Enter mantém o valor atual. O programa avisa quando as medidas não fazem sentido juntas, salva em `config/ilha.json` e mostra o mapa visto de cima.
   ```
   .venv/Scripts/python tools/configurar_ilha.py
   ```
   Para mudar um valor só: `--set mesa.altura_cm=78` ou `--set telas.tubo_esq.ao_longo_cm=88`.
2. **Fita no chão** na distância `zonas.perto_cm` da borda da mesa, dos dois lados.
3. **Câmeras M3 e M4.** Se ainda não estiverem cadastradas, cadastrar com `tools/calibrate_cameras.py`, papel `master`. O `cameras.json` só tem M1 e M2.
4. **Calibrar o tracking, um lado por vez.** Duas marcas no chão, a 60 e a 150 cm da borda da mesa, no meio do comprimento. A pessoa fica nas marcas olhando para as telas daquele lado, aperta 1 e 2, depois s.
   ```
   .venv/Scripts/python tools/calibrate_tracking.py --lado esq --olhos 160
   .venv/Scripts/python tools/calibrate_tracking.py --lado dir --olhos 160
   ```
   Câmera calibrada fica marcada com `"calibrado": true` em `cameras.json`, e a calibração passa a valer mais que a estimativa por medidas. Se mexer na câmera depois, calibre de novo.
5. **Conferir no simulador**, depois com gente:
   ```
   cd src && ../.venv/Scripts/python -m observacao.render.app
   ```
   A janela mostra as 5 telas com nome e o que cada uma está mostrando, além do mapa visto de cima. **No mapa:** clique para pôr uma pessoa, arraste para mover, use o botão direito para tirar e a roda do mouse sobre a pessoa para mudar a altura. Teclas: `0`–`9` pessoas automáticas, `C` limpa, `T` usa o tracking real.
6. **No evento:** `cd src && ../.venv/Scripts/python -m observacao.render.app --perfil evento --telas`

Teste sem câmeras: `--fake 8 --pessoas 4` (pessoas simuladas entrando e saindo das zonas). Teclas: 0–9 pessoas, V mapa, G grade, H texto.

## Arquivos

| Arquivo | O quê |
|---|---|
| `config/ilha.json` | medidas da montagem (gerado/editado por `tools/configurar_ilha.py`) |
| `config/profiles/ilha.json`, `evento.json` | perfis da ilha (tracking até 4,5 m, até 12 pessoas) |
| `src/observacao/ilha.py` | medidas → telas, câmeras, zonas, referencial de cada lado, mapa visto de cima |
| `src/observacao/estado_ilha.py` | regras por lado (dono, o que vê, lotação, alerta, sessões) |
| `src/observacao/render/app.py` | render da ilha (uma cena 3D por lado, 32" como painel) |
| `src/observacao/render/app_u.py` | render antigo do U, só como referência |
| `tools/configurar_ilha.py` | perguntas das medidas, avisos, mapa |
| `tools/calibrate_tracking.py` | agora com `--lado esq/dir` para a ilha |

## Ainda não feito (camada de conteúdo, decisões da reunião de 10/11)

- recorte do rosto do dono fixo em destaque (na 32");
- aviso de consumo excessivo + falha visual sincronizada em todas as telas (o estado já sinaliza `alerta`);
- filtro 80/20: só fotos com gente no mural e nas cenas;
- palpites de idade, altura, humor e peso;
- ajuste de cor por tela para as TVs de tubo;
- frases (desligadas em `app.json`) e texto espacial.
