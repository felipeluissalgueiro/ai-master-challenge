# Checkpoint — estrutura e conteúdo

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e hipótese

Felipe pediu verificar nulos, duplicatas, unidades e se conteúdo permite
analisar gancho, contexto, explicação, CTA e comentários. A hipótese era que a
presença das colunas textuais poderia não representar conteúdo real do post.

## Alteração

Criado `solution/analysis/build_silver_content.py`. O script reconstrói
`silver_posts_content` e calcula somente features observáveis: comprimento,
palavras, caracteres não ASCII, quantidade de hashtags, presença de texto de
comentário e validade estrutural de URL. Não classifica semântica.

SHA-256:
`aa283624d0e80011cdd083d1d3f8aa88e34474cd61ecc108032da0ec79e2a161`.

## Comando e teste

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_content.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Conferência posterior: paridade, `PRAGMA integrity_check`, hashes do script,
banco e dump lógico.

## Resultado observado

- 52.214 linhas estruturais válidas; zero flags.
- Zero IDs duplicados, zero `content_id` duplicados e zero linhas-fonte
  totalmente duplicadas.
- Vazios: 8.688 em `comments_text` e 8.743 em `hashtags`; zero nas demais 25
  colunas.
- `content_length`: inteiro de 10 a 599; os quatro formatos usam todos os 590
  valores. Medianas: image 173, mixed 175, text 174, video 174. Unidade ausente.
- Descrição: 52.214 valores únicos; 29–302 caracteres, mediana 120; 6–42
  palavras, mediana 18.
- Comentários presentes: 43.526; todos distintos. Mediana 109 caracteres, 16
  palavras e três marcas de sentença.
- Hashtags: zero a cinco tokens; mediana dois; tokens separados por vírgula e
  sem prefixo `#`.
- URLs: 28.037 valores distintos, 24.187 hosts; 26.209 HTTP e 26.005 HTTPS.
- Todos os textos de descrição e comentário são ASCII, inclusive nas linhas
  Chinese, Hindi, Japanese e Spanish.
- `PRAGMA integrity_check`: `ok`.

## Conclusão e limite

A estrutura é completa e parseável, mas os sinais textuais são compatíveis com
dados Faker/sintéticos e incoerentes com o idioma declarado. Descrição,
hashtags e comentários não permitem inferir com validade gancho, contexto,
explicação, CTA, dúvidas ou objeções reais. URLs não foram acessadas e não são
tratadas como mídia do post.

`content_length` não recebe unidade na tabela e não pode ser chamado de duração
ou tamanho textual. Sua distribuição praticamente idêntica entre image, mixed,
text e video reforça a necessidade de não interpretar a unidade.

## Erros e correções

O script concluiu na primeira execução. Nenhuma classificação semântica foi
tentada e nenhum texto ausente foi imputado.

## Artefato local

- Banco ignorado: `solution/data/generated/social_media_bronze.sqlite`.
- SHA-256 físico:
  `8c71ce1ccf0cd0d83ddf90af7206d9a4eed95f445aebf080d99045340d1a0624`.
- SHA-256 do dump lógico:
  `dc907912b76a6fcbc96969731426e7ae8672e335baec6e2bc50c75a2c5aee596`.

## Pendência

Definir faixas de seguidores declarados por post e construir comparações
descritivas, sem causalidade.
