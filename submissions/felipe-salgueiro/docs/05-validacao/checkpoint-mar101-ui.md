# Checkpoint MAR-101 — shell Astryx e navegação

Data: 2026-09-23 20:47 BRT. Executor: Herdr `w2X:p8`, agente `g4-ui`.

Estado: **checkpoint técnico estável, sem commit e sem publicação**. Não é
`Done`, não foi encaminhado a QA humano e não inclui aceite visual por captura.

## Fronteira de execução

- Worktree: `/home/felipe/Work/worktrees/g4-mar101-ui`.
- Branch: `feature/mar-101-featg4-ui-estabelecer-shell-astryx-e-navegacao-entre`.
- HEAD de partida, não alterado: `23ae142333140b96caa5c7f0114b919c782c3aa5`.
- Manifest observado: `.pd/issue-flow/MAR-101.json`, estado `started`, modo B e
  E2E obrigatório. Linear MAR-101 foi observado em `Oferta`, projeto P-MAR-55.
- Não havia `PD_OMARCHY_DESCRIPTOR_REF` nem `PD_OMARCHY_CONVERSATION_ID`.
  O owner central observado era `null`; nenhum owner ou `launch_id` foi criado,
  transferido ou copiado da sessão Lia `w2X:p1`.
- Alterações limitadas a `solution/app/**` e a este checkpoint. `.pd/` é output
  prévio do runner e não foi editado.
- Nenhum stage, commit, push, PR, merge, deploy, publicação, mudança de issue ou
  leitura de credencial foi executado.

## Fontes e decisões aplicadas

Foram lidos plano MAR-101, RFC-001, parecer UX integral da Sofia,
`solution/reports/README.md`, documentação real do Astryx e as skills canônicas
`linear-start-issue`, `astryx-planejar-ui` e `qa-ui-e2e`.

O contrato integrado foi consultado somente em
`/home/felipe/Work/worktrees/g4-ai-master-felipe-20260923/submissions/felipe-salgueiro/solution/data/app/dashboard.json`.
Confirmaram-se `schema_version: 1`, `snapshot_id`, unidades `percent` e
`percentage_points`, evidências `ev-*`, recomendações `rec-q1..q8`, referências
`evidence_ids`, campos comerciais nulos e limites explícitos. O JSON não foi
editado, copiado, tipado nem transformado nesta Story.

## Implementação entregue

- Next.js/TypeScript com lockfile e versões diretas fixadas.
- Astryx real: `AppShell`, `Layout`, `Grid`, `Card`, `Heading`, `Text`, `Badge`,
  `Banner`, `EmptyState`, `Skeleton` e `Button`; tema neutral conectado.
- Identidade independente `C004 Insight Lab — Solução independente`, com navy e
  coral aproximados. Nenhum logo oficial e nenhuma paleta `gold-v2` integrada.
- Home orientada às oito decisões do Head de Social Media, sem navegação por
  orgânico/pago, números inventados ou regras econômicas.
- Navegação principal e rotas `/`, `/explorar`, `/relatorios`,
  `/relatorios/executivo` e `/relatorios/visualizador`, além de loading, empty,
  error, global-error e not-found.
- Query string preservada nos CTAs para relatórios; a MAR-101 não interpreta
  filtros nem implementa o dashboard MAR-105.
- Skip link, foco visível, semântica de headings, responsividade e suporte a
  `prefers-reduced-motion`.
- Nenhum LLM, login, API, servidor de banco ou SQLite no bundle.

O congelamento está restrito à integração de novas versões de
`solution/reports/**`, `solution/prototype/**` e `gold-v2`. O shell continua
ativo. As rotas dos artefatos exibem estado indisponível e não carregam iframe.
O guard `check:artifact-freeze` falha se `public/artifacts` contiver arquivos;
as cópias geradas numa tentativa anterior foram removidas. As fontes canônicas
não foram alteradas.

## Reservas MAR-103 preservadas

Estes paths não foram criados nem editados nesta worktree:

- `solution/app/src/lib/simulator.ts`;
- `solution/app/tests/simulator.test.mjs`;
- `solution/app/src/components/simulator/cost-simulator.tsx`;
- `solution/app/src/app/simulador/page.tsx`.

O fork MAR-103 `96731d0` é apenas referência para integração posterior pela
Lia. O shell não depende dele.

## Dependências fixadas

Produção: `@astryxdesign/core@0.6.3`,
`@astryxdesign/theme-neutral@0.6.3`, `@stylexjs/stylex@0.19.1`,
`next@16.3.6`, `react@19.3.0` e `react-dom@19.3.0`.

Desenvolvimento: `@astryxdesign/cli@0.6.3`,
`@playwright/test@1.63.0`, `typescript@5.9.3`, `eslint@9.39.5`,
`eslint-config-next@16.3.6` e tipos React/Node fixados no lockfile.

