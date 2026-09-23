# Checkpoint — snapshot SQLite de evidência

Data: 23/09/2026. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e decisão

Felipe determinou que o banco completo deve acompanhar o fork para auditoria.
Também corrigiu o objetivo do manual: explicar o racional da arquitetura e o
contrato de leitura, não esperar que pessoas inspecionem 52 mil linhas.

O SQLite é evidência; Vercel e chat consumirão exportações Ouro versionadas.

## Execução

Foi criado um snapshot pelo mecanismo nativo `.backup` do SQLite a partir do
banco validado existente. O pipeline verde não foi reexecutado, e o original
não foi movido, apagado ou alterado.

Origem:
`solution/data/generated/social_media_bronze.sqlite`.

Destino:
`solution/data/evidence/social_media_analysis.sqlite`.

## Resultado

- Tamanho exato: 61.607.936 bytes (58,75390625 MiB).
- SHA-256 físico:
  `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.
- SHA-256 do dump lógico:
  `7e74618660769dfcd944c005844fd9cb02d51638fd0ead6ebeaa2ef2a6a5abc5`.
- Dump lógico idêntico ao banco de origem.
- `PRAGMA integrity_check`: `ok`.
- Estrutura: 14 tabelas e 9 índices.
- Bronze: 52.214 posts.
- Prata por post: 52.214 linhas em cada tabela temática.
- Creators auditados: 5.000.
- Ouro: 68 resumos, 60 comparações e 45 correlações.

## Entrega e limite GitHub

O artefato fica abaixo do limite rígido de 100 MiB do Git regular e acima do
patamar de aviso de 50 MiB. Como excede 25 MiB, não deve ser enviado pela UI do
GitHub; Lia fará a integração pela linha de comando. Não foi configurado Git
LFS porque não é exigido pelo tamanho atual e mudaria o fluxo de download.

## Documentação criada/alterada

- `solution/data/evidence/README.md`: racional Bronze/Prata/Ouro, contrato para
  LLM, métricas, limites e proveniência.
- `solution/data/evidence/manifest.json`: contrato legível por máquina.
- `solution/data/evidence/.gitignore`: exclui somente journals/WAL/SHM.
- `docs/01-brief/dados/manifest.json`: passa a distinguir banco de trabalho e
  snapshot rastreado.
- `docs/01-brief/dados/relatorio-final.md`: corrige a política de entrega.
- `docs/01-brief/dados/como-verificar-dados.md`: aponta para a evidência final.

## Privacidade e licença

A fonte é declarada simulada e licenciada sob MIT. Nomes, comentários e URLs
são tratados como campos simulados, não como pessoas ou destinos reais. Não é
feita alegação de anonimização verificada.

## Pendência

Lia deve revisar e integrar os caminhos exatos no fork. O SQLite de evidência
precisa ser adicionado explicitamente porque o diretório `submissions/` é
ignorado na raiz. Bancos gerados e auxiliares continuam fora do Git.
