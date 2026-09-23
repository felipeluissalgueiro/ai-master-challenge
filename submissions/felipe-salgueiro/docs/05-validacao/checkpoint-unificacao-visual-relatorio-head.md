# Checkpoint — relatório do Head e padrão visual unificado

Data: 23/09/2026. Execução exclusiva na worktree
`/home/felipe/Work/worktrees/g4-ai-master-felipe-20260923-data`, branch
`analysis/felipe-salgueiro-data`. Não houve stage, commit, push, merge, PR ou
deploy. O SQLite de evidência não foi alterado.

Este checkpoint substitui apenas os hashes de artefatos apresentados em
`checkpoint-relatorio-executivo.md` e `checkpoint-prototipo-html.md`; não
reescreve o histórico desses checkpoints.

## Pedido e decisões de Felipe

Felipe corrigiu o objetivo do relatório: ele é a página usada pelo Head de
Marketing, e não um teste visual. A entrega deve responder com dados a três
decisões centrais do Challenge 004:

1. o que gera engajamento de verdade;
2. se vale patrocinar influenciadores;
3. qual estratégia de conteúdo adotar.

O relatório precisava ainda provar os números e sua origem, trazer dashboards
visuais e números destacados e adotar o padrão visual definido pela Sofia. O
visualizador Ouro deveria ser preservado como artefato separado, mas receber o
mesmo sistema visual e navegação cruzada.

## Referências conferidas

- enunciado canônico do Challenge 004 no fork do GitHub;
- resumo de Sofia em
  `Obsidian_Vaults_Pessoal/Sessoes/Logs/2026-09-23 sofia-ux-parecer-g4-challenge-004.md`;
- parecer UX completo de Sofia no snapshot `7e7f4fd`, arquivo
  `docs/03-rfc/parecer-ux-sofia-g4-challenge004-20260923.md`;
- padrão Astryx em `times/dev/sofia/docs/astryx-ui-standard.md`.

O sistema aplicado usa navy, coral, branco, tipografia sans forte, hierarquia
executiva, contraste alto, abas consistentes e leitura responsiva. As páginas
declaram que são artefatos do Challenge 004 e não produto oficial ou afiliação
com o G4 Educação.

## Alterações

### Relatório executivo

- reorganização explícita nos três pilares do desafio;
- headline e resumo dirigidos ao gestor;
- painel visual com quatro KPIs destacados;
- quatro dot plots com plataforma, formato, categoria e faixa de seguidores;
- escala visual comum baseada no P25–P75 global, evitando ampliar diferenças de
  centésimos;
- painel patrocinado versus não patrocinado segundo a flag, com medianas, `n` e
  divisão das 60 células comparáveis;
- painel de audiência com amplitude por rótulo predominante e aviso de
  instabilidade contextual;
- plano de estratégia em três passos: hipótese comercial, conteúdo
  instrumentado e escala condicionada;
- oito respostas com prova visível: número, amostra, tabela, cálculo e ID de
  evidência;
- apêndice técnico preservado para IQR, correlações, hashes e tabelas;
- status alterado de preliminar para relatório executivo do Head de Marketing.

### Visualizador Ouro

- aplicação do mesmo sistema visual G4/Sofia;
- abas entre relatório executivo e exploração de dados;
- tipografia sans, hierarquia, cards e tabelas em navy/coral/branco;
- correção da nota de creators: `creator_id` é válido; `creator_name` é
  inconsistente; ranking ficou fora por escopo, não pela regra histórica de
  elegibilidade.

## Arquivos e hashes finais

| Arquivo | SHA-256 |
|---|---|
| `solution/reports/README.md` | `df2f6634c0ce2ff628670b435291a71c634c2dc492e5b82036bb182b3479cc44` |
| `solution/reports/generate.py` | `45add35927b9f0df81e7baaff7b9caf6383628eb3b6fc89ff9c85c17e8775215` |
| `solution/reports/evidence.json` | `e4a0b622450b1dbd089bac8e2c910772a817a028fb7fca2f819b56a7eeda6c4f` |
| `solution/reports/performance-strategy.html` | `57a2cbd5837499b353d53668799e52e7efc6eec1863ad8557b131f244954b165` |
| `solution/reports/manifest.json` | `f9bbdd45ca4b955189f15ebe6d4833da41ab99edff2c0e43489253ad3f9862cb` |
| `solution/prototype/README.md` | `425ca5fae8afa7ee1db105fb3d4561be036082781a5475a8354447572aa2614a` |
| `solution/prototype/generate.py` | `8c27fa297ad0efafefb2ed9e60b246e19d8e63a9f4dbdbd59f43cc9d6e94a91c` |
| `solution/prototype/index.html` | `3e4dbd2812e83d91a1a5f2aec5968235e84e14a8b00992c1b7ac4bbf329f3b28` |
| `solution/data/evidence/social_media_analysis.sqlite` | `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad` |

