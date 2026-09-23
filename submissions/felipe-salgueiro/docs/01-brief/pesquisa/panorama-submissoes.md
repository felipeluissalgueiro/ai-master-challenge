<!-- Snapshot da nota Panorama das submissoes; 23/09/2026. Consulte revisao-critica.md antes de interpretar os totais. -->


# G4 AI Master — panorama das submissões públicas

## Cobertura e corte

Levantamento público do repositório [ai-master-challenge](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge), com corte em **2026-09-23T15:54:37Z (UTC)**. Foram paginadas 146 PRs: 126 abertas, 20 fechadas e nenhuma marcada como merged no endpoint. Esse estado não foi usado como sinal de aprovação, reprovação ou estágio de qualquer pessoa. O panorama está concluído; o inventário associado está **PARCIAL** porque ainda consolida algumas PRs em blocos, onde o requisito pede uma linha individual com URL.

Há 134 autores públicos (inclui um bot) e 133 PRs com estrutura de submissão convencional (`submissions/` com diretório); isso equivale a 123 logins nessa fatia. O repositório tem reenvios/atualizações: oito logins aparecem em mais de uma PR, com dez PRs excedentes. PRs #8/#9, #41/#49, #59/#77, #62/#78, #65/#86 e #119/#120 são exemplos de pares; #140/#141/#145/#147 são quatro cases de um mesmo login. Eles não devem ser somados como candidatos independentes.

