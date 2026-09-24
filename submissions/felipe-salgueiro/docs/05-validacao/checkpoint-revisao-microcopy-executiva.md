# Checkpoint — revisão de microcopy executiva

Data: 23/09/2026. Trabalho executado somente na worktree
`analysis/felipe-salgueiro-data`. Sem stage, commit, push, PR ou deploy.

## Pedido de Felipe

Remover textos que explicavam as mudanças feitas no relatório ou falavam sobre
a própria construção da página. Exemplos rejeitados:

- “Para facilitar a leitura, os resultados foram traduzidos...”;
- “Três decisões que os dados sustentam agora”.

## Regra aplicada

O relatório mantém somente:

1. conclusão;
2. consequência para o negócio;
3. ação recomendada;
4. definição indispensável da métrica.

Instruções de navegação permanecem apenas no explorador do SQLite, onde são
necessárias para operar filtros e interpretar pontos, faixas e amostras.

## Alterações

- “Três decisões que os dados sustentam agora” virou “Decisões para conteúdo e
  investimento”;
- o parágrafo sobre “facilitar a leitura” virou uma definição direta da unidade;
- “Como interpretar o painel” virou “Limite da decisão”;
- “O que os dados mostram” virou “Resultado observado”;
- “Resposta direta” virou “Decisão”;
- a abertura da comprovação passou a “Fontes, cálculos e limites”;
- textos de implementação como “protótipo estático”, “sem backend”, “por
  escolha de escopo” e “não é interface final aprovada” foram removidos das
  páginas;
- título, status e rodapé do explorador passaram a descrevê-lo como explorador
  de dados, sem narrar o processo de desenvolvimento.

## Verificações

```bash
python -m py_compile solution/reports/generate.py solution/prototype/generate.py
python solution/reports/generate.py
python solution/prototype/generate.py
rg -i 'para facilitar|foram traduzid|tradução executiva|sustentam agora|como interpretar|relatório principal traduz|protótipo estático|não é interface final|sem login|sem llm|sem backend|sem deploy|por escolha de escopo|regra histórica' \
  solution/reports/performance-strategy.html solution/prototype/index.html
```

Resultado: nenhuma expressão de bastidor procurada permaneceu nas páginas;
HTML sem IDs duplicados ou links locais ausentes. SQLite permaneceu inalterado,
com `integrity_check=ok`, leitura `mode=ro`/`query_only=1` e SHA-256
`7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.

## Hashes finais deste checkpoint

| Arquivo | SHA-256 |
|---|---|
| `solution/reports/README.md` | `fee0900b5b2f936124e7d6e4e43fa342b04b5127e46ace75837ef8d36f987377` |
| `solution/reports/generate.py` | `c46a209e7202ae170087b563c3583936732f2bee14dd03141b378649e8656f68` |
| `solution/reports/evidence.json` | `de0502d33bec4b09fe6970686196f4c83c1fe484b659c40fc607b75d6d1ddf1d` |
| `solution/reports/performance-strategy.html` | `b3f4a9e1cb3a04021926fef6aa3d98910fdefd5a6830cc004b25009194e98f2f` |
| `solution/reports/manifest.json` | `f86dc7edec0e4a6364cecc661b475ff21518e085787eb4687509ba60050236ed` |
| `solution/prototype/README.md` | `36c0e1d51d61ef54dd7e494ebd5d700474584935c58fb24b35ab8f9319dd59ea` |
| `solution/prototype/generate.py` | `e21a6478443b287c4089a19b246427cb9bd47a71a9274ae8f2e8bd9a4be753de` |
| `solution/prototype/index.html` | `4bb3b412f47ba9932fe78db3eeeb74a90088b6bee1ff4a559deda090731d767b` |

Lia deve revisar e integrar somente após validação de Felipe.
