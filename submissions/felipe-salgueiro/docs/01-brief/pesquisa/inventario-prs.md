<!-- Snapshot da nota Inventario das PRs; 23/09/2026. PARCIAL; não representa auditoria individual concluída. -->


# G4 AI Master — inventário das PRs (PARCIAL — consolidação por blocos)

## Método e legenda

Corte: 2026-09-23T15:54:37Z (UTC). Fonte por linha: `GET /pulls?state=all` e `refs/pull/<n>/head` do repositório público. `case` é conteúdo/documentação quando presente; `indet` não foi forçado. `nao-submissao` significa ausência de pasta `submissions/` no head, não juízo sobre a pessoa. `Estado` é GitHub; `closed` não significa rejeição e `open` não significa aprovação. `head` é SHA abreviado. A coluna artefatos é inventário estático por extensão; não prova que código executa. Profundidade: **D** = árvore + README/process-log/documentação textual inspecionados; **E** = árvore somente, por ausência/ambiguidade estrutural. Comentários/reviews públicos foram consultados quando existentes.

**Limitação explícita:** a cobertura do corpus é integral (146 heads e metadados), mas várias linhas abaixo agrupam PRs para caber nesta primeira publicação. Falta expandir esses grupos para uma linha por PR, com URL e campos individuais de diferencial, testes/validação, limitação e profundidade. Não usar este arquivo como inventário final individualizado.

