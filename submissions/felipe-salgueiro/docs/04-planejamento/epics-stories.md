# Epics e Stories — G4 Challenge 004

Snapshot do Linear P-MAR-55 em 23/09/2026. Três Epics e sete Stories, todas Backlog, prioridade High e responsável Felipe. Meta interna 23/09, não deadline externo. Sem cycle ativo. Cadastro não inicia implementação nem aprova deploy/PR final. RFC-001 é rascunho consolidado; pendências técnicas foram encaminhadas às Stories.

| Issue | Epic | Entrega | Bloqueada por |
|---|---|---|---|
| [MAR-97](issues/MAR-97.md) | Epic | Epic 1 — Evidência e comparações rastreáveis | — |
| [MAR-98](issues/MAR-98.md) | Epic | Epic 2 — Decisão, interface e simulador | — |
| [MAR-96](issues/MAR-96.md) | Epic | Epic 3 — Chat protegido e validação | — |
| [MAR-99](issues/MAR-99.md) | MAR-97 | fechar contrato e exportar evidências para a aplicação | — |
| [MAR-100](issues/MAR-100.md) | MAR-97 | integrar e revisar as oito respostas executivas | — |
| [MAR-101](issues/MAR-101.md) | MAR-98 | estabelecer shell Astryx e navegação entre relatórios | — |
| [MAR-105](issues/MAR-105.md) | MAR-98 | apresentar performance e recomendações com evidência | MAR-99, MAR-101 |
| [MAR-103](issues/MAR-103.md) | MAR-98 | calcular custo hipotético por views, interação e venda | MAR-99, MAR-101 |
| [MAR-102](issues/MAR-102.md) | MAR-96 | explicar recomendação por OpenRouter com acesso protegido | MAR-99, MAR-105 |
| [MAR-104](issues/MAR-104.md) | MAR-96 | verificar jornada e preparar pacote de avaliação | MAR-100, MAR-105, MAR-103, MAR-102 |

## Ordem de execução

Preparar MAR-99 (contrato de dados), MAR-100 (integrar relatório existente) e MAR-101 (shell Astryx) em paralelo, respeitando posse de arquivos. MAR-105 e MAR-103 consomem contrato e shell; MAR-102 depende das recomendações. MAR-104 integra validação após as demais. Não repetir o pipeline já validado sem necessidade.

## Evidência de planejamento

Dez descrições passaram no template_guard feature. Critérios, cenários e verificações futuras estão nos snapshots; não são testes executados da aplicação. Dependências de execução foram registradas no Linear. Não foram criadas issues no repositório upstream do G4.

## Espelho GitHub

[Project público](https://github.com/users/felipeluissalgueiro/projects/2). Linear é a fonte; cartões são drafts de planejamento, não issues upstream. Atualização manual por checkpoints. Hierarquia e dependências constam no corpo dos cartões; não simular sub-issues nativas entre drafts.
