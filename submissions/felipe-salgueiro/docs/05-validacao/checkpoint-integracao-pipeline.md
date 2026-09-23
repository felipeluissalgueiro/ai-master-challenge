# Integração de scripts e documentos — 23/09/2026

Origem: branch isolada `analysis/felipe-salgueiro-data`; destino: `submission/felipe-salgueiro`, após `cf0ba031`. Integração seletiva, sem merge da branch nem alterações no SQLite de evidência, Brief ou PRD.

- Oito scripts novos; os dois já existentes foram preservados.
- Dez hashes Python conferidos contra o manifesto: todos iguais.
- Sintaxe dos dez scripts validada por `ast.parse`; imports e parser do runner verificados por `python3 -B .../run_pipeline.py --help`.
- Pipeline completo não reexecutado: execução anterior é evidência do agente de dados, não desta integração.
- SHA-256 do SQLite permanece `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.
- Catálogo, diagnóstico e manifesto atualizados; relatório e checkpoints integrados.
- Checkpoints históricos receberam aviso e link para a revisão oficial; exemplo do relatório passou a usar caminhos genéricos e guia de inspeção aponta ao snapshot publicado.

## Limites para o próximo contrato

`creator_profile_eligible` aplica uma regra superada. `measure_better` é fixo no código histórico de Gold, não uma decisão inferida por classificador. Manter os scripts permite reproduzir esse snapshot; não significa endossar esses campos no produto. A revisão oficial e o relatório atualizado prevalecem na interpretação.

Ainda faltam contrato/exportador Ouro da UI, critérios de recomendação, implementação e validação da aplicação. Não houve teste funcional completo novo ou aprovação do PRD.
