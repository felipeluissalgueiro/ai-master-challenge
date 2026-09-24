# Export sanitizado — paloma-prd — Challenge 004

Snapshot de mensagens visíveis da sessão identificada no índice. Inclui pedidos de Felipe, instruções de coordenação e handoffs no canal do usuário e respostas públicas da IA; não atribui todos os prompts a falas autorais de Felipe. Horários em UTC. Sessões derivadas podem conter contexto herdado; isso não é execução independente repetida.

Foram excluídos bootstrap, instruções de sistema/desenvolvedor, ferramentas, raciocínio interno, imagens binárias e notificações automáticas. Caminhos locais, e-mails, IDs e padrões de credenciais foram substituídos. Não é transcript bruto integral. As outras sessões estão separadas no índice. Propostas e estados históricos não comprovam a execução; consulte workflow e checkpoints.

Mensagens: 3. Início: 2026-09-23T19:27:18.260Z. Fim: 2026-09-23T19:28:56.935Z.

SHA-256 do snapshot de origem privado: `04a8c301fb761f0b0cbfcb58c4ff7bbb0a7410724c150d5da691216067d21ac3`. O hash identifica o snapshot, não oferece acesso à origem nem prova suas alegações.

Blocos automáticos de usuário omitidos após início: 1.

## 1. Entrada — Felipe / coordenação / handoff · 2026-09-23T19:27:18.260Z

```text
Você é Paloma (PO), subagente requisitado pela skill linear-prd. Produza SOMENTE rascunho PRD em português, sem persistir, sem issues, sem publicar. Leia integralmente fontes canônicas [caminho local omitido] + memory/STATE.md + decisions.md (localize decisions exato se necessário), times/marketing/CLAUDE.md, stamper/context/perfil-felipe.md. Template obrigatório [caminho local omitido] §3. Brief aprovado local: [caminho local omitido] (fonte Linear id63205b66-ba2b-4bf2-b2d8-04fb382fe605, conferida neste turno). Leia enunciado no mesmo repo challenges/marketing-004-social/README.md e submission-guide.md. Checkpoint mais recente [caminho local omitido] catálogo/diagnóstico no repo principal docs/01-brief/dados. Projeto P-MAR-55 https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c. Decisão atual explícita: iniciar PRD em paralelo à auditoria, NÃO fechar para aprovação nem criar Epics enquanto faltam creators/seguidores, datas, demografia e comparações de performance. Página pública independente, sem login; Python SQLite Bronze/Prata/Ouro já escolhidos; não decidir framework/hospedagem agora. Sem Cadência operacional, APIs, preditor, Jev, sem ROI, causalidade ou interpretação de textos sintéticos. Diferencial é decisão rastreável, não dashboard genérico; cada recomendação tem pergunta, evidência, limite, ação candidata. Não patrocinado pela flag != orgânico. Audiência agregada != indivíduos que engajaram. Métricas de aceite reais testáveis da entrega, não inventar aumento de negócio. Stories previstas apenas candidatas agrupadas em 3 capacidades verticais, sem tickets. Marcar tudo ainda não implementado, premissas condicionais. Conciso ~1000 palavras máximo, todas seções template, pendências concretas dentro riscos. Retorne PRD e separado observações do grill, sem alegar aprovação. Leitura/revisão de conteúdo público somente; não copiar dados privados de outros projetos. Não precisa abrir outro pane.
```

## 2. Assistente — resposta pública · 2026-09-23T19:27:22.948Z

```text
Vou usar as skills linear-prd, Paloma e grill para preparar o rascunho conforme o template e revisar suas lacunas. Lerei as fontes indicadas, sem persistir conteúdo nem criar itens no Linear.
```

## 3. Assistente — resposta pública · 2026-09-23T19:28:56.935Z

