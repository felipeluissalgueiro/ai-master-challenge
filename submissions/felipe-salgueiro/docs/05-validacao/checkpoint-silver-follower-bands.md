# Checkpoint — quartis de seguidores declarados por post

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e decisão

Felipe pediu comparações por faixa de creator. O checkpoint de creators mostrou
que `creator_id` não preserva identidade ou seguidores. A decisão metodológica
deste bloco é usar quartis de `follower_count` por post, explicitamente
rotulados como amostrais, sem chamá-los de tamanho estável do creator.

## Alteração

Criado `solution/analysis/build_silver_follower_bands.py`. O script calcula
quartis pelo método nearest-rank, grava os limites em
`silver_follower_band_definitions` e atribui uma faixa a cada post em
`silver_posts_follower_bands`.

SHA-256:
`40336c6b29212c3eccde1343791eb821dc8067020138c3066e247a7ba787afb5`.

## Comando e teste

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_follower_bands.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Conferência posterior por leitura das definições, paridade, `PRAGMA
integrity_check` e hashes.

## Resultado observado

| Faixa | Mínimo | Máximo | n |
|---|---:|---:|---:|
| `post_followers_q1` | 1.013 | 250.811 | 13.054 |
| `post_followers_q2` | 250.838 | 498.488 | 13.053 |
| `post_followers_q3` | 498.492 | 749.826 | 13.054 |
| `post_followers_q4` | 749.841 | 999.998 | 13.053 |

- 52.214/52.214 posts atribuídos; zero inválidos.
- `PRAGMA integrity_check`: `ok`.

## Limite

Os cortes são relativos a este dataset sintético e não representam categorias
de mercado. A unidade de análise é o post; o rótulo correto é “seguidores
declarados no post — Q1…Q4”. A faixa não deve ser chamada de nano, micro, macro
ou tamanho do creator.

## Erros e correções

O script concluiu na primeira execução. Não houve imputação nem arredondamento
dos valores de seguidores.

## Artefato local

- Banco ignorado: `solution/data/generated/social_media_bronze.sqlite`.
- SHA-256 físico:
  `dbc1ea27b805f421eb3f03eac7b52f6cbf1c5a197af6e1165f32284627019fcc`.
- SHA-256 do dump lógico:
  `3f69db4ba6caf01559eaf1b6e14c6a6dbb19696b5b4ae10408f4ddf61b4172e0`.

## Pendência

Construir comparações descritivas com `n`, mediana e dispersão, sem inferência
causal.
