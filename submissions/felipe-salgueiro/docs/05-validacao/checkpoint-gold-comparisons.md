# Checkpoint — Gold descritiva e correlações

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e decisão

Felipe pediu correlações para indicar engajamento e comparações entre
patrocinado e não patrocinado, sempre segmentadas antes de inferir. Este bloco
produz medianas, IQR, tamanhos de amostra e Spearman. Não calcula causalidade,
p-valor, ROI ou modelo preditivo.

## Alteração

Criado `solution/analysis/build_gold_comparisons.py`, que reconstrói:

- `gold_segment_summaries`: plataforma, formato, categoria, quartil de
  seguidores por post e rótulos de audiência, separados pela flag.
- `gold_sponsorship_comparisons`: 60 células plataforma × categoria × quartil.
- `gold_numeric_correlations`: 45 pares de Spearman.

SHA-256:
`dfd1b042e98c81a9895fc978420936937d17297daa4f2abcdeef984fb871268b`.

## Comando e teste

```bash
python submissions/felipe-salgueiro/solution/analysis/build_gold_comparisons.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Depois foram consultadas amplitudes por dimensão, maiores diferenças entre
células, correlações brutas, paridade, `PRAGMA integrity_check` e hashes.

## Resultado observado

### Geral

| Grupo | n | Mediana views | Mediana interações | Mediana interações/views | Mediana interações/seguidores |
|---|---:|---:|---:|---:|---:|
| Não patrocinado segundo flag | 29.900 | 10.100 | 2.010 | 19,8977% | 0,4033% |
| Patrocinado | 22.314 | 10.100 | 2.010 | 19,9014% | 0,4035% |

### Células comparáveis

- 60 células plataforma × categoria × quartil.
- Cada lado contém de 191 a 668 posts; mediana 447.
- Diferença patrocinado menos não patrocinado em interações/views:
  - mínimo -0,1296 ponto percentual;
  - mediana +0,0024;
  - máximo +0,1125;
  - mediana absoluta 0,0282;
  - 33 células positivas, 27 negativas, nenhuma exatamente zero.
- A amplitude entre medianas de todos os rótulos dentro de cada dimensão é
  pequena: 0,0201–0,0386 ponto percentual.

### Correlações de Spearman selecionadas

| Par | rho |
|---|---:|
| Patrocínio × views | 0,0010 |
| Patrocínio × interações totais | 0,0012 |
| Patrocínio × interações/views | 0,0007 |
| Seguidores × interações/seguidores | -0,9991 |
| Seguidores × views/seguidores | -0,9998 |
| Interações totais × interações/views | 0,9070 |
| Views × interações/views | -0,3916 |
| Likes × interações totais | 0,8570 |
| Views × interações totais | -0,0032 |

## Conclusão

Não existe separação descritiva consistente de patrocínio. As direções se
alternam entre as células e a flag é praticamente não correlacionada às
métricas. As razões por seguidores são quase inteiramente determinadas pelo
denominador; não devem ser usadas como “engajamento real”.

Como a fonte é sintética e não tem custo, alcance, exposição ou conversão, a
ação Gold é `medir melhor`. O resultado demonstra o método; não sustenta ampliar,
reduzir ou realocar investimento.

## Erros e correções

O script concluiu na primeira execução. Não houve treino de modelo, teste de
significância ou transformação da associação em causalidade.

## Artefato local

- Banco ignorado: `solution/data/generated/social_media_bronze.sqlite`.
- SHA-256 físico:
  `dfd96b591d495fc302cef20bbb25d98fef5f7e7670c4859694e6ddb769eea2c3`.
- SHA-256 do dump lógico:
  `7e74618660769dfcd944c005844fd9cb02d51638fd0ead6ebeaa2ef2a6a5abc5`.

## Pendência

Consolidar o relatório final de perguntas respondíveis, achados, limitações e
instrumentação necessária para dados reais.
