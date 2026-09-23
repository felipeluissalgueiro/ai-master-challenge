# Diagnóstico de dados — estado atual

## Observado

- Fonte oficial declarada como dataset simulado, sob licença MIT.
- CSV com 52.214 linhas e 27 colunas; `content_id` é único nas 52.214 linhas.
- O campo `engagement_rate` citado no enunciado não existe no CSV recebido.
- Cinco contagens foram convertidas em 52.214/52.214 linhas, sem inválidos ou
  zeros: views, likes, shares, comentários e seguidores.
- As distribuições são estreitas: views 9.676–10.551, likes 1.354–1.668,
  shares 227–380 e comentários 140–258.
- `comments_text` está presente em 43.526 posts (83,36%), mas o conteúdo é
  sintético, sem estrutura por comentário e incoerente com os idiomas
  declarados. Não representa voz real da audiência.
- Não existem alcance, impressões, gasto, receita, conversões, visualizações de
  3 segundos, curva de retenção, conclusão de vídeo ou watch time.

## Hipótese

A dispersão estreita das contagens é compatível com o processo de simulação
declarado pelo publicador. Comparações internas podem demonstrar o método, mas
não estabelecem benchmarks reais nem efeito causal.

## Limitações

- Views não substituem alcance, impressões ou retenção.
- Seguidores não são espectadores reais do post.
- `is_sponsored=false` significa somente “não patrocinado segundo a flag”; não
  prova distribuição orgânica.
- Data de publicação não assegura a mesma janela de exposição.
- Patrocínio sem gasto, receita e atribuição não permite ROI.
- Descrição, hashtags e comentários sintéticos não permitem inferir com
  validade gancho, contexto, explicação, CTA, dúvidas ou objeções reais.

## Próxima verificação

Auditar dimensões e consistência antes de qualquer comparação: patrocínio,
plataforma, formato, categoria, repetição de creator, datas, seguidores por
creator e distribuições demográficas. Comparações posteriores devem informar
recorte, tamanho de amostra, dispersão e ausência de causalidade.
