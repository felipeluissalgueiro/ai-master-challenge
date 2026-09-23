# Evidência analítica — Challenge 004

Esta pasta entrega o banco SQLite completo da análise para auditoria pelos
avaliadores e por ferramentas LLM. O objetivo do banco não é obrigar uma pessoa
a ler 52 mil linhas: ele preserva a cadeia de evidência entre fonte, tratamento
e conclusões.

## Artefatos

- `social_media_analysis.sqlite`: evidência integral Bronze, Prata e Ouro.
- `manifest.json`: hashes, tamanho, proveniência, contagens, licença e limites.
- `README.md`: racional e contrato de interpretação.

O banco não é utilizado no runtime da aplicação Vercel. A aplicação e o chat
consumirão exportações Ouro menores e versionadas. Este SQLite existe para que
um avaliador ou LLM consiga auditar como uma conclusão foi produzida.

## Por que SQLite

SQLite foi escolhido porque reúne, em um arquivo portátil e sem servidor:

- a fonte preservada;
- transformações determinísticas;
- resultados analíticos;
- tipos e índices;
- consultas reproduzíveis.

Isso evita planilhas desconectadas, permite verificar a linhagem de uma métrica
e mantém o artefato independente de VPS, credenciais e serviços externos.

## Por que Bronze, Prata e Ouro

```text
CSV Kaggle
   │
   ▼
Bronze — preservar o recebido e sua proveniência
   │
   ▼
Prata — tipar, padronizar, validar e derivar métricas
   │
   ▼
Ouro — responder perguntas comparáveis com n, mediana, dispersão e limites
   │
   ├──► exportação estática para UI
   └──► contexto controlado para o chat explicativo
```

### Bronze: evidência, não opinião

`bronze_posts_raw` mantém as 52.214 linhas como chegaram no CSV. Essa camada
permite confirmar que uma plataforma, contagem, flag ou texto existia na fonte.
`bronze_manifest` e `bronze_columns` registram ingestão e estrutura.

O Bronze não recebe interpretação de marketing. Sua função é impedir que uma
transformação apague a origem do dado.

### Prata: um contrato por responsabilidade

A Prata foi separada em tabelas temáticas para que cada transformação possa ser
auditada sem misturar conceitos:

| Tabela | Responsabilidade |
|---|---|
| `silver_posts_metrics` | Converter contagens e calcular métricas por post |
| `silver_posts_dimensions` | Padronizar plataforma, conteúdo e patrocínio |
| `silver_creator_profiles` | Auditar recorrência e identidade de creators |
| `silver_posts_dates` | Normalizar data e registrar validade temporal |
| `silver_posts_audience` | Representar grupos predominantes declarados |
| `silver_posts_content` | Medir estrutura de descrição, comentário, hashtags e URL |
| `silver_posts_follower_bands` | Classificar seguidores na data do post em quartis da amostra |
| `silver_follower_band_definitions` | Tornar explícitos os limites dos quartis |

Separar as tabelas reduz acoplamento: uma correção de creator não precisa
reescrever a regra de audiência, e uma nova métrica não altera o Bronze.

Correção conhecida: a versão atual de `silver_creator_profiles` marcou zero
creators elegíveis porque exigia `follower_count` estável. O dicionário oficial
define seguidores na data do post, portanto essa regra está superada. Para
leitura atual, use `creator_id` como chave canônica e ignore
`creator_profile_eligible` e `creator_name` em rankings.

### Ouro: decisão explicável, não dado bruto

O Ouro reduz 52.214 posts a três superfícies de decisão:

| Tabela | Pergunta respondida |
|---|---|
| `gold_segment_summaries` | Como cada plataforma, formato, categoria, audiência e faixa se comporta? |
| `gold_sponsorship_comparisons` | Patrocinado difere de não patrocinado dentro de recortes comparáveis? |
| `gold_numeric_correlations` | Quais variáveis variam juntas e quais relações são mecânicas? |

Os resultados trazem tamanho da amostra (`n`), mediana, p25, p75 e limite de
interpretação. A mediana foi priorizada porque reduz a influência de extremos;
p25–p75 mostra a dispersão central; `n` impede apresentar uma célula pequena
como uma verdade geral.

## Métricas e racional

### Interações totais

```text
likes + shares + comments_count
```

