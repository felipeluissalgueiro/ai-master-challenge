# Checkpoint — Silver de audiência

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado apenas na branch local
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e hipótese

Felipe pediu verificar se os dados permitem entender que audiência engaja. A
hipótese deste bloco era que os três campos chamados de `distribution`
pudessem conter composições percentuais. Antes de associá-los às métricas, foi
necessário validar sua estrutura real.

## Alteração

Criado `solution/analysis/build_silver_audience.py`. O script reconstrói
`silver_posts_audience`, valida vocabulários e registra explicitamente a
granularidade `single_label_per_post`, sem converter rótulos em distribuições.

SHA-256:
`ef1373c48e868a97ddd7da7e48f376fe2460a3967f5f8577996d191a84ea946d`.

## Comando e teste

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_audience.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Conferência posterior: contagens somente leitura, `PRAGMA integrity_check` e
hashes do script, banco e dump lógico.

## Resultado observado

- 52.214 linhas e 52.214 registros válidos; zero flags.
- Idade: 13–18, 7.852; 19–25, 18.276; 26–35, 15.700; 36–50, 7.736;
  50+, 2.650.
- Gênero: female, 20.743; male, 20.987; non-binary, 5.249; unknown, 5.235.
- País: Brazil 6.505; China 6.648; Germany 6.497; India 6.484; Japan 6.553;
  Russia 6.459; UK 6.570; USA 6.498.
- `PRAGMA integrity_check`: `ok`.

## Conclusão e limite

Apesar dos nomes das colunas, não existem percentuais nem vetores de
distribuição. Cada linha tem apenas um rótulo de idade, gênero e país. Esses
rótulos podem formar recortes descritivos de posts, mas não identificam quem
visualizou, interagiu ou converteu. Associação posterior não será chamada de
preferência ou causalidade da audiência.

## Erros e correções

O script concluiu na primeira execução, sem erro. A hipótese de distribuição
percentual foi rejeitada pela estrutura observada; nenhum percentual inexistente
foi fabricado.

## Artefato local

- Banco ignorado: `solution/data/generated/social_media_bronze.sqlite`.
- SHA-256 físico:
  `b652c46a6a03364bcb47f3509959e7478d8cf060334cefcdfca8f7f8d87b1f00`.
- SHA-256 do dump lógico:
  `e682b5b9e14b675cdac29c2364e6c32004a03659a566e9d1dd2f95733ae4ec0c`.

## Pendência

Auditar estrutura global, nulos, duplicatas, unidades e conteúdo antes das
comparações descritivas.
