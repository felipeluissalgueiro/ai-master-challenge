# Scripts analíticos

`build_bronze.py` preserva as 27 colunas como texto e registra proveniência. `build_silver_metrics.py` valida cinco contagens e deriva razões com nomes explícitos. Python 3.10+; biblioteca padrão, sem dependências externas.

Comandos em [Solução](../README.md). Bronze substitui o banco de saída; Silver reconstrói sua tabela derivada. Execute somente em destinos de trabalho que possam ser reconstruídos, nunca em uma base com dados insubstituíveis.
