# Solução

Destino da análise reproduzível, estratégia e eventual página pública do
Challenge 004. A interface ainda não foi implementada. A ingestão Bronze e o
primeiro segmento Silver de métricas já possuem scripts determinísticos.

## Estrutura analítica

- `analysis/`: scripts Python versionáveis, somente com biblioteca padrão.
- `data/generated/`: SQLite derivado e reconstruível, ignorado pelo Git.
- [data/evidence/](data/evidence/README.md): snapshot completo Bronze/Prata/Ouro, manifesto e contrato de leitura; evidência para auditoria, não banco da aplicação.
- `../docs/01-brief/dados/`: proveniência, diagnóstico, catálogo de métricas e
  matriz de perguntas.

O banco local canônico é
`data/generated/social_media_bronze.sqlite`. O CSV e o ZIP de origem não são
copiados para o repositório.

## Reconstrução do checkpoint inicial

Executar a partir da raiz da submissão, informando os arquivos-fonte locais:

Requer Python 3.10+ e os arquivos do [dataset Kaggle](https://www.kaggle.com/datasets/omenkj/social-media-sponsorship-and-engagement-dataset/data). Crie o diretório de saída antes da primeira execução. Os comandos abaixo recriam dados derivados; não aponte para banco com trabalho insubstituível.

```bash
mkdir -p solution/data/generated

python solution/analysis/build_bronze.py \
  --csv /caminho/social_media_dataset.csv \
  --zip /caminho/dataset.zip \
  --output solution/data/generated/social_media_bronze.sqlite

python solution/analysis/build_silver_metrics.py \
  --database solution/data/generated/social_media_bronze.sqlite

sqlite3 -readonly solution/data/generated/social_media_bronze.sqlite \
  "PRAGMA integrity_check;"
```

O primeiro comando recria a camada Bronze. O segundo acrescenta a tabela
`silver_posts_metrics`. Estes dois comandos reproduzem somente o checkpoint inicial,
não todas as tabelas do snapshot completo. Os scripts finais do outro agente
ainda aguardam integração/revisão nesta branch. O snapshot já contém Ouro;
app e modelo ainda não foram implementados.

Validação executada e limites: [checkpoint Bronze/Silver](../docs/05-validacao/checkpoint-bronze-silver.md).
