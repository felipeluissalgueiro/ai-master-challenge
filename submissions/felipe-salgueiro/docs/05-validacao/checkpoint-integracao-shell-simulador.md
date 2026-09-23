# Integração MAR-101 + MAR-103

Data: 23/09/2026. Executora: Lia. Estado: integrado e validado tecnicamente;
QA visual, aceite humano, deploy e conclusão das issues permanecem pendentes.

## Origem e alterações

Handoff estável do executor g4-ui: 28 arquivos do app; manifesto e testes
próprios em [checkpoint MAR-101](checkpoint-mar101-ui.md).
SHA-256 do checkpoint recebido e conferido:
`95e2b3cbf1cc23430591ea65a7cb0f1170355594aa8ba601d5ecd61039047868`.

Preservei o simulador já publicado. Acrescentei o link “Simular custos”,
atualizei o README e ignore de cache TypeScript. Não alterei SQLite,
reports/prototype, paleta gold-v2 ou a worktree do executor.

## Validação reexecutada na branch de entrega

- Instalação limpa pelo lockfile: 431 pacotes, audit informou zero vulnerabilidades;
  scripts de instalação desativados. Aviso de suporte encerrado do ESLint 9 preservado.
- ESLint, TypeScript e build Next: PASS; sete rotas, incluindo /simulador e 404.
- Unitários: 12/12 PASS (10 simulador + 2 guard de artefatos).
- Browser Chromium: 20/20 PASS, 10 desktop e 10 mobile.
- Rotas incluídas na checagem de overflow: simulador, shell e relatórios.
- Screenshots, vídeo e trace desligados. Esses testes não equivalem a QA visual.

Primeira rodada de navegador: 17/20. O seletor global de alerta colidiu com
o anunciador de rotas do Next em dois cenários; o seletor global do Banner
encontrou uma duplicação transitória no mobile. Corrigidos escopos sem remover
asserções: alerta dentro da região do simulador e Banner dentro do conteúdo
principal. Segunda rodada: 20/20, mantendo validação de erro e valores esperados.

## Revisão e limites

Autorrevisão conforme autorização de Felipe, sem revisão independente.
Regras de cálculo continuam no módulo puro; formulário não duplica fórmulas.
Ausência comercial não vira zero; alteração de hipótese invalida resultado.
Não houve chamada de LLM, leitura de credencial ou publicação de aplicação.
Dados reais do snapshot ainda não alimentam a home; isso pertence à MAR-105.
As novas versões dos relatórios continuam congeladas até handoff revisado.