```text
# PRD — Challenge 004: Estratégia Social Media rastreável

**Projeto Linear:** [P-MAR-55](https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c) · **Autor:** Felipe · **Status:** Draft · **Data:** 23/09/2026
Elaboração: Paloma (PO). Rascunho em paralelo à auditoria; não submetido à aprovação. Requisitos abaixo são propostos e ainda não implementados como entrega integrada.

## Problema

O Head de Marketing precisa decidir onde concentrar esforço, quais parcerias testar e o que reduzir ou medir melhor. Contagens e médias isoladas não sustentam essas decisões.

A fonte contém 52.214 registros sintéticos e 27 colunas. O checkpoint registra Bronze, métricas e dimensões Prata com paridade de linhas; creators/seguidores, datas, demografia e comparações de performance permanecem pendentes. Não há estratégia validada, camada Ouro ou página implementada. O volume não comprova representatividade nem utilidade dos sinais.

## Objetivo & métricas de sucesso

Entregar análise reproduzível, estratégia priorizada e página pública que permita inspecionar cada decisão.

Critérios propostos de aceite:

- Cobrir as quatro perguntas analíticas e os quatro tópicos estratégicos obrigatórios com evidência ou limitação explícita.
- Vincular 100% das recomendações a pergunta, evidência, limite e ação candidata.
- Reconciliar todos os valores exibidos com os resultados analíticos, admitindo apenas arredondamento documentado.
- Permitir concluir sem conta os percursos de panorama, comparação, recomendação e método.
- Reconstruir resultados seguindo as instruções entregues e disponibilizar process log revisado.

São critérios da entrega; não prometem aumento de engajamento, receita ou desempenho empresarial.

## Usuários & casos de uso

- **Head de Marketing:** compreender prioridades e distinguir hipótese de conclusão sustentada.
- **Equipe de conteúdo:** examinar recortes antes de propor continuidade, teste, redução ou nova medição.
- **Avaliador:** rastrear recomendações até cálculos, limites e evidências do uso de IA.
- **Felipe:** revisar precisão analítica e adequação da entrega antes de autorizar publicação e submissão.

## Escopo (in)

- Análise descritiva por plataforma, formato, categoria, patrocínio e, condicionalmente à auditoria, tamanho de creator, período e demografia.
- Estratégia priorizada sobre concentração de esforço, política de patrocínio, atividades a reduzir e quick wins.
- Página independente: panorama → comparação → justificativa → método.
- Python, SQLite reconstruível e camadas Bronze/Prata/Ouro, já escolhidos.
- Código, instruções de reprodução e process log público revisado.

## Fora de escopo (out)

Cadência operacional, login, tenants, APIs externas, campanhas, publicação de conteúdo, dados privados de outros projetos, Jev e preditor. Não calcular ROI, inventar alcance/retenção, atribuir causalidade ou interpretar textos sintéticos como voz da audiência. Framework e hospedagem permanecem sem decisão.

## Requisitos funcionais

- [ ] **Panorama:** apresentar origem, natureza sintética, cobertura, perguntas obrigatórias e estado das evidências, sem antecipar findings.
- [ ] **Comparação:** filtrar plataforma, formato, categoria e flag de patrocínio; incorporar creator/período somente após validação. Exibir recorte, `n`, denominador, medida, dispersão e exclusões.
- [ ] **Métricas:** nomear explicitamente interações/views, interações/seguidores e views/seguidores; informar fórmula e agregação. O CSV não contém `engagement_rate`.
- [ ] **Patrocínio:** comparar grupos equivalentes nas dimensões validadas; usar “não patrocinado segundo a flag”. Explicitar limites para decisão de investimento.
- [ ] **Audiência:** apresentar composição agregada apenas após auditoria; não identificar essa composição como perfil dos indivíduos que engajaram.
- [ ] **Recomendação:** mostrar pergunta, evidência identificável, limite, ação candidata e justificativa da prioridade. Separar continuidade do tema, da execução e desdobramento editorial.
- [ ] **Insuficiência:** distinguir recorte vazio, dado inválido, evidência insuficiente e desempenho inferior. Sem sustentação, recomendar medir melhor.
- [ ] **Reprodução:** ligar resultados Ouro às transformações Prata e à origem Bronze; documentar execução e incluir process log com ferramentas, decomposição, erros, correções e julgamento humano.

## Requisitos não-funcionais

Acesso público somente leitura, sem credenciais ou dependência operacional. Conteúdo e controles legíveis em desktop e celular, operáveis por teclado; tabelas e textos devem explicar gráficos.

Transformações determinísticas, proveniência verificável, exclusões explícitas e ausência de imputação silenciosa. Divisão por zero deve produzir valor nulo sinalizado.

Desempenho de carregamento e contrato de exportação serão definidos com o volume Ouro e a arquitetura; nenhum SLA está validado. Revisão prévia dos arquivos públicos deve impedir exposição de segredos, diário privado integral ou material sem permissão.

## Riscos & dependências

- **Creators/seguidores:** validar identidade, repetição e consistência antes de definir faixas ou tratar posts como observações independentes.
- **Datas:** validar formato, período e cobertura; data de publicação não comprova janela equivalente de exposição nem frequência ótima.
- **Demografia:** validar estrutura, somas e consistência por creator/post; campos inadequados devem gerar limitação explícita.
- **Performance:** concluir comparações, dispersão, sensibilidade e regra de suficiência antes de rankings ou thresholds. Critérios ainda não definidos não serão substituídos por cortes arbitrários.
- **Fonte sintética:** contagens estreitas e ausência de zeros limitam generalização; nenhum resultado será benchmark real.
- **Lacunas do enunciado:** faltam gasto, receita, alcance e retenção; solicitações incompatíveis serão respondidas com limites e medição necessária.
- **Entrega:** conciliar snapshots documentais, concluir Ouro, definir exportação/UI e revisar permissões de eventual reutilização. Prazo externo não confirmado; 4–6 horas são referência do desafio.

Essas pendências impedem fechar o PRD para aprovação e criar Epics, sem impedir seu refinamento paralelo.

## Stories previstas

Candidatas, sem tickets, agrupadas em três capacidades verticais:

1. **Entender a evidência:** consultar panorama; verificar cobertura e qualidade; reproduzir métricas com proveniência.
2. **Comparar com contexto:** selecionar recortes válidos; comparar patrocínio; reconhecer insuficiência e limites demográficos/temporais.
3. **Decidir com rastreabilidade:** inspecionar recomendações priorizadas; navegar à evidência; consultar método, limitações e process log.

## Marcos

1. **Design + plano — em elaboração:** concluir auditoria, resolver pendências e revisar este rascunho; somente depois encaminhar aprovação e decomposição.
2. **Implementação — prevista:** concluir Ouro, página e documentação; verificar todos os critérios de aceite.
3. **Release — prevista:** revisão final por Felipe; publicação e submissão via PR dependem de autorizações próprias.

---

## Observações do grill — separadas do PRD

**Avaliação preliminar: ⏸ repensa antes de fechar; rascunho pode continuar.** Não constitui aprovação nem entrevista concluída.

- O diferencial é verificável: cada recomendação precisa sobreviver à inspeção de sua evidência. Gráficos isolados não cumprem o objetivo.
- Uma análise sem diferenças úteis continua válida se demonstrar insuficiência e indicar o que medir; não há obrigação de fabricar vencedores.
- A menor entrega coerente concentra a navegação nas perguntas obrigatórias e nos recortes sustentados.
- O próximo fechamento depende de creators, datas, demografia e comparações concluídos, com critérios explícitos de suficiência. Só então será possível avaliar se as três capacidades candidatas estão prontas para decomposição.
```
