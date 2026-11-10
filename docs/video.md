# Vídeo: 5 telas em 4 saídas

O controlador de video wall 2×2 (MLB22145200) está em casa desde 05/11.

## Ligação

| Tela | Saída do PC | Caminho |
|---|---|---|
| TV LED 32" vertical | DisplayPort 1 | direto (adaptador DP→HDMI se a TV só tiver HDMI) |
| Monitor 21" esquerdo | DisplayPort 2 | direto |
| Monitor 21" touch | DisplayPort 3 | direto + cabo USB do touch na 4ª porta USB 2.0 preta |
| TV de tubo esquerda | HDMI | HDMI do PC → entrada do video wall → saída 1 → conversor HDMI→AV → TV |
| TV de tubo direita | HDMI | mesma entrada → saída 2 → conversor → TV |

## Teste em 10 minutos

1. Ligue tudo com o video wall no modo **2×2** (botão do painel ou controle).
2. No Windows, em Configurações > Sistema > Tela: confira que aparecem 4 telas, gire a 32" para retrato e ponha a saída do video wall em 1920×1080.
3. Rode o teste. O primeiro comando lista as telas com índice; use no segundo o índice da que mede 1920×1080 e está no HDMI.

```
.venv/Scripts/python tools/test_screens.py --listar
.venv/Scripts/python tools/test_screens.py --videowall 3
```

4. Cada TV de tubo deve mostrar uma letra. Anote qual letra chegou em cada uma (esperado: A na esquerda, B na direita). Se vier trocado, inverta os cabos nas saídas do controlador.
5. Confira se o conversor HDMI→AV corta as bordas (overscan das TVs de tubo). Se cortar, o software deixa margem; anote quanto some.

Resultado vai para `config/screens.json` (campo `via_videowall` de cada TV de tubo).
