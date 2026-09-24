# Preview Vercel — publicação e validação

## Publicado

### Correção final de microcopy

- Preview: https://g4-social-insight-da2ghmdai-felipeluissalgueiros-projects.vercel.app
- Deployment: `dpl_DMNmSJHAXAPa2KQGUgYv2zT4Uvm2`; target preview e Ready confirmados por `vercel inspect`.
- Única alteração funcional de apresentação: nomes dos campos nas mensagens de erro em português; nenhuma fórmula alterada.
- 19 testes unitários, lint, tipos e build passaram; ver reteste no [checkpoint Brave](checkpoint-qa-brave.md).

### Revisão anterior após QA

- Preview atual: https://g4-social-insight-the4349yo-felipeluissalgueiros-projects.vercel.app
- Deployment `dpl_3c4p61YaXRvN4LPdhUJhMEA8JwVU`: target preview e Ready confirmados por `vercel inspect`.
- Correções: menu do relatório sem sobreposição em âncoras e filtros traduzidos.
- Lint, typecheck, 18 testes unitários e build passaram localmente; reteste remoto registrado no [checkpoint Brave](checkpoint-qa-brave.md).
- Dados evidence.json e SQLite preservados. Sem novo domínio, credencial ou serviço.

### Primeira Preview (histórico)

- Projeto dedicado: g4-social-insight, sem domínio personalizado.
- Código: 5fca9b2 + filtro de upload solution/.vercelignore.
- Raiz de upload solution; raiz de build app; arquivos externos à raiz habilitados.
- Node 24, Next.js, npm ci e npm run build.
- Preview: https://g4-social-insight-1e2g3f722-felipeluissalgueiros-projects.vercel.app
- Deployment dpl_8SoT2viBwVyBdzvCPJfB2iHV93Ab: target preview, status Ready,
  confirmados com vercel inspect.
- Login Vercel desativado somente neste projeto após autorização explícita de
  Felipe. Sem chave OpenRouter ou login próprio.
- SQLite, CSVs, scripts analíticos, dependências locais e caches excluídos do
  upload; fontes e artefatos públicos reconstruídos pelo build.

## Divergência registrada

A primeira chamada CLI, apesar de --target preview, gerou deployment classificado
como production: dpl_7dMjfPYaW838A1DBSJDEVZGfobz6. O provedor criou aliases
automáticos g4-social-insight.vercel.app e
g4-social-insight-felipeluissalgueiros-projects.vercel.app.
Nenhum domínio personalizado, DNS ou aplicação existente foi alterado.
A segunda chamada gerou a Preview correta. O primeiro deployment não foi
apagado ou despublicado sem autorização; não confundir os dois ambientes.
Há relato compatível no upstream:
https://github.com/vercel/vercel/issues/17069

## QA remoto

Felipe pediu um subagente para validar diretamente no navegador in-app, sem
Playwright. Camila foi acionada após criação da Preview com a matriz de
dashboard, filtros, relatórios, explorador, simulador, navegação e falhas.
QA BLOQUEADO antes da navegação: subagente e sessão principal retornaram
`Browser is not available: iab`. Diagnóstico documentado mostrou somente
extensão Brave disponível. Nenhum fallback executado: zero rotas testadas,
zero rodadas completas, nenhum PASS atribuído. Não é falha comprovada da aplicação.
Felipe esclareceu em seguida que se referia ao Brave conectado e autorizou
explicitamente seu uso. O mesmo subagente foi retomado para executar a matriz
pela extensão, sem Playwright. A rodada parcial foi concluída:
[cobertura, achados e correções](checkpoint-qa-brave.md). Duas falhas de
apresentação encontradas, corrigidas localmente e aguardando reteste.
Ready não significa QA.
