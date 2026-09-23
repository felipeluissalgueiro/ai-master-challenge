# Challenge 004 Insight Lab — shell UI e simulador

Aplicação Next.js/TypeScript mínima para a MAR-101. Entrega chrome Astryx,
navegação acessível, estados técnicos e rotas reservadas para o relatório
executivo e o explorador.

## Limite da Story

O shell não implementa o dashboard analítico da MAR-105, não lê SQLite, não
define contrato concorrente e não inclui LLM, login ou servidor de banco.

O shell segue o plano da MAR-101 e apresenta as oito decisões do Head de Social
Media com identidade própria navy/coral aproximada. Não atribui essa identidade
à marca analisada e não antecipa métricas ou recomendações.

Apenas a integração de novas versões de `solution/reports/**`,
`solution/prototype/**` e da paleta `gold-v2` permanece congelada até o handoff
aprovado da revisão da Maria.

## Freeze de artefatos

`npm run check:artifact-freeze` bloqueia dev/build se `public/artifacts` contiver
qualquer arquivo. O shell preserva as rotas desacopladas, mas não copia nem exibe
as páginas em revisão.

O simulador MAR-103 está integrado em `/simulador`, acessível pela navegação.
Calcula custos hipotéticos por mil views, interação e venda, sem preencher
dados comerciais inexistentes. Sua lógica pura permanece separada da UI.
Dashboard analítico e chat ainda não estão implementados.

## Desenvolvimento e validação

```bash
npm ci
npm run dev
npm run lint
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

Versões de Astryx, React, Next.js e ferramentas estão fixadas em `package.json`
e `package-lock.json`.
