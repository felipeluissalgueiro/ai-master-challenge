# Checkpoint — Silver temporal

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado somente na branch
local `analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e decisão de Felipe

Felipe determinou que a análise use apenas campos presentes na tabela e seja
segmentada antes das inferências. Este bloco valida exclusivamente `post_date`.
Não calcula frequência por creator, porque o checkpoint anterior invalidou essa
identidade, nem presume janela igual de exposição.

## Hipótese

Era necessário verificar formato, validade e cobertura temporal antes de usar
datas como dimensão. A hipótese de trabalho era que o campo pudesse descrever o
período da amostra, mas não necessariamente frequência editorial ou idade
comparável das métricas.

## Alteração

Criado `solution/analysis/build_silver_dates.py`. O script preserva o texto
original, converte estritamente o formato `M/D/YY h:mm AM/PM` para ISO, deriva
data/ano/mês/hora/dia da semana e grava `timezone_known=0`. Nenhum fuso,
timestamp de coleta ou instante ausente foi fabricado.

SHA-256 do script:
`fc845250367e6372403aa696be55abed4989235dc2ee641f45e4b252ede63029`.

## Comando executado

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_dates.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Depois foram executadas consultas somente leitura de paridade, intervalo e
`PRAGMA integrity_check`, além dos hashes do script, banco e dump lógico.

## Resultado observado

- 52.214 datas válidas e zero inválidas.
- Zero linhas com fuso horário conhecido.
- Primeiro instante: `2023-05-29 00:15:00`.
- Último instante: `2025-05-28 11:08:00`.
- Período inclusivo: 731 dias; todos os 731 dias têm posts.
- 50.905 instantes exatos distintos; máximo de três posts no mesmo minuto.
- Posts por dia: mínimo 31; mediana 71; p99 93; máximo 98.
- Por ano: 15.506 em 2023; 26.288 em 2024; 10.420 em 2025. Os anos de borda
  são parciais.
- Dias da semana variam de 7.343 a 7.537 posts.
- Horas do dia variam de 2.097 a 2.267 posts.
- Todas as cinco plataformas aparecem desde o primeiro dia e chegam ao último
  dia do intervalo, com diferenças apenas de horas.
- Banco mantém 52.214 linhas Bronze, métricas, dimensões e datas, além de 5.000
  perfis de creator.
- `PRAGMA integrity_check`: `ok`.

## Observado, hipótese e limite

Observado: o dataset cobre exatamente dois anos, todos os dias, com distribuição
quase uniforme por dia da semana, hora e plataforma. Hipótese: o padrão é
compatível com datas sorteadas no gerador sintético. Limite: não prova o
algoritmo exato de geração.

O período pode ser usado para descrever a amostra. Não permite recomendar
frequência, comparar idade de posts ou chamar diferenças temporais de tendência:
não há fuso, instante de coleta das métricas nem janela de exposição.

## Erro e correção

A inspeção exploratória inicial tentou `date(post_date)` no SQLite e retornou
52.214 valores não reconhecidos; `MIN`, `MAX` e `SUBSTR` também produziram ordem
lexicográfica e agrupamentos incorretos. Nenhum desses resultados foi usado. O
campo foi então convertido estritamente em Python com `%m/%d/%y %I:%M %p` e
validado linha a linha.

## Artefato local

Banco ignorado pelo Git:
`solution/data/generated/social_media_bronze.sqlite`.

- SHA-256 físico após este segmento:
  `424d99c4bb704678f3906119c3ee4d9d94a8b519201ac188c45b711990239321`.
- SHA-256 do dump lógico:
  `6fe6e88a8853c4886bfc25a18a3e21c79587320af61e4aadcd874665d980d1e3`.

## Pendências

Auditar distribuições demográficas. Faixas de seguidores por post e qualquer
comparação de performance permanecem não iniciadas.
