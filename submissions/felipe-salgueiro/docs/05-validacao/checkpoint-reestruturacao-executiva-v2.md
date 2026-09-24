# Checkpoint — reestruturação executiva do relatório e onboarding do explorador

Data: 23/09/2026. Execução exclusiva na worktree
`/home/felipe/Work/worktrees/g4-ai-master-felipe-20260923-data`, branch
`analysis/felipe-salgueiro-data`. Não houve stage, commit, push, merge, PR ou
deploy. Lia permanece responsável pela integração e publicação no fork.

## Pedido e decisão de Felipe

Depois de aprovar a identidade visual navy/dourado/Manrope, Felipe autorizou a
reestruturação. O relatório deveria deixar de parecer uma landing page e passar
a funcionar como briefing para o Head de Marketing. O fluxo principal deveria
responder em linguagem comum aos três pilares do desafio:

1. o que gera engajamento de verdade;
2. se vale a pena patrocinar influenciadores;
3. qual estratégia de conteúdo adotar.

O explorador deveria explicar claramente que é a interface para navegar e
comprovar as tabelas Ouro do SQLite, incluindo instruções e dicionário dos
recortes. A comprovação técnica não deveria desaparecer; deveria sair do fluxo
principal e permanecer no apêndice, no JSON de evidência e no explorador.

## Referências aplicadas

- parecer da Maria, Head de Marketing, solicitado por Felipe;
- identidade oficial observada no CSS público de `https://g4business.com/`:
  navy `#001F35`, azul `#184560`, dourado `#B9915B`, texto `#031A26`, fundo
  `#F5F4F3` e tipografia Manrope;
- números calculados do SQLite publicado, sempre aberto em modo somente leitura.

## Alterações no relatório executivo

- cabeçalho compacto com a resposta central, sem linguagem de landing page;
- resumo com três decisões para conteúdo, patrocínio e próximo ciclo;
- números técnicos traduzidos para interações adicionais a cada 10 mil views;
- quatro indicadores gerenciais: maior distância entre grupos, placar das 60
  comparações, instabilidade em 14 de 15 combinações e ROI não calculável;
- gráficos simplificados com escala de zero a duas interações adicionais por 10
  mil views para plataforma, formato, categoria e tamanho do creator;
- painel de audiência com a mesma unidade humana;
- resposta direta aos três pilares e estratégia em cinco passos;
- decisões possíveis separadas de limitações e campos ausentes;
- cobertura das oito perguntas preservada em bloco recolhível;
- `n`, mediana, IQR, rho, nomes SQL, hashes e detalhes de amostra mantidos no
  apêndice e no explorador, não no fluxo principal.

## Alterações no explorador

- título explícito: explorador do banco SQLite e das tabelas Ouro;
- aviso de que a página comprova o relatório e não altera o banco;
- guia de uso em quatro passos;
- instrução de leitura dos pontos, faixas e sobreposição;
- dicionário de plataforma, formato, categoria, tamanho do creator, audiência,
  patrocínio e métrica;
- títulos e colunas traduzidos para linguagem mais clara;
- navegação de volta ao relatório executivo.

## Evidência reproduzível

Foi acrescentado a `evidence.json` o bloco `executive_translation`, calculado
pelo gerador, com fórmula, unidade, valores e caminhos de origem. A tradução é:

```text
diferença em pontos percentuais × 100
= interações adicionais a cada 10 mil visualizações
```

Valores resultantes:

- plataforma: `1.567600220850096`;
- formato: `1.6698027146563987`;
- categoria: `0.5912995394428577`;
- tamanho do creator: `1.6470999274876164`;
- idade predominante: `0.5293289511495658`;
- gênero predominante: `1.231699417177623`;
- localização principal: `1.7584613665505344`;
- diferença típica de patrocínio: `0.24007317714325183`;
- comparações: 33 patrocinadas acima, 27 sem marcação acima;
- padrão misto: 14 de 15 combinações.

## Comandos e verificações executados

```bash
python -m py_compile \
  submissions/felipe-salgueiro/solution/reports/generate.py \
  submissions/felipe-salgueiro/solution/prototype/generate.py
python submissions/felipe-salgueiro/solution/reports/generate.py
python submissions/felipe-salgueiro/solution/prototype/generate.py
sha256sum submissions/felipe-salgueiro/solution/data/evidence/social_media_analysis.sqlite
```

Também foi executada validação estrutural com `html.parser`: nenhum ID duplicado
e nenhum link local ausente nas duas páginas. Os placeholders foram procurados
com `rg`; nenhum token não resolvido permaneceu. O relatório e o explorador
foram abertos localmente no Brave para revisão de Felipe.

Resultado do acesso ao SQLite:

- `mode=ro`;
- `PRAGMA query_only=1`;
- `integrity_check=ok`;
- 52.214 linhas consumidas;
- hash antes e depois idêntico:
  `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.

## Arquivos e hashes

| Arquivo | SHA-256 |
|---|---|
| `solution/reports/README.md` | `737111c2d132fb311679fd424516f23f54ab5c8b3e761bbbf873a3ba000a5389` |
| `solution/reports/generate.py` | `59b1f518a50fab1a1bfc1c678f158217722dd9344ffd33a0f39e7721f5fa575a` |
| `solution/reports/evidence.json` | `de0502d33bec4b09fe6970686196f4c83c1fe484b659c40fc607b75d6d1ddf1d` |
| `solution/reports/performance-strategy.html` | `c16c4dd2f895646f7ae4a6e4e55962f54717a7e33550e1bb215e9419889f8daf` |
| `solution/reports/manifest.json` | `9a57d689e338fa837ef2aa27cc1cbda066bfe220fc0e544719d9af0ab349bec3` |
| `solution/prototype/README.md` | `afba281ad65d6f3ea4d08d5b4521027cbe22c66d7b5578de3b8bc173d4e5e023` |
| `solution/prototype/generate.py` | `7c5389ab25ba2aed5ea3164e04f711e62cd611441f22912d70d57749aa9bfa8a` |
| `solution/prototype/index.html` | `ff25203423f8f9bc1b71d90986a3ea57eed2545b45582a054ad5e0f1f519a708` |
| `solution/assets/fonts/manrope-latin-variable.woff2.b64` | `adab05b4f4899a536269273ea0fe507cf735547fa72f26a4d118cbac423fbb67` |
| `solution/data/evidence/social_media_analysis.sqlite` | `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad` |

## Limites preservados

- dataset simulado, não benchmark de mercado;
- diferenças descritivas não são efeitos causais;
- ROI, frequência, retenção, melhor gancho e melhor CTA não foram inventados;
- política de teste é recomendação de governança, não threshold descoberto;
- nenhum arquivo da worktree de Lia foi alterado.