Tamanhos: relatório HTML 56.694 bytes; JSON de evidência 294.498 bytes;
manifesto 2.056 bytes; visualizador 94.741 bytes.

## Comandos executados

Da raiz `submissions/felipe-salgueiro/`:

```bash
python3 -m py_compile solution/reports/generate.py solution/prototype/generate.py
python3 solution/reports/generate.py
python3 solution/prototype/generate.py
sha256sum solution/reports/performance-strategy.html \
  solution/reports/evidence.json solution/reports/manifest.json \
  solution/prototype/index.html \
  solution/data/evidence/social_media_analysis.sqlite
```

Foram executadas validações com `html.parser`, `node --check`, `rg`,
`sha256sum`, `stat`, Chromium headless e servidor HTTP local. A segunda geração
dos dois HTMLs e das evidências produziu os mesmos hashes.

## Resultado das verificações

- SQLite aberto com URI `mode=ro`, `PRAGMA query_only=1` e
  `integrity_check=ok`;
- 52.214 posts consumidos; 731 dias cobertos; zero posts com views ou
  interações totais iguais a zero;
- oito respostas `q1` a `q8`, 16 provas numéricas visíveis, oito faixas de
  rastreabilidade, quatro gráficos segmentados e três passos de estratégia;
- HTML das duas páginas parseável;
- os três blocos `application/json` do visualizador são JSON válido; o único
  bloco JavaScript executável é válido em `node --check`;
- links relativos relatório ↔ visualizador e links para JSON, manifesto e
  README resolvidos;
- HTTP local: relatório `200`, visualizador `200`, JSON de evidência `200`;
- desktop e mobile renderizaram sem quebra estrutural observada;
- expressões rejeitadas (`preliminar`, frase antiga sobre comparações,
  `priorizar Instagram`, `manter portfólio`) ausentes;
- nenhum asset externo, dependência nova, backend, login, LLM ou deploy;
- hash do SQLite permaneceu inalterado.

## Erros e correções

1. A primeira chamada do patch amplo do visualizador falhou porque esperava
   duas tags `</style>`; nenhuma alteração parcial foi aplicada. O patch foi
   dividido em blocos menores e aplicado com sucesso.
2. O primeiro teste HTTP retornou `404` porque a porta `8765` não estava
   servindo a raiz esperada. O teste foi repetido isoladamente na porta `18765`
   com retry de inicialização e retornou `200` nos três artefatos.
3. Foram geradas capturas temporárias com Chromium somente para QA visual,
   apesar da orientação anterior de não produzir screenshots. Os PNGs foram
   removidos imediatamente, não fazem parte da entrega e não foram publicados.
4. `py_compile` criou diretórios `__pycache__`; eles foram removidos após a
   validação.
5. Na revisão de integração, Lia identificou que o contrato JSON chamava a taxa
   `interaction_per_view_pct` de `percentage_points`. A taxa foi corrigida para
   `unit=percent`; foi acrescentado `difference_unit=percentage_points` para
   deltas entre taxas. O relatório não mudou visualmente, o JSON e o manifesto
   foram regenerados e o teste de determinismo passou novamente.
6. A primeira checagem JavaScript na worktree de integração concatenou também
   os três blocos `application/json` e falhou. Isso não era um erro do produto.
   A validação correta separou os três JSONs, aprovados com `json.loads`, e
   enviou somente o bloco executável que contém `use strict` ao
   `node --check`, que retornou código zero.

## Limites preservados

- O dataset é simulado e não é benchmark externo.
- Rankings são descritivos e não provam equivalência ou causalidade.
- ROI, alcance, custo, conversão e receita não são calculáveis com a fonte.
- Retenção após 3s, ponto de 50%, conclusão e CTA aparecem somente como campos
  propostos para instrumentação futura, nunca como achados da base.
- A política de teste e escala é uma recomendação de governança, não um
  threshold descoberto.
- Lia permanece responsável por revisar, copiar os arquivos para o fork,
  registrar no workflow e fazer commit/push. Nenhuma publicação ocorreu nesta
  worktree.