## Validação automatizada executada

| Comando | Resultado real |
|---|---|
| `npm run check:artifact-freeze` | PASS; nenhum asset de relatório/protótipo publicado. |
| `npx astryx doctor` | PASS; 5 checks, 0 warnings, 0 failures, 4 infos. |
| `npm run lint` | PASS, exit 0. |
| `npm run typecheck` | PASS, exit 0. |
| `npm test` | PASS; 2 testes, 0 falhas. |
| `npm run build` | PASS; Next `16.3.6`, seis rotas estáticas contando `/_not-found`. |
| `npm run test:e2e` | PASS; 12/12 em Chromium: 6 desktop e 6 mobile. |
| busca por `*.sqlite`, `*.sqlite3`, `*.db` em `public`/`.next` | PASS; nenhum resultado. |

Playwright manteve `screenshot`, `video` e `trace` em `off`. Nenhuma foto,
captura ou gravação foi produzida. O E2E monitora `console.error` e `pageerror`;
as rotas válidas ficaram limpas. A mensagem de rede do 404 é aceita somente
quando a própria resposta testada é `404` em `/rota-inexistente`.

## Matriz de QA e aceite

| Requisito | Estado | Evidência/limite |
|---|---|---|
| Shell Astryx e oito decisões | PASS | Build + DOM E2E, oito `h3`, sem números provisórios. |
| Rotas e query preservada | PASS | E2E desktop/mobile, incluindo teclado e Enter. |
| Navegação por teclado e foco | PASS | Skip link primeiro, foco visível calculado e CTAs focáveis. |
| Mobile e overflow | PASS | Seis rotas verificadas em Pixel 5 e desktop; diferença horizontal <= 1 px. |
| Hierarquia e legibilidade textual do shell | PASS | `h1 > h2 > h3`; cards com `h3 >= 18 px` e apoio `>= 14 px`. |
| Empty e not-found | PASS | Exercitados no browser; estados sem conversão de ausência em zero. |
| Loading/error em falha real | PENDENTE | Componentes compilam; não houve injeção de falha runtime nesta Story. |
| Console do browser | PASS | Sem erros nas rotas válidas; 404 intencional isolado. |
| JSON real -> UI | PENDENTE | Consumo pertence à integração/dashboard; contrato não foi copiado nem concorrenciado. |
| Simulador MAR-103 -> UI | PENDENTE | Quatro paths reservados à Lia; não integrados pela MAR-101. |
| Gráficos e HTMLs report/prototype | PENDENTE | Integração congelada; nenhum gráfico/iframe foi publicado ou avaliado. |
| Inspeção visual por imagem desktop/mobile | PENDENTE | `qa-ui-e2e` exige screenshot; restrição explícita proíbe captura. Não há `agent-browser` instalado. |
| Aceite humano/UX em aparelho real | PENDENTE | Não encaminhado; depende primeiro do item visual acima. |

Não há requisito em estado FAIL neste checkpoint. Isso não converte os itens
pendentes em aprovação visual ou funcional.

## Falhas encontradas e corrigidas

1. `@stylexjs/stylex@0.19.3` não existe; corrigido para `0.19.1`, compatível
   com o peer `^0.19.0` do Astryx.
2. `eslint@10.11.0` apresentou overrides de peer com Next; fixado em
   `eslint@9.39.5`. O npm alerta fim de suporte upstream desta major.
3. A preparação antiga de assets falhou com `EXDEV`; depois, a coordenação
   congelou esses artefatos. O copiador foi removido e substituído pelo guard
   que mantém `public/artifacts` vazio.
4. `Text type="caption"` não pertence à API Astryx `0.6.3`; substituído por
   `supporting`.
5. O QA ampliado detectou `h3` a 17 px e texto de apoio a 12 px. Os cards foram
   ajustados para 18 px e 14 px/1.5, e os 12 testes passaram.
6. A rota 404 intencional gera a mensagem de rede padrão no console. O teste
   valida status 404 e permite apenas essa mensagem nessa URL; qualquer outro
   erro continua reprovando.
7. npm v11 bloqueou scripts de instalação por política; nenhum foi aprovado.
   Os pacotes publicados continham os artefatos necessários e doctor/build/E2E
   passaram.

## Manifesto exato para integração

SHA-256 agregado das 28 linhas `sha256sum`, ordenadas por path e excluindo
`node_modules`, `.next`, `test-results` e `tsconfig.tsbuildinfo`:
`dbf2c979f875bbd70467ca315f80060dce070e5d995792238d9d11bf44063767`.

