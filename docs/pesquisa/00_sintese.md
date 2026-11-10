# 00 — Síntese: o que a pesquisa inteira diz sobre os danos da vigilância

Escrito em 28/10/2026 a partir dos sete dossiês reescritos (~83 mil palavras, cerca de 200 fontes lidas na íntegra, cada uma resumida no seu dossiê com a linha "Fonte:"). Este arquivo não repete os fatos: ele explica o que eles significam quando postos lado a lado, e termina com as conclusões que a obra pode sustentar.

| Dossiê | Tema | Tamanho | O que mais pesa |
|---|---|---|---|
| 01 | Danos: chilling effect, saúde mental, viés, eficácia, desvio de finalidade | 17.400 palavras, 46 fontes | Penney (Wikipédia pós-Snowden), Ravid (meta-análise de monitoramento no trabalho), NIST IR 8280, Piza (76 avaliações de CCTV), Met Police 2024-25 |
| 02 | Gabriel (câmeras privadas integradas à polícia, Brasil) | 10.500, 28 fontes | Intercept Brasil 2023 (Slack/WhatsApp), CPI do Rio, Smart Sampa como destino das imagens |
| 03 | Flock Safety (leitores de placa em rede nacional, EUA) | 11.600, 34 fontes | 404 Media/EFF (busca por mulher que abortou), logs de buscas para o ICE, Evanston |
| 04 | Clearview AI (rostos raspados da internet) | 9.400, 20 fontes | Contratos ICE/CBP, € 90,5 mi em multas sem pagamento, caso Angela Lipps |
| 05 | Smart Sampa, Córtex, Bahia (Estado brasileiro) | 12.500, 23 fontes | Relatórios de transparência da Prefeitura de SP, Agência Pública sobre o Córtex, estudo CESeC |
| 06 | Corretores de dados, vazamentos, informação privilegiada | 12.300, 40 fontes | FTC 2014, Serasa/TJDFT, Fog Reveal, vazamento dos 223 milhões de CPFs |
| 07 | LGPD e o que a obra pode fazer | 9.000, 25 fontes | Texto da lei, ViaQuatro, Hering, Nota Técnica ANPD sobre escolas do Paraná |

---

## 1. A tese em uma página

A vigilância em massa é vendida como uma troca: um pouco de privacidade por mais segurança. A pesquisa mostra que a troca não existe como foi anunciada. Do lado da "segurança", o que se mede é pequeno (câmeras reduzem crime em torno de 13 %, quase todo em estacionamento, nada em crime violento), e o que se anuncia é grande, porque quem opera escolhe o denominador. Do lado da "privacidade", o custo não é abstrato nem uniforme: ele aparece como pessoas que deixam de ler e de falar, trabalhadores mais estressados sem ficarem mais produtivos, homens negros presos por um "z" no sobrenome, uma mulher procurada em 83 mil câmeras por ter abortado, uma pessoa inteira vendida por R$ 0,98 ou por US$ 40.

O que liga os sete dossiês é um mecanismo único: **a vigilância transfere risco de quem vigia para quem é vigiado, e transfere responsabilidade de quem decide para ninguém.** A câmera não cria o erro; ela amplifica o erro que já existe no cadastro, no mandado vencido, no banco de placas, no algoritmo que viu poucos rostos negros. E quando o erro chega à ponta de uma arma, cada elo da cadeia aponta para o próximo: a empresa diz que "só gera pistas", a prefeitura diz que "só consome bases", o Estado diz que o mandado era do Judiciário, a plataforma diz que "o cliente é dono dos dados". A pessoa abordada recebe R$ 5 mil, ou nada.

Para uma instalação, a consequência é direta: o dano da vigilância não está em ser visto. Está em ser visto **por um sistema que decide sobre você sem que você possa responder.** É isso que a obra pode encenar com cinco telas e quinze câmeras: o momento em que a pessoa percebe que o sistema já tem uma versão dela, feita por outros, e que a versão vale mais do que ela.

---

## 2. Os mecanismos do dano, cruzando os dossiês

### 2.1 O olhar muda o comportamento antes de qualquer punição

É o resultado mais robusto da pesquisa e o menos visível na rua. Três métodos independentes convergem (dossiê 01): tráfego da Wikipédia em artigos sobre terrorismo caiu 20–30 % depois de Snowden e não voltou em 14 meses; buscas no Google por termos sensíveis caíram em onze países; escritores do PEN relataram evitar temas, e o experimento de Stoycheff mostrou que o simples lembrete de vigilância silencia quem se sente em minoria. Hong Kong transformou isso em tática física (máscaras, guarda-chuvas, dinheiro vivo).

