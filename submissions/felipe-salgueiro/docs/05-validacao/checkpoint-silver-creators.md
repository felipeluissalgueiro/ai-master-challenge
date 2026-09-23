# Checkpoint — Silver de creators e seguidores

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado exclusivamente na
branch local `analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou
PR.

## Pedido e decisão de Felipe

Felipe determinou segmentar os dados antes de qualquer inferência e pediu
comparações posteriores por faixa de creator. Este bloco verifica se
`creator_id`, `creator_name` e `follower_count` formam perfis consistentes antes
de criar essas faixas. Datas, demografia e performance permanecem fora do
escopo.

## Hipótese

Se um `creator_id` representar a mesma entidade entre posts, ele deve ao menos
ter identidade nominal utilizável. Seguidores podem variar ao longo do tempo,
mas não devem ser transformados em perfil canônico quando a própria identidade
é inconsistente.

## Alteração

Criado `solution/analysis/build_silver_creators.py`. O script reconstrói a
tabela `silver_creator_profiles` com contagens de posts, nomes, plataformas e
valores de seguidores por ID. Nome canônico e elegibilidade só são preenchidos
quando a identidade é consistente; o script não escolhe arbitrariamente o
primeiro nome ou uma média de seguidores.

SHA-256 do script:
`ed91e5c31138ccb4568a9d13a83c39572afd6ae8a77bff6269c183b9591a6279`.

## Comando executado

```bash
python submissions/felipe-salgueiro/solution/analysis/build_silver_creators.py \
  --database submissions/felipe-salgueiro/solution/data/generated/social_media_bronze.sqlite
```

Depois foram executadas consultas somente leitura de paridade e `PRAGMA
integrity_check`, além de hashes do script, banco físico e dump lógico.

## Resultado observado

- 52.214 posts e 5.000 `creator_id`.
- 2.786 IDs têm 10 posts; 2.214 têm 11 posts.
- Todos os 5.000 IDs têm múltiplos nomes.
- Todos os 5.000 IDs têm um valor de seguidores diferente em cada post.
- Zero identidades consistentes e zero perfis elegíveis para agregação.
- Nomes distintos por ID: 2.787 IDs com 10 nomes, 2.212 com 11 e um ID com 9.
- Plataformas distintas por ID: 2 IDs em 2 plataformas; 211 em 3; 1.974 em 4;
  2.813 em 5.
- Amplitude de seguidores dentro de um mesmo ID: mínimo 246.977; mediana
  842.331,5; p99 982.719,45; máximo 996.601.
- Existem 42.213 nomes distintos; 6.309 nomes estão ligados a múltiplos IDs;
  um mesmo nome chega a 19 IDs.
- Banco: 52.214 linhas Bronze, métricas e dimensões; 5.000 perfis de creator.
- `PRAGMA integrity_check`: `ok`.

## Observado, hipótese e limite

Observado: `creator_id` agrupa 10–11 linhas, mas não preserva nome nem valor de
seguidores. Hipótese: o padrão é compatível com atribuição sintética e
independente desses campos. Limite: não é possível determinar apenas pela
tabela como o gerador construiu cada campo.

Consequência: frequência, evolução de audiência, perfil médio ou tamanho
estável por creator não são respondíveis. `follower_count` pode permanecer como
atributo declarado de cada post, desde que qualquer recorte seja chamado de
“faixa de seguidores declarada no post”, não “faixa de creator”.

## Erros e correções

O script foi executado uma vez e concluiu sem erro. Nenhum nome, plataforma ou
valor de seguidores foi selecionado como canônico quando a identidade falhou.

## Artefato local

Banco ignorado pelo Git:
`solution/data/generated/social_media_bronze.sqlite`.

- SHA-256 físico após este segmento:
  `3a59524ecc78e00522fa500eec823fc68da18ed1274a63813cb4862195c05cca`.
- SHA-256 do dump lógico:
  `4a95543b37d89e4492b542e5dae267d73e7f9ca0dda2c29847bbb5d705f46822`.

## Pendências

Auditar datas/período e depois distribuições demográficas. A definição de
faixas de seguidores por post exige decisão explícita sobre cortes; nenhuma
faixa, correlação ou comparação de performance foi criada neste bloco.
