# QA remoto — Brave e preparação do PR

## Método e versão

Subagente Camila, Preview `dpl_8SoT2viBwVyBdzvCPJfB2iHV93Ab`, código
`5fca9b2`. Navegação real por DOM/CUA na extensão Brave, sem Playwright.
Resultados abaixo reportados pelo subagente; não reexecutados pela coordenação.

## Cobertura observada

| Área | Resultado observado |
|---|---|
| Home | Três decisões visíveis; sete dimensões selecionadas |
| Comparações | Formato → Vídeo: 31.500 posts, mediana 19,895%; mudar dimensão reseta grupo; limpar retorna Plataforma; URL com grupo inexistente mostra recorte vazio |
| Relatórios | Listagem com dois relatórios; executivo em iframe e tela inteira; três âncoras carregaram seções |
| Visualizador | Conteúdo carregou; botão de tela inteira acionado, destino não inspecionado |
| Explorar | Iframe interativo e gráfico por formato; Bilibili + Beleza + Q1: 438 patrocinados, 633 sem marcação, diferença −0,0417 p.p. |
| Simulador | 2000/10000/2000/20 → R$200 por mil views, R$1 por interação, R$100 por venda; alteração invalida resultado; zero vendas e formulário vazio tratados |

Uma suspeita de link quebrado foi descartada: o navegador abriu nova aba.

## Achados e correções locais

1. Títulos encobertos pelo menu fixo ao acessar `#engajamento`, `#patrocinio` e `#estrategia`. Removido posicionamento sticky do menu no gerador; relatório regenerado. Menu continua navegável, sem sobrepor as seções.
2. Rótulos `mixed` e `Select…` na comparação. Adicionadas tradução “Misto” e placeholders explícitos em português conforme contrato Selector do Astryx.

As duas correções passaram no reteste abaixo. A regeneração preservou
evidence.json e SQLite; somente apresentação/manifesto do relatório mudou.

## Reteste direcionado na Preview corrigida

Deployment `dpl_3c4p61YaXRvN4LPdhUJhMEA8JwVU`, Brave DOM/CUA, sem Playwright.
Resultado reportado pelo mesmo subagente:

- Três títulos de âncora completos, sem sobreposição: corrigido.
- “Misto” selecionável, URL `value=mixed`; vazio com “Selecione um grupo”: corrigido.
- Fluxo home → relatórios → explorar → simulador concluído por cliques.
- Vendas negativas e fracionárias rejeitadas; cenário válido recalculou R$100/venda, R$200/mil views, R$1/interação.
- 404 e retorno à home funcionaram.
- Viewport 390×844: home legível e navegação ao simulador; formulário em uma coluna, sem corte lateral observado. Não é teste de todas as rotas em mobile.
- Nenhum painel/controle de chat observado nas telas inspecionadas.

Achado menor remanescente: erros exibiam `sales`. Tradução dos nomes dos quatro
campos corrigida posteriormente, com teste de regressão específico. Lint, tipos,
19 testes unitários e build passaram. Não houve mudança de fórmula.

Último reteste na Preview `da2ghmdai` pelo Brave DOM/CUA: mensagens para vendas
`-1` e `1,5` iniciaram com **Vendas**, sem `sales`. Confirmado visualmente pelo
subagente; a primeira aba ficou indisponível, uma nova aba permitiu concluir.
Sem bloqueio pendente nesses casos. A matriz inteira não foi repetida.

## Cobertura pendente

Ausência parcial e outros zeros do simulador no navegador (cobertos em testes
unitários); mobile em todas as rotas; matriz completa de teclado e acessibilidade.
Teclado usado em rolagem e filtros nativos
não equivale a auditoria de acessibilidade completa.

**Conclusão:** QA parcial, sem aprovação integral da matriz.
