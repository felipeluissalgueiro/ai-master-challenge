# Revisão de conformidade da submissão

Fontes: [guia](../../../../submission-guide.md),
[CONTRIBUTING](../../../../CONTRIBUTING.md),
[template](../../../../templates/submission-template.md) e
[Challenge 004](../../../../challenges/marketing-004-social/README.md).
Base oficial consultada: `4aed364d572fabe0f1fff1f0c6f32960b30fe575`.

## Requisitos de envio

| Requisito | Evidência / estado |
|---|---|
| Uma solução para um challenge | 004; análise, estratégia e aplicação |
| Pasta exclusiva | Diff contra main oficial restrito a submissions/felipe-salgueiro |
| README baseado no template | Identificação, LinkedIn confirmado, resumo, abordagem, resultados, recomendações, limites, processo e evidências |
| Process log obrigatório | Narrativa, ferramentas e motivos, decomposição, erros/correções, contribuição humana e iterações por frente |
| Evidências de IA | Cinco screenshots, vídeo, narrativa, evolução Git e 15 exports de sessões com legenda das personas; formatos complementares |
| Código com setup | Clone/branch, Node 24, npm ci/dev, localhost, testes/build; sem framework privado ou credenciais necessários |
| Acesso à solução | Preview pública e HTMLs locais; SQLite no fork, fora do deploy |
| Um PR por pessoa, para main | Nenhuma PR dessa branch encontrada na consulta; envio ainda pendente |
| Título correto | [Submission] Felipe Salgueiro — Challenge 004, preparado no rascunho |

## Oito perguntas do Challenge

| Pergunta | Onde encontrar | Limite explícito |
|---|---|---|
| Engajamento por plataforma/formato/categoria/creator | Relatório, Pilar 1 e tabelas do apêndice; explorador | Descritivo; quartis de seguidores no post, não classificação estável do creator |
| Patrocínio funciona? | Pilar 2, comparação geral e 60 células comparáveis | Flag não comprova distribuição orgânica/paga; views não são alcance; não há custo/ROI observado |
| Perfil de audiência | Pilar 1 e nove cruzamentos no apêndice | Rótulos predominantes, não distribuição individual dos engajados |
| O que não funciona? | Pilar 1, limites e cobertura | Nenhum desperdício econômico comprovado; não inventar cortes |
| Onde concentrar esforço e frequência | Pilar 3 | Ranking insuficiente; frequência não inferível de datas aleatórias |
| Política de patrocínio e threshold | Pilar 2 e regra de decisão | Política proposta; limiar econômico depende de custo/margem/conversão não presentes |
| O que parar | Pilar 3 | Parar de usar ranking/seguidores como critério isolado, não alegar canal deficitário |
| Quick wins | Plano em cinco passos e próximo ciclo | Ações propostas e priorizadas, não resultados observados |

O texto do enunciado sugere que a flag permite calcular ROI diretamente. A
submissão explica por que a fonte real não permite isso: faltam investimento e
resultado financeiro. Cobrir a pergunta não significa fabricar o número pedido.
Dashboard e simulador são o diferencial; modelo preditivo não é obrigatório.

## Verificações executadas nesta revisão

- Inventário: 163 arquivos versionados antes desta revisão, 91 Markdown.
- Todos os links relativos de arquivos dos Markdown conferidos: zero destinos ausentes. Não é teste de todos os links externos ou âncoras Markdown.
- Texto completo do relatório executivo lido e mapeado às oito perguntas.
- Varredura de padrões de credenciais nos arquivos textuais versionados: zero achados; não equivale a garantia universal de ausência de segredo.
- Nenhum .env, node_modules, .next ou configuração privada Vercel versionado.
- SQLite: integrity_check=ok, SHA-256 preservado; manifests do relatório e exportador reconciliados com os arquivos referenciados.
- 10 testes Python do exportador passaram (determinismo, contrato, proteção e snapshot).
- Lint, TypeScript, 19 testes unitários da aplicação e build passaram.
- [QA Brave](checkpoint-qa-brave.md): reteste confirmou as duas correções, fluxo principal, simulador, 404 e recorte mobile.
- Reteste final da microcopy de erros no simulador aprovado no Brave na Preview da2ghmdai.
- Exports de chat: 15 sessões identificadas por ID completo e vínculo ao projeto; 1.013 mensagens visíveis, com sanitização e exclusões declaradas. Não são 1.013 execuções independentes.

## Limites que permanecem

- Não foi reexecutado todo o pipeline desde o CSV nesta revisão; execução histórica está nos checkpoints.
- QA no navegador é direcionado, não auditoria integral de acessibilidade ou matriz mobile de todas as páginas.
- Vídeo revisado por quadros a cada segundo; gravações brutas não publicadas.
- Documentos de planejamento preservam snapshots históricos; índices e README orientam o escopo atual.
- O time budget sugerido é 4–6h. Não há medição auditada de horas totais; não declaramos que esse limite foi cumprido.
- Revisão humana do conteúdo final e envio da PR não são substituídos por este documento.

**Parecer:** estrutura e artefatos exigidos presentes, com limitações analíticas e
de validação declaradas. Não foi identificada falta de formato obrigatório.
Não é garantia de aprovação pelo avaliador nem alegação de auditoria exaustiva
de cada linha de código ou documento histórico.
