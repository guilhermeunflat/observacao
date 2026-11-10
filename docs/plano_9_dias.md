# Plano de corte: 9 dias até a festa (05/11 → 14/11/2026)

O plano completo continua em `plano.md`. Este arquivo diz **o que entra, o que sai e em que ordem**, para chegar no dia 14 com uma obra que funciona em vez de uma obra completa pela metade.

## Regra de corte

Nunca cortar: captura estável, tracking da cabeça, paralaxe nas telas, troca de pessoa (vê a anterior), frases.
Corta primeiro, nesta ordem, se apertar: estimativa de altura → emoção → idade → dossiê no touch → mural com vídeo (fica só foto) → identidade visual elaborada (fica uma fonte e duas cores).

## Sem solda

O ESP32 com RJ45 saiu da obra (decisão do usuário em 05/11). Tudo roda no PC. Nada que exija solda entra no plano.

## Câmeras (decidido em 05/11)

O PC mantém 6 webcams abertas (2 por controlador). Distribuição: 2 master de tracking, 2 de vídeo ao vivo, e 6 câmeras de foto revezando 2 vagas (cada uma fotografa a cada ~8 s). O notebook serve mais câmeras pela rede (`docs/notebook.md`). Total previsto: 10 no PC + as do notebook.

## Dias

| Dia | Data | Software (Claude) | Físico (você) |
|---|---|---|---|
| 1 | qua 05/11 | captura, teste de carga USB, calibração de câmeras, grade do operador, mosaico 2D | tirar os discos das portas traseiras; plugar 3 a 5 webcams; rodar os testes |
| 2 | qui 06/11 | tracking de cabeça (MediaPipe) nas câmeras master; render off-axis numa tela | plugar as 15; comprar pinças e abraçadeiras; primeiro esboço das varas |
| 3 | sex 07/11 | render nas 5 telas (3 DP + video wall 2×2); calibração de telas por fotos (docs/fotos_medicao.md) | montar as 5 telas em U em casa; medir a área de imagem de cada tela; fotos de medição e documentação |
| 4 | sáb 08/11 | banco de sessões, troca de pessoa (anterior / anel de 3), modo 4+ (texto grande + mural de fotos) | gravar a pessoa 0 (você) |
| 5 | dom 09/11 | banco de frases a partir da síntese (texto ESPACIAL no 3D, não letreiro 2D; ver README) + palpites (idade se der tempo) + fonte e cores | escolher fonte/cores em 30 min; revisar as frases |
| 6 | seg 10/11 | correções do teste completo; `start.bat` sobe tudo | teste completo em casa com 2–3 pessoas |
| 7 | ter 11/11 | pacote para o amigo; perfil `evento`; roteiro de recalibração | placa de entrada; separar e etiquetar cabos |
| 8 | qua 12/11 | só correções | ensaio de 1 h; desmontar etiquetando |
| 9 | qui 13/11 | — | folga / transporte |
| — | sex 14/11 | — | montagem + recalibração (15 min) + festa |
