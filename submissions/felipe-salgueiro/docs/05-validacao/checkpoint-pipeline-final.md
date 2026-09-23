# Checkpoint — pipeline analítico final

**Registro histórico:** conclusões abaixo precedem a [revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md). Para interpretação atual, use o [relatório revisado](../01-brief/dados/relatorio-final.md). Preservar este registro não valida regras superadas nem autoriza usá-las no produto.

Data: 23/09/2026. Referência documental:
`b137f2c46695996ed84726046d64e5c5acb3cc18`. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge ou PR.

## Pedido e decisão de Felipe

Felipe autorizou prosseguir continuamente até concluir o objetivo, registrando
um checkpoint ao fim de cada etapa. A arquitetura aprovada é Bronze → Silver →
Gold, com Python determinístico e SQLite local reconstruível. JEV foi removido
porque não aceita novas contas. Nenhum timestamp, alcance, retenção ou sinal
ausente foi inventado.

## Alterações deste bloco

- Restaurados na worktree isolada os dois scripts-base já publicados por Lia
  no checkpoint `b137f2c...`, sem alteração de conteúdo.
- Criado `solution/analysis/run_pipeline.py` para executar sequencialmente
  Bronze, sete transformações/auditorias Silver e Gold descritiva.
- Criado `docs/01-brief/dados/relatorio-final.md` com matriz de
  respondibilidade e decisão.
- Atualizados diagnóstico e manifesto para refletir a conclusão do pipeline.

SHA-256 dos scripts-base recuperados:

- `build_bronze.py`:
  `6b2033da25e0aab7be3c7ca36bfad3922e542fb0adba9790b4fc51ee60c72a4b`.
- `build_silver_metrics.py`:
  `e8add1ddd4181f711b6d4154b9d86cd517dfd67ac9398455c965ed168d951f1f`.
- `run_pipeline.py`:
  `9039350df7d8e5769eb45660ba062a7b7b4766289cd0ded80fe92a054021c28b`.

## Comando de integração executado

```bash
python submissions/felipe-salgueiro/solution/analysis/run_pipeline.py \
  --csv /tmp/g4-social-kaggle-OB927aw1/social_media_dataset.csv \
  --zip /tmp/g4-social-kaggle-OB927aw1/dataset.zip \
  --database /tmp/g4-social-final-K6Ux2A/social_media_bronze.sqlite
```

Também foram executados `PRAGMA integrity_check`, inventário de contagens,
hash do dump lógico e:

```bash
python -m py_compile submissions/felipe-salgueiro/solution/analysis/*.py
```

## Resultado real

- Pipeline completo: exit code 0.
- Compilação: exit code 0.
- Integridade: `ok`.
- Fonte: 52.214 linhas, 27 colunas.
- Paridade: 52.214 linhas em Bronze e em cada tabela Silver por post.
- Perfis de creator auditados: 5.000; elegíveis: zero.
- Definições de quartil: 4.
- Gold: 68 resumos, 60 células comparativas e 45 correlações.
- Decisão produzida: `measure_better`.
- SHA-256 físico do banco temporário:
  `44e51bf98d6c2e05d3f7b90c662223dd9ec130bd00ba2cd28c36ba309ded628d`.
- SHA-256 físico do banco persistente:
  `dfd96b591d495fc302cef20bbb25d98fef5f7e7670c4859694e6ddb769eea2c3`.
- Ambos têm o mesmo SHA-256 do dump lógico:
  `7e74618660769dfcd944c005844fd9cb02d51638fd0ead6ebeaa2ef2a6a5abc5`.

A diferença física é permitida pela serialização interna do SQLite; a
igualdade lógica demonstra reprodutibilidade do conteúdo.

## Erros e correções registrados

1. A primeira integração falhou com `ModuleNotFoundError: No module named
   'build_bronze'`: os dois scripts publicados no checkpoint de Lia ainda não
   existiam na worktree isolada. Foram copiados exatamente a partir de
   `b137f2c...` e os hashes coincidiram.
2. A repetição seguinte chamou parâmetros incorretos (`--db` e sem `--zip`). O
   parser recusou a execução; nenhum banco foi criado. A chamada foi corrigida
   para `--zip` e `--database` conforme `--help`.
3. A consulta auxiliar de inventário usou aspas duplas para `table` e presumiu
   `silver_follower_bands`. O SQLite recusou a consulta. O catálogo real foi
   lido de `sqlite_master` e a contagem refeita com
   `silver_posts_follower_bands`. Nenhum dado foi alterado.

## Conclusão e pendência

