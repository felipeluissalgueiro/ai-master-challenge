# Protótipo exploratório — relatório Ouro

Página HTML estática e autocontida, gerada deterministicamente das tabelas Ouro
do SQLite de evidência. Não possui login, LLM, backend, dependências externas ou
deploy. Não é a interface final aprovada.

## Gerar

A partir da raiz da submissão:

```bash
python3 solution/prototype/generate.py
```

O gerador abre por padrão
`solution/data/evidence/social_media_analysis.sqlite` com `mode=ro` e
`PRAGMA query_only = ON`, valida integridade e as três tabelas Ouro e grava
`solution/prototype/index.html`.

Para caminhos explícitos:

```bash
python3 solution/prototype/generate.py \
  --database solution/data/evidence/social_media_analysis.sqlite \
  --output solution/prototype/index.html
```

## Abrir

Abra `solution/prototype/index.html` diretamente no navegador. Não é necessário
iniciar servidor. Opcionalmente:

```bash
xdg-open solution/prototype/index.html
```

No GitHub, baixe o arquivo ou clone o fork e abra localmente. O GitHub exibe o
código-fonte do HTML, não hospeda esta página como site; deploy ficou
explicitamente fora deste protótipo.

## O que a página mostra

- comparações de engajamento por plataforma, formato, categoria, idade/gênero
  predominantes e localização principal;
- `n`, mediana e p25–p75 por segmento e grupo de patrocínio;
- as 60 comparações patrocinado versus não patrocinado, com filtros e magnitude
  do delta;
- achado descritivo, limitação e hipótese de próximo teste;
- fórmula, tabela de origem, hash do SQLite e natureza simulada da fonte.

## Limites deliberados

- Não usa `creator_profile_eligible` nem mostra ranking de creators.
- Não consome `action_candidate` nem apresenta `measure_better` como decisão.
- Não calcula ROI, alcance, impressões ou retenção ausentes.
- Não transforma diferenças pequenas em instrução de corte ou escala.
- Não altera o SQLite de evidência.
