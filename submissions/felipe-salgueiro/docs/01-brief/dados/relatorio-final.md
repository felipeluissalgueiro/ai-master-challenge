# Relatório final — respondibilidade e decisão

Data da auditoria: 23/09/2026. Dataset recebido: 52.214 posts, 27 campos,
declarado pelo publicador como simulado. Este relatório não transforma
associação em causalidade e não treina modelo.

## Decisão executiva revisada

O pipeline Bronze → Silver → Gold é reproduzível e permite analisar o cenário
simulado proposto pelo desafio. Ser simulado não torna o dataset defeituoso: os
rankings descritivos são úteis para demonstrar a estratégia e priorizar testes.
Eles não são benchmarks de mercado nem justificam decisões causais em uma
operação real.

Não há diferença descritiva material entre patrocinado e não patrocinado
segundo a flag: ambos têm mediana de 10.100 views e 2.010 interações. A mediana
de interações por view é 19,9014% no patrocinado e 19,8977% no não patrocinado.
Nas 60 células comparáveis de plataforma × categoria × quartil de seguidores,
a diferença mediana é +0,0024 ponto percentual, com 33 direções positivas e 27
negativas. A leitura correta é “diferença pequena e instável neste cenário”,
não “efeito zero”. A estratégia é testar recortes promissores com critérios
prévios, sem corte ou escala automática, enquanto se melhora a medição.

## Matriz pergunta → evidência → decisão

| Pergunta | Campo/cálculo disponível | Resultado observado | Limite | Decisão permitida |
|---|---|---|---|---|
| Qual o engajamento disponível? | `(likes + shares + comments_count) / views` | Mediana geral próxima de 19,9% | Views não são alcance, impressões nem pessoas únicas | Usar somente como proxy descritiva desta amostra |
| Qual o “engajamento real”? | Interações / `follower_count` | Calculável, mas rho com seguidores = -0,9991 | Razão dominada mecanicamente pelo denominador; seguidores não são espectadores | Não chamar de engajamento real nem ranquear creators |
| Patrocínio melhora desempenho? | Flag, plataforma, categoria, quartil e métricas | Diferenças pequenas, alternando sinal; rho da flag entre 0,0007 e 0,0012 | Sem randomização, gasto, alcance ou janela comum | Priorizar testes; não afirmar efeito zero nem causalidade |
| Que plataforma/categoria/formato vence? | 68 resumos segmentados com n, mediana e IQR | Amplitude entre medianas de interações/views de 0,0201 a 0,0386 p.p. | Rankings pertencem ao cenário simulado | Exibir ranking descritivo e tamanho da diferença; não tratar como benchmark real |
| Que audiência prefere cada conteúdo? | Grupo predominante de idade/gênero e localização principal | 5 idades, 4 gêneros, 8 países | Não contém composição percentual nem identidade individual | Comparar os segmentos predominantes dentro do cenário |
| Qual creator performa melhor? | `creator_id`, 10–11 posts por ID, seguidores na data do post | Agregação por ID é permitida pelo dicionário oficial | `creator_name` é incompatível com o ID e não serve para exibição | Ranking demonstrativo por ID, com n e dispersão; corrigir a regra Silver anterior |
| Qual frequência funciona? | `creator_id` e data aleatória | Posts podem ser contados por ID | Datas foram sorteadas e não representam calendário editorial real | Não recomendar frequência/horário com esta fonte |
| O gancho segura após 3 segundos? | Nenhum evento de vídeo | Ausente | Views não substituem início nem retenção | Instrumentar início e view de 3 s |
| Qual a retenção final e o ponto de 50%? | Nenhuma curva/watch time/conclusão | Ausente | `content_length` é duração do vídeo, não retenção | Instrumentar curva temporal e eventos de conclusão |
| Gancho, contexto, explicação e CTA explicam desempenho? | Descrição resumida e comentários sintéticos | Textos únicos, ASCII e incoerentes com idiomas declarados | Não há criativo/roteiro real nem marcação estrutural | Não inferir; coletar conteúdo real e anotar blocos |
| Comentários revelam dúvidas e objeções? | Zero a cinco comentários concatenados, presentes em 43.526 posts | Texto sintético agregado | Sem autor, ordem ou thread; não representa clientes reais | Demonstrar temas no cenário, sem declarar voz real da audiência |
| Há ROI? | Nenhum gasto, receita, conversão ou atribuição | Ausente | `is_sponsored` não é custo nem mídia paga comprovada | Não calcular ROI |