O objetivo analítico está concluído na worktree isolada. A fonte permite
demonstrar o método, não tomar decisão de marketing real. Não há pendência de
análise neste escopo; resta somente Lia integrar e publicar os caminhos
explicitamente selecionados, preservando sua documentação mais nova.

## Mapa de integração para Lia

Comparação feita contra o checkpoint publicado
`b137f2c46695996ed84726046d64e5c5acb3cc18`.

### Documentos alterados

| Caminho relativo a `submissions/felipe-salgueiro/` | SHA-256 |
|---|---|
| `docs/01-brief/dados/diagnostico.md` | `d3ef48e8ca176ef6433ce747a2fdca28f189c7c4f776a409434d3f8565836356` |
| `docs/01-brief/dados/catalogo-metricas.md` | `60c0ab409811321ec5e12dd40d7a8468d135a6f7fddcfe294954eeaed7a38594` |
| `docs/01-brief/dados/manifest.json` | `777c71cea76120f7e7cdee136c73218dc58cc50c1aa6c7c2487b3136f792bf9f` |

### Documentos novos

| Caminho relativo a `submissions/felipe-salgueiro/` | SHA-256 |
|---|---|
| `docs/01-brief/dados/relatorio-final.md` | `0c08fabd4cd0475138137a615b7bc39c00a859a7065ad6976c33ef9ec7b58b50` |
| `docs/05-validacao/checkpoint-silver-dimensions.md` | `683290b4461d6d97ccf1af42e8c95ab2ee908c8bd6def39538e80e7812204d93` |
| `docs/05-validacao/checkpoint-silver-creators.md` | `6730ffce8beb268a2c8825f9539fac219f42186419b3e0c388dbff5d444478fd` |
| `docs/05-validacao/checkpoint-silver-dates.md` | `e4a0ae981189737b3d6a3e653868fa0420da95ca784a4e677da6d60d036dfa57` |
| `docs/05-validacao/checkpoint-silver-audience.md` | `af13e93304d6419bc482bdd68c294880f6e14caba8b71ee0fb1efe3b604a5f1f` |
| `docs/05-validacao/checkpoint-silver-content.md` | `5a41e9193213583f06cd7bcb72ef0d48808fcd1b1157a5c7e02a8672ca140332` |
| `docs/05-validacao/checkpoint-silver-follower-bands.md` | `32b6853c026625ab652ad0fe888d7daf973923283316a11d64980e716bf57b97` |
| `docs/05-validacao/checkpoint-gold-comparisons.md` | `fe16bb32ae9dbdf44471aafe68eec243eb5cc24f6af7c23905c1c2d2611c0481` |

Este próprio checkpoint deve ser integrado pela versão presente na worktree;
seu hash final é informado no terminal após esta atualização, evitando um hash
autorreferente dentro do arquivo.

### Scripts novos

| Caminho relativo a `submissions/felipe-salgueiro/` | SHA-256 |
|---|---|
| `solution/analysis/build_silver_dimensions.py` | `dd8de14a843ab91f9f7365904d8007780733bb8af9e42f7967908a3f89b58e3d` |
| `solution/analysis/build_silver_creators.py` | `ed91e5c31138ccb4568a9d13a83c39572afd6ae8a77bff6269c183b9591a6279` |
| `solution/analysis/build_silver_dates.py` | `fc845250367e6372403aa696be55abed4989235dc2ee641f45e4b252ede63029` |
| `solution/analysis/build_silver_audience.py` | `ef1373c48e868a97ddd7da7e48f376fe2460a3967f5f8577996d191a84ea946d` |
| `solution/analysis/build_silver_content.py` | `aa283624d0e80011cdd083d1d3f8aa88e34474cd61ecc108032da0ec79e2a161` |
| `solution/analysis/build_silver_follower_bands.py` | `40336c6b29212c3eccde1343791eb821dc8067020138c3066e247a7ba787afb5` |
| `solution/analysis/build_gold_comparisons.py` | `dfd1b042e98c81a9895fc978420936937d17297daa4f2abcdeef984fb871268b` |
| `solution/analysis/run_pipeline.py` | `9039350df7d8e5769eb45660ba062a7b7b4766289cd0ded80fe92a054021c28b` |

### Arquivos já publicados e inalterados

- `solution/analysis/build_bronze.py` —
  `6b2033da25e0aab7be3c7ca36bfad3922e542fb0adba9790b4fc51ee60c72a4b`.
- `solution/analysis/build_silver_metrics.py` —
  `e8add1ddd4181f711b6d4154b9d86cd517dfd67ac9398455c965ed168d951f1f`.

O SQLite em `solution/data/generated/` permanece artefato derivado ignorado e
não integra o checkpoint Git.
