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

Correções ainda aguardam reteste na nova Preview. A regeneração preservou
evidence.json e SQLite; somente apresentação/manifesto do relatório mudou.

## Cobertura pendente

Negativos, fracionários, ausência parcial e outros zeros do simulador; viewport
mobile; matriz completa de teclado; 404; ausência de chat em todas as rotas;
segunda rodada do caminho crítico. Teclado usado em rolagem e filtros nativos
não equivale a auditoria de acessibilidade completa.

**Conclusão:** QA parcial, sem aprovação integral da matriz.