## Observado

- CSV e ZIP conferem com os SHA-256 documentados; `content_id` não se repete.
- Cinco contagens numéricas são válidas nas 52.214 linhas, sem zeros, mas têm
  dispersão muito estreita.
- Existem 22.314 linhas patrocinadas e 29.900 não patrocinadas segundo a flag.
- Cada uma das 60 células comparativas tem 191–668 observações por lado;
  mediana 447. Tamanho amostral não corrige baixa validade da fonte.
- O dicionário oficial define 5.000 `creator_id` cíclicos e seguidores na data
  do post. Variação de seguidores é esperada e não invalida o creator.
- A incompatibilidade está no nome: todos os IDs têm 9–11 nomes e 100% dos
  pares creator–plataforma recorrentes têm mais de um nome.
- As datas cobrem os 731 dias entre 29/05/2023 e 28/05/2025 e foram geradas
  aleatoriamente, conforme declarado pelo publicador.
- `content_length` significa segundos em vídeo e palavras em texto. A unidade
  de imagem e mixed não foi documentada.
- Audiência representa grupos predominantes e localização principal, não
  percentuais completos.

## Hipóteses que não viraram conclusão

- A uniformidade de datas e a distribuição Poisson de views fazem parte do
  desenho declarado da simulação. As regras exatas de likes, shares,
  comentários e patrocínio não foram documentadas em código.
- Uma diferença em uma célula pode ser flutuação amostral. Não foi usado teste
  causal nem busca de significância porque a validade da medição falha antes.
- Conteúdo real poderia produzir relações entre tema, estrutura e retenção,
  mas os textos fornecidos não permitem testar essa hipótese.

## Limitações decisivas

- `is_sponsored=false` significa somente não patrocinado segundo a flag; não
  comprova distribuição orgânica.
- A data do post não garante mesma janela de exposição nem registra quando as
  métricas foram coletadas.
- `follower_count` é a quantidade declarada na data de cada post; não deve ser
  forçada a permanecer estável.
- `creator_name` não é consistente com `creator_id`; usar o ID como chave e um
  rótulo neutro na interface.
- `content_length` tem unidade conhecida somente para vídeo e texto.
- Views não substituem alcance, impressões, retenção ou pessoas únicas.
- Sem custo e receita atribuída não existe ROI; sem conteúdo real não existe
  auditoria válida de gancho/contexto/explicação/CTA.

## Próxima verificação em dados reais

Registrar por post e por janela de medição:

1. IDs estáveis de conta, creator, post e variante criativa.
2. Plataforma, formato, tema e marcações revisadas de gancho, contexto,
   explicação e CTA, com o conteúdo real preservado.
3. Publicação e coleta com fuso, idade do post e janelas comparáveis.
4. Impressões, alcance, frequência, inícios de vídeo, views de 3 s, curva de
   retenção, conclusões, duração e watch time.
5. Likes, comentários e compartilhamentos com comentários individuais e
   metadados mínimos para análise semântica responsável.
6. Gasto, campanha, conversões, receita e regra de atribuição versionada.

No cenário simulado, o padrão segmentado já permite rankings de demonstração e
priorização de testes, sempre expondo n, tamanho da diferença e limitações. Com
os campos adicionais, ele também poderá orientar ampliar/testar/reduzir/medir
melhor em dados operacionais. Ainda não há justificativa para modelo preditivo.

## Reprodutibilidade

```bash
python solution/analysis/run_pipeline.py \
  --csv /caminho/social_media_dataset.csv \
  --zip /caminho/dataset.zip \
  --database solution/data/generated/social_media_bronze.sqlite
```

O banco de trabalho em `solution/data/generated/` permanece derivado e
ignorado. Um snapshot integral e validado é entregue deliberadamente em
`solution/data/evidence/social_media_analysis.sqlite` para auditoria dos
avaliadores; ele não é utilizado no runtime da Vercel. O manifesto registra
hashes, contagens e a política de ambos os artefatos.
