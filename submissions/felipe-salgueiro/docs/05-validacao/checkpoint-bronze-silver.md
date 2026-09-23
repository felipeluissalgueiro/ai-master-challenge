# Checkpoint de validação — 23/09/2026

Lia executou os dois scripts em um banco temporário novo, separado do banco de trabalho. Comandos equivalentes aos do [README da solução](../../solution/README.md), com saída temporária.

## Resultados observados

- Bronze: 52.214 registros, 27 colunas de origem, hashes do CSV/ZIP conferidos e `integrity_check: ok`.
- Silver: 52.214 registros; cinco contagens analisadas (`views`, `likes`, `shares`, `comments_count`, `follower_count`), sem valores inválidos ou zero nesta base.
- Conferência final somente leitura: `PRAGMA integrity_check` → `ok`; contagens Bronze/Silver → `52214` / `52214`.
- Não são achados de negócio, prova de qualidade semântica ou teste de todos os casos-limite. Gold, UI, regressões e testes com entradas inválidas permanecem pendentes.

## Versões executadas (SHA-256)

- `build_bronze.py`: `6b2033da25e0aab7be3c7ca36bfad3922e542fb0adba9790b4fc51ee60c72a4b`.
- `build_silver_metrics.py`: `e8add1ddd4181f711b6d4154b9d86cd517dfd67ac9398455c965ed168d951f1f`.

Não há afirmação de validação da solução inteira ou de efeito causal de patrocínio.
