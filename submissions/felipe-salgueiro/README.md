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

**Por que escolhi o 004.** Minha experiência combina gestão de marcas, criação de conteúdo e construção de ferramentas de marketing no Cadência. O desafio permitia conectar essas três frentes: analisar performance, propor uma estratégia e demonstrar como a análise pode virar uma decisão recorrente. Eu queria mostrar mais do que capacidade de produzir código com IA: queria testar se conseguiria reconhecer uma informação útil para um gestor, questionar a conclusão do modelo e transformar o resultado em uma interface utilizável. O 003 também se aproximava do lead scoring que já havíamos trabalhado, e cheguei a considerar três cases; escolher apenas o 004 foi uma decisão de foco. A menor presença de Social Media no levantamento parcial das PRs também pesou, mas não foi tratada como prova de menor concorrência ativa nem como substituto da aderência à minha experiência.

**Por que separei análise, estratégia e interface.** São três responsabilidades diferentes: verificar o que a tabela sustenta, decidir o que fazer com isso e comunicar a decisão ao usuário. Pedi análise independente para que uma tela desejada não determinasse antecipadamente o resultado dos dados. Separei também relatório executivo de explorador: o primeiro responde às perguntas do gestor; o segundo permite conferir o banco e os recortes. Essa separação de responsabilidades evita confundir uma tabela correta com uma recomendação útil.

**Que técnica usei nos dados e por quê.** Adotei a organização em camadas Bronze/Prata/Ouro, conhecida como arquitetura medalhão, em uma implementação local com Python e SQLite — não uma infraestrutura de datalake em nuvem. Na Bronze preservei o CSV recebido e sua proveniência; na Prata fiz tipagem, padronização, validações e métricas; na Ouro reuni agregações e comparações para responder às perguntas do case. Assim, uma correção de fórmula ou classificação pode ser rastreada até a origem sem apagar o dado recebido, e a interface não precisa refazer cálculos. As tabelas temáticas da Prata separam métricas, creators, datas, audiência e conteúdo para reduzir dependências entre regras.

Nas comparações de patrocínio, usei recortes por plataforma, categoria e quartil de seguidores na data do post, em vez de depender somente de uma média geral que mistura perfis diferentes. Mediana, dispersão e tamanho da amostra contextualizam a comparação; a segmentação melhora a leitura, mas não elimina fatores de confusão nem prova causalidade. O [contrato do banco](solution/data/evidence/README.md) documenta fórmulas, tabelas e correções conhecidas. SQLite tornou essa cadeia portátil e auditável, e as exportações Ouro desacoplaram o site do banco.

**Como conduzi a execução:**

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

