# Insumo UX para a RFC — Sofia

Data: 23/09/2026. **Proposta investigada, não interface implementada nem RFC aprovada.** Base escolhida por Felipe: Astryx; referência visual: G4 Educação. Parecer produzido pela persona Sofia em pane separado, consolidado por Lia.

## Jornada e hierarquia

O Head precisa entender, decidir e aprofundar: **conclusão → um ou dois números contextualizados → ação → evidência**. Não organizar o menu pelas tabelas nem separar a jornada apenas em orgânico/pago. Termos estatísticos são explicados no aprofundamento, sem dominar a leitura inicial.

| Pergunta do gestor | Seção/ação | Componentes candidatos Astryx |
|---|---|---|
| O que gera engajamento? | Comparar plataforma, formato, categoria e faixa de seguidores | Card, Grid, Tabs/TabList |
| Patrocínio funciona? | Comparar recortes equivalentes e explicitar limites de investimento | Card, Badge, Banner |
| Quem mais engaja? | Comparar grupos predominantes por contexto, sem inventar indivíduos | Tabs/TabList, Card |
| O que não funciona? | Distinguir evidência de baixo desempenho de ausência de evidência | Card, Banner |
| Onde concentrar esforço? | Priorizar ações/hipóteses, sem frequência ou faixa ótima fictícia | Card, Badge |
| Qual política de patrocínio? | Condições de teste e simulação hipotética de custos | FormLayout, TextInput, Button |
| O que parar? | Separar recomendação proposta de desperdício financeiro comprovado | Card, Banner |
| Quais quick wins? | Ações concretas com justificativa e link à evidência | Card, Button |

Nomes são candidatos levantados por Sofia; conferir exports/API na versão instalada antes de codar. Table fica no aprofundamento, não como abertura da experiência. Evitar componentes experimentais lab/vega não publicados.

## Superfícies distintas

- **Dashboard:** resumo orientado às oito perguntas, simulador e chat contextual como diferencial.
- **Relatório executivo HTML:** análise e estratégia completas, separadas do dashboard e do visualizador.
- **Visualizador Ouro existente:** preservado em `solution/prototype/index.html`.

Botão **Ver relatórios** apresenta “Análise de performance e estratégia” e “Explorar os dados”. Abrir HTML em nova aba com indicação explícita; manter o estado do dashboard. Relatórios futuros são capacidade prevista, não links funcionais fictícios.

## Composição visual

Desktop: Layout/LayoutHeader/LayoutContent; header com identificação do challenge e Ver relatórios; Performance e estratégia como entrada, Explorar dados como aprofundamento; resumo e oito blocos na coluna principal; simulador/chat em coluna lateral, sem competir com a conclusão. AppShell apenas se necessário à estrutura de navegação.

Mobile: header compacto, navegação horizontal acessível, coluna única; botões para simulador/chat sem cobrir conteúdo/foco; tabela com scroll rotulado ou apresentação em cards. Não declarar validação mobile sem dispositivo real.

## Identidade G4 e fontes

Sofia reportou navy escuro, coral, branco e tipografia sans geométrica como referência observada em [G4 Educação](https://g4educacao.com/) e [blog oficial](https://g4educacao.com/blog). **Não encontrou manual oficial que estabeleça hex/fontes exatos.** Não fixar valores aproximados como tokens oficiais. Esta rodada da Lia não conseguiu abrir a home pela ferramenta web; a leitura visual é atribuída ao parecer da Sofia, não revalidada independentemente.

Usar tema por variáveis CSS, não copiar genericamente a aparência Meta/Cadência. Identificar a aplicação como solução independente do challenge; referência visual não significa afiliação oficial. Assets e fontes dependem de procedência e uso permitido.

[Astryx — fork de referência](https://github.com/felipeluissalgueiro/astryx) e [CLI](https://github.com/felipeluissalgueiro/astryx/blob/main/packages/cli/README.md). O README consultado confirma beta, theming por CSS variables e lab/vega ainda não publicados no npm. Compatibilidade da versão, React e build Next deve ser validada num teste mínimo; clone ausente neste host foi reportado por Sofia, não impeditivo para consultar documentação.

## Estados e aceite

- Loading: Skeleton com rótulo acessível.
- Recorte vazio: EmptyState e limpar filtros.
- Evidência insuficiente: motivo específico e próximo teste/medição; não confundir com desempenho ruim.
- Erro: tentar novamente sem perder evidência/filtros.
- Chat indisponível: relatório e simulador continuam funcionando; explicar que o chat não está disponível, sem resposta inventada.
- Dado observado, hipótese e simulação recebem rótulos textuais distintos; não depender só de cor.
- Teclado, foco visível, contraste, rótulos de campos, desktop e mobile real são critérios de validação futura.

## Guardrails de dados

Base simulada; creator_id canônico, nomes inconsistentes. Não usar elegibilidade superada ou measure_better fixo como motor. Datas aleatórias não sustentam frequência ótima. Ausência de custo/conversão/alcance/retenção é explícita. Simulador é hipotético. Todos os números devem reconciliar com evidências identificáveis.

## Pendências para arquitetura

Confirmar composição da RFC, contrato dos exports, versão/build Astryx, tokens e assets G4, acesso protegido Vercel e controles/modelo OpenRouter. Sem instalação, implementação ou deploy nesta investigação.
