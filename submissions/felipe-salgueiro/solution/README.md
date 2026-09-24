# Solução

Análise reproduzível, estratégia e aplicação do Challenge 004.
[Acesso e roteiro de uso](../README.md#acesso-e-roteiro-de-avaliação).
A ingestão Bronze e o pipeline completo Bronze/Prata/Ouro possuem scripts determinísticos versionados.

## Estrutura analítica

- [reports/](reports/README.md): relatório executivo de performance e estratégia, com evidência estruturada e navegação para o visualizador.
- [prototype/](prototype/README.md): explorador HTML e gerador reproduzível; disponível na aplicação e como `index.html` local.
- [app/](app/README.md): aplicação Next.js, setup, dashboard, relatórios e simulador.
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
não todas as tabelas do snapshot completo. Os scripts finais foram integrados;
o snapshot já contém Ouro;
a aplicação usa o exportador posterior; modelo preditivo não foi implementado.

Validação executada e limites: [checkpoint Bronze/Silver](../docs/05-validacao/checkpoint-bronze-silver.md).

## Reprodução integral do snapshot histórico

Da raiz da submissão, com Python 3.10+ e os arquivos Kaggle:

```bash
python3 solution/analysis/run_pipeline.py \
  --csv /caminho/social_media_dataset.csv \
  --zip /caminho/dataset.zip \
  --database solution/data/generated/social_media_bronze.sqlite
```

**Atenção:** o pipeline reconstrói tabelas no destino. Nunca aponte para o banco de evidência publicado nem para um banco com trabalho a preservar. O diretório de saída é criado pelo runner.

Os dez scripts preservam os hashes do [manifesto](../docs/01-brief/dados/manifest.json). Esta integração verificou sintaxe, imports via `--help` e hashes; a execução completa foi realizada pelo agente de dados e consta no [checkpoint histórico](../docs/05-validacao/checkpoint-pipeline-final.md), sem repetição nesta integração.

**Limites conhecidos:** `creator_profile_eligible` foi gerado por regra superada. O valor `measure_better` é fixo na implementação histórica do Ouro, não saída de um classificador de decisões validado. Esses campos não são utilizados como política do produto. Consulte a [revisão oficial](../docs/05-validacao/checkpoint-revisao-dicionario-oficial.md) e o [contrato/exportador da aplicação](data/app/README.md).
