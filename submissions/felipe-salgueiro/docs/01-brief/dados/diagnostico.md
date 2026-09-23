# Diagnóstico de dados — estado atual

## Observado

- Fonte oficial declarada como dataset simulado, sob licença MIT.
- CSV com 52.214 linhas e 27 colunas; `content_id` é único nas 52.214 linhas.
- O campo `engagement_rate` citado no enunciado não existe no CSV recebido.
- Cinco contagens foram convertidas em 52.214/52.214 linhas, sem inválidos ou
  zeros: views, likes, shares, comentários e seguidores.
- As distribuições são estreitas: views 9.676–10.551, likes 1.354–1.668,
  shares 227–380 e comentários 140–258.
- `comments_text` está presente em 43.526 posts (83,36%). O dicionário oficial
  o define como zero a cinco comentários concatenados. O texto pode demonstrar
  análise semântica no cenário simulado, mas não representa voz real de
  clientes.
- O contrato Silver de dimensões categóricas validou 52.214/52.214 linhas sem
  flags. Há 22.314 posts patrocinados (42,74%) e 29.900 não patrocinados
  segundo a flag (57,26%).
- A participação patrocinada é muito uniforme entre plataformas (41,92% a
  43,46%), formatos (42,42% a 42,86%) e categorias (42,46% a 43,12%).
- Entre 22.314 posts patrocinados existem 18.005 nomes de sponsor distintos;
  o maior aparece em 32 posts. A alta cardinalidade limita análises por marca.
- Existem 5.000 `creator_id`, cada um associado a 10 ou 11 posts. O dicionário
  oficial informa que o ID cicla por 5.000 creators e que `follower_count`
  representa seguidores na data do post. Portanto, variar seguidores não é
  defeito nem impede agregação pelo ID.
- A regra Silver anterior que exigia seguidores estáveis e produziu zero
  creators elegíveis está conceitualmente invalidada e não deve alimentar o
  Ouro ou o produto.
- Existe, porém, uma incompatibilidade real entre ID e nome: todos os 5.000 IDs
  têm múltiplos `creator_name` (mínimo 9, média 10,4422, máximo 11). Entre pares
  creator–plataforma com mais de um post, 100% usam múltiplos nomes: 3.294 no
  Bilibili, 3.229 no Instagram, 3.248 no RedNote, 3.224 no TikTok e 3.272 no
  YouTube. O ID pode ser usado como chave canônica da simulação; o nome não é
  confiável para exibição ou agrupamento.
- Há 42.213 nomes distintos; 6.309 aparecem associados a mais de um
  `creator_id`, com máximo de 19 IDs para o mesmo nome.
- As 52.214 datas são válidas no formato `M/D/YY h:mm AM/PM`, mas nenhuma
  informa fuso horário. O intervalo normalizado vai de 29/05/2023 00:15 a
  28/05/2025 11:08.
- O intervalo cobre exatamente 731 dias e todos têm posts. A mediana é 71 posts
  por dia, com mínimo 31, p99 93 e máximo 98. O dicionário oficial declara que
  as datas foram distribuídas aleatoriamente; a uniformidade é esperada na
  simulação, não um defeito de qualidade.
- Existem 50.905 instantes distintos; no máximo três posts compartilham o mesmo
  minuto. Dias da semana, horas e plataformas cobrem o período de forma quase
  uniforme.
- Apesar do sufixo `distribution`, o dicionário oficial define idade e gênero
  como grupo predominante da audiência e localização como local principal.
  São rótulos categóricos válidos para segmentar o cenário, não percentuais.
- Os 52.214 registros usam cinco faixas etárias, quatro rótulos de gênero e
  oito países conhecidos; 5.235 posts têm gênero `unknown`.
- Não existem IDs, `content_id` ou linhas-fonte totalmente duplicadas.
- Somente `comments_text` (8.688 vazios) e `hashtags` (8.743 vazios) têm string
  vazia; as demais 25 colunas estão preenchidas, incluindo sentinelas de
  ausência nos campos de sponsor.
- `content_length` é inteiro de 10 a 599 em todos os quatro formatos. Segundo o
  dicionário oficial, a unidade é segundos para vídeo e palavras para texto;
  a unidade de imagem e mixed não está especificada.
- As 52.214 descrições são únicas e todas são ASCII, inclusive quando o idioma
  declarado é Chinese, Hindi ou Japanese. O mesmo ocorre nos comentários.
- Hashtags são zero a cinco tokens separados por vírgula, sem `#`; 35.637
  combinações não vazias são distintas.
- Existem 28.037 URLs distintas e 24.187 hosts, divididos quase igualmente
  entre HTTP e HTTPS; não foram acessados.