O que importa para a obra: o efeito é **assimétrico**. Ele cala primeiro quem discorda, quem pesquisa o proibido, quem é minoria. A maioria que "não tem nada a esconder" não sente nada, e por isso aprova (85 % dos londrinos apoiam reconhecimento facial ao vivo). A vigilância produz o próprio consenso que a legitima.

### 2.2 O erro não é da câmera; a câmera dá velocidade e arma ao erro

Esse é o achado que mais mudou com a leitura integral das fontes. A narrativa comum é "o algoritmo errou o rosto". Nos dados oficiais de São Paulo (dossiês 01, 02, 05), dois terços das pessoas conduzidas à delegacia por engano foram levadas por **mandado que já não valia** (141 de 211 no primeiro ano), e só um terço por erro do reconhecimento (59). No Rio, em 2019, a primeira "prisão por reconhecimento facial" foi de uma mulher confundida com uma procurada que já estava presa. Na Flock (03), o erro é um "7" lido como "2", mas o resultado é um cão policial e uma arma apontada. Na Clearview (04), Angela Lipps ficou 108 dias presa por uma correspondência que a empresa descreve como "pista, não identificação".

O padrão: sistemas de vigilância são **amplificadores de cadastro**. Eles pegam um banco de dados sujo (mandados não baixados, placas mal lidas, fotos de documento falso) e o transformam em abordagem armada em segundos. O NIST mede o viés do algoritmo; a rua mede o viés do cadastro mais o do algoritmo mais o do policial. Os três apontam na mesma direção.

### 2.3 Quem paga é sempre o mesmo

NIST: falsos positivos de 10 a 100 vezes maiores para rostos negros, asiáticos e indígenas; Gender Shades: até 34,7 % de erro em mulheres de pele escura contra 0,8 % em homens de pele clara. Na rua: 90,5 % das pessoas presas por reconhecimento facial no Brasil em 2019 eram negras; 8 dos 10 falsos positivos confirmados da polícia de Londres em 2024-25 eram negros; as câmeras do Smart Sampa se concentram no Brás e na Cracolândia; a Gabriel cobre Leblon, Ipanema, Jardins. Crianças: um milhão de alunos do Paraná fotografados diariamente por três anos, sem opção de recusa, com 91,1 % de acerto.

E o Estado **não registra a cor** de 59 % dos abordados em São Paulo. A ausência do dado não é descuido: é o que impede a conclusão de virar fato oficial. Força: forte na direção, média na magnitude, exatamente porque o denominador é escondido.

### 2.4 Resultado pequeno, propaganda grande: o denominador é uma escolha

Piza et al. (76 avaliações, 9 países, quarenta anos): CCTV reduz crime em 13 % no agregado, 37 % em estacionamentos, zero em crime violento, e nada sem monitoramento ativo. CESeC sobre o Smart Sampa (único estudo com grupo de controle): nenhum efeito mensurável sobre furtos, roubos, homicídios ou produtividade policial. Flock: "um milhão de crimes por ano" autodeclarados, sem contrafactual. Gabriel: 802 indiciados, autodeclarados.

Enquanto isso o mesmo ano da Met Police é "0,0003 % de erro" (sobre rostos escaneados), "0,48 %" (sobre alertas) ou "8 em 10 falsos positivos são negros" (sobre pessoas abordadas). A Prefeitura de São Paulo publica "99,5 % de assertividade" sem dizer o que divide por quê. Metade das prisões do Smart Sampa é "outros", e mais de 90 % disso é pensão alimentícia: o programa vendido para proteger mulheres prende sobretudo devedores de pensão.

### 2.5 A infraestrutura é fungível: comprada para um fim, usada para outro

É o mecanismo mais repetido em todos os dossiês, em três países. Câmeras de placa holandesas para cobrar imposto; a rede da Flock, vendida contra roubo de carro, usada para procurar uma mulher que abortou, para o ICE "pela porta lateral" (mais de 4 mil buscas) e por policiais contra ex-parceiras (26 casos); a Abin usando o FirstMile contra jornalistas e ministros do STF (60.734 consultas); a Gabriel, que "não faz reconhecimento facial", entregando o vídeo ao Smart Sampa, que faz; o Córtex, onde 55 mil usuários consultam sem justificar e um usuário fez um milhão de consultas num dia. A Clearview, condenada em quatro países, cresceu depois: 3 bilhões de rostos em 2020, mais de 60 bilhões no contrato com a CBP em 2026.

A lição: **não existe vigilância "só para isso"**. O limite de finalidade é a primeira coisa que cai, porque o banco já existe e a busca custa zero.

