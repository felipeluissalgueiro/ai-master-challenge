# Challenge 004 Insight Lab — aplicação de decisão

Aplicação Next.js/TypeScript com componentes Astryx, dashboard, simulador,
relatório executivo e explorador de dados. Tema navy/gold e fonte Manrope
alinhados aos artefatos revisados, sem se apresentar como produto oficial G4.

## Limite da Story

A home consome diretamente o snapshot canônico de MAR-99 em
`../data/app/dashboard.json`. Não lê SQLite, não define contrato concorrente
e não inclui LLM, login ou servidor de banco.

A home apresenta oito recomendações com evidência, regra e limites, além de
comparações por plataforma, formato, categoria, seguidores e audiência.
Seletores Astryx atualizam `dimension`/`value` imediatamente na URL; trocar dimensão
limpa o grupo anterior. O filtro afeta só o painel comparativo; não recalcula
as conclusões gerais. Recortes vazios e combinações não exportadas têm estados
explícitos e ação de limpeza. A leitura valida unidade, contagens e referências;
contrato inválido aciona a página de erro em vez de mostrar números parciais.
As oito recomendações são organizadas em conteúdo/audiência, patrocínio e
próximo ciclo, com títulos de decisão. Enunciados e regras não são a navegação.

## Artefatos revisados

O handoff `2d7b2b5` substitui o freeze anterior. `npm run prepare:artifacts`
confere hashes fixos e copia somente cinco arquivos de reports/prototype e a
fonte local para `public/artifacts`, ignorado do Git. Dev/build executam essa
preparação; arquivos inesperados (incluindo SQLite) são recusados.
Não há cópia recursiva nem fonte de dados concorrente. Mudanças de hash exigem
revisão explícita do próximo handoff. Relatório e explorador usam iframe
isolado e oferecem abertura em tela inteira; links relativos são preservados.

O simulador MAR-103 está integrado em `/simulador`, acessível pela navegação.
Calcula custos hipotéticos por mil views, interação e venda, sem preencher
dados comerciais inexistentes. Sua lógica pura permanece separada da UI.
Chat contextual tem UI, montagem de contexto e transporte OpenRouter implementados
e testados com mocks. A rota real retorna 503 até autorização e quota global
serem implementadas/verificadas; `chat-policy.ts` falha fechado, sem flag de bypass.
Veja [checkpoint MAR-102](../../docs/05-validacao/checkpoint-mar102-chat.md).
Integração ao CRM ainda não está implementada.

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