- Para comparações foi criado um recorte amostral de seguidores declarados por
  post em quatro quartis, com aproximadamente 13 mil linhas por faixa. Os
  limites são 250.811, 498.488 e 749.826.
- A mediana de interações por view é 19,8977% nas linhas não patrocinadas
  segundo a flag e 19,9014% nas patrocinadas; views e interações têm a mesma
  mediana nos dois grupos: 10.100 e 2.010.
- Em 60 células plataforma × categoria × quartil, com 191–668 observações por
  lado, a diferença mediana patrocinado menos não patrocinado é +0,0024 ponto
  percentual; 33 células são positivas e 27 negativas. Os extremos são
  -0,1296 e +0,1125 ponto percentual.
- A correlação de Spearman da flag com views, interações totais e interações por
  view fica entre 0,0007 e 0,0012. Nesta simulação, a flag não separa os grupos
  de forma material; isso não prova efeito zero fora dela.
- Seguidores versus interações por seguidores tem rho -0,9991 e seguidores
  versus views por seguidores, -0,9998: as razões são dominadas mecanicamente
  pelo denominador, pois numeradores variam pouco.
- Entre métricas brutas, likes explica a maior parte da soma de interações
  (rho 0,857); views e interações totais são praticamente independentes
  (rho -0,0032).
- Não existem alcance, impressões, gasto, receita, conversões, visualizações de
  3 segundos, curva de retenção, conclusão de vídeo ou watch time.

## Hipótese

A dispersão estreita é compatível com o processo declarado: `views` foi gerado
por Poisson e as demais variáveis pertencem a um dataset simulado. Isso não
invalida a análise do cenário pedido no desafio; limita sua generalização para
operações reais e impede tratar os valores como benchmarks de mercado.

A uniformidade da taxa de patrocínio entre dimensões e a alta cardinalidade de
nomes também são compatíveis com geração sintética. Isso é hipótese sobre o
mecanismo gerador, não prova independente de como cada linha foi criada.

O período de dois anos e a distribuição quase uniforme refletem datas
aleatórias declaradas pelo publicador. Podem compor recortes descritivos do
cenário, mas não sustentam recomendação de horário ou cadência editorial.

A identidade textual incoerente com os idiomas, URLs Faker-like, comprimentos
iguais entre formatos e unicidade ampla dos textos são compatíveis com conteúdo
sintético. Features estruturais podem ser contadas, mas não transformam esse
material em voz ou criativo real.

As comparações Gold revelam diferenças pequenas, e a ordem dos segmentos muda
entre patrocinado e não patrocinado. Elas permitem rankings descritivos de
demonstração e priorização de testes, mas não sustentam corte ou escala. O
principal sinal aparente — taxas normalizadas por seguidores — é uma
consequência matemática do denominador e não uma evidência de preferência ou
qualidade.

## Limitações

- Views não substituem alcance, impressões ou retenção.
- Seguidores não são espectadores reais do post.
- `is_sponsored=false` significa somente “não patrocinado segundo a flag”; não
  prova distribuição orgânica.
- Data de publicação não assegura a mesma janela de exposição.
- O campo temporal não possui fuso nem instante de coleta das métricas; posts
  antigos e recentes não têm exposição comparável demonstrada.
- `creator_id` é a chave canônica declarada e pode sustentar rankings de
  demonstração com 10–11 posts por ID. `creator_name` é inconsistente e não
  pode rotular esses rankings de forma confiável.
- `follower_count` é uma fotografia válida na data do post; usar mediana,
  faixa ou valor contemporâneo, nunca exigir constância histórica.
- Os quartis de seguidores são relativos a esta amostra e não equivalem a
  categorias de mercado como nano, micro ou macro influenciador.
- Os rótulos de audiência representam grupos predominantes declarados e são
  válidos para segmentação do cenário; não identificam indivíduos nem trazem a
  composição percentual completa.
- Patrocínio sem gasto, receita e atribuição não permite ROI.
- Descrição, hashtags e comentários sintéticos permitem demonstrar
  classificação temática/semântica, mas não provar dúvidas ou objeções de uma
  audiência real. Gancho, contexto, explicação e CTA continuam sem marcação ou
  criativo integral.
- `content_length` deve ser interpretado como segundos em vídeo e palavras em
  texto. Para imagem e mixed, a unidade permanece não documentada.

## Próxima verificação

A respondibilidade revisada está em `relatorio-final.md`. O próximo Ouro deve
preservar os rankings descritivos do cenário, corrigir a elegibilidade de
creators usando `creator_id` como chave e transformar diferenças pequenas em
priorização de testes — nunca em corte ou escala automática. Para decisões
operacionais reais ainda são necessários alcance/impressões, janela de
exposição, eventos de vídeo, conteúdo verdadeiro, gasto e conversões.
