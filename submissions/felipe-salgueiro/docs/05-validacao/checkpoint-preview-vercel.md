# Preview Vercel — publicação e validação

## Publicado

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
Necessário disponibilizar iab ou obter autorização de Felipe para usar Brave
pela extensão. Ready não significa QA.
