# Challenge 004 Insight Lab — shell UI e simulador

Aplicação Next.js/TypeScript mínima para a MAR-101. Entrega chrome Astryx,
navegação acessível, estados técnicos e rotas reservadas para o relatório
executivo e o explorador.

## Limite da Story

A home consome diretamente o snapshot canônico de MAR-99 em
`../data/app/dashboard.json`. Não lê SQLite, não define contrato concorrente
e não inclui LLM, login ou servidor de banco.

A home apresenta oito recomendações com evidência, regra e limites, além de
comparações por plataforma, formato, categoria, seguidores e audiência.
O filtro GET `dimension`/`value` afeta só o painel comparativo; não recalcula
as conclusões gerais. Recortes vazios e combinações não exportadas têm estados
explícitos e ação de limpeza. A leitura valida unidade, contagens e referências;
contrato inválido aciona a página de erro em vez de mostrar números parciais.
Identidade navy/coral aproximada; não é um manual de marca oficial.

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
Chat e integração ao CRM ainda não estão implementados.

O build precisa da pasta `solution/`, não só de `app/`: Turbopack e tracing
resolvem a raiz um nível acima para importar o JSON sem duplicá-lo.
Não há dependência de SQLite no runtime.

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
