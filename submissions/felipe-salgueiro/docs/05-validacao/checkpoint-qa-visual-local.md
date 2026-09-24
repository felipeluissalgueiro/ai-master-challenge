# QA visual local — dashboard, simulador e formulário do chat

Data: 23/09/2026. Lia, inspeção efetiva das imagens da aplicação.
Escopo local: Chromium 1440×900 e 390×844, não aparelho físico.

## Método e resultado

Skill qa-ui-e2e consultada: scripts originais do Cadência não são aplicáveis
a este repo; nenhum endpoint/tenant Cadência foi acessado. A verificação
agent-browser foi adaptada para Playwright já instalado, pois a CLI não está
disponível. Isso não é declaração de PASS do gate cross-stack Cadência.

Foram capturados e vistos: home, recomendações, formulário do chat, formulário
do simulador e resultados. Nenhum pane, conversa, desktop ou vídeo foi capturado.

Achados corrigidos:
- Mobile sem margem lateral: 16px aplicados ao conteúdo.
- Menu mobile ocultava destinos em rolagem horizontal: grade com duas colunas.
- Links indistinguíveis de texto: cor e sublinhado.
- Badge esticado por flex: envoltório ajustado.
- Botão de relatórios com contraste insuficiente: fundo #c43f37 e texto #fff,
  razão calculada 5,11:1. Uma regra do menu sobrescrevia o branco; corrigida
  e cores computadas verificadas em teste browser.

Após correções: imagens conferidas novamente, build/TypeScript e 34/34
cenários browser passaram. Novo teste fixa margens, menu sem overflow e
cores reais do botão. Os 27 unitários já verdes não foram repetidos para CSS.
Primeira inspeção de console/pageerror: arrays vazios em desktop/mobile.

## Evidência local

Capturas temporárias em /tmp/g4-visual-qa-hnj3SZ; não anexadas ao fork nem
selecionadas como screenshots finais de submissão.

- mobile-approved-local.png: d1461433ed43139a90340d93e656742c000332125cbfa64668a738ea72dd5854
- desktop-approved-local.png: 627cfa5bc7028837a067a8ee071bebe034fccc1a4a05425e6cab6a9fe51720ed

O sufixo dos arquivos significa revisão local pelo agente, não aceite de Felipe.
As imagens temporárias podem ser removidas pelo sistema; hashes registram
somente as versões inspecionadas.

## Limites

QA visual local concluído para os estados inspecionados, sem auditoria completa
de acessibilidade, teste de celular físico, aceite humano ou validação em deploy.
Relatórios externos em revisão não foram avaliados nem integrados.
Chat real continua fechado; testes de resposta usam mocks e não validam
autenticação, quota global ou comportamento de uma LLM real.