### 2.6 A pessoa nunca é parte: consentimento como ficção

No mercado de dados (06), sete em nove corretores compram uns dos outros, e a origem de um dado é irreconstituível. O app pede o GPS, o SDK revende, o agregador revende, o corretor revende, o governo compra para não pedir mandado (Fog Reveal: US$ 7.500 por ano por buscas equivalentes a geofence warrant; ICE: 1,2 milhão de buscas na LexisNexis em sete meses). A Serasa vendia CPF, nome, endereço, três telefones, sexo e classe social de 150 milhões de brasileiros a R$ 0,98, com base legal de "proteção ao crédito". O vazamento de 2021 (223 milhões de CPFs) não produziu origem apurada, sanção nem indenização em cinco anos; em 2026, 251 milhões de registros custam US$ 500.

Isso conversa com a ViaQuatro (07): condenada a R$ 500 mil não por ler emoções, mas porque os usuários "não foram advertidos nem comunicados, antes ou depois". O que a lei e os tribunais punem, quando punem, é **a ausência de aviso**, não a câmera. É o que torna a placa na entrada da festa um gesto político, e não só jurídico.

### 2.7 A sanção não muda o modelo; a impunidade é assimétrica

Clearview: € 90,5 milhões em multas definitivas na União Europeia, zero pago, "não temos presença na UE". Facebook: multa de US$ 5 bilhões e a ação sobe US$ 10,4 bilhões no mesmo dia. ANPD: uma multa em toda a existência (2023), um clube intimado em 15 meses, sem diretor nomeado. Gabriel: cinco multas por ocupar praça pública, nenhum processo judicial. Smart Sampa: indenizações de R$ 5 mil por "detenção de curtíssima duração" ou nada por "mero aborrecimento".

Do outro lado, a mesma lei pede a uma instalação artística a placa, o prazo de retenção e o canal de exclusão que não pede, na prática, ao Estado nem às 30 mil câmeras privadas conectadas ao Smart Sampa. **A assimetria é o argumento da obra.**

### 2.8 Normalização: cada passo torna o próximo invisível

A aceitação de vigiar o parceiro "em certas circunstâncias" subiu de 17 % para 38 % em três anos; o Brasil é o segundo país do mundo em stalkerware detectado; os fundadores da Gabriel dizem em voz alta que "a maioria dos brasileiros está disposta a trocar privacidade por segurança" e que a China é "lugar de aprendizado". Sair é mais difícil do que entrar (Evanston mandou desligar 19 câmeras e a Flock reinstalou; Denver trocou Flock por Axon). Quanto mais normal, menos quem é atingido é ouvido.

---

## 3. O Brasil, especificamente

1. **Não há lei.** O reconhecimento facial policial opera sem norma que defina erro, retenção, auditoria ou contestação, e a LGPD exclui a segurança pública (art. 4º, III) sem que a lei específica prometida tenha sido aprovada. A ANPD regulou escolas, não polícias.
2. **A escala é de centenas de milhões:** R$ 588 milhões em cinco anos em São Paulo, R$ 665 milhões na Bahia, 376 projetos ativos e 83 milhões de pessoas ao alcance (CESeC/DPU, totais a conferir).
3. **A integração público-privada é o vetor.** Gabriel, condomínios, "segurança colaborativa": a prefeitura recebe imagens de câmeras que não escolheu e admite por LAI que não tem acesso ao código nem aos modelos que comprou.
4. **Os dados vazam nos dois sentidos:** 181 senhas, 6 mil agentes e 58 mil câmeras do Smart Sampa expostos por onze meses; credenciais do Córtex vendidas; 70 milhões de CPFs consultados por chaves do governo do Rio.
5. **Nenhum estado publica falsos positivos**, e a cor fica em branco. A opacidade é verificável pela ausência de dados.
6. **A vigilância de movimentos sociais é documentada:** Abin em 2013, PM infiltrado em 2014, "Abin paralela" em 2019-21.

---

## 4. O que isso significa para a obra

**O argumento artístico.** A obra não precisa dizer que ser visto é ruim; precisa fazer a pessoa sentir o que a pesquisa mostra: que o sistema já tem uma versão dela (a pessoa anterior, os cacos, os palpites de idade e humor), que essa versão foi feita sem perguntar, que ela circula (a próxima pessoa vai ver você), e que quando o sistema erra ("parece 40 anos", "parece irritado") não há a quem reclamar. As frases nas telas devem vir dos mecanismos da seção 2, não de slogans: o denominador escolhido, o mandado vencido, o "z" no sobrenome, o R$ 0,98, o "our part is over".

