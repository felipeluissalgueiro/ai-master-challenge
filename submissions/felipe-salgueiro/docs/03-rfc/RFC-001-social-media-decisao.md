# RFC-001: Evidência, decisão e explicação de Social Media

> **Status:** Rascunho consolidado para revisão técnica; não implementada.
> **Data:** 2026-09-23 · **Autor:** Felipe, com consolidação por Lia e insumos de Vitor/Sofia.
> **Projeto:** [P-MAR-55](https://linear.app/cadencia/project/tech-g4-ai-master-challenge-004-social-media-6da71df65f6c)
> **PRD:** [v0.5](https://linear.app/cadencia/document/prd-challenge-004-estrategia-social-media-rastreavel-53e713ae38cf)
> **Fonte canônica:** submissions/felipe-salgueiro/docs/03-rfc/RFC-001-social-media-decisao.md no fork. Linear é espelho.

## Contexto e organização

Uma RFC cobre a entrega: patrocinado e não patrocinado são recortes do mesmo contrato analítico, não sistemas distintos. O Head precisa entender as oito perguntas, decidir e conferir a evidência. Preservar três artefatos: visualizador Ouro existente, relatório executivo HTML separado e dashboard/simulador/chat como diferencial. O relatório entregue pelo agente segue preliminar; não presumir integração ou validação visual.

## Componentes e fluxo

`SQLite de evidência (offline, somente leitura) → exportador Python → JSON versionado → dashboard Next.js/TypeScript + relatórios estáticos`

O dashboard chama uma rota servidor separada para explicação via OpenRouter. Simulador e leitura dos relatórios não dependem dessa chamada. Vercel hospeda aplicação/rota; sem SQLite em runtime, VPS ou migração da operação Cadência. Versões de dependências serão fixadas após teste de compatibilidade.

## Contratos entre componentes

| Fronteira | Entrada → saída e falha |
|---|---|
| Exportador → consumidores | Snapshot com hash conhecido → JSON com `schema_version`, hash da origem, métrica/fórmula/unidade/agregação, filtros, n, dispersão, exclusões e evidências com IDs estáveis. Taxas usam %, diferenças usam pontos percentuais. Valores indisponíveis são `null` com motivo, nunca zero. Hash/esquema/validação incompatíveis interrompem a exportação. Não reescrever o snapshot histórico. |
| Evidência → recomendação | IDs de evidência + regra determinística identificada → pergunta, conclusão, ação candidata, justificativa, limites e estado observado/hipótese/insuficiente. Não usar elegibilidade histórica superada ou `measure_better` fixo. Sem threshold validado, não classificar automaticamente em cortar/escalar. |
| UI → simulador | Custo e componentes declarados, vendas hipotéticas inteiras, referência de views/interações e unidade/período compatíveis → custo/1.000 views, custo/interação e custo/venda. Cálculo puro compartilhado/testável, independente de LLM. Rejeitar negativos/não finitos; denominador zero/vazio produz resultado não calculável com motivo. |
| UI → chat servidor | `recommendation_id`, versão do snapshot e pergunta limitada → servidor resolve evidências autorizadas e monta contexto; cliente não fornece fatos ou instruções de sistema. Resposta: explicação, IDs de evidência e limites. IDs desconhecidos retornam erro; referências inventadas são rejeitadas. Não executar ferramentas nem cálculos de negócio no LLM. |
| Servidor → OpenRouter | Chave exclusiva somente no servidor; modelo permitido por configuração, não pelo cliente. Limites de entrada/contexto/saída, timeout e controle de chamadas serão fixados/testados na Story. Não registrar chave ou conversa integral. Falta de configuração/proteção mantém chat indisponível, não endpoint aberto. |

A evidência é a fonte numérica comum; não redigitar números em HTML/cards/chat. O JSON do relatório preliminar será reconciliado com o contrato da UI, sem assumir que já é o export final. Se houver adaptação, usar transformador explícito e testar concordância.

## Interface e componentes visuais

Hierarquia: **conclusão → 1–2 números contextualizados → ação → evidência**. Entrada “Performance e estratégia”; aprofundamento “Explorar dados”. Os oito blocos cobrem engajamento, patrocínio, audiência, o que não funciona, concentração, política de patrocínio, o que parar e quick wins.

Astryx seletivo: Layout/LayoutHeader/LayoutContent, Card, Grid, Tabs/TabList, Badge, Banner; Table apenas no aprofundamento; EmptyState, Skeleton, Button, TextInput e FormLayout. Conferir exports na versão instalada; não depender de lab/vega experimentais. Desktop: coluna principal e lateral contextual de simulador/chat. Mobile: coluna única, tabs acessíveis, tabela adaptada e CTA sem cobrir conteúdo/foco.

“Ver relatórios” abre o relatório executivo ou o visualizador em nova aba, preservando filtros; URLs relativas ao mesmo projeto, sem links futuros fictícios. Assets estáticos publicados devem incluir seus JSON/manifesta/links de método necessários, com teste de resolução.

Referência G4: navy/coral/branco e sans conforme observação da Sofia; hex/fontes propostos são aproximados, não manual oficial. Usar tokens CSS e identificação de solução independente. [Parecer completo e wireframes](parecer-ux-sofia-g4-challenge004-20260923.md) e [síntese](ux-sofia.md) detalham os oito blocos.

## Regras de domínio e falhas

- Base sintética; creator_id canônico, nomes inconsistentes. Flag falsa não comprova distribuição orgânica; views não são alcance; diferenças descritivas não provam causalidade/equivalência. Datas aleatórias não justificam frequência ótima.
- Simulador explicitamente hipotético: custo de campanha não divide mediana por post sem premissa compatível. R$ 2.000 / 20 vendas = R$ 100/venda; zero vendas: “sem vendas atribuídas no cenário”. Custo/venda não é CAC.
- CRM, leads/vendas reais e CAC: não mensurados/futuro, nunca zero inventado. Benchmark externo só com fonte, período e fórmula comparáveis; ausência não bloqueia o núcleo.
- Loading, recorte vazio, insuficiência e erro são estados distintos. Chat indisponível não bloqueia análise ou simulação. Não fazer retry automático de inferência paga; evitar envio duplo e descartar resposta obsoleta após troca de recomendação.
- Proteção nativa Vercel é a direção acordada, mas exige verificação cobrindo páginas e rota. Configuração da chave/orçamento no provedor fica fora da atuação da Lia por determinação de Felipe; criação da chave foi confirmada por ele. US$ 5 foi sugestão não aprovada, não configuração existente.

## Regras resolvidas no grill e pendências

**Segue para consolidação documental**, após orientação de Felipe para prosseguir. Mantidos dados offline, Vercel, Astryx, três artefatos, cálculo determinístico, chat contextual e configuração da chave fora desta atuação. Isso não declara aprovação final dos detalhes técnicos propostos.

Pendências da implementação: schema final/IDs e regras de suficiência; compatibilidade Astryx; modelo e parâmetros técnicos do chat; mecanismo efetivo de limitação de chamadas e proteção Vercel. Sem valores configurados/verificados, chat falha fechado. Resolver nas Stories antes de habilitar, sem reabrir decisões de produto.

## Validação e sequência

1. **Evidência/comparações:** esquema, hashes, reconciliação de números, n/denominadores, ausência dos campos superados e oito perguntas rastreáveis.
2. **Decisão/simulador/UI:** testes das fórmulas e zeros/vazios, filtros, links dos dois relatórios, teclado/contraste e desktop/celular real.
3. **Chat protegido:** acesso não autorizado negado, limites aplicados, perguntas fora de contexto, referências inválidas, indisponibilidade, envio duplo e ausência de segredo no bundle/logs.

Critérios são futuros, não PASS. [Gate Vitor](../04-planejamento/gate-tecnico-vitor.md) fundamenta as três Epics; tickets ainda não criados por esta RFC. Deploy e PR final exigem autorização própria.

## Fora de escopo e alternativas

Sem preditor/Jiang, SLM treinada, CRM real, scraping, login próprio, banco em produção ou port da plataforma Cadência. SQLite/VPS em runtime foram descartados por complexidade desnecessária neste escopo; usar LLM para calcular foi descartado por falta de determinismo. Não implementar gráficos ou classificações sem evidência.