Foram classificados 131 PRs de submissão por conteúdo de README, process-log, artefatos e/ou corpo da PR; duas permaneceram indeterminadas (#29, que parece um follow-up de log, e #71, sem identificação inequívoca no material textual). Onze PRs não tinham entrega dentro de `submissions/` no head inspecionado e foram separadas como não-conformes/não-submissão estrutural. A classificação por case é de cobertura declarada e artefatos presentes, não avaliação de execução.

| Case              | PRs com cobertura | % de 133 PRs estruturadas | Logins únicos | Observação                   |
| ----------------- | ----------------: | ------------------------: | ------------: | ---------------------------- |
| 001 — Churn       |                34 |                     25,6% |            32 | inclui 5 PRs multi-case      |
| 002 — Suporte     |                33 |                     24,8% |            33 | inclui 7 PRs multi-case      |
| 003 — Lead Scorer |                66 |                     49,6% |            62 | concentração clara do corpus |
| 004 — Social      |                 9 |                      6,8% |             9 | inclui 3 PRs multi-case      |

As linhas somam 142 coberturas, pois nove PRs cobrem dois ou quatro cases. Em denominador por candidato/login, os percentuais não são aditivos pelos mesmos motivos e por reenvios. Dois casos são indeterminados; não foram forçados a uma categoria.

## Padrões, diferenciais e riscos

O case 003 está saturado de dashboards React/Next/Streamlit e scores heurísticos por estágio, aging, valor e histórico. O padrão útil é explicabilidade por deal e filtros por vendedor/gestor; a lacuna recorrente é separar dados encerrados dos deals acionáveis e evitar usar informação posterior ao momento da decisão. Interfaces não provam funcionamento: neste levantamento não foram instaladas dependências, executados projetos ou acessadas demos.

No churn, há muitos notebooks e relatórios. O melhor padrão é juntar explicitamente as cinco tabelas, reportar a unidade de análise e distinguir associação de causalidade. Riscos recorrentes: joins que multiplicam assinaturas/uso, janela temporal não declarada, recomendações causais sem desenho causal e métricas de churn/receita sem denominador.

Em suporte, aparecem diagnóstico operacional, roteamento/classificação e front-ends. Os materiais mais úteis delimitam a intervenção humana, registram confiança/encaminhamento e estimam horas ou custo com premissas. A alternativa original para MAR-49 não deve repetir “classificador + dashboard”: vale discutir uma fila que evidencia incerteza, risco de automação e auditoria de decisão.

Social é menos concorrido e abre espaço para rigor: comparar patrocinado/orgânico requer controlar plataforma, categoria, período e tamanho de creator. A maior lacuna é tratar engajamento como causalidade de patrocínio sem contrafactual, custo demonstrado ou sensibilidade. Em todos os cases, process-log forte mostra hipótese, prompt/saída, verificação, correção e decisão humana; screenshot isolado ou narrativa sem rastreio é evidência fraca.

## Referências públicas por qualidade de evidência

Estas são referências de formatos e evidências, não ranking de pessoas nem inferência de situação seletiva.

- [PR #3](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/pull/3): README, aplicação front-end, engine de scoring, screenshots e registro de correção de score.
- [PR #4](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/pull/4): análise social, registro de evidências, scripts de validação e process-log extenso; a reavaliação pública do mantenedor está separada de nossa leitura.
- [PR #37](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/pull/37): entrega multi-case, útil para estudar consistência de produto e o custo de ampliar escopo.
- [PR #38](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/pull/38): documentação ampla de suporte e lead scoring, incluindo auditoria de aderência; alegações de validação permanecem alegações até reprodução independente.
- [PR #84](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/pull/84): comentário público documenta correção de join de produto, um sinal concreto de revisão sobre dados.

## Feedback de mantenedores versus inferências desta análise

Foram lidos 115 comentários de issue/PR e 6 comentários de revisão via API pública. Há feedback explícito de mantenedor sobre process logs insuficientes, estrutura fora de `submissions/`, dados reais, correções de join e revisões técnicas. Menções administrativas de inscrição/etapa posterior não são tratadas como prova de resultado nem aplicadas a autores sem comentário explícito. Padrões de leakage, causalidade, reprodutibilidade e cobertura acima são inferências deste levantamento, baseadas nos materiais públicos, não vereditos do G4.

## Oportunidades para discutir no MAR-49

1. Escolher um problema menos saturado que o lead score genérico e definir a decisão operacional antes da interface.
2. Tornar a unidade temporal auditável: o que era conhecido no momento da recomendação e o que só aparece depois.
3. Incluir um registro de decisão com confiança, evidência, exceção humana e custo; não apenas score e recomendação.
4. Mostrar verificação reprodutível por inspeção: comandos, dados de entrada, asserts e limitações, sem prometer execução que não foi demonstrada.

## Process Log — Como usei IA

### Ferramentas usadas e por quê

Usei Codex para organizar a investigação e `curl` na API pública do GitHub para paginação de PRs e comentários. Usei Git com `refs/pull/*/head` e filtro sem blobs para inspecionar o head de cada PR sem confundir com a branch deste worktree. Não foi observado modelo dos autores de forma confiável; quando uma ferramenta aparece em process-logs públicos, ela é evidência declarada pelo autor.

### Workflow

1. Li README raiz, CONTRIBUTING, submission-guide e os quatro enunciados.
2. Paginei `state=all`, fixei o corte UTC e contei estado, autores e SHAs.
3. Inspecionei árvore de arquivos dos 146 heads; li README, process-log e documentos textuais de 133 PRs estruturadas; li corpo de PR e comentários/reviews públicos relevantes.
4. Classifiquei case pelo conteúdo quando disponível, sinalizei multi-case, reenvio, indeterminado e ausência estrutural separadamente.

### Onde a IA errou e como corrigi

A primeira extração de Markdown incluiu READMEs de dependências vendorizadas, o que inflava ruído e atrasava a leitura. Corrigi o filtro para README/process-log/documentação no diretório de submissão, excluindo dependências. Também corrigi a contagem que confundia presença de `submissions/` com conformidade de diretório de autor; a nota separa essas situações.

### Direção humana versus decisões do agente

Direção humana: Felipe autorizou leitura pública integral, definiu os campos, o corte explícito, a vedação de execução/demos e as duas notas. O ajuste posterior exigiu esta seção de Process Log. Decisões do agente: método de inspeção, taxonomia estrutural, exemplos de referência e inferências analíticas. Nenhuma inferência foi atribuída a Felipe.

### Iterações

Não há número inventado de iterações. Registro apenas duas correções observáveis no workflow descritas acima. A investigação inclui paginação, extração estrutural e leitura documental; essas são etapas, não “iterações” equivalentes a ciclos de produto.

### Evidências e limitações

Fontes: API pública de PRs e comentários, heads `refs/pull/<n>/head`, corpo das PRs e arquivos versionados. Não executei código, instalei dependências, chamei demos ou validei links externos. Portanto, “funcional”, métricas, custos, testes e resultados descritos por autores permanecem declarações, salvo quando há arquivo/versionamento que permite apenas inspeção estática. O inventário detalha a profundidade real.
