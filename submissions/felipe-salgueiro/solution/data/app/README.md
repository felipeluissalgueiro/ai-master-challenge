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

Estado: dez testes, Ruff, Radon (máximo B) e JSCPD (0% em dois arquivos)
passaram no escopo do exportador e seus testes. O gate anterior da pasta
analysis inteira continua sem aprovação; não foi confundido com esse escopo.
Tipagem/integração com UI e registro dos gates formais permanecem pendentes.
Não há fechamento da MAR-99. Ver checkpoint de validação em docs/05-validacao.

A validação verifica estruturas consumidas, unidades, cobertura das oito
perguntas, ordem dos quartis e IQR, reconciliação dos segmentos e ausência de
valores não finitos/campos históricos superados. O snapshot ID depende de todo
o conteúdo exportado; IDs de evidência/recomendação permanecem estáveis.