Uso o **PD Framework como meu OS de agentes**: é o meu sistema de trabalho para reunir contexto do projeto, instruções reutilizáveis (skills), papéis de IA, planejamento, coordenação e critérios de qualidade. Ele não substitui o modelo nem decide por mim. Sua função neste projeto foi dar contexto e limites às tarefas, organizar as passagens entre análise e implementação e manter decisões e evidências recuperáveis. As personas são papéis dentro desse sistema, não ferramentas adicionais nem pessoas da equipe; a [legenda dos papéis](process-log/README.md#quem-são-as-personas-mencionadas) explica a participação de cada uma.

| Ferramenta / tecnologia | Como usei neste projeto e por quê |
|---|---|
| PD Framework | Organizei o trabalho com contexto, skills e Dev Workflow; usei os princípios DRY, facilidade de mudança e separação de responsabilidades para orientar as decisões. |
| Codex | Ambiente de execução dos agentes de IA para ler documentos, propor análises, escrever código, revisar e testar. Separei frentes e confrontei suas entregas antes de integrar. |
| Gemini | Consulta pontual durante a pesquisa preparatória; não produziu os cálculos nem validou os resultados do dataset. |
| Herdr | Coordenei sessões e panes de agentes em paralelo, com tarefas delimitadas e handoffs, mantendo análise de dados e construção da interface separadas. |
| Linear | Organizei briefing, PRD, RFC, marcos e tarefas. Exportei os documentos para o fork para o avaliador não depender de acesso ao meu workspace. |
| Obsidian | Mantive o diário de decisões, perguntas e correções. O workflow publicado é uma edição desse registro para leitura externa, não uma transcrição integral. |
| Python | Executei ingestão, validações, cálculos, geração dos relatórios e exportações determinísticas. A IA ajudou a escrever os scripts; os números vêm de código, não de uma resposta textual do modelo. |
| SQLite | Reuni a fonte, transformações e resultados em um arquivo consultável, com integridade e hashes registrados. Permite auditar a análise sem servidor ou credencial. |
| Next.js, React, TypeScript e Astryx | Construí a aplicação e seus componentes, com contratos de tipos e interface reutilizável, em vez de somente anexar tabelas. |
| Vercel | Publiquei a aplicação como Preview pública. O site consome exportações estáticas; não hospeda o SQLite como backend e não usa chave de LLM na versão final. |
| Git e GitHub | Mantive fork, branch de entrega, diffs e checkpoints reais; reuni código, documentos e evidências dentro da pasta exigida pela submissão. |
| ESLint, TypeScript, testes Node/Python e Playwright | Verifiquei estilo, tipos, cálculos, contratos e fluxos automatizados locais. Esses testes não substituíram leitura gerencial nem inspeção visual. |
| Brave | Fizemos QA funcional da Preview e retestes no navegador conectado, sem usar Playwright nessa etapa remota. |
| Omarchy / GPU Screen Recorder e FFmpeg | Gravei a tela e preparei uma seleção de vídeo sem áudio, com cortes e limites documentados. Omacut foi consultado, mas não fez a exportação. |

Não atribuo um único modelo a toda a execução nem confundo uma persona com um modelo independente. O [método](docs/metodo/README.md), os [checkpoints de validação](docs/05-validacao/submission-audit.md) e os [exports](process-log/chat-exports/README.md) documentam o uso e seus limites.

### Workflow
1. Comparei os cases e escolhi Social Media pela aderência à minha experiência.
2. Pedi auditoria dos dados antes de fechar recomendações e requisitos.
3. Organizei briefing, PRD, arquitetura e tarefas; agentes trabalharam em frentes delimitadas.
4. Revisei a linguagem dos relatórios, questionei hipóteses e reduzi o escopo.
5. Exigi testes, evidências, publicação em Preview e QA no navegador.

O [registro detalhado](process-log/workflow.md) documenta as iterações por frente. Não há contagem auditada de todos os prompts; os ciclos documentados não são apresentados como total exato.
### Onde a IA errou e como corrigi

As correções mais importantes não foram de sintaxe, mas de direção do produto e de interpretação. Eu não tratei a primeira resposta da IA como requisito aprovado nem aceitei teste automatizado como prova de que a solução fazia sentido para o gestor.

1. **A comparação dos cases virou uma entrevista que não ajudava a decidir.** A IA começou a perguntar novamente sobre minha trajetória, embora o contexto já estivesse disponível. Expliquei que precisava comparar os desafios com minhas experiências, não recomeçar uma entrevista. Pedi perspectivas de Marketing e Desenvolvimento e fiz minha própria escolha pelo 004, mesmo quando os pareceres priorizavam Lead Scorer.
2. **O PRD avançou antes de discutir comigo as decisões de uso.** Questionei o documento porque não estava claro o que havia sido colocado como requisito. Retomei a discussão a partir do dia a dia do Head de Marketing: entender o que funciona, quando patrocinar, o que parar e qual ação tomar. Isso mudou a prioridade de apresentar perguntas e métricas para apresentar decisões justificadas.
3. **A análise ameaçou extrapolar os campos disponíveis.** Meus critérios de conteúdo incluíam retenção de três segundos e comentários que revelam novos ganchos. Pedi confrontá-los com a tabela e questionei suposições sobre timestamps. A análise passou a separar o que conseguimos calcular do que exigiria outra coleta. Também ressaltei que a base era fictícia: a simulação não deveria ser tratada, por si só, como falha do case. A revisão técnica corrigiu a interpretação de seguidores na data do post e identificou uma regra histórica de elegibilidade que não deveria orientar o produto.
4. **O primeiro relatório não comunicava uma decisão de marketing.** Reprovei páginas com muitos números, linguagem técnica e pouca explicação. Um visualizador do banco é útil para auditoria, mas não substitui o relatório para o gestor. Pedi separar os dois usos e organizar a leitura em conclusão, número contextualizado, ação e acesso à evidência. Comparações passaram a ser explicadas também como interações por 10 mil views, sem transformar uma diferença pequena em promessa de retorno.
5. **A interface passou em testes técnicos, mas ainda não cumpria o combinado.** Apontei cores inadequadas, acesso incompleto aos relatórios, filtros sem resposta clara e cards que exibiam perguntas cruas e identificadores internos como se fossem explicação. Pedi correção da experiência: filtros reativos, links para a evidência real e três decisões principais em vez de repetição de estatísticas. Isso mostrou por que lint, build e testes de navegação precisam ser complementados por QA visual e minha revisão do produto.
6. **O escopo cresceu além do necessário para comprovar a solução.** Eu havia proposto conversar com um agente sobre cada recomendação, mas retirei o chat quando vi que acesso, custo e segurança aumentavam o esforço sem resolver a prioridade da entrega. A implementação anterior permanece no Git; a versão final não contém a funcionalidade. Mantive relatório, explorador, dashboard e simulador, que demonstram a análise e a decisão sem depender de inferência paga.

As correções técnicas encontradas pelos agentes também estão identificadas como trabalho deles: por exemplo, unidade de taxa versus diferença em pontos percentuais, títulos encobertos pela navegação e rótulos em inglês no simulador. Minha contribuição foi exigir a conferência e revisar a utilidade da entrega; não reivindico ter localizado pessoalmente cada defeito.

Evidências: [workflow](process-log/workflow.md) — especialmente itens 41, 67–70, 83, 89 e 126–138 —, [screenshots contextualizados](process-log/evidencias/README.md), [QA no Brave](docs/05-validacao/checkpoint-qa-brave.md) e [histórico Git](process-log/git-history.md).

### O que eu adicionei que a IA sozinha não faria
Trouxe meu contexto de marcas/conteúdo, propus examinar gancho/contexto/informação/chamada se houver dados e defini o foco do projeto. São contribuições observáveis, não alegações de exclusividade humana.

## Evidências
- [Histórico Git da branch de submissão](https://github.com/felipeluissalgueiro/ai-master-challenge/commits/submission/felipe-salgueiro/) e [guia dos checkpoints](process-log/git-history.md) — evolução real do código, correções e decisões de escopo.
- [Revisão contra o guia e cobertura das oito perguntas](docs/05-validacao/submission-audit.md).
- [Planejamento e issues exportadas](docs/04-planejamento/issues/README.md) — leitura no próprio repositório, sem depender do Linear ou da renderização do GitHub Projects.
- [Projeto e marcos](docs/00-projeto/README.md).
- [Documentos por etapa](docs/README.md).
- [Pesquisa preparatória e ressalvas](docs/01-brief/pesquisa/README.md).
- [Workflow](process-log/README.md), [48 screenshots do processo](process-log/evidencias/README.md) e [proveniência dos exports](docs/proveniencia.md).
- [Conversas de 15 sessões do projeto](process-log/chat-exports/README.md), com [legenda das personas](process-log/README.md#quem-são-as-personas-mencionadas).

O [snapshot integral do banco](solution/data/evidence/README.md) está no fork com manifesto e limites conhecidos; a aplicação usa exportações Ouro, sem SQLite no deploy. O histórico Git registra a evolução, sem retroagir datas. Incluí uma [seleção de vídeo do processo](process-log/videos/README.md), de 24 segundos, com cortes documentados; gravações brutas e notebook não foram anexados. Chat com LLM e integração ao CRM não fazem parte da versão entregue.

**Submissão enviada em:** não enviada.
