# Checkpoint — revisão pelo dicionário oficial

Data: 23/09/2026. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge, PR, snapshot
ou exportação.

## Motivo

Felipe questionou corretamente se a simulação havia sido tratada como defeito.
O diagnóstico foi confrontado com a descrição oficial da versão 1 do dataset
no endpoint Kaggle. A análise numérica verde não foi reconstruída.

## Definições oficiais que mudam a interpretação

- `creator_id` identifica o creator e cicla por 5.000 IDs.
- `follower_count` é a quantidade de seguidores na data do post; variar é
  esperado.
- `content_length` é segundos para vídeo e palavras para texto.
- Os campos de audiência são grupo predominante/localização principal.
- `post_date` foi distribuído aleatoriamente nos dois anos.
- `views` foi simulado por distribuição Poisson.
- `comments_text` agrega de zero a cinco comentários concatenados.
- O dataset é simulado e licenciado sob MIT.

## Incompatibilidade real quantificada

`creator_name` não acompanha o identificador declarado:

| Plataforma | Pares creator–plataforma recorrentes | Pares com múltiplos nomes |
|---|---:|---:|
| Bilibili | 3.294 | 3.294 (100%) |
| Instagram | 3.229 | 3.229 (100%) |
| RedNote | 3.248 | 3.248 (100%) |
| TikTok | 3.224 | 3.224 (100%) |
| YouTube | 3.272 | 3.272 (100%) |

Globalmente, os 5.000 IDs têm múltiplos nomes: mínimo 9, média 10,4422 e
máximo 11. O produto pode usar `creator_id` como chave canônica da simulação,
mas não deve usar `creator_name` como rótulo confiável.

## O que muda

- A regra que zerou creators elegíveis por exigir seguidores estáveis está
  invalidada e deve ser corrigida antes do Ouro exportado.
- Rankings por `creator_id` podem ser produzidos como demonstração, sempre com
  n, dispersão e rótulo neutro.
- Segmentos predominantes de audiência podem participar das comparações.
- Comprimento pode ser analisado em segundos para vídeo e palavras para texto,
  nunca misturando as unidades; imagem/mixed continuam indefinidos.
- Datas aleatórias e views Poisson são desenho da simulação, não falha de
  qualidade.
- Diferenças pequenas sustentam priorização de testes, não prova de efeito zero,
  corte ou escala.
- `medir melhor` continua necessário para uso operacional real, mas não é a
  única resposta ao cenário simulado do desafio.

## O que não muda

- Não há alcance, impressões, gasto, receita, conversões, retenção de três
  segundos, curva de retenção, conclusão ou watch time.
- ROI e causalidade continuam não calculáveis.
- `is_sponsored=false` continua significando apenas não patrocinado segundo a
  flag.
- Comentários e descrições podem demonstrar método, mas não representam voz
  real de clientes.
- Nenhum modelo foi treinado.

## Erros e correções durante a revisão

- A primeira leitura do endpoint presumiu a chave `datasetFiles`; a API usa
  `files`. A estrutura foi lida com `jq 'keys'` antes da extração correta.
- A primeira consulta aos resumos Ouro presumiu `dimension` e `segment`; as
  colunas reais são `slice_type` e `slice_key`. A consulta foi refeita sem
  alterar dados.

## Pendência controlada

Não foi alterado código Silver/Gold, snapshot, exportador ou PRD. A regra de
creator e os rankings devem ser ajustados somente após o contrato Ouro ser
fechado com Lia e Felipe.
