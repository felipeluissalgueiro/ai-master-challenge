# Proveniência e atualização dos documentos

Snapshot revisado em 23/09/2026 para checkpoints no fork, autorizados por Felipe. Publicar a branch não equivale a enviar a PR de submissão.

## Fontes de trabalho
- **Linear:** P-MAR-55 é a fonte do projeto, marcos e futuros documentos/issues. Os links privados são referências, não pré-requisito para leitura.
- **Obsidian:** o diário é a fonte do workflow; as duas notas de pesquisa são registros históricos do levantamento.
- **Repositório oficial:** enunciado, guia e template já existem no clone. Base local desta preparação: `4aed364d572fabe0f1fff1f0c6f32960b30fe575`.
- **PD Framework:** princípios internos e papéis orientam o método. Esta submissão documenta sua aplicação sem copiar toda a instalação.

## Manifesto deste snapshot
| Artefato | Origem | Tratamento / limite |
|---|---|---|
| [Projeto](00-projeto/projeto.md) | Descrição real de P-MAR-55 | Removida linha de caminho privado do diário |
| [Marcos](00-projeto/marcos.md) | Três marcos retornados pela API | Formato Markdown; IDs/estado preservados |
| [Workflow](../process-log/workflow.md) | Nota “2026-09-23 - G4 AI Master - Diario de processo” | Frontmatter, caminhos locais, IDs internos de sessão e referências privadas de navegação removidos; histórico preservado |
| [Panorama](01-brief/pesquisa/panorama-submissoes.md) | Nota “2026-09-23 - G4 AI Master - Panorama das submissoes” | Frontmatter e navegação específica do Obsidian removidos |
| [Inventário](01-brief/pesquisa/inventario-prs.md) | Nota “2026-09-23 - G4 AI Master - Inventario das PRs” | Mesmo tratamento; documento permanece PARCIAL |
| [Revisão crítica](01-brief/pesquisa/revisao-critica.md) | Conferências registradas no workflow 47–48 | Síntese editorial, não export de documento Linear |
| [Hipóteses](01-brief/hipoteses-e-lacunas.md) | Debate registrado no workflow | Síntese editorial; não é Brief aprovado |
| READMEs e método | Organização solicitada por Felipe | Redação assistida por Lia, sem validar a solução |
| [Parecer UX completo](03-rfc/parecer-ux-sofia-g4-challenge004-20260923.md) | Parecer e síntese de Sofia registrados na worktree Marketing por Lia | Snapshot integral com wireframes, fontes, tokens aproximados e ressalva analítica; proposta não implementada, validada em browser ou publicada como aplicação |

Na consulta inicial havia zero documentos e issues. Posteriormente, o [Brief v1](01-brief/brief.md) foi criado no Linear e exportado. O [PRD Draft v0.3](02-prd/prd.md) foi elaborado por Paloma e consolidado por Lia; seu fechamento depende da análise e revisão. RFC e tarefas individuais permanecem pendentes; não foram fabricados para preencher a estrutura.

SHA-256 das notas originais no momento da exportação (antes do tratamento):
- Diário atualizado até workflow 111: `7231a177a62a3a1dc2ee10735ef71e76d62a591965850d5fadc8845d25affa8e`.
- Panorama: `9168a5b643541134189f1418a93c1aade7a881e9ab10ae97b61e374d6f79538b`.
- Inventário: `04490e62970f30ac2ea7ac950d25fd88ad1d8ff3a635165baf3770ad551de33d`.

Hashes registram versão de origem, não comprovam a veracidade do conteúdo nem dão acesso às notas privadas.

## Evitar divergência — DRY
Os exports são snapshots derivados, não cópias editáveis independentes. Mudanças nas fontes exigem uma nova exportação, revisão das transformações, atualização deste manifesto e diff visível no Git. Ainda não há sincronização automática instalada. Decisões da fonte não devem ser corrigidas somente no snapshot. Sínteses editoriais têm função explicativa e remetem à fonte.

## Limite de compartilhamento
Foram preparados apenas materiais do processo G4. Não copiamos a ficha pessoal completa da candidatura, credenciais, dados de clientes, conversas de outros projetos ou a instalação privada do framework. Gravações e transcripts completos não foram anexados. Caminhos locais, IDs de sessão e detalhes internos de segurança foram omitidos do workflow público. A revisão deste checkpoint não substitui a revisão da entrega final.
