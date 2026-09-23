# Checkpoint — protótipo HTML estático do Ouro

Data: 23/09/2026. Executado somente na branch
`analysis/felipe-salgueiro-data`, sem stage, commit, push, merge, PR ou deploy.
O SQLite de evidência, Brief e PRD não foram alterados.

## Pedido e decisão

Felipe pediu uma entrega pequena: página HTML estática, autocontida e gerada a
partir das tabelas Ouro, sem login, LLM, backend ou deploy. A página deve expor
engajamento por dimensões, magnitude de patrocínio, decisão com limites e
rastreabilidade. É identificada como protótipo exploratório, não interface
final aprovada.

Dois campos foram deliberadamente excluídos:

- `creator_profile_eligible`, cuja regra está superada;
- `action_candidate`, que contém o valor histórico fixo `measure_better`.

Ranking de creators ficou fora, sem bloquear as demais dimensões.

## Implementação

Criados em `solution/prototype/`:

- `generate.py`: gerador Python 3, somente biblioteca padrão;
- `index.html`: relatório estático autocontido;
- `README.md`: como gerar e abrir localmente.

O gerador usa URI SQLite com `mode=ro`, ativa `PRAGMA query_only = ON`, executa
`PRAGMA integrity_check` e exige as três tabelas:

- `gold_segment_summaries`;
- `gold_sponsorship_comparisons`;
- `gold_numeric_correlations`.

## Conteúdo da página

- 52.214 posts simulados identificados como cenário, não benchmark real.
- Plataforma, formato, categoria, idade/gênero predominantes e localização
  principal, com `n`, mediana e p25–p75.
- 60 células patrocinado versus não patrocinado, com magnitude, filtros e
  escala centrada em zero.
- Achado descritivo, limitação e hipótese de próximo teste.
- Fórmula, origem, hash do banco e correlações de controle.
- Aviso explícito de que diferenças pequenas não autorizam corte ou escala.

## Comando realmente executado

Da raiz da submissão:

```bash
python3 solution/prototype/generate.py
```

Resultado:

- SQLite lido:
  `solution/data/evidence/social_media_analysis.sqlite`;
- HTML gerado: `solution/prototype/index.html`;
- tamanho final: 93.599 bytes;
- servidor local de prévia: `python3 -m http.server 8766 --bind 127.0.0.1`;
- resposta HTTP: `200 OK`.

## Verificações executadas

- `PRAGMA integrity_check`: `ok`.
- SHA-256 do SQLite permaneceu
  `7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad`.
- AST do gerador Python: válido.
- HTML parseável: válido.
- JavaScript inline: sintaxe validada com `node --check`.
- Assets externos: zero.
- Dados incorporados: 58 linhas das dimensões escolhidas, 60 comparações.
- Contagens Ouro conferidas: 68 resumos, 60 comparações, 45 correlações.
- `action_candidate` ausente do JSON incorporado.
- `creator_profile_eligible` ausente dos dados incorporados.
- Geração repetida em arquivo temporário: saída byte a byte idêntica (`cmp`).

Hashes finais:

- `generate.py`:
  `7f39863914d56f3a21c095346a66ff361eb5dbea542c4fe618645c95aa1e8b45`;
- `index.html`:
  `a7387dfb3b65c2b6dbb2e607856613e23d5fd75323f7ebe1173b219e325be194`;
- `README.md`:
  `5589905a9747b86bdce1d4f927cd1aaf13cfaf2abd4683ac5d5fff10020bbc60`.

## Erro e correção

O primeiro validador procurou a frase `Dataset simulado` com capitalização
exata e falhou, embora a página já trouxesse `dataset simulado` e `natureza
simulada`. A asserção foi corrigida para comparação sem depender de maiúsculas;
a validação seguinte passou. O erro não alterou página, banco ou dados.

Durante a revisão do HTML, foi identificado que `SELECT *` incorporava
`action_candidate` ao JSON mesmo sem exibi-lo. O gerador foi corrigido para uma
lista explícita de campos permitidos; o valor fixo não integra o HTML final.

## Pendência

Lia deve revisar e portar somente os três arquivos de `solution/prototype/` e
este checkpoint para `submission/felipe-salgueiro`, atualizar o workflow e
publicar no fork. A página pode ser aberta localmente a partir do repositório;
nenhum deploy foi autorizado ou realizado.
