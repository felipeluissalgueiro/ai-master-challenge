Fonte canônica: [Brief no Linear](https://linear.app/cadencia/document/brief-d5c5e4cd5481). Snapshot v1 de 23/09/2026; atualizar a partir da fonte, não manter versões paralelas.

# Brief — Challenge 004: Estratégia Social Media

**Projeto:** [P-MAR-55](https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c)
**Squad:** `times/marketing` · **Condução:** Lia · **Decisão e revisão:** Felipe
**Data/versão:** 23/09/2026 · v1
**Estado:** escopo consolidado após revisão de Felipe; implementação e publicação da página não realizadas.

## O que é e por que existe

Análise reproduzível do dataset do Challenge 004, acompanhada de estratégia priorizada e página pública exclusiva para explorar resultados e compreender o raciocínio por trás das decisões.

O problema é decidir o que continuar, testar, reduzir ou medir melhor no conteúdo e nas parcerias. A interface serve a essas decisões; não é uma demonstração genérica do Cadência. Deve permitir ao avaliador entender a conclusão, inspecionar evidências e reconhecer limites, sem login.

## Stakeholders

- Felipe: responsável pelo projeto, critérios de marketing, decisões e aprovação final.
- Lia/Marketing: Brief, interpretação de negócio, coordenação e process log.
- Catarina: experiência do produto Cadência e recorte funcional.
- Vitor: viabilidade, arquitetura, segurança e reaproveitamento técnico.
- Head de Marketing/equipe de conteúdo: usuários de referência da solução.
- Avaliador: acesso público de leitura; identidade e contato não necessários ao produto.

## Estado atual

Fork e estrutura de submissão preparados. Auditoria analítica em andamento em agente separado. O inventário relatado pelo agente identifica 52.214 registros e 27 colunas; a fonte é descrita como sintética. Isso não comprova qualidade, sinal estatístico ou aplicabilidade a operações reais.

Cadência possui criação estruturada de posts, análise social e Gestão de Tráfego documentadas/implementadas. Consultas de Catarina e Vitor ao SHA `c63a53ba8065e08eeca65c461d62f3896050483f` não equivalem a teste atual em produção. O método de triagem, exceções, suficiência de evidência e justificativas é referência reutilizável. Seus dados financeiros, regras específicas e integrações não se transferem automaticamente.

## Arquitetura e stack

- Página pública exclusiva do challenge, autônoma, sem login e sem dependência da operação do Cadência.
- Python para processamento determinístico; SQLite como armazenamento analítico local derivado e reconstruível.
- Camadas Bronze/Prata/Ouro: preservação da origem, validação/normalização e resultados por pergunta.
- Interface consome resultados validados; não precisa carregar todo o processamento nem reproduzir a plataforma.
- Framework de UI, hospedagem e contrato de exportação: a definir no PRD/RFC conforme necessidade. Não decidir stack por antecipação.
- Repositório: fork `felipeluissalgueiro/ai-master-challenge`; entregas em `submissions/felipe-salgueiro/`.

## Decisões tomadas e escopo

1. Entregar análise de performance, estratégia recomendada e process log exigidos pelo enunciado.
2. Comparar plataforma, formato, categoria, tamanho de creator e patrocínio com recortes, denominadores, volume e dispersão explícitos.
3. Reaproveitar componentes do Cadência apenas quando extraíveis com baixo acoplamento e adequados à publicação; não copiar a plataforma nem expor código privado implicitamente.
4. Separar continuar o tema, continuar a execução e criar um desdobramento editorial.
5. Recomendações exibem pergunta, evidência, limite e ação candidata. Ausência de evidência não equivale a desempenho ruim.
6. UI orientada à tarefa: entender o panorama, comparar recortes, examinar justificativas e consultar método/limitações. Layout e interações serão detalhados no PRD.
7. Resultados de fonte sintética demonstram método e hipóteses, não benchmarks reais ou prova de impacto no G4.
8. A página não substitui análise, código/instruções de reprodução e process log no fork.

## Perguntas e limites dos dados

| Pergunta | Tratamento |
|---|---|
| O que gera engajamento? | Associações descritivas por recorte; nomear precisamente interações/views e interações/seguidores, sem causalidade. |
| Patrocínio funciona? | Comparar flags dentro de grupos comparáveis. Não patrocinado segundo a flag não comprova distribuição orgânica. Sem gasto/receita, não calcular ROI. |
| Qual audiência engaja? | Validar campos demográficos primeiro; composição de audiência não identifica necessariamente quem interagiu. |
| O que não funciona? | Diferenciar desempenho inferior consistente de amostra insuficiente; não decretar cortes a partir de ruído. |
| Onde concentrar, o que parar e quick wins? | Priorizar ações condicionais e testes apoiados nos achados. Frequência ótima não é inferida apenas da data do post. |
| Gancho, retenção e comentários? | Retenção de 3s ausente. Auditoria do agente relata textos sintéticos inadequados à interpretação de voz real da audiência; não inventar classificação narrativa. |

## O que NÃO fazer

Não criar login, tenant avaliador ou adaptação do Cadência operacional. Não conectar campanhas, publicar posts, disparar mensagens ou alcançar dados/credenciais de clientes. Não implementar Jev ou preditor no escopo atual. Não fabricar alcance, retenção, custos, conversões, ROI ou inferências causais. Não expor diário privado integral sem revisão.

## Dependências críticas pendentes

Concluir validação de métricas, consistência e segmentos; registrar proveniência e limitações. Selecionar componentes reutilizáveis e suas permissões de redistribuição. Definir UI, stack mínima, hospedagem e verificações proporcionais. Prazo externo não confirmado; as 4–6h do enunciado são referência, não prazo assumido. Publicação da página e envio da PR serão ações separadas, mediante autorização.

## Critério de conclusão

- Perguntas obrigatórias respondidas com evidência ou limitação explícita.
- Estratégia priorizada e rastreável aos recortes analisados, sem afirmações reais indevidas sobre dados sintéticos.
- Página acessível sem conta, com filtros/comparações coerentes, estados vazios/insuficientes e evidências legíveis.
- Números da UI consistentes com resultados reproduzíveis; denominadores e origem identificados.
- Nenhuma dependência de dados privados, credenciais produtivas ou ações operacionais.
- Código/instruções, validações e process log revisados; Felipe aprova entrega antes da publicação/submissão.

## Regras resolvidas no grill

- **Problema e prioridade:** concluir o desafio escolhido; não transformar a entrega em expansão do Cadência.
- **Reaproveitamento:** componentes e método quando economizarem trabalho comprovadamente; produto operacional fica fora.
- **Acesso:** Felipe escolheu página pública sem login para reduzir complexidade.
- **Valor da UI:** tornar raciocínio, evidência e decisão inspecionáveis, não apenas exibir gráficos.
- **Veredito:** segue para PRD com esse escopo. Arquitetura detalhada e publicação não estão aprovadas por este Brief.

## Fontes

- [Enunciado](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/challenges/marketing-004-social/README.md)
- [Dataset](https://www.kaggle.com/datasets/omenkj/social-media-sponsorship-and-engagement-dataset)
- [Guia de submissão](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/submission-guide.md)
- Decisões de Felipe e pareceres de Catarina/Vitor registrados no diário privado; export público somente após revisão.
