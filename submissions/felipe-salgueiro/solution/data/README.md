# Dados e evidência

`generated/social_media_bronze.sqlite` permanece banco de trabalho local reconstruível e ignorado. Por decisão de Felipe, um snapshot integral consistente será entregue em `evidence/social_media_analysis.sqlite`, acompanhado de manifesto, hashes e instruções. **Snapshot ainda não preparado nem publicado.** A exceção de versionamento será limitada a esse arquivo; temporários, journals, WAL e SHM continuam excluídos.

A aplicação na Vercel consumirá resultados Ouro exportados, não este banco em produção. Contrato e exportador ainda pendentes. CSV/ZIP são obtidos do Kaggle; scripts e evidências permitem reproduzir o processamento.

Proveniência e limites em [diagnóstico](../../docs/01-brief/dados/README.md); comandos em [Solução](../README.md). A interpretação analítica está em revisão contra o dicionário oficial; não tratar o relatório anterior como conclusão definitiva.
