# Correção da UI após reprovação de Felipe

## Causa e correção

O shell manteve tokens coral provisórios e placeholders do freeze mesmo com o
handoff revisado. A comparação usava formulário GET manual e texto livre; a
home exibia perguntas do desafio como títulos. Testes anteriores não cobriam a
fidelidade ao produto esperado. Não converter aquele PASS em aceite humano.

- Handoff 2d7b2b5 integrado por fast-forward, sem tocar SQLite/geradores.
- Navy #001F35, gold #B9915B, blue #184560 e fonte Manrope do handoff.
- Selector Astryx consultado no CLI: value/options/onChange, com navegação
  reativa, estado de atualização e limpeza de seleção dependente.
- Removido CSS genérico de formulário que alterava a anatomia do Selector.
- Recomendações agrupadas por decisão; perguntas/rules permanecem na evidência.
- Relatório/explorador acessíveis por iframe isolado e em tela inteira.
- Gerador público verifica hashes antes de escrever somente lista fechada de
  artefatos; não publica SQLite, scripts Python ou diretórios inteiros.

## Contratos e dados

Comparação profunda entre evidence.json anterior e atual: todos os campos
preexistentes idênticos; adicionado apenas executive_translation. Hash do
exportador atualizado conscientemente; dashboard.json permaneceu byte a byte
inalterado. Manifesto derivado atualizado. Banco SHA-256:
7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad.

## Verificação

- Lint e TypeScript: PASS.
- Build Next: PASS.
- Unitários Node: 27/27.
- Python, da raiz da submission: 10/10. Tentativa inicial no diretório analysis
  falhou por import solution; corrigido cwd, não alterados testes para ocultar falha.
- Playwright: 36/36, desktop/mobile emulado. Inclui mudança real de seletores,
  reset do grupo, recuperação de vazio, relatório/explorador carregados,
  teclado, ausência de overflow, simulador e chat fail-closed.
- QA por imagem: home, filtros, decisões e artefatos incorporados; capturas
  temporárias locais, não publicadas. Corrigida também margem mobile do viewer.
- Self-review autorizada: dados e regras preservados; sem segunda revisão por modelo.

Skills Astryx consultadas para API/tokens; Storybook não iniciado porque a
validação necessária é na aplicação consumidora. QA UI adaptado ao runtime
local; não executar scripts de Cadência em produto distinto.

## Limites

Sem deploy, PR upstream, auth provisionada ou inferência paga. Chat real segue
503 por segurança. Sem teste em celular físico nem aceite humano presumido.
HTMLs preservam o conteúdo do handoff; este patch não refaz análise estatística.
