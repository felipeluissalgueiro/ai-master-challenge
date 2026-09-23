# MAR-99 — feat(g4-dados): fechar contrato e exportar evidências para a aplicação

## Plano Técnico — MAR-99

Planejado em 23/09/2026 por Lia, com execução enxuta solicitada por Felipe. **Planejado, não iniciado.** Repo confirmado: felipeluissalgueiro/ai-master-challenge. Squad: times/marketing; responsável humano: Felipe.

### Análise

Fontes: Brief, PRD v0.5, RFC-001, gate Vitor, parecer/síntese Sofia, README da solução e evidência SQLite, catálogo de métricas, matriz histórica (superada onde conflita com revisão oficial), checkpoint de revisão do dicionário, handoff/README/manifesto do relatório e descrição integral desta issue.

Já existe: SQLite/pipeline já publicados; consultas do relatório existem no agente de dados; falta export final.
Delta: fechar contrato e exportar evidências para a aplicação. DRY: reaproveitar cálculos e artefatos existentes; não copiar regras do Cadência sem entradas equivalentes. ETC: paths relativos, modelo/config no servidor, UI não conhece SQLite. Rollout: snapshot imutável; sem deploy/PR final nesta etapa.

### Implementação proposta

1. Definir evidence_id e recommendation_id estáveis; separar valores %, deltas pp, n, fórmula, exclusões e limites.
2. Reaproveitar consultas validadas do relatório/Prata; exportar somente o que a UI usa, sem alterar SQLite ou executar novamente Bronze/Prata.
3. Validar JSON e gerar manifesto determinístico; registrar ausência e não calcular vencedor/threshold econômico.

### Arquivos previstos

solution/analysis/export_app.py; solution/data/app/; solution/app/src/lib/data-contract.ts. Caminhos relativos à submission; todos são alvos propostos, não arquivos já implementados.

### Critério de aceite e testes proporcionais

Manter os aceites/Gherkin originais da issue. Verificação planejada: Schema válido/inválido; export idêntico duas vezes; hash DB intacto; números reconciliados; campos históricos proibidos ausentes.

### Dependências e riscos

Nenhuma para planejar; alinhar formato compartilhado com MAR-100. unit=percentage_points do JSON preliminar precisa ser revisto para taxas em percent; não propagar nomenclatura incorreta.

### Regras reaproveitadas e pendências

Sem nova rodada de perguntas: Felipe solicitou planejamento enxuto; regras já fechadas no PRD/RFC foram reaproveitadas. Isso não é um grill de implementação independente executado. Pendências técnicas acima ficam explícitas e devem ser resolvidas antes da parte afetada; testes de dados/segurança não são dispensados.

### Repo, branch e execução

Entrega final: submission/felipe-salgueiro; branch sugerida pelo Linear: feature/mar-99-featg4-dados-fechar-contrato-e-exportar-evidencias-para-a. Nenhuma branch será criada/trocada no planejamento. Start deve preservar a branch única de submissão e resolver isolamento de escritores, sem duplicar repo nem tomar posse da worktree do agente de dados.

Stack: Python/SQLite offline, JSON; Next.js/TypeScript/Astryx na aplicação. Integrações externas somente na Story pertinente. Estimativa é a já registrada na issue, não promessa de horas. A auto-inicialização da skill não foi aplicada ao lote: o pedido atual é planejar, não iniciar sete execuções.