Soma somente as três interações presentes no dataset.

### Interações por view

```text
100 × total_interactions / views
```

É a principal proxy comparável disponível. Não é engagement por alcance,
impressões ou pessoas únicas, porque esses campos não existem.

### Interações por seguidores

```text
100 × total_interactions / follower_count
```

É mantida como descrição, não como “engajamento real”. Nesta amostra a razão é
quase determinada pelo denominador; não deve ser usada isoladamente para dizer
que creators menores são melhores.

### Patrocínio

As comparações usam células de plataforma × categoria × quartil de seguidores
na data do post. Isso torna os grupos mais comparáveis do que uma média geral.
Ainda assim, a análise é observacional: `is_sponsored=false` significa apenas
“não patrocinado segundo a flag”, e não existe custo, receita ou atribuição para
calcular ROI.

## Como um LLM deve consultar este banco

Ordem obrigatória de leitura:

1. Ler `manifest.json` e este contrato.
2. Consultar as tabelas Ouro para responder perguntas de negócio.
3. Citar tabela, chaves do segmento, `n`, métrica, mediana e dispersão.
4. Consultar a Prata para explicar fórmula, classificação ou qualidade.
5. Consultar o Bronze apenas para verificar o valor de origem.
6. Declarar métricas ausentes em vez de estimá-las.

Um LLM pode explicar uma recomendação determinística, mas não deve criar
classificações, substituir cálculos SQL/Python ou decidir autonomamente.

Formato mínimo de uma resposta fundamentada:

```text
Conclusão descritiva:
Evidência: <tabela + segmento + n + mediana/p25/p75>
Comparação:
Limitação:
Próximo teste:
```

## Regras de interpretação

- O dataset é simulado por definição e serve ao cenário do desafio; não é um
  benchmark de mercado real.
- Diferença pequena não significa efeito comprovadamente zero, mas também não
  sustenta corte ou escala automática.
- Correlação não demonstra causalidade.
- `creator_id` é a identidade canônica; `creator_name` é inconsistente.
- `follower_count` é a quantidade na data do post e pode variar.
- `content_length` é segundos para vídeo e palavras para texto; não misturar as
  duas unidades. Imagem e mixed permanecem sem unidade documentada.
- Idade/gênero representam grupo predominante, e localização representa o local
  principal; não são distribuições percentuais completas.
- Datas foram geradas aleatoriamente e não sustentam recomendação de horário ou
  frequência editorial.
- Views foram simuladas por Poisson.
- Comentários agregados permitem demonstrar método sem representar voz real de
  clientes.
- Alcance, impressões, gasto, receita, conversões e retenção de vídeo estão
  ausentes e nunca devem ser inventados.

## Integridade e proveniência

| Propriedade | Valor |
|---|---|
| Tamanho | 61.607.936 bytes (58,75390625 MiB) |
| SHA-256 do SQLite | `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad` |
| SHA-256 do dump lógico | `7e74618660769dfcd944c005844fd9cb02d51638fd0ead6ebeaa2ef2a6a5abc5` |
| `PRAGMA integrity_check` | `ok` |
| Tabelas / índices explícitos | 14 / 9 (mais 7 índices automáticos do SQLite) |
| Fonte | Social Media Sponsorship & Engagement Dataset — omenKJ/Kaggle |
| Natureza | Simulada, declarada pelo publicador |
| Licença | MIT |

O dump lógico do snapshot é igual ao do artefato validado que o originou. O
backup foi criado pelo mecanismo nativo do SQLite, sem reconstruir o pipeline e
sem mover ou apagar o banco original.

## Entrega pelo GitHub

O arquivo tem 58,75 MiB: ultrapassa o patamar de aviso de 50 MiB, mas permanece
abaixo do limite rígido de 100 MiB para Git regular. Como excede 25 MiB, não
pode ser enviado pela interface web; a integração é pela linha de comando.
Journals, WAL, SHM e bancos auxiliares continuam ignorados.

Referência: [limites oficiais de arquivos do GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

## O que este banco não é

- Não é banco de produção nem backend da Vercel.
- Não contém ROI, alcance ou retenção que não existiam na fonte.
- Não é prova causal.
- Não é corpus para o LLM recalcular ou inventar decisões.
- Não substitui as exportações Ouro versionadas que alimentarão a aplicação.
