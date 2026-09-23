# MAR-103 — núcleo do simulador

Estado: função pura e testes implementados; formulário, integração e QA visual
pendentes. Não é funcionalidade de UI pronta nem issue concluída.

## Contrato

`simulateCosts(Scenario)` recebe custo em BRL, views, interações e vendas
hipotéticos, além de escopo (`post` ou `campaign`) e período de custo/resultados.
Os dois escopos e períodos precisam coincidir; não é permitido dividir custo de
campanha pela mediana de um post. Essa verificação depende da declaração de
entrada, não de integração CRM inexistente.

Retorna custo por mil views, por interação e por venda, cada um com estado e
motivo. Não calcula CAC, ROI ou atribuição real. Ausência/denominador zero
retornam null, não zero; custo zero com resultado positivo pode retornar zero.
Vendas devem ser inteiras e seguras; valores negativos, não finitos e tipos
inválidos são rejeitados. Precisão é preservada no cálculo e arredondada apenas
na formatação monetária. Não usa LLM ou rede.

## Evidência local

- `node --test solution/app/tests/simulator.test.mjs`: 10 testes PASS.
- TypeScript 5.9.3: `tsc --noEmit --strict --skipLibCheck --target ES2020 --module nodenext solution/app/src/lib/simulator.ts`, exit 0.
- ESLint 9.39.5: dois arquivos via stdin usando configuração Next/TypeScript do shell MAR-101, exit 0, sem achados.
- JSCPD 5.3.2: dois arquivos com min-tokens 50/threshold 3, exit 0.
- R$ 2.000 / 20 vendas = R$ 100/venda validado, além de zeros, vazios,
  negativos, NaN/Infinity, vendas fracionárias, escopos/períodos incompatíveis,
  precisão, overflow e imutabilidade.

| Artefato | SHA-256 |
|---|---|
| solution/app/src/lib/simulator.ts | 1fefdd48c1168e73e8428f4b96f3c91feb76579b610c9d01fe9f89be5712ece5 |
| solution/app/tests/simulator.test.mjs | e154eee5f30a37f2a3735334edeef2619df31ad8fec28ee1aba13249f67eb1cf |

Autorrevisão por Lia/modelo executor: conferidos fórmulas/unidades, nulidade,
limites numéricos, ausência de dependências e separação entre cálculo/formatação.
Não é revisão por pares. A UI deve identificar cenário hipotético e pedir
entradas do mesmo escopo/período; testes de função não comprovam essa jornada.
Sem alterações em relatórios, paleta, dados, credenciais ou deploy.