**O que a obra pode usar com força** (todos com fonte nos dossiês): Penney, Ravid, NIST, Piza, Met 2024-25, relatórios de transparência de SP, ViaQuatro, Serasa R$ 0,98, Flock/aborto, Clearview 60 bilhões e zero pago, Córtex 55 mil usuários, Paraná 1 milhão de alunos.

**O que a obra não pode fazer** (dossiê 07, forte): identificar pessoas, guardar template biométrico, classificar por raça, compartilhar ou reaproveitar as imagens fora da obra. O que ela deve fazer: placa completa na entrada (quem controla, o que capta, para quê, que não há reconhecimento facial, por quanto tempo guarda, como pedir exclusão), retenção curta e declarada, canal de exclusão. Inferir idade e humor de forma anônima e efêmera, sem gravar o atributo ligado a uma pessoa identificável, fica no regime leve; a placa deve dizer que esses palpites existem.

---

## 5. Conclusões

1. **A vigilância muda comportamento sem reprimir ninguém, e cala primeiro quem discorda.** Forte: três métodos independentes convergem.
2. **Ser monitorado aumenta estresse e não melhora desempenho.** Forte no trabalho (duas meta-análises, 23 mil pessoas); transferência para a rua por analogia.
3. **O reconhecimento facial erra mais com rostos negros, asiáticos, indígenas, femininos, jovens e idosos, e o viés reaparece na rua.** Forte no laboratório; média-forte na rua, porque o Estado esconde o denominador.
4. **A maior parte das abordagens erradas vem de cadastro sujo, não de rosto; a câmera dá velocidade e arma a um erro burocrático, e ninguém responde por ele.** Forte (números oficiais de SP, casos nomeados em quatro países).
5. **Para quem é abordado, "liberado após documentos" é uma detenção.** Forte quanto aos fatos; interpretação sobre o que conta como dano.
6. **Câmeras reduzem crime pouco, só em estacionamentos e com monitoramento ativo; reconhecimento facial ao vivo rende quase nada por rosto escaneado.** Forte (revisões sistemáticas de quarenta anos; único estudo controlado no Brasil sem efeito).
7. **Quem vigia escolhe o denominador.** Forte: é aritmética sobre números publicados pelas próprias polícias.
8. **Toda infraestrutura de vigilância é usada para outro fim que não o declarado.** Forte: documentado em três países com documentos oficiais.
9. **A pessoa nunca é parte da cadeia de dados; o consentimento é ficção e o governo compra para não pedir mandado.** Forte (FTC, TJDFT, EFF).
10. **As sanções não mudam o modelo e a impunidade é assimétrica: a empresa estrangeira não paga, o Estado não presta contas, a vítima recebe R$ 5 mil.** Forte.
11. **O que a lei pune, quando pune, é a ausência de aviso, não a câmera; a obra deve fazer exatamente o que o Estado não faz.** Forte (ViaQuatro, Hering, ANPD/Paraná, texto da LGPD).
12. **A normalização está medida, e cada passo torna o próximo invisível.** Média (pesquisas de opinião, um fornecedor de antivírus), direção clara.

---

## 6. Lacunas que atravessam os dossiês

- Nenhum estudo quantitativo sobre queda de participação em protestos atribuída a câmeras (só Hong Kong, qualitativo).
- Nenhum estado brasileiro publica falsos positivos; os totais nacionais (CESeC 525 projetos/R$ 2,65 bi vs. DPU 376/R$ 160 mi) divergem e estão marcados "a conferir".
- Sem medição independente da Clearview no uso policial real; contagem de prisões erradas nos EUA (14–16) é piso.
- Páginas que bloquearam leitura (NYT, ICO, CNIL, Intercept em parte, 404 Media integral, Piauí, Band): cada dossiê lista as suas e o que outra fonte confirma.
- Dados que **não devem** ir para as telas por falta de confirmação: "oferta de 6 anos" a Parks, "Mosaico/700 temas" da Abin, uso do Córtex pelo PCC, "70 bilhões" da Clearview (só Wikipedia), números antigos da Comparitech.

## 7. Próximo passo para as frases

As 123 frases antigas e as 42 selecionadas foram descartadas. O novo banco sai da seção 2 deste arquivo e das "Frases candidatas" de cada dossiê (cerca de 110 frases novas, cada uma com fonte), organizadas por mecanismo (olhar, erro amplificado, quem paga, denominador, desvio de fim, cadeia de dados, impunidade, normalização). Isso é a próxima entrega da pesquisa, depois que o usuário ler esta síntese.
