# MAR-99 — exportador e contrato de dados

Estado: implementado/testado localmente, integração frontend pendente; issue aberta.
Autorrevisão por Lia/modelo executor, conforme escolha explícita de Felipe.
Não é revisão independente nem aceite do produto inteiro.

## Escopo e hashes

| Arquivo | SHA-256 |
|---|---|
| solution/analysis/export_app.py | e3c8998272e040b1d2128cf849800a78d4e7bd6faae79a11df270c48d5626a4d |
| solution/analysis/test_export_app.py | 72011ad46ae08f861250c7a405e9ace4cdede09fca3d679a45077cda6dc0301e |
| solution/data/app/dashboard.json | 3d6d4bc7debbafcd61a4d2091c3da4f3ff7b09c23ead33ab121952abdb901cf3 |
| solution/data/app/manifest.json | 0f68de72115f1599069201dd3206a6e5bab6b158d6415ba398fa6fa1e7623bf9 |

## Verificações executadas

Da raiz da submission; Python 3.14.7, Ruff 0.16.6, Radon 6.0.1, JSCPD 5.3.2:

```sh
python3 -m unittest solution.analysis.test_export_app -v
ruff check solution/analysis/export_app.py solution/analysis/test_export_app.py
radon cc solution/analysis/export_app.py solution/analysis/test_export_app.py -s
npx --yes jscpd@5.3.2 solution/analysis/export_app.py solution/analysis/test_export_app.py --min-tokens 50 --threshold 3 --reporters json --output /tmp/g4-mar99-jscpd
python3 solution/analysis/export_app.py
```

- 10 testes: PASS; leitura do SQLite real, reprodução idêntica e hash preservado.
- Ruff: PASS, zero achados nos dois arquivos do escopo.
- Radon: máximo B, complexidade máxima 9; nenhuma função C+.
- JSCPD: PASS, 2 fontes/291 linhas/2.433 tokens analisados, 0 clones e 0% duplicação.
- Cache npm temporário gravável foi usado na execução JSCPD; nenhuma redução de threshold.
- Erros de schema/unidade, hash, ausência de seção, campos históricos, NaN/Inf,
  ordem de cobertura, IDs injetados, quartis e soma das amostras são rejeitados.
- Saídas que colidem com a evidência ou são symlinks são rejeitadas antes da gravação.
- Snapshot ID muda com conteúdo; IDs de recomendações permanecem estáveis.

## Correções e limites

A primeira implementação comparou schema com inteiro em vez de string 1.0.0;
o teste com dado real revelou o erro. Na ampliação, o validador usou inicialmente
post_follower_band onde o relatório exporta follower_band; corrigido sem alterar
a fonte. Fechamento da conexão foi tornado explícito. A função de validação
foi dividida para reduzir complexidade de C para B, sem remover verificações.

Autorrevisão examinou código, testes e diferença contra o checkpoint inicial:
nenhuma fórmula analítica foi duplicada; dados continuam numéricos e rastreáveis;
recomendações são propostas, não classificação econômica validada; valores
comerciais são null, não zero inventado. O JSON da fonte é fixado por hash.

Esta validação é de contrato offline: não comprova navegação, build Next.js,
proteção de acesso ou comportamento do chat. O gate anterior de toda a pasta
analítica apresentou falhas e não recebeu PASS retroativo. Recibos formais do
Issue Flow e aceites integrados continuam pendentes. Sem deploy ou PR final.
