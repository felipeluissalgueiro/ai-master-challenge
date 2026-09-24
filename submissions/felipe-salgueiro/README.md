# Submissão — Felipe Salgueiro — Challenge 004

**Preview publicada; pacote preparado para PR.** [Abrir aplicação](https://g4-social-insight-da2ghmdai-felipeluissalgueiros-projects.vercel.app), sem login. Pipeline, dashboard, relatórios, explorador e simulador integrados. Fluxo principal e correções retestados no Brave; [cobertura e limites](docs/05-validacao/checkpoint-qa-brave.md). [Estado do deploy](docs/05-validacao/checkpoint-preview-vercel.md).

## Sobre mim
- **Nome:** Felipe Salgueiro.
- **LinkedIn:** [Felipe Luis Salgueiro](https://www.linkedin.com/in/felipe-luis-salgueiro/).
- **Challenge:** 004 — Estratégia Social Media.

## Executive Summary
Escolhi o case pela minha experiência com marcas e conteúdo. Usei IA para investigar uma base sintética e transformar a análise em dashboard, relatório executivo e explorador. As diferenças descritivas não justificam prometer um canal vencedor ou retorno financeiro sem custos e conversões. Recomendo testes orientados ao objetivo da campanha e medição antes de ampliar ou cortar investimentos; um simulador separado permite explorar custos hipotéticos sem inventar vendas.

## Solução

### Acesso e roteiro de avaliação

Abra a **[Preview pública](https://g4-social-insight-da2ghmdai-felipeluissalgueiros-projects.vercel.app)** no navegador. Não precisa de conta, senha, chave de API ou instalação.

1. **Performance e decisões:** leia os três cards e o plano de ação proposto. Eles separam engajamento observado, condições de patrocínio e lacunas para decidir cortes.
2. **Comparações:** escolha dimensão e grupo. A URL e o painel comparativo mudam; as conclusões gerais não são recalculadas pelo filtro.
3. **Ver relatórios:** abra o relatório executivo para consultar as oito respostas, gráficos e provas. Use a opção de tela inteira para leitura ampliada.
4. **Explorar dados:** consulte o dicionário e os recortes do Ouro. O navegador lê artefatos exportados; não acessa o SQLite diretamente.
5. **Simulador:** escolha o escopo e informe um período comum (ex.: “1 a 7 de outubro”). Exemplo: R$ 2.000, 10.000 views, 2.000 interações e 20 vendas resultam em R$ 200 por mil views, R$ 1 por interação e R$ 100 por venda. Esses valores são hipotéticos, não resultados do dataset.

Para rodar localmente, clone o fork e siga o [setup da aplicação](solution/app/README.md). Para conferir a origem dos números, consulte o [banco de evidência](solution/data/evidence/README.md). O snapshot é sintético e estático: não é um painel conectado aos canais ou CRM do G4.

[Relatório executivo para o Head de Marketing](solution/reports/README.md): oito respostas organizadas em três pilares, provas numéricas e estratégia. Acesse pela aplicação ou baixe/clone e abra `solution/reports/performance-strategy.html` no navegador.

As versões iniciais foram reprovadas por mim e reformuladas para leitura gerencial. As correções e os limites dos testes estão nos [checkpoints](docs/05-validacao/).

[Aplicação e setup](solution/app/README.md), [contrato de dados](solution/data/app/README.md) e [simulador](docs/05-validacao/checkpoint-mar103-simulator.md): cálculo determinístico de custo por mil views, interação e venda; cenário hipotético, não resultado comercial observado.

[Explorador dos dados Ouro](solution/prototype/README.md): disponível na aplicação e como HTML local em `solution/prototype/index.html`. O GitHub exibe o código-fonte; a Preview permite navegar.

### Abordagem

1. **Comecei pela decisão do gestor, não pelo gráfico.** Escolhi Social Media pela proximidade com minha experiência em gerir marcas e produzir conteúdo. Queria responder o que continuar fazendo, quando patrocinar e o que interromper. Comparei os cases com apoio das personas de Marketing e Desenvolvimento, mas mantive comigo a escolha e a revisão do resultado.
2. **Confrontei minha experiência com o que a base realmente permite.** Trouxe critérios que uso em conteúdo: views, retenção nos primeiros três segundos e comentários como pistas para novos ganchos. Pedi verificar esses campos antes de desenhar a solução. Não transformei métricas ausentes nem textos sintéticos em evidência de comportamento real.
3. **Separei as perguntas em análise, estratégia e ferramenta de decisão.** Pedi uma frente independente de auditoria enquanto discutia os requisitos com o time de agentes. O planejamento passou por [Brief](docs/01-brief/brief.md), [PRD](docs/02-prd/prd.md), arquitetura e [tarefas](docs/04-planejamento/issues/README.md). Os documentos preservam propostas históricas; nem toda capacidade discutida virou implementação.
4. **Exigi uma origem verificável para cada número.** Preservei a fonte na Bronze, validei e derivei métricas na Prata e produzi comparações na Ouro. Mantive o SQLite reconstruível no fork para auditoria e usei exportações estáticas na aplicação, evitando banco e infraestrutura adicionais no deploy. O [contrato de dados](solution/data/app/README.md) explica o consumo.
5. **Distingui engajamento de aquisição e venda.** Meu racional é que conteúdo pode ser um canal de aquisição, mas seu retorno precisa ser medido conforme o objetivo. Como faltam custos e conversões, preferi um simulador explícito a inventar ROI. CRM, atribuição e modelo especializado de marketing ficaram como evolução, não entrega atual.
6. **Reduzi escopo e revisei a usabilidade.** Considerei aproveitar o Cadência inteiro, depois optei por uma aplicação mais simples. Separei relatório executivo, explorador e dashboard; reprovei versões com números sem contexto e pedi conclusão, justificativa e ação. Retirei o chat com LLM para concentrar a entrega em análise verificável e navegação funcional.
7. **Validei antes de preparar a submissão.** Usei gates de lint, tipos, testes e build, além de QA no Brave e correções após minha leitura. Autorizei revisão pelo próprio modelo para equilibrar prazo e qualidade, sem declarar revisão independente inexistente. A [matriz de validação](docs/05-validacao/submission-audit.md) distingue cobertura comprovada de limites.

O [diário do processo](process-log/workflow.md) preserva a sequência, mudanças de ideia e intervenções; os [exports multiagente](process-log/chat-exports/README.md) mostram mensagens visíveis de 15 sessões. Esta seção é a síntese das decisões registradas, não uma reconstrução de raciocínio interno dos modelos.

### Resultados / Findings
Pipeline analítico, banco de evidência, exportador e comparações descritivas integrados. A análise utiliza 52.214 posts; os resultados e suas provas estão no relatório executivo. [Reprodução e artefatos](solution/README.md).

- Nas dimensões de conteúdo, a maior diferença entre medianas equivale a cerca de 1,7 interação por 10 mil views: não basta para escolher um vencedor de negócio.
- Das 60 células de patrocínio comparáveis, 33 favoreceram posts marcados como patrocinados e 27 os demais; o sentido mudou entre faixas de seguidores em 14 de 15 combinações.
- Retorno financeiro permanece desconhecido. O simulador separa explicitamente hipóteses comerciais dos resultados da base.
### Recomendações

1. **Definir objetivo e medição antes de investir.** Para engajamento, acompanhar interações por views; para aquisição e vendas, registrar custos e conversões com rastreamento e CRM. Sem isso, não recomendo escolher canais por suposto retorno financeiro.
2. **Testar conteúdo em recortes comparáveis.** As diferenças pequenas entre grupos não justificam reorganizar a produção só pelo ranking da base. Formular uma hipótese por teste e avaliar contexto, volume e consistência antes de escalar.
3. **Tratar patrocínio como experimento, não regra universal.** A divisão de 33 contra 27 células e as mudanças entre faixas de seguidores não sustentam um perfil vencedor universal. Escolher parceiros pela aderência ao objetivo e à audiência e pactuar medição antes do investimento.
4. **Não recomendar cortes financeiros sem evidência financeira.** Interromper a prática de decidir apenas por seguidores ou médias agregadas; a base não permite declarar que um investimento específico desperdiçou dinheiro.
5. **Executar os primeiros passos nesta semana.** Definir objetivo e indicadores, selecionar uma hipótese de conteúdo e uma de parceria, registrar o cenário no simulador e preparar a coleta comercial. São ações propostas a partir das lacunas e dos achados, não ganhos já demonstrados.

O [relatório executivo](solution/reports/README.md) detalha as oito perguntas, números e condições. O plano semanal é proposto, não uma série temporal real do G4.

### Limitações

- **Fonte e causalidade:** dataset sintético. Comparações são descritivas; associação não prova causa. A marcação de patrocínio não comprova compra de mídia nem permite calcular seu retorno.
- **Criativo e audiência:** faltam retenção de 3s e evidência real dos comentários para testar meus critérios de gancho e conteúdo. Campos textuais sintéticos não representam a voz real de consumidores.
- **Negócio:** sem alcance, impressões, custos ou conversões, não determinei ROI, CAC, custo por venda observado nem um threshold de investimento validado. O simulador calcula cenários informados pelo usuário.
- **Tempo e recorrência:** o snapshot não sustenta recomendações de frequência de postagem nem “insights desta semana” como monitoramento real. Não há integração ativa com canais ou CRM.
- **Escopo entregue:** chat/LLM, SLM especializado e atribuição comercial não foram implementados na versão final. Não anexei notebook; disponibilizei scripts, banco, manifestos, relatórios e aplicação.
- **Validação:** os gates e o QA cobrem os casos registrados, não todos os dispositivos ou uma auditoria completa de acessibilidade. O [checkpoint do Brave](docs/05-validacao/checkpoint-qa-brave.md) explicita o que foi testado.

#### O que retirei e o que faria com mais tempo

**Decisões de corte para esta entrega:** não portar o Cadência inteiro; não hospedar SQLite como backend; não acrescentar autenticação a um painel público sem dados privados; retirar o chat com LLM. Mantive o banco como evidência no fork e o deploy com dados estáticos. Também deixei de perseguir um modelo preditivo experimental para não desviar da análise e da estratégia obrigatórias. Esses cortes preservaram o núcleo da entrega e reduziram dependências.

**Próximo ciclo, em ordem de prioridade:**

1. **Validar com dados reais e um gestor.** Testar a compreensão das recomendações e coletar métricas de conteúdo, retenção e audiência com definições consistentes. Só então propor uma cadência recorrente de atualização.
2. **Conectar resultados comerciais.** Integrar custos, links/cupom e CRM para acompanhar leads e vendas por campanha/parceiro, explicitando limites de atribuição. Separar custo por venda de CAC, que exige identificar novos clientes e delimitar quais custos entram no cálculo.
3. **Validar critérios de decisão.** Comparar o creator com seu próprio histórico e, havendo fonte comparável, com benchmark externo. Testar regras determinísticas antes de definir thresholds ou automatizar recomendações; não tratar benchmark ilustrativo como resultado medido.
4. **Ampliar qualidade e operação.** Completar a matriz de QA mobile/acessibilidade, testar atualização dos dados e monitorar o uso. A implantação atual é uma Preview, não uma operação de marketing integrada.
5. **Reavaliar assistência por IA.** Retomar uma conversa contextual sobre a recomendação, restrita às evidências, com avaliações de respostas, autenticação e controles de custo. Um SLM especializado em marketing foi uma proposta futura minha, condicionada a dados, acesso e validação; não um modelo treinado ou disponível neste projeto.

Mais tempo, sozinho, não resolveria a ausência de dados comerciais nem transformaria uma base sintética em evidência de retorno real.

## Process Log — Como usei IA

### Organização e quality gates

Segui meu **Dev Workflow do PD Framework**: briefing → PRD → RFC/arquitetura → decomposição em tarefas → implementação → validação → Preview → revisão humana → preparação da PR. Usei Linear para organizar o trabalho, Obsidian para registrar decisões e Git para checkpoints. A [documentação por etapa](docs/README.md) e as [tarefas exportadas](docs/04-planejamento/issues/README.md) permitem conferir esse processo sem acesso às minhas ferramentas privadas.

Separei as frentes de dados, interface, UX e QA e revisei os handoffs antes da integração. As personas são papéis de IA do meu OS de agentes, não uma equipe humana adicional. Usei DRY, facilidade de mudança e separação de responsabilidades como critérios de arquitetura.

Para equilibrar prazo e qualidade, **autorizei a revisão pelo próprio modelo em vez de exigir revisão por pares/múltiplos modelos**. Essa simplificação não dispensou os gates técnicos: lint, tipos, 19 testes unitários da aplicação, 10 testes Python do exportador e build passaram na revisão registrada. O QA visual e funcional teve checkpoints e retestes no Brave; mantive explícita sua cobertura limitada. Não afirmo que cada commit passou novamente por todos esses gates.

O histórico preserva erros e correções: relatório difícil de ler, navegação/âncoras, linguagem do simulador e redução de escopo. O [registro de validação](docs/05-validacao/submission-audit.md) mostra evidências e pendências, em vez de usar o método como garantia abstrata de qualidade. **Publicar a Preview e preparar a branch não equivale a enviar a PR.**
### Ferramentas usadas
Codex apoiou análise, implementação, documentação e QA por agentes com papéis definidos; Gemini apoiou uma consulta sobre a transcrição de podcast trazida por mim. Usei Herdr para coordenar sessões, Linear para planejar, Obsidian para o diário e Git para versionar a evolução. Python/SQLite fizeram os cálculos determinísticos; FFmpeg preparou o vídeo. [Método de trabalho](docs/metodo/README.md).
### Workflow
1. Comparei os cases e escolhi Social Media pela aderência à minha experiência.
2. Pedi auditoria dos dados antes de fechar recomendações e requisitos.
3. Organizei briefing, PRD, arquitetura e tarefas; agentes trabalharam em frentes delimitadas.
4. Revisei a linguagem dos relatórios, questionei hipóteses e reduzi o escopo.
5. Exigi testes, evidências, publicação em Preview e QA no navegador.

O [registro detalhado](process-log/workflow.md) documenta as iterações por frente. Não há contagem auditada de todos os prompts; os ciclos documentados não são apresentados como total exato.
### Onde a IA errou e como corrigi
Uma lembrança sobre Tallis não foi confirmada e deixou de sustentar a escolha. Questionei o PRD elaborado sem discussão suficiente, reprovei relatórios tecnicamente corretos mas difíceis de usar e pedi conclusões, números contextualizados e ações. Também retirei o chat para concentrar a entrega no que já estava sustentado por dados. Os prints e o workflow mostram essas intervenções.
### O que eu adicionei que a IA sozinha não faria
Trouxe meu contexto de marcas/conteúdo, propus examinar gancho/contexto/informação/chamada se houver dados e defini o foco do projeto. São contribuições observáveis, não alegações de exclusividade humana.

## Evidências
- [Histórico Git da branch de submissão](https://github.com/felipeluissalgueiro/ai-master-challenge/commits/submission/felipe-salgueiro/) e [guia dos checkpoints](process-log/git-history.md) — evolução real do código, correções e decisões de escopo.
- [Revisão contra o guia e cobertura das oito perguntas](docs/05-validacao/submission-audit.md).
- [Planejamento e issues exportadas](docs/04-planejamento/issues/README.md) — leitura no próprio repositório, sem depender do Linear ou da renderização do GitHub Projects.
- [Projeto e marcos](docs/00-projeto/README.md).
- [Documentos por etapa](docs/README.md).
- [Pesquisa preparatória e ressalvas](docs/01-brief/pesquisa/README.md).
- [Workflow](process-log/README.md), [cinco screenshots comentados](process-log/evidencias/README.md) e [proveniência dos exports](docs/proveniencia.md).
- [Conversas de 15 sessões do projeto](process-log/chat-exports/README.md), com [legenda das personas](process-log/README.md#quem-são-as-personas-mencionadas).

O [snapshot integral do banco](solution/data/evidence/README.md) está no fork com manifesto e limites conhecidos; a aplicação usa exportações Ouro, sem SQLite no deploy. O histórico Git registra a evolução, sem retroagir datas. Incluí uma [seleção de vídeo do processo](process-log/videos/README.md), de 24 segundos, com cortes documentados; gravações brutas e notebook não foram anexados. Chat com LLM e integração ao CRM não fazem parte da versão entregue.

**Submissão enviada em:** não enviada.