| PR | Autor público | Estado | Case | Head | Prof. | Artefatos / observação |
|---|---|---|---|---|---|---|
| #1 | atlassian-compass[bot] | open | nao-submissao | c1c178e0ba | E | 9 arquivos; bot/configuração |
| #2 | rsperle | closed | 001+002 | ab99a353b6 | D | 2 CSV, 3 HTML, 5 Python |
| #3 | BarryBits | open | 003 | c682472d15 | D | 10 CSV, 6 JS, 7 JSX; app e screenshots |
| #4 | Lenoncardozo | open | 004 | 63dece7c38 | D | CSV, HTML, JS, Python; validação e log |
| #5 | juniorpagedown | closed | 001+002 | ec279a52d6 | D | notebook, Python, JSX |
| #6 | agenciablattai | open | 003 | a4c310163b | D | Python |
| #7 | gscopetti | open | 003 | 33efc7b0a3 | D | CSV, HTML, JS, TS/TSX; estrutura atípica |
| #8/#9 | brunocamparadiniz | closed/open | 003 | 501bc1371d / 11da703913 | D | reenvio; TS/TSX, CSV, HTML |
| #10 | marcelinhonunes | open | 001 | 534da17712 | D | CSV, HTML, Python |
| #11 | Typebotkings | open | 002 | 5c7789364b | D | CSV, PDF, Python; comentário de correção estrutural |
| #12 | mirandaaa36 | open | 001 | b40e9b37b2 | D | notebook |
| #13 | eduramofo | open | 003 | 60af249a4b | D | CSV, Python |
| #14 | VinicusVaccari | open | 003 | 8eb058d482 | D | CSV, HTML, JS |
| #15 | renygrando | open | 002 | 62fd81e1d9 | D | PDF, JS, TS/TSX; estrutura atípica |
| #16 | Mateus-Nogueira-GT | open | 003 | db6dcb9482 | D | CSV, HTML, JS, Python |
| #17 | olandare | open | 004 | e7f855684a | D | Python, TS/TSX; feedback cita testes estatísticos |
| #18 | jeskgrb | open | 003 | 2facafaadc | D | CSV, Python |
| #19 | jurandircln | closed | nao-submissao | e8d260b541 | E | 63 arquivos, sem pasta submissions |
| #20 | betitanx | open | 002 | 94fe0f7601 | D | notebook, Python, TS/TSX |
| #21–#25 | DanielSchkolnick; Mpetrato; felipecalgaro; kabutaro-design; oetnegro | open/open/closed/open/open | 003 | 7a47981510…2fe1bf3227 | D | cinco entregas de lead scoring; stack varia Python/JS/TS/TSX |
| #26–#27 | fer-paes; gferreirauni | open/open | 002 | c94da04ab3 / 955852f95d | D | front-end grande; Python |
| #28/#29 | cordeirodyego50-debug | open/closed | 001 / indet | 30ac2bdad9 / 858d0ceafb | D | #29 aparenta follow-up de process log |
| #30 | wendelcastro | open | 004 | 1e139eb6f2 | D | Python |
| #31–#33 | pedromargon21; chiquetom; Jefdfbr | open/closed/open | 003/002/003 | aa2b300d1b…f4fe19d6ab | D | app TS/TSX; notebook/PDF; Python |
| #34 | markespro | open | nao-submissao | 95f06648e4 | E | sem pasta submissions |
| #35–#40 | LucasReisVillasBoas; 1uc4sm4theus; Bubex; leopas; theoggarcia7-source; lucascliberato | open | 001/004/001+002+003+004/002+003/001/001 | fece8952a1…cd3caf5ad4 | D | notebook/Python e entregas multi-case; #39 tem trace e screenshots |
| #41/#49 | feelipebelisario-oss | closed/open | 003 | 48f7241efb / a01332987c | D | reenvio; #41 incluía dependências vendorizadas, #49 é versão enxuta |
| #42–#47 | almeidavictorvk; viniciuscury; vfxcodes; maripeixotoc; lucasoriani; nickolasdaniel-gif | open/open/open/closed/open/open | 003/002/003/003/001/003 | 2f292c7691…0cc7756072 | D | Python, TS/TSX, HTML/PDF; comentários citam correções de evidência |
| #48 | joaopedrotesta01-cell | open | 003 | 86c3400240 | D | árvore muito grande; CSV/JS/Python/TS; inspeção textual, sem execução |
| #50 | mpobzl | open | nao-submissao | ef4eb50e6b | E | sem pasta submissions; #58 é entrega 003 do mesmo login |
| #51–#54 | THEDELFIM; brunoogp; luis-braghin; AluisioJr | open | 003/002/003/001 | e0549076c4…7291596159 | D | PDFs, Python e front-end |
| #55 | vepisco | open | nao-submissao | ea6bf5b0a7 | E | sem pasta submissions |
| #56–#61 | pedrohsonda-AImaster; G4bsudr3; mpobzl; gse77e; duartebruno496; juanordonezn | open/open/open/closed/open/open | 003 | f79495212f…dc504e959a | D | seis lead scorers; #59 reenvio de #77 |
| #62/#78 | gustavoptavares | closed/open | 001 | 2bcc94094f / 7ae675c8be | D | reenvio; CSV/PDF/Python |
| #63, #65, #67, #69 | jmarinssousa-source; guipardindev; rwpl12; aehirota | open/closed/closed/closed | 003 | 5603237073…12ce7c5519 | D | #65 refeito em #86; PDFs/Python |
| #68 | pedrohsnd1412 | open | 002 | 07a9e91d73 | D | Python, TS/TSX |
| #70 | jonatamarinssousa-lab | open | 003 | 314c6fde8c | D | CSV, HTML, PDF, Python, TS/TSX |
| #71 | jeanflp | open | indet | fe37402d61 | D | Python, TS/TSX; conteúdo não identificou case com segurança |
| #72–#75 | beatrizdantasstudy-spec; spinellidaniel; leandroruel; OficinaMartech | open | 004/001/003/003 | 825c4eaebd…e08a556826 | D | HTML; notebook/Python; JS/JSX |
| #76 | pedlima11 | open | nao-submissao | 9b118e67e3 | E | sem pasta submissions |
| #77 | gse77e | open | 003 | 3f21a3dec9 | D | reenvio do login de #59 |
| #79/#80 | JoaoCouto1; RGGPiva | open | nao-submissao | ded0fbabfa / 64e0268c6f | E | sem pasta submissions |
| #81–#90 | saraandrade0; marcossssantos1; Kadugarcia1; olucasdamata; gabrieloliveiradt; guipardindev; generalrodolfao; lucasmstein; jeanjeferson; Arturrochaa | open | 002/003/001/003/003/003/001/003/003/001 | 8da1a2b12d…00a0f85770 | D | dez entregas; #84 tem correção pública de join; #86 reenvio |
| #91–#100 | FelipeFreire23; mathmoraisdev; Paulinhojr; LucioPinto; gmcleffe; PortamentoDesign; Gattiboni; Jaypi10; fernandofreitas03; tsapuppo | open | 001+004/003/001/003/003/003/002/001/002/002 | 06d40c69ae…7f935d8fba | D | Python, notebooks, HTML, TS/TSX; #97 log atualizado por comentário |
| #101–#108 | joaolucasmarques2503-dotcom; Bruno-Milford; dradicchi; afonsoPablo; RafaSanches89; acarloshenrique; pedrotgon; xXThiagoReisXx | open/open/closed/closed/open/open/open/open | 002/001/003/002/002+003/001+002/002/001 | cec0ce525f…575845ad93 | D | PDFs, Python, HTML; #106 é multi-case grande |
| #109 | eduardohasson | open | nao-submissao | f0e5902cf8 | E | sem pasta submissions |
| #110–#118 | ga987123; josenascimento1; fagundesjv; contatocarlospersike-commits; allysonassuncao; lucas3322; MikaelAllef; RojasAuditto; cleitoneugenio | open | 003/001/003/003/003/003/003/001+003/002 | 48b8bd1148…ea34c4e0c8 | D | Python, JS, TS/TSX; #117 multi-case |
| #119/#120 | adailtonmontinegro | closed/open | 001 | e59b242692 / ad7f3a4f7d | D | reenvio; CSV/PDF/Python |
| #121–#124 | filipefagundes; AlexandreQ-creator; coniose; julyanmatheus2002 | open | 002/001/001/003 | 42350e4de3…5f53dcd1ac | D | Python, TS/TSX, HTML |
| #125 | AlexandreQ-creator | open | nao-submissao | 1ebd9c45d3 | E | docs/ajustes; #122 é a entrega |
| #126–#138 | fabiobarboza7; Gor0d; gvaRenan; GuilhermeF01; geoffreyporto; fernandowilliam; rafaelreis-r5; RicardoBarao; StartIACode; douglasfrannca; RomarioDelphin; marcusbarbosa92; RobMartello | open | 002/002/001/003/001+002/002/002/002/002/004/003/003/002 | 879cbb55b8…01dcc499de | D | 13 entregas; Python e front-end; #130 multi-case |
| #139 | adrianoaguiar | open | nao-submissao | a1ce838d86 | E | 1.067 arquivos, sem pasta submissions |
| #140–#147 | luisroquette; luisroquette; dspinillo; candidozara; rodrigo-christo; luisroquette; Emansecio; luisroquette | closed/closed/open/open/open/closed/open/open | 003/002/002/001/003/004/003/001 | 5a7d3a8719…779a1990a7 | D | quatro cases do mesmo login (#140/#141/#145/#147), mais quatro entregas distintas |

## Limites de leitura por linha

Cada head teve árvore de arquivos inspecionada e as PRs estruturadas tiveram README, process log e documentação textual de entrega lidos quando presentes. Não foi feito code review linha a linha de todos os fontes, nem execução, instalação, validação de URL externa ou teste de dados. Assim, a coluna de stack/artefatos é observacional; “testes”, “custo”, “métrica” e “funcionalidade” apenas contam como demonstrados quando há artefato estático correspondente, e ainda não como execução independente.