```text
25a8a1a80a0554a63c40f5154c910b924de790d1bace8b578ef855fa44a4495a  solution/app/.gitignore
5ffcc9d295f98227e25e425f855b83c5ad51e01b328ce853f09d877422ba845c  solution/app/README.md
cc6367e604d5e8b578856e7b93695ca31ea333ee190758ba13e748aa933902d5  solution/app/e2e/navigation.spec.ts
610d6bd1f9b6705c4148e0d2e32616cfb8cb1c7ccdde357dc7a4492dba6f7337  solution/app/eslint.config.mjs
1862ac4bbbc5192d4bf562161df66ea547ed3e67173100656ab606ae9797db2b  solution/app/next-env.d.ts
17ddb76ff0aeecab9ed6a3fe10f71576c1a8bff8cf6fd87739a1c09cae0ea4d4  solution/app/next.config.ts
9ee789c9fcfb156eb6e54e3ff51b6bb7e692b9468db3c4ffa4e05626cdce7f44  solution/app/package-lock.json
904e206afdf9fb63bb83c719b32400aa1f5f349b4b54494ee3c6aa5bb4dbe161  solution/app/package.json
d2fdae834b429ad68d5c683023765f2a12992d800ce403df452f88a4bc9c9982  solution/app/playwright.config.ts
4469ae9a95457ac813e1d335562467366d1d17600a39b5850565256aa650289c  solution/app/scripts/assert-artifacts-frozen.mjs
c532da1197e65846df490cc86803e421fd53c892bd75d84c9cf887c37f5b7f40  solution/app/src/app/error.tsx
493fba2bf5c759e715d3ea62a0de93ad2912845664ebfed31000731c218ee158  solution/app/src/app/explorar/page.tsx
7e51d5729c765b4a58440a8f52abe26f557154be41dc53a05b82b94bc9a07f21  solution/app/src/app/global-error.tsx
0fd1222577d72d5122e93572a90ca884701e5ff25fdcda3ce13613798ce1ff32  solution/app/src/app/globals.css
117eb4e0a85cfd0b5bcbee3285d57f17c1aad371dfc3fe00052912eb6d412e0b  solution/app/src/app/layout.tsx
19dd9cb28102139ab3b699eb3429a0cd7e4630a0dbf75509ff974444b5e1dde1  solution/app/src/app/loading.tsx
bb13d7dacb3dcb1532ac2fa08d7516c9e11a8fcf54406768fdfd62c75201c07e  solution/app/src/app/not-found.tsx
a4a17bc1f00e6ed8f5f15d00a9db6c9e73e70b8525b86e40570bf8edc3e55265  solution/app/src/app/page.tsx
9062f8dfce9eed403a5e21d0f63003b5ea045b02f19c7a5583a80b11c6959dc3  solution/app/src/app/providers.tsx
f418fa5dcdd20ec9f0519f3e8bd81ec5d6d4e9cf5844b958fab00ceb465559d3  solution/app/src/app/relatorios/executivo/page.tsx
917b8adf3f55d4e223d246a0b03c8d49dae1560a85fa8fccbfc672f922bdf4b5  solution/app/src/app/relatorios/page.tsx
c8216eb5442cf0938e9512d7b8c73eadb5785e78f03d3ccbf9202978d7ca255a  solution/app/src/app/relatorios/visualizador/page.tsx
538401503b42948f1e7bc2eba9678ec6a3ff60faab90beac15e5f37ecba4d3e3  solution/app/src/components/artifact-viewer.tsx
e8e231a744744e6469c82d25557a85be96996a4b6f2895e1d6e1e6bebcb1fcc4  solution/app/src/components/query-preserving-button.tsx
435851f28063c7d15ce49196173175185c025a894864604abdaf1b538d7847b8  solution/app/src/components/site-shell.tsx
851010d7c6747f76694b1880e20ddc7b9207902c692a8e64a7f3206a773b24a8  solution/app/src/lib/decisions.ts
309b3c12f2f9d8e8793b552c94d7f89df34c69d9f181cb0bdcc33c244e2b93e3  solution/app/tests/artifact-freeze.test.mjs
5563bf72ae43a35ad7902e45d2c0e491e6ac05cb1d35ea3b0c10e3711484903b  solution/app/tsconfig.json
```

Os paths acima são relativos a `submissions/felipe-salgueiro/`. O `.gitignore`
raiz ignora `submissions/`, portanto Lia deverá integrar explicitamente esses
28 arquivos e este checkpoint. Não integrar `node_modules`, `.next`,
`test-results`, `playwright-report`, `tsconfig.tsbuildinfo` ou
`public/artifacts`.

## Próxima integração

Lia pode conectar o `dashboard.json` e os quatro arquivos reservados da MAR-103
sem reestruturar o shell. Ainda deve manter os HTMLs e `gold-v2` desconectados
até o handoff aprovado de Maria. Antes de QA humano, permanece necessária uma
inspeção visual por imagem autorizada ou um mecanismo equivalente que não viole
a restrição atual de captura.
