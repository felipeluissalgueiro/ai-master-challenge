# Relatório executivo — performance e estratégia

Entrega humana dos itens obrigatórios **Análise de performance** e
**Estratégia recomendada** do Challenge 004. É o relatório executivo estático e
autocontido para o Head de Marketing; o visualizador exploratório permanece como
artefato separado em `../prototype/`.

## Abrir

Abra `performance-strategy.html` diretamente no navegador. Não há login,
backend, LLM, dependência externa ou deploy.

## Regerar

A partir da raiz da submissão:

```bash
python3 solution/reports/generate.py
```

O gerador abre `../data/evidence/social_media_analysis.sqlite` com SQLite URI
`mode=ro`, ativa `PRAGMA query_only=ON`, valida a integridade e produz:

- `evidence.json`: números e conclusões estruturadas usados pelo relatório;
- `performance-strategy.html`: relatório executivo autocontido;
- `manifest.json`: linhagem, hashes, tabelas consultadas e limites.

Para caminhos explícitos:

```bash
python3 solution/reports/generate.py \
  --database solution/data/evidence/social_media_analysis.sqlite \
  --evidence solution/reports/evidence.json \
  --output solution/reports/performance-strategy.html \
  --manifest solution/reports/manifest.json
```

## Contrato de leitura

- O corpo principal responde aos três pilares: o que gera engajamento, se vale
  patrocinar influenciadores e qual estratégia de conteúdo adotar.
- Os indicadores usam interações adicionais a cada 10 mil visualizações como
  unidade de comparação executiva.
- A leitura executiva apresenta conclusão, implicação e ação; amostra,
  mediana, IQR, correlações, nomes SQL e hashes ficam no apêndice recolhível e
  no explorador de dados.
- As oito perguntas do desafio possuem uma cobertura resumida no apêndice.
- O dataset é simulado e não é benchmark de mercado.
- Diferenças observadas são descritivas; não são efeito causal, teste de
  equivalência ou limiar econômico.
- ROI permanece desconhecido porque gasto, conversão, receita e atribuição não
  existem na fonte.
- O relatório não recomenda vencedor, corte, frequência ou threshold que os
  dados não sustentem.
