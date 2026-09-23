# MAR-99 — feat(g4-dados): fechar contrato e exportar evidências para a aplicação

Fonte: [Linear](https://linear.app/cadencia/issue/MAR-99/featg4-dados-fechar-contrato-e-exportar-evidencias-para-a-aplicacao) · snapshot 2026-09-23 · Status: Backlog · Responsável: Felipe.
Epic: MAR-97 · Dependências: nenhuma.

## O que será construído

Disponibilizar JSON versionado que dashboard, simulador e chat possam consumir sem SQLite em runtime.

Projeto P-MAR-55 / Marketing por decisão de Felipe. Fonte técnica: [RFC-001](<https://linear.app/cadencia/document/rfc-001-evidencia-decisao-e-explicacao-de-social-media-aa1e95216d25>), rascunho consolidado; esta issue resolve suas pendências pertinentes, não presume validação final. Escopo Git: submissions/felipe-salgueiro/ no fork ai-master-challenge.

## Tech stack

* Linguagem / runtime: Python offline e TypeScript na aplicação.
* Framework / libs principais: SQLite de evidência, JSON, Next.js/Astryx; biblioteca padrão para análise.

## Integrações externas

Nenhuma operação externa necessária ao cadastro; Vercel é destino futuro da aplicação.

## Regras de negócio explícitas

Schema com IDs estáveis, hash, fórmula, unidade, agregação, filtros, n, dispersão e exclusões. Taxas em %, diferenças em pp; ausência é null com motivo. Revisar regras de suficiência sem inventar thresholds; snapshot permanece intacto.

## Critério de aceite

- [ ] Export gerado em leitura somente e reconciliado com snapshot de 52.214 registros.
- [ ] Schema e IDs validados; campos históricos superados não orientam decisão.
- [ ] Teste determinístico e rejeição de hash/schema incompatível documentados.

## Estimativa

3 pontos de planejamento; não é promessa de duração. Meta interna de entrega: 23/09/2026 conforme Felipe; não representa prazo externo confirmado.

## Dependências

Nenhuma dependência de outra Story para planejar; usar PRD/RFC e artefatos existentes.

## Riscos

JSON do relatório é preliminar; reconciliar antes de adotá-lo como contrato final.

## Cenários de aceite (Gherkin)

```gherkin
@AC-1
Scenario: fechar contrato e exportar evidências para a aplicação
  Given um snapshot conhecido e íntegro
  When a exportação é executada duas vezes
  Then os resultados são idênticos e o hash do SQLite permanece intacto
```

## Mapeamento de evidências

| Then | Evidência |
| -- | -- |
| AC-1:1 | gate:reproducibilidade-e-reconciliacao — verificação objetiva descrita no cenário, a implementar/executar; não é PASS existente |

Plano técnico: [plano MAR-99](../planos/MAR-99.md), anexado também ao Linear e à issue real do GitHub; estado planejado, não iniciado.
