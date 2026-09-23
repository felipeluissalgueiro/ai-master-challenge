# MAR-97 — feat(g4): Epic 1 — Evidência e comparações rastreáveis

Fonte: [Linear](https://linear.app/cadencia/issue/MAR-97/featg4-epic-1-evidencia-e-comparacoes-rastreaveis) · snapshot 2026-09-23 · Status: Backlog · Responsável: Felipe.
Epic: agregadora · Dependências: nenhuma.

## O que será construído

Permitir ao gestor conferir as oito perguntas até a evidência numérica, reutilizando SQLite, pipeline e relatório existentes.

Projeto P-MAR-55 / Marketing por decisão de Felipe. Fonte técnica: [RFC-001](<https://linear.app/cadencia/document/rfc-001-evidencia-decisao-e-explicacao-de-social-media-aa1e95216d25>), rascunho consolidado; esta issue resolve suas pendências pertinentes, não presume validação final. Escopo Git: submissions/felipe-salgueiro/ no fork ai-master-challenge.

## Tech stack

* Linguagem / runtime: Python offline e TypeScript na aplicação.
* Framework / libs principais: SQLite de evidência, JSON, Next.js/Astryx; biblioteca padrão para análise.

## Integrações externas

Nenhuma operação externa necessária ao cadastro; Vercel é destino futuro da aplicação.

## Regras de negócio explícitas

Somente leitura do snapshot; não usar creator_profile_eligible ou measure_better como política. Fonte sintética não fundamenta causalidade.

## Critério de aceite

- [ ] Stories A e B entregues com evidência reproduzível.
- [ ] Relatório e export reconciliados; banco e visualizador preservados.

## Estimativa

Epic agregadora; estimativa nas filhas, sem duplicar pontos. Meta interna de entrega: 23/09/2026 conforme Felipe; não representa prazo externo confirmado.

## Dependências

Nenhuma dependência de outra Story para planejar; usar PRD/RFC e artefatos existentes.

## Riscos

Diferenças pequenas e campos ausentes não devem virar vencedores ou ROI fictícios.
