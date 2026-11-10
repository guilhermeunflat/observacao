# Fotos de medição: espaçamento das telas

Para a paralaxe ficar certa, o software precisa saber onde cada tela está de verdade: posição, altura, ângulo e tamanho da área de imagem. Um erro de 10 cm ou 10° já desalinha o espaço entre uma tela e outra.

Medimos com fotos em cada montagem: no teste em casa, na casa do amigo e no evento. Toda montagem tira fotos de dois tipos.

- **A. Fotos de medição.** As telas mostram marcadores e `tools/fotos_telas.py` calcula as posições sozinho.
- **B. Fotos de documentação.** Servem para nós dois entendermos o espaço (altura, distâncias, sensação) e para conferir o que o script calculou.

## Pastas

```
docs/fotos/
  marcador_chao.pdf              imprimir em A4, 100%
  2026-11-07_casa/
    medicao/                     fotos tipo A (o script lê esta pasta)
    documentacao/                fotos tipo B
    notas.md                     medidas de trena e observações
  2026-11-14_evento/
    ...
```

## Antes das fotos (5 min)

1. **Tamanho da imagem de cada tela.** Meça com trena a largura e a altura **só da área que acende**, sem a moldura. Isso vale principalmente para as TVs de tubo, que cortam a borda da imagem (overscan): ligue o app com `M` e meça do primeiro ao último ponto branco visível. Anote em `notas.md` e, se mudou, corrija `largura_cm`/`altura_cm` no screens.json. O script usa essas medidas como escala.
2. **Marcador do chão.** Imprima `docs/fotos/marcador_chao.pdf` em A4, tamanho real (100%, sem "ajustar à página"). Confira com a régua se o quadrado preto mede 15 cm; se não medir, passe o valor real com `--chao-cm`. Deixe a folha deitada no chão no meio do U, bem plana. Ela dá a altura das telas em relação ao chão.
3. **Ligar os marcadores.** Abra o app no modo real (`--telas`) e aperte `M`. Cada tela mostra uma grade de quadrados pretos e brancos.
4. **Luz.** Use luz ambiente normal, sem reflexo forte nas telas. Desligue o modo noturno ou o filtro de luz azul do Windows.

## A. Fotos de medição (6 a 10 fotos, 3 min)

- **Celular e lente.** Use o mesmo celular, a lente principal (1×) e nada de zoom, ultra-wide, retrato ou panorama. Todas as fotos na mesma orientação, todas deitadas ou todas em pé.
- **Ângulos.** Fotografe de onde o público fica, de ângulos diferentes: centro, esquerda, direita, mais perto, mais longe, mais alto (braço esticado) e mais baixo (agachado).
- **A TV 32 do centro aparece em todas.** Ela é a referência. Cada foto mostra pelo menos 2 telas inteiras; as pontas (TVs de tubo) precisam aparecer em pelo menos 3 fotos.
- **Foto com o chão.** Pelo menos 2 fotos apontando mais para baixo, mostrando a folha do chão **e** a TV 32.
- **Nitidez.** Foto tremida não serve: o celular firme, com foco tocando na tela.
- **Formato.** No iPhone, mande em JPG (Ajustes > Câmera > Formatos > Mais Compatível) ou exporte.

Depois, no PC:

```bash
.venv/Scripts/python tools/fotos_telas.py docs/fotos/2026-11-07_casa/medicao
```

O script mostra para cada tela a posição (x, y, z em cm), os ângulos `yaw` e `pitch`, o valor atual do screens.json para comparar e a **variação** entre as fotos. Uma variação acima de ~2 cm pede mais fotos daquela tela. Também mostra os vãos entre telas vizinhas e de onde cada foto foi tirada.

Em `medicao/_resultado/` ficam a **vista de cima** (cinza = configuração atual, verde = medido) e cada foto com os marcadores reconhecidos. Se estiver bom:

```bash
.venv/Scripts/python tools/fotos_telas.py docs/fotos/2026-11-07_casa/medicao --escrever
```

O script grava no screens.json do perfil e guarda uma cópia de segurança do arquivo antigo. No evento, use `--perfil evento`.

Sem a folha do chão, informe a altura do centro da TV 32 medida com trena: `--altura-centro 120`.

## B. Fotos de documentação (10 min)

Servem para entendermos juntos o espaço. Sempre que der, deixe uma **trena aberta** ou um objeto de tamanho conhecido na foto (folha A4: 21 × 29,7 cm).

| # | Foto | Por quê |
|---|---|---|
| 1 | De onde a pessoa fica, na altura dos olhos (~1,55 m), com o U inteiro | o que o público vê |
| 2 | A mesma, de 1,70 m e de 1,40 m | pessoas altas e baixas |
| 3 | De cima: em cima de uma cadeira ou escada, celular apontando para baixo, U e chão visíveis | espaçamento e ângulos vistos de cima |
| 4 | Lateral esquerda e lateral direita, mostrando a profundidade do U | quanto as pontas avançam |
| 5 | Cada tela de perto, com a trena vertical do chão até a borda de baixo da imagem | altura de cada tela |
| 6 | Trena no chão do centro da TV 32 até onde a pessoa fica | distância de interação |
| 7 | Trena entre as bordas de telas vizinhas | vãos |
| 8 | Onde estão as câmeras master e as câmeras olho (varas) | posição das câmeras |
| 9 | O ambiente em volta: paredes, luz, por onde as pessoas chegam | entrada e fluxo |
| 10 | Uma foto com a luz do evento (ou simulada baixa) | reflexo e legibilidade |

Em `notas.md`, anote o que a trena mostrou, o que foi improvisado (calço, livro, banquinho) e o que vai ser diferente no evento.

## Por que funciona

Cada marcador tem posição conhecida em cm no plano da sua tela, porque o app desenha a grade a partir de `largura_cm`/`altura_cm`. Numa foto, isso basta para calcular onde a tela está em relação ao celular. Juntando as fotos pela TV 32, todas as telas entram num mesmo espaço. A lente do celular é estimada pelas próprias fotos, e a folha do chão define o "para cima" e a altura.

No teste com fotos sintéticas, o script recuperou a posição de todas as telas com menos de 0,5 cm e menos de 0,2° de erro.
