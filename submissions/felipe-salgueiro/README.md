# Submissão — Felipe Salgueiro — Challenge 004

**Preview publicada; preparação do PR em andamento.** [Abrir aplicação](https://g4-social-insight-the4349yo-felipeluissalgueiros-projects.vercel.app), sem login. Pipeline, dashboard, relatórios, explorador e simulador integrados. QA remoto no Brave parcial; [cobertura e achados](docs/05-validacao/checkpoint-qa-brave.md). [Estado do deploy](docs/05-validacao/checkpoint-preview-vercel.md).

## Sobre mim
- **Nome:** Felipe Salgueiro.
- **LinkedIn:** a conferir.
- **Challenge:** 004 — Estratégia Social Media.

## Executive Summary
Escolhi o case pela minha experiência com marcas e conteúdo. Usei IA para investigar uma base sintética e transformar a análise em dashboard, relatório executivo e explorador. As diferenças descritivas não justificam prometer um canal vencedor ou retorno financeiro sem custos e conversões. Recomendo testes orientados ao objetivo da campanha e medição antes de ampliar ou cortar investimentos; um simulador separado permite explorar custos hipotéticos sem inventar vendas.

## Solução

### Acesso e roteiro de avaliação

Abra a **[Preview pública](https://g4-social-insight-the4349yo-felipeluissalgueiros-projects.vercel.app)** no navegador. Não precisa de conta, senha, chave de API ou instalação.

1. **Performance e decisões:** leia os três cards e o plano de ação proposto. Eles separam engajamento observado, condições de patrocínio e lacunas para decidir cortes.
2. **Comparações:** escolha dimensão e grupo. A URL e o painel comparativo mudam; as conclusões gerais não são recalculadas pelo filtro.
3. **Ver relatórios:** abra o relatório executivo para consultar as oito respostas, gráficos e provas. Use a opção de tela inteira para leitura ampliada.
4. **Explorar dados:** consulte o dicionário e os recortes do Ouro. O navegador lê artefatos exportados; não acessa o SQLite diretamente.
5. **Simulador:** informe um cenário. Exemplo: R$ 2.000, 10.000 views, 2.000 interações e 20 vendas resultam em R$ 200 por mil views, R$ 1 por interação e R$ 100 por venda. Esses valores são hipotéticos, não resultados do dataset.

Para rodar localmente, clone o fork e siga o [setup da aplicação](solution/app/README.md). Para conferir a origem dos números, consulte o [banco de evidência](solution/data/evidence/README.md). O snapshot é sintético e estático: não é um painel conectado aos canais ou CRM do G4.

[Relatório executivo para o Head de Marketing](solution/reports/README.md): oito respostas organizadas em três pilares, provas numéricas e estratégia. Acesse pela aplicação ou baixe/clone e abra `solution/reports/performance-strategy.html` no navegador.

As versões iniciais foram reprovadas por mim e reformuladas para leitura gerencial. As correções e os limites dos testes estão nos [checkpoints](docs/05-validacao/).

[Aplicação e setup](solution/app/README.md), [contrato de dados](solution/data/app/README.md) e [simulador](docs/05-validacao/checkpoint-mar103-simulator.md): cálculo determinístico de custo por mil views, interação e venda; cenário hipotético, não resultado comercial observado.

[Explorador dos dados Ouro](solution/prototype/README.md): disponível na aplicação e como HTML local em `solution/prototype/index.html`. O GitHub exibe o código-fonte; a Preview permite navegar.

### Abordagem
Preservar a fonte na camada Bronze; validar e derivar métricas na Prata; somente depois produzir comparações e recomendações. [Brief consolidado](docs/01-brief/brief.md).
### Resultados / Findings
Pipeline analítico, banco de evidência, exportador e comparações descritivas integrados. A análise utiliza 52.214 posts; os resultados e suas provas estão no relatório executivo. [Reprodução e artefatos](solution/README.md).
### Recomendações
Priorizar testes de conteúdo e medir o resultado correspondente ao objetivo da campanha antes de ampliar ou cortar investimento. O relatório detalha condições, limites e ações; o plano semanal é proposto, não uma série temporal real do G4.
### Limitações
Fonte sintética; sem retenção de 3s, alcance, impressões, custos ou conversões. Campos textuais não serão tratados como voz real da audiência. Patrocínio não comprova mídia paga; associação não prova causalidade.

## Process Log — Como usei IA
### Ferramentas usadas
Codex e personas do PD Framework; Gemini em uma consulta trazida por mim; Herdr, Linear, Obsidian e Git. [Método de trabalho](docs/metodo/README.md).
### Workflow
Comparei os cases, questionei recomendações da IA, escolhi Social Media e organizei a investigação. [Registro detalhado](process-log/workflow.md).
### Onde a IA errou e como corrigi
Uma lembrança sobre Tallis não foi confirmada e deixou de sustentar a escolha. Questionei o PRD elaborado sem discussão suficiente, reprovei relatórios tecnicamente corretos mas difíceis de usar e pedi conclusões, números contextualizados e ações. Também retirei o chat para concentrar a entrega no que já estava sustentado por dados. Os prints e o workflow mostram essas intervenções.
### O que eu adicionei que a IA sozinha não faria
Trouxe meu contexto de marcas/conteúdo, propus examinar gancho/contexto/informação/chamada se houver dados e defini o foco do projeto. São contribuições observáveis, não alegações de exclusividade humana.

## Evidências
- [Planejamento e issues exportadas](docs/04-planejamento/issues/README.md) — leitura no próprio repositório, sem depender do Linear ou da renderização do GitHub Projects.
- [Projeto e marcos](docs/00-projeto/README.md).
- [Documentos por etapa](docs/README.md).
- [Pesquisa preparatória e ressalvas](docs/01-brief/pesquisa/README.md).
- [Workflow](process-log/README.md), [cinco screenshots comentados](process-log/evidencias/README.md) e [proveniência dos exports](docs/proveniencia.md).

O [snapshot integral do banco](solution/data/evidence/README.md) está no fork com manifesto e limites conhecidos; a aplicação usa exportações Ouro, sem SQLite no deploy. O histórico Git registra a evolução, sem retroagir datas. Gravações e notebook não anexados: o guia aceita formatos alternativos. Chat com LLM e integração ao CRM não fazem parte da versão entregue.

**Submissão enviada em:** não enviada.
