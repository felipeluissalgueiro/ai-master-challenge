# Como verificar Bronze, Prata e Ouro

O SQLite reúne todas as camadas em um único arquivo. Ele não precisa ser lido
como código: pode ser aberto em uma interface gráfica como DB Browser for
SQLite. Não instalar ou alterar ferramentas sem alinhamento; este guia descreve
as opções.

## Arquivo atual

`solution/data/evidence/social_media_analysis.sqlite` (snapshot publicado; abrir somente para leitura).

O snapshot definitivo para os avaliadores foi criado em
`solution/data/evidence/social_media_analysis.sqlite`. O racional da modelagem,
o contrato de interpretação por LLM e os hashes estão no `README.md` da mesma
pasta. Nenhuma exportação Ouro para o runtime foi criada nesta etapa.

## Opção visual

No DB Browser for SQLite:

1. Abra o arquivo `.sqlite`.
2. Use **Database Structure** para ver as tabelas.
3. Use **Browse Data** e escolha uma tabela.
4. Use os filtros das colunas para plataforma, categoria ou patrocínio.
5. Não clique em **Write Changes**; o objetivo é somente leitura.

Mapa das tabelas:

| Camada | Tabela | O que mostra |
|---|---|---|
| Bronze | `bronze_posts_raw` | As 52.214 linhas como chegaram no CSV |
| Bronze | `bronze_manifest` | Origem, hashes e contagens |
| Bronze | `bronze_columns` | Catálogo das colunas de origem |
| Prata | `silver_posts_metrics` | Números normalizados e métricas derivadas |
| Prata | `silver_posts_dimensions` | Plataforma, conteúdo e patrocínio padronizados |
| Prata | `silver_creator_profiles` | Auditoria de creators; a elegibilidade atual está obsoleta |
| Prata | `silver_posts_dates` | Datas normalizadas |
| Prata | `silver_posts_audience` | Grupos predominantes de audiência |
| Prata | `silver_posts_content` | Características estruturais de texto/hashtags/URL |
| Prata | `silver_posts_follower_bands` | Quartil de seguidores na data do post |
| Ouro | `gold_segment_summaries` | n, mediana e IQR por segmento e patrocínio |
| Ouro | `gold_sponsorship_comparisons` | Comparações controladas por plataforma/categoria/faixa |
| Ouro | `gold_numeric_correlations` | Correlações de Spearman e limites de interpretação |

## Opção no terminal, somente leitura

```bash
sqlite3 -readonly solution/data/evidence/social_media_analysis.sqlite
```

Dentro do SQLite:

```sql
.headers on
.mode column
.tables
SELECT * FROM gold_segment_summaries LIMIT 20;
SELECT * FROM gold_sponsorship_comparisons LIMIT 20;
SELECT * FROM gold_numeric_correlations LIMIT 20;
.quit
```

## O que será mais simples para avaliação

Depois que o contrato Ouro for aprovado, a proposta é disponibilizar:

- dashboard com filtros e explicação das camadas;
- tabelas Ouro em JSON versionado para a Vercel;
- download em CSV das tabelas relevantes;
- IDs de evidência que ligam cada recomendação aos números;
- avisos explícitos sobre simulação, qualidade e métricas ausentes.

Assim, Felipe e os avaliadores não precisarão consultar SQL para conferir as
separações e as recomendações.
