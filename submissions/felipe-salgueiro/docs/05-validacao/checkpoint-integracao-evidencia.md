# Integração do snapshot — 23/09/2026

Lia integrou os quatro artefatos de `solution/data/evidence/` e o checkpoint de origem a partir da worktree isolada do agente de dados, sem mover ou alterar o original. O arquivo binário foi copiado sem sobrescrita; os textos foram portados com patch explícito. Não houve merge de branch nem reexecução do pipeline.

Verificação independente na cópia de destino:

- SHA-256 físico: `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.
- SHA-256 do dump lógico: `7e74618660769dfcd944c005844fd9cb02d51638fd0ead6ebeaa2ef2a6a5abc5`.
- `PRAGMA integrity_check`: `ok`.
- 52.214 linhas Bronze, 14 tabelas, 9 índices explícitos e 7 automáticos.
- Licença MIT conferida no endpoint público de metadados do Kaggle.

Uma consulta inicial de contagem usou aspas duplas em um literal e falhou; foi corrigida com aspas simples. O resultado final acima é da consulta corrigida. O manifesto de origem contava apenas índices explícitos; esclarecemos essa definição sem alterar o SQLite.

O checkpoint do agente descreve a preparação antes de publicação e foi preservado como histórico. Não se deve interpretar sua seção de pendência como o estado final desta integração.

## Limites

Integridade não valida todas as hipóteses analíticas. A regra `creator_profile_eligible` está superada, conforme README e manifesto, e não deve alimentar rankings. A revisão e integração dos scripts finais e do relatório corrigido permanecem pendentes; os comandos anteriores do fork só reproduzem Bronze e métricas iniciais. Nenhuma aprovação do PRD ou deploy é inferida deste checkpoint.
