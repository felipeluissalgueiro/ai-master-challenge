# Contrato da aplicação — implementação inicial MAR-99

Fonte numérica: relatório auditado `../../reports/evidence.json`, reconciliado
com o hash e a contagem do SQLite de evidência aberto somente para leitura.
O exportador não replica cálculos de métricas. Sem SQLite em runtime da UI.

Da raiz da submission:

```sh
python3 solution/analysis/export_app.py
python3 -m unittest solution.analysis.test_export_app -v
ruff check solution/analysis/export_app.py solution/analysis/test_export_app.py
```

`dashboard.json` inclui fonte, fórmula, unidades, evidências com IDs estáveis,
oito recomendações propostas (não decisões econômicas validadas), cobertura e
limites. Números indisponíveis são null com motivo. `manifest.json` registra
hashes da fonte, banco, gerador e resultado; sem relógio variável no export.

Estado: quatro testes e Ruff dos dois arquivos novos passaram. O gate completo
da pasta analysis não passou (Ruff, complexidade e coleta JSCPD), portanto não
há aprovação geral nem fechamento da MAR-99. Validação de schema completa,
tipagem/integração com UI e gates formais permanecem pendentes.
