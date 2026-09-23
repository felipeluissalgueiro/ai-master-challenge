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

- O corpo principal organiza as oito perguntas em três decisões: o que gera
  engajamento, se vale patrocinar influenciadores e qual estratégia adotar.
- O painel visual destaca os indicadores centrais e mantém uma escala comum
  para que diferenças de centésimos não pareçam grandes efeitos.
- Cada resposta exibe número, amostra, tabela de origem, cálculo e ID de
  evidência. IQR, correlações e hashes também ficam no apêndice recolhível.
- O dataset é simulado e não é benchmark de mercado.
- Diferenças observadas são descritivas; não são efeito causal, teste de
  equivalência ou limiar econômico.
- O recorte Instagram/Tech foi encontrado após examinar as combinações e serve
  apenas como exemplo exploratório de teste, se houver aderência comercial.
- Campos ausentes e análises pendentes são separados explicitamente.
