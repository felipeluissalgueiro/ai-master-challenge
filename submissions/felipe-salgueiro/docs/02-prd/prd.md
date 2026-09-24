Fonte canônica: [PRD no Linear](https://linear.app/cadencia/document/prd-challenge-004-estrategia-social-media-rastreavel-53e713ae38cf). Snapshot consolidado v0.5 de 23/09/2026; gate técnico pendente; não editar independentemente da fonte.

# PRD — Challenge 004: Estratégia Social Media rastreável

**Decisão posterior ao snapshot:** [chat retirado por Felipe](../03-rfc/decisao-retirada-chat.md).
Este snapshot histórico não deve ser usado para reintroduzir a funcionalidade.

**Projeto Linear:** [P-MAR-55](<https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c>) · **Autor:** Felipe, com elaboração assistida por Paloma (PO) e consolidação por Lia · **Status:** Consolidado v0.5 — gate técnico pendente · **Data:** 23/09/2026

Escopo consolidado por solicitação de Felipe após as decisões do grill, com prioridade de entrega em 23/09/2026. Gate técnico, arquitetura e validação da entrega ainda pendentes. Consolidar não significa implementar, fazer deploy ou enviar a PR final. Fonte de escopo: [Brief aprovado](<https://linear.app/cadencia/document/brief-d5c5e4cd5481>).

## Problema

O Head de Marketing precisa decidir onde concentrar esforço, quais parcerias testar e o que reduzir ou medir melhor. Contagens e médias isoladas não sustentam essas decisões. Esse é o problema proposto pelo enunciado; não é diagnóstico de uma operação real do G4.

A fonte contém 52.214 registros sintéticos e 27 colunas. Pipeline Bronze/Prata/Ouro, relatório revisado pelo dicionário oficial e SQLite de evidência foram integrados ao fork (checkpoints cf0ba03 e f04988b). A integração conferiu hashes, integridade do banco e sintaxe/imports dos scripts; a execução completa foi realizada pelo agente de dados, sem repetição pela Lia. As análises descritivas estão disponíveis; contrato/exportador Ouro e página permanecem pendentes. O volume não comprova representatividade nem utilidade dos sinais.

## Objetivo & métricas de sucesso

Entregar análise reproduzível, estratégia priorizada e página acessível aos avaliadores autorizados que permita inspecionar cada decisão.

Critérios propostos de aceite:

* Cobrir as quatro perguntas analíticas e os quatro tópicos estratégicos obrigatórios com evidência ou limitação explícita.
* Vincular 100% das recomendações a pergunta, evidência, limite e ação candidata.
* Reconciliar todos os valores exibidos com os resultados analíticos, admitindo apenas arredondamento documentado.
* Permitir aos avaliadores autorizados concluir os percursos de panorama, comparação, recomendação e método.
* Reconstruir resultados seguindo as instruções entregues e disponibilizar process log revisado.

São critérios da entrega; não prometem aumento de engajamento, receita ou desempenho empresarial.

## Usuários & casos de uso

* **Head de Marketing:** compreender prioridades e distinguir hipótese de conclusão sustentada.
* **Equipe de conteúdo:** examinar recortes antes de propor continuidade, teste, redução ou nova medição.
* **Avaliador:** rastrear recomendações até cálculos, limites e evidências do uso de IA.
* **Felipe:** revisar precisão analítica e adequação da entrega antes de autorizar publicação da página e submissão.

## Escopo (in)

* Aplicação e função do chat na Vercel; consumo de arquivos Ouro exportados, sem SQLite gravável em produção nem VPS Master/Dev. Chave OpenRouter exclusiva do challenge, somente no servidor e com limite de crédito a definir.
* SQLite completo como evidência no fork, em snapshot consistente acompanhado de scripts, manifesto e instruções de consulta. Snapshot publicado com 58,75 MiB, integridade e hashes conferidos; original de trabalho e auxiliares permanecem preservados/ignorados.
* Análise descritiva por plataforma, formato, categoria, patrocínio, quartis de seguidores na data do post e grupos predominantes de audiência. Rankings de creators usam creator_id e rótulos neutros; a camada de consumo não pode usar a elegibilidade histórica superada. Recortes por período descrevem a amostra, não frequência ótima.
* Estratégia priorizada: concentração de esforço, política de patrocínio, atividades a reduzir e quick wins.
* Página independente: panorama → comparação → justificativa → método.
* Python, SQLite reconstruível e camadas Bronze/Prata/Ouro, já escolhidos.
* Código, instruções de reprodução e process log público revisado.

## Fora de escopo (out)

**Evolução futura proposta por Felipe:** avaliar a criação/adaptação de uma SLM especializada em marketing com dados autorizados dos creators da empresa. É uma proposta de gestão para o G4, não um recurso disponível nem treinamento aprovado. Depende de governança, consentimentos/permissões, qualidade do corpus e avaliação de fidelidade, custo e utilidade; modelo menor não garante menos alucinações. A entrega atual usa LLM via OpenRouter.

Cadência operacional, cadastro próprio de usuários, tenants, integrações operacionais externas (CRM/Meta), campanhas, publicação de conteúdo, dados privados de outros projetos, Jev e preditor. Não calcular ROI, inventar alcance/retenção, atribuir causalidade ou interpretar textos sintéticos como voz da audiência. Hospedagem escolhida: Vercel. Framework de UI ainda a definir.

## Requisitos funcionais

- [ ] **RF01 — Panorama:** abrir com o que os dados sustentam sobre engajamento, patrocínio e próxima ação, priorizando recomendações com números e limites; apresentar origem, natureza sintética e cobertura. Não converter posições em ranking em prova de superioridade.
- [ ] **RF02 — Comparação:** filtrar plataforma, formato, categoria e flag de patrocínio; usar creator_id e recortes temporais descritivos após validação da camada de consumo; nomes de creators não são confiáveis. Exibir recorte, n, denominador, medida, dispersão e exclusões.
- [ ] **RF03 — Métricas:** nomear explicitamente interações/views, interações/seguidores e views/seguidores; informar fórmula e agregação. O CSV não contém engagement_rate.
- [ ] **RF04 — Patrocínio:** comparar grupos comparáveis nas dimensões validadas, sem alegar equivalência causal; usar “não patrocinado segundo a flag”. Explicitar limites para custo implícito e decisão de investimento. Sem custo observado, explorar custos somente no simulador hipotético RF12; nenhum cenário comprova retorno ou preço justo da parceria.
- [ ] **RF05 — Audiência:** comparar posts pelos rótulos de idade/gênero predominantes e localização principal. Não apresentar esses rótulos como distribuição percentual completa nem identidade dos indivíduos que engajaram; evidenciar recorte, n e dispersão.
- [ ] **RF06 — Recomendação:** mostrar pergunta, evidência identificável, limite, ação candidata e justificativa da prioridade. Cobrir foco, patrocínio, o que parar e quick wins; indicar quando frequência ou threshold de seguidores/engajamento não são identificáveis. Separar continuidade do tema, da execução e desdobramento editorial, sem classificar conteúdo sem evidência semântica.
- [ ] **RF07 — Insuficiência:** distinguir recorte vazio, dado inválido, evidência insuficiente e desempenho inferior. Sem sustentação, recomendar medir melhor ou um experimento.
- [ ] **RF08 — Reprodução:** ligar resultados Ouro às transformações Prata e à origem Bronze; documentar execução e incluir process log com ferramentas, decomposição, erros, correções e julgamento humano.
- [ ] **RF09 — Conversa contextual:** usar LLM via OpenRouter nesta entrega para explicar exclusivamente a recomendação selecionada, seus indicadores calculados, regras e limitações. Não realizar cálculos de negócio no modelo, inventar números, responder fora do contexto ou executar ações. Informar insuficiência de dados e apontar a evidência de cada resposta factual. Modelo específico e configuração ainda a definir.
- [ ] **RF10 — Comparação e decisão:** priorizar o que continuar, rever/parar ou testar, com justificativas numéricas. Comparar com a média do próprio creator quando houver histórico comparável; apresentar benchmark genérico estático, com fonte, período e fórmula verificados, sem scraping. A referência externa é contextual e não fundamenta automaticamente decisões de investimento em uma base sintética.
- [ ] **RF11 — Visão comercial futura:** representar na UI leads, vendas e CAC como não mensurados, nunca como zero ou dados fictícios. Conexão ao CRM é capacidade futura: associar vendas efetivamente registradas ao parceiro por link rastreado ou cupom, com regra de atribuição e deduplicação explícitas. Clique não comprova venda. CAC por campanha exige custos e novos clientes atribuídos; venda de cliente recorrente não conta como nova aquisição.
- [ ] **RF12 — Simulador hipotético de patrocínio:** permitir informar o custo considerado da parceria e a quantidade hipotética de vendas atribuídas. Calcular deterministicamente custo por mil views (`1000 × custo / views`), custo por interação (`custo / interações`) e custo por venda (`custo / vendas atribuídas`). Explicitar componentes de custo (parceria, comissão, produção ou outros informados), unidades, período/recorte e origem de cada denominador. Views e interações podem vir do recorte selecionado como referência descritiva, nunca previsão de entrega; se a referência for por post, indicar a hipótese de custo de um post, sem misturar custo de campanha com mediana por post. Separar visualmente métricas observadas no dataset de entradas e resultados hipotéticos. Não preencher vendas ou taxas de conversão fictícias como evidência. Com zero vendas, exibir custo por venda não calculável e “sem vendas atribuídas no cenário”; vazio significa não informado. Rejeitar valores negativos e vendas fracionárias. Não denominar custo por venda como CAC ou ROI. Exemplo de aceite: R$ 2.000 / 20 vendas hipotéticas = R$ 100 por venda.

## Requisitos não-funcionais

Acesso restrito aos avaliadores, com proteção nativa da Vercel como direção escolhida por Felipe; confirmar habilitação e cobrança do recurso no plano antes de ativá-lo. Não criar sistema próprio de usuários neste escopo. Sem ações operacionais. A integração de inferência via OpenRouter usará credencial apenas no servidor, nunca no navegador ou no Git; limites de uso/custo, contexto enviado, proteção contra abuso e estado de indisponibilidade devem ser definidos na RFC antes de disponibilizar o chat. Conteúdo e controles legíveis em desktop e celular, operáveis por teclado; tabelas e textos devem explicar gráficos.

Transformações determinísticas, proveniência verificável, exclusões explícitas e ausência de imputação silenciosa. Divisão por zero deve produzir valor nulo sinalizado.

Desempenho de carregamento e contrato de exportação serão definidos com o volume Ouro e a arquitetura; nenhum SLA está validado. Revisão prévia dos arquivos públicos deve impedir exposição de segredos, diário privado integral ou material sem permissão. Mudanças de Git restritas a submissions/felipe-salgueiro/.

## Riscos & dependências

* **Revisão de interpretação solicitada por Felipe:** fonte fictícia é intencional e não invalida análise descritiva do cenário. O dicionário oficial define seguidores na data do post, idade/gênero predominantes e duração em segundos para vídeos ou palavras para texto. Variar seguidores não invalida sozinho um creator; identidade e nomes devem ser avaliados separadamente. A revisão permite rankings descritivos por creator_id e segmentos predominantes. creator_name não é confiável; a elegibilidade histórica baseada em seguidores estáveis foi superada. O valor measure_better é fixo no código Ouro histórico, não um classificador aprovado; ambos os campos não podem orientar o produto. Não inventar diferenças relevantes nem ROI ausente. Fonte: [descrição do Kaggle](<https://www.kaggle.com/datasets/omenkj/social-media-sponsorship-and-engagement-dataset/data>), conferida via API em 23/09/2026.
* **Creators/seguidores:** creator_id é a chave da simulação; nomes inconsistentes não rotulam rankings. Corrigir o contrato de consumo sem reescrever o snapshot histórico. Repetição de posts por creator impede presumir independência automaticamente.
* **Datas:** formato e cobertura foram auditados; datas aleatórias não comprovam janela equivalente de exposição, tendência real ou frequência ótima.
* **Demografia:** rótulos predominantes já auditados; não há percentuais para somar nem composição individual a inferir.
* **Performance:** concluir comparações, dispersão, sensibilidade e regra de suficiência antes de rankings ou thresholds. Não substituir critérios pendentes por cortes arbitrários.
* **Fonte sintética:** contagens estreitas e ausência de zeros nas métricas auditadas limitam generalização; nenhum resultado será benchmark real.
* **Lacunas do enunciado:** faltam gasto, receita, alcance e retenção; solicitações incompatíveis serão respondidas com limites e medição necessária.
* **Classificação:** reaproveitar os critérios de mídia paga do Cadência apontados por Felipe como validados, verificando os campos de entrada; não aplicar regras sem os dados necessários. Para orgânico, histórico do creator e referência externa têm papéis separados. Classificação e cálculo determinísticos precedem explicações do LLM. JEV é possibilidade condicional a disponibilidade e utilidade, não dependência desta versão.
* **Chat:** OpenRouter foi escolhido por Felipe; seleção do modelo, testes de respostas sem evidência, isolamento do contexto e limite de consumo permanecem pendentes. Não houve chamada de inferência nesta etapa.
* **Entrega:** conciliar snapshots documentais, concluir Ouro, definir exportação/UI e revisar permissões de eventual reutilização. Prazo externo não confirmado; 4–6 horas são referência do desafio.

## Regras resolvidas no grill

* Head de Marketing é o usuário de referência; deve enxergar o que funciona, limites e próxima ação com justificativa numérica.
* Rankings são descritivos da simulação; diferenças pequenas levam a hipóteses/testes, não corte ou escala automáticos.
* Cálculo e classificação são determinísticos; o LLM explica somente a recomendação selecionada, com evidências e limites.
* Simulador inclui custo por mil views, interação e venda; custo e vendas hipotéticos são separados dos dados observados. Custo por venda não é CAC.
* CRM, vendas atribuídas reais e SLM são evolução futura; UI comercial mostra não mensurado, não zero.
* Vercel com acesso protegido, chave exclusiva OpenRouter no servidor e dados Ouro exportados; sem banco em runtime ou VPS.
* Reaproveitar componentes pontuais quando reduzir trabalho; não portar a operação Cadência.
* Benchmark externo é referência contextual estática verificável, sem scraping nem falsa equivalência com a fonte sintética.

**Veredito do grill de produto: segue para gate técnico.** Felipe solicitou consolidar e avançar após fechar o simulador. Isso não é aprovação antecipada da arquitetura nem declaração de entrega pronta.

## Prioridade de entrega — 23/09/2026

Sem expandir escopo, executar um corte vertical completo: evidência Ouro → panorama/comparação → recomendação explicável → simulador → chat protegido → validação e instruções. Protótipo HTML é exploração paralela, não um segundo produto e não bloqueia a arquitetura.

Não iniciar novos conectores, modelos, scraping, login próprio ou migração Cadência. Reusar análise e SQLite já publicados. Não repetir o pipeline validado sem necessidade; novos exports e cálculos exigem testes proporcionais.

Chat e proteção mantêm seus requisitos: falta de credencial, entitlement ou controle de custo é bloqueio específico a comunicar, nunca motivo para expor chave ou disponibilizar endpoint aberto. Não retirar funcionalidade acordada silenciosamente para cumprir o prazo. Deploy e envio da PR continuam dependendo de autorização própria.

## Stories previstas

Candidatas, sem tickets, agrupadas em três capacidades verticais:

1. **Entender a evidência:** consultar panorama; verificar cobertura e qualidade; reproduzir métricas com proveniência.
2. **Comparar com contexto:** selecionar recortes válidos; comparar patrocínio; reconhecer insuficiência e limites demográficos/temporais.
3. **Decidir com rastreabilidade:** inspecionar recomendações priorizadas; navegar à evidência; simular custos por views, interação e venda sem confundir cenários com observações; consultar método, limitações e process log.

## Marcos

1. **Diagnóstico — em andamento:** concluir auditoria, refinar este PRD, fechar grill e obter revisão de Felipe; depois validação técnica de Vitor e arquitetura conforme o gate da cascata.
2. **Execução — etapa futura para a página:** concluir Ouro, interface e documentação após requisitos/planejamento aprovados. Scripts exploratórios Bronze/Prata já existem; isso não equivale à entrega integrada.
3. **Validação — pendente:** verificar reprodução, fidelidade dos números, jornadas e critérios obrigatórios; revisão final por Felipe. Deploy da página e PR ao G4 exigem autorizações próprias; checkpoints no fork já estão autorizados.
