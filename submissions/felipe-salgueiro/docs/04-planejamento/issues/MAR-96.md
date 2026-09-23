# MAR-96 — feat(g4): Epic 3 — Chat protegido e validação

Fonte: [Linear](https://linear.app/cadencia/issue/MAR-96/featg4-epic-3-chat-protegido-e-validacao) · snapshot 2026-09-23 · Status: Backlog · Responsável: Felipe.
Epic: agregadora · Dependências: nenhuma.

## O que será construído

Explicar recomendações com contexto controlado e verificar a entrega antes de disponibilizá-la.

Projeto P-MAR-55 / Marketing por decisão de Felipe. Fonte técnica: [RFC-001](<https://linear.app/cadencia/document/rfc-001-evidencia-decisao-e-explicacao-de-social-media-aa1e95216d25>), rascunho consolidado; esta issue resolve suas pendências pertinentes, não presume validação final. Escopo Git: submissions/felipe-salgueiro/ no fork ai-master-challenge.

## Tech stack

* Linguagem / runtime: Python offline e TypeScript na aplicação.
* Framework / libs principais: SQLite de evidência, JSON, Next.js/Astryx; biblioteca padrão para análise.

## Integrações externas

Vercel/OpenRouter conforme RFC; sem habilitação, cobrança, deploy ou envio externo implícitos.

## Regras de negócio explícitas

Chave exclusiva somente no servidor. Sem ferramentas ou cálculos de negócio no LLM. Deploy e PR final não autorizados por esta Epic.

## Critério de aceite

- [ ] Stories F e G entregues com testes e limites documentados.
- [ ] Chat indisponível não afeta relatório ou simulador; pacote pronto para revisão de Felipe.

## Estimativa

Epic agregadora; estimativa nas filhas, sem duplicar pontos. Meta interna de entrega: 23/09/2026 conforme Felipe; não representa prazo externo confirmado.

## Dependências

Nenhuma dependência de outra Story para planejar; usar PRD/RFC e artefatos existentes.

## Riscos

Proteção Vercel e limites efetivos precisam ser verificados; configuração do orçamento não cabe à Lia.
