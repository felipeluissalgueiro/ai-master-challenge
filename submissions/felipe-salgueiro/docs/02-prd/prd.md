Fonte canônica: [PRD no Linear](https://linear.app/cadencia/document/prd-challenge-004-estrategia-social-media-rastreavel-53e713ae38cf). Snapshot Draft v0.2 de 23/09/2026; não editar independentemente da fonte.

# PRD — Challenge 004: Estratégia Social Media rastreável

**Projeto Linear:** [P-MAR-55](<https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c>) · **Autor:** Felipe, com elaboração assistida por Paloma (PO) e consolidação por Lia · **Status:** Draft v0.2 · **Data:** 23/09/2026

Rascunho em paralelo à auditoria, ainda não submetido à aprovação. Requisitos propostos; não implementados como entrega integrada. Fonte de escopo: [Brief aprovado](<https://linear.app/cadencia/document/brief-d5c5e4cd5481>).

## Problema

O Head de Marketing precisa decidir onde concentrar esforço, quais parcerias testar e o que reduzir ou medir melhor. Contagens e médias isoladas não sustentam essas decisões. Esse é o problema proposto pelo enunciado; não é diagnóstico de uma operação real do G4.

A fonte contém 52.214 registros sintéticos e 27 colunas. O checkpoint do agente registra Bronze, métricas e dimensões Prata com paridade de linhas; creators/seguidores, datas, demografia e comparações de performance permanecem pendentes. Não há estratégia validada, camada Ouro ou página implementada. O volume não comprova representatividade nem utilidade dos sinais.

## Objetivo & métricas de sucesso

Entregar análise reproduzível, estratégia priorizada e página pública que permita inspecionar cada decisão.

Critérios propostos de aceite:

* Cobrir as quatro perguntas analíticas e os quatro tópicos estratégicos obrigatórios com evidência ou limitação explícita.
* Vincular 100% das recomendações a pergunta, evidência, limite e ação candidata.
* Reconciliar todos os valores exibidos com os resultados analíticos, admitindo apenas arredondamento documentado.
* Permitir concluir sem conta os percursos de panorama, comparação, recomendação e método.
* Reconstruir resultados seguindo as instruções entregues e disponibilizar process log revisado.

São critérios da entrega; não prometem aumento de engajamento, receita ou desempenho empresarial.

## Usuários & casos de uso

* **Head de Marketing:** compreender prioridades e distinguir hipótese de conclusão sustentada.
* **Equipe de conteúdo:** examinar recortes antes de propor continuidade, teste, redução ou nova medição.
* **Avaliador:** rastrear recomendações até cálculos, limites e evidências do uso de IA.
* **Felipe:** revisar precisão analítica e adequação da entrega antes de autorizar publicação da página e submissão.

## Escopo (in)

* Análise descritiva por plataforma, formato, categoria e patrocínio; tamanho de creator e demografia são perguntas obrigatórias cuja resposta depende da auditoria, podendo resultar em limitação documentada. Recortes por período são condicionais à utilidade comprovada.
* Estratégia priorizada: concentração de esforço, política de patrocínio, atividades a reduzir e quick wins.
* Página independente: panorama → comparação → justificativa → método.
* Python, SQLite reconstruível e camadas Bronze/Prata/Ouro, já escolhidos.
* Código, instruções de reprodução e process log público revisado.

## Fora de escopo (out)

**Evolução futura proposta por Felipe:** avaliar a criação/adaptação de uma SLM especializada em marketing com dados autorizados dos creators da empresa. É uma proposta de gestão para o G4, não um recurso disponível nem treinamento aprovado. Depende de governança, consentimentos/permissões, qualidade do corpus e avaliação de fidelidade, custo e utilidade; modelo menor não garante menos alucinações. A entrega atual usa LLM via OpenRouter.

Cadência operacional, login, tenants, integrações operacionais externas (CRM/Meta), campanhas, publicação de conteúdo, dados privados de outros projetos, Jev e preditor. Não calcular ROI, inventar alcance/retenção, atribuir causalidade ou interpretar textos sintéticos como voz da audiência. Framework e hospedagem permanecem sem decisão.

## Requisitos funcionais

- [ ] **RF01 — Panorama:** apresentar origem, natureza sintética, cobertura, perguntas obrigatórias e estado das evidências, sem antecipar findings.
- [ ] **RF02 — Comparação:** filtrar plataforma, formato, categoria e flag de patrocínio; incorporar creator/período somente após validação de qualidade e utilidade. Exibir recorte, n, denominador, medida, dispersão e exclusões.
- [ ] **RF03 — Métricas:** nomear explicitamente interações/views, interações/seguidores e views/seguidores; informar fórmula e agregação. O CSV não contém engagement_rate.
- [ ] **RF04 — Patrocínio:** comparar grupos comparáveis nas dimensões validadas, sem alegar equivalência causal; usar “não patrocinado segundo a flag”. Explicitar limites para custo implícito e decisão de investimento. Sem custo, qualquer preço-limite será cenário com premissas, nunca resultado observado; sua inclusão depende do fechamento do escopo.
- [ ] **RF05 — Audiência:** apresentar composição agregada apenas após auditoria; não identificar essa composição como perfil dos indivíduos que engajaram. Se inadequada, responder à pergunta com a lacuna e medição necessária.
- [ ] **RF06 — Recomendação:** mostrar pergunta, evidência identificável, limite, ação candidata e justificativa da prioridade. Cobrir foco, patrocínio, o que parar e quick wins; indicar quando frequência ou threshold de seguidores/engajamento não são identificáveis. Separar continuidade do tema, da execução e desdobramento editorial, sem classificar conteúdo sem evidência semântica.
- [ ] **RF07 — Insuficiência:** distinguir recorte vazio, dado inválido, evidência insuficiente e desempenho inferior. Sem sustentação, recomendar medir melhor ou um experimento.
- [ ] **RF08 — Reprodução:** ligar resultados Ouro às transformações Prata e à origem Bronze; documentar execução e incluir process log com ferramentas, decomposição, erros, correções e julgamento humano.
- [ ] **RF09 — Conversa contextual:** usar LLM via OpenRouter nesta entrega para explicar exclusivamente a recomendação selecionada, seus indicadores calculados, regras e limitações. Não realizar cálculos de negócio no modelo, inventar números, responder fora do contexto ou executar ações. Informar insuficiência de dados e apontar a evidência de cada resposta factual. Modelo específico e configuração ainda a definir.
- [ ] **RF10 — Comparação e decisão:** priorizar o que continuar, rever/parar ou testar, com justificativas numéricas. Comparar com a média do próprio creator quando houver histórico comparável; apresentar benchmark genérico estático, com fonte, período e fórmula verificados, sem scraping. A referência externa é contextual e não fundamenta automaticamente decisões de investimento em uma base sintética.
- [ ] **RF11 — Visão comercial futura:** representar na UI leads, vendas e CAC como não mensurados, nunca como zero ou dados fictícios. Conexão ao CRM é capacidade futura; CAC por campanha requer custos, novos clientes e atribuição definidos.

## Requisitos não-funcionais

Acesso público sem login e sem ações operacionais. A integração de inferência via OpenRouter usará credencial apenas no servidor, nunca no navegador ou no Git; limites de uso/custo, contexto enviado, proteção contra abuso e estado de indisponibilidade devem ser definidos na RFC antes de disponibilizar o chat. Conteúdo e controles legíveis em desktop e celular, operáveis por teclado; tabelas e textos devem explicar gráficos.

Transformações determinísticas, proveniência verificável, exclusões explícitas e ausência de imputação silenciosa. Divisão por zero deve produzir valor nulo sinalizado.

Desempenho de carregamento e contrato de exportação serão definidos com o volume Ouro e a arquitetura; nenhum SLA está validado. Revisão prévia dos arquivos públicos deve impedir exposição de segredos, diário privado integral ou material sem permissão. Mudanças de Git restritas a submissions/felipe-salgueiro/.

## Riscos & dependências

* **Creators/seguidores:** validar identidade, repetição e consistência antes de definir faixas ou tratar posts como observações independentes.
* **Datas:** validar formato, período e cobertura; data de publicação não comprova janela equivalente de exposição nem frequência ótima.
* **Demografia:** validar estrutura, somas e consistência por creator/post; campos inadequados devem gerar limitação explícita.
* **Performance:** concluir comparações, dispersão, sensibilidade e regra de suficiência antes de rankings ou thresholds. Não substituir critérios pendentes por cortes arbitrários.
* **Fonte sintética:** contagens estreitas e ausência de zeros nas métricas auditadas limitam generalização; nenhum resultado será benchmark real.
* **Lacunas do enunciado:** faltam gasto, receita, alcance e retenção; solicitações incompatíveis serão respondidas com limites e medição necessária.
* **Classificação:** reaproveitar os critérios de mídia paga do Cadência apontados por Felipe como validados, verificando os campos de entrada; não aplicar regras sem os dados necessários. Para orgânico, histórico do creator e referência externa têm papéis separados. Classificação e cálculo determinísticos precedem explicações do LLM. JEV é possibilidade condicional a disponibilidade e utilidade, não dependência desta versão.
* **Chat:** OpenRouter foi escolhido por Felipe; seleção do modelo, testes de respostas sem evidência, isolamento do contexto e limite de consumo permanecem pendentes. Não houve chamada de inferência nesta etapa.
* **Entrega:** conciliar snapshots documentais, concluir Ouro, definir exportação/UI e revisar permissões de eventual reutilização. Prazo externo não confirmado; 4–6 horas são referência do desafio.

**Grill — avaliação preliminar:** manter em rascunho; fechamento pendente. O usuário de referência e os limites de acesso/reutilização vêm do Brief aprovado. A rastreabilidade é critério verificável, não promessa de impacto de negócio. Se não houver diferenças úteis, a entrega deve demonstrar insuficiência e orientar medição/experimentos, sem fabricar vencedores. O grill está em andamento com Felipe: recomendações fundamentadas, conversa restrita à recomendação, benchmark estático, CRM/SLM futuros e LLM via OpenRouter foram definidos durante a discussão. O documento completo ainda não foi aprovado.

As dependências analíticas impedem fechar o PRD para aprovação e criar Epics, sem impedir seu refinamento paralelo. Vitor valida viabilidade e agrupamento somente após o fechamento do grill; RFC e implementação da página não foram autorizadas por este rascunho.

## Stories previstas

Candidatas, sem tickets, agrupadas em três capacidades verticais:

1. **Entender a evidência:** consultar panorama; verificar cobertura e qualidade; reproduzir métricas com proveniência.
2. **Comparar com contexto:** selecionar recortes válidos; comparar patrocínio; reconhecer insuficiência e limites demográficos/temporais.
3. **Decidir com rastreabilidade:** inspecionar recomendações priorizadas; navegar à evidência; consultar método, limitações e process log.

## Marcos

1. **Diagnóstico — em andamento:** concluir auditoria, refinar este PRD, fechar grill e obter revisão de Felipe; depois validação técnica de Vitor e arquitetura conforme o gate da cascata.
2. **Execução — etapa futura para a página:** concluir Ouro, interface e documentação após requisitos/planejamento aprovados. Scripts exploratórios Bronze/Prata já existem; isso não equivale à entrega integrada.
3. **Validação — pendente:** verificar reprodução, fidelidade dos números, jornadas e critérios obrigatórios; revisão final por Felipe. Deploy da página e PR ao G4 exigem autorizações próprias; checkpoints no fork já estão autorizados.
