# Checkpoint — Silver de dimensões e patrocínio

Data: 23/09/2026. Base de referência: commit
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Trabalho executado somente na
branch local `analysis/felipe-salgueiro-data`, sem stage, commit, push ou PR.

## Origem e decisão

Felipe definiu Bronze/Prata/Ouro, processamento determinístico em Python,
SQLite reconstruível e segmentação anterior a inferências. Após o checkpoint
Bronze/Silver, autorizou a continuidade em worktree própria para evitar colisão
com a Lia. Este bloco cobre somente dimensões categóricas e consistência interna
do patrocínio; não compara performance e não chama `FALSE` de orgânico.

## Hipótese verificada

Antes de comparar posts patrocinados e não patrocinados segundo a flag, era
necessário verificar se plataforma, formato, categoria e campos de sponsor têm
vocabulário conhecido e combinações internamente consistentes.

## Alteração

Criado
`solution/analysis/build_silver_dimensions.py`. O script reconstrói
`silver_posts_dimensions`, preserva uma linha por registro Bronze, converte
`TRUE`/`FALSE` em 1/0, cria o rótulo explícito
`not_sponsored_by_flag`, adiciona flags de qualidade e índices para recortes.

SHA-256 do script:
`dd8de14a843ab91f9f7365904d8007780733bb8af9e42f7967908a3f89b58e3d`.

## Comando executado

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_dimensions.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

A conferência final usou consultas SQLite somente leitura, `PRAGMA
integrity_check`, contagens de paridade, percentuais por dimensão e `sha256sum`.

## Resultado observado

- 52.214 linhas Bronze, 52.214 métricas e 52.214 dimensões.
- 52.214 dimensões válidas, zero inválidas e nenhuma flag de qualidade.
- `PRAGMA integrity_check`: `ok`.
- Patrocinados: 22.314 (42,74%).
- Não patrocinados segundo a flag: 29.900 (57,26%).

### Tamanho de amostra e participação patrocinada

| Dimensão | Valor | n total | n patrocinado | % patrocinado |
|---|---|---:|---:|---:|
| Plataforma | Bilibili | 10.598 | 4.453 | 42,02% |
| Plataforma | Instagram | 10.423 | 4.369 | 41,92% |
| Plataforma | RedNote | 10.402 | 4.521 | 43,46% |
| Plataforma | TikTok | 10.296 | 4.441 | 43,13% |
| Plataforma | YouTube | 10.495 | 4.530 | 43,16% |
| Formato | image | 10.303 | 4.416 | 42,86% |
| Formato | mixed | 5.213 | 2.224 | 42,66% |
| Formato | text | 5.198 | 2.205 | 42,42% |
| Formato | video | 31.500 | 13.469 | 42,76% |
| Categoria | beauty | 21.023 | 8.926 | 42,46% |
| Categoria | lifestyle | 20.761 | 8.891 | 42,83% |
| Categoria | tech | 10.430 | 4.497 | 43,12% |

### Campos de disclosure e sponsor

- Disclosure: 11.784 `explicit`, 10.530 `implicit` e 29.900 `none`.
- Local: 8.944 `caption`, 6.124 `hashtags`, 7.246 `video` e 29.900
  `none`.
- Categorias patrocinadas: cosmetics 3.688; electronics 3.750; fashion 3.710;
  food 3.846; gaming 3.687; travel 3.633.
- As 29.900 linhas `FALSE` usam exatamente os sentinelas `none`,
  `Not sponsors`, `Not sponsors`, `none`.
- As 22.314 linhas `TRUE` têm disclosure explícito/implícito, nome não sentinela,
  uma das seis categorias e local não `none`.
- Há 18.005 nomes distintos nos posts patrocinados, equivalentes a 80,69 nomes
  distintos por 100 posts; o maior nome aparece em 32 posts.

## Interpretação e limite

A consistência interna permite usar a flag e as três dimensões em recortes
posteriores. Não valida que houve mídia paga, investimento, entrega orgânica ou
efeito de patrocínio. A uniformidade da participação patrocinada e a alta
cardinalidade dos nomes são compatíveis com artefatos da geração sintética; não
são prova independente do mecanismo gerador.

## Erro e correção

Uma consulta exploratória inicial filtrou `is_sponsored='True'`, mas o valor
real é `TRUE`; ela retornou zero sponsors. A consulta foi corrigida para o valor
exato antes de qualquer conclusão. O script usa conversão estrita de `TRUE` e
`FALSE` e não repetiu o erro.

## Artefato local

Banco ignorado pelo Git:
`solution/data/generated/social_media_bronze.sqlite`.

- SHA-256 físico após este segmento:
  `38ae39fb783091614c118dd3de39b21f7df4435e181c7013ee29a9a9e7eadb9b`.
- SHA-256 do dump lógico:
  `aabe39c5bab017a3ec96c08e22645686e4cb4551dfb4d98cc8a6de696fab3741`.

## Pendências

Auditar creators e consistência de seguidores; depois datas/período e
distribuições demográficas. Comparações de performance, faixas de creator,
correlações e Gold permanecem não iniciadas.
