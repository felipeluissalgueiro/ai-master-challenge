# Validação

## Aplicação e entrega

- [Preview e QA remoto](checkpoint-preview-vercel.md): ambiente publicado, acesso público e cobertura do navegador.
- [QA visual local](checkpoint-qa-visual-local.md): evidência local, distinta da validação remota.
- [Política de quality gates](quality-gates.md): critérios, exceções e atribuição dos resultados.
- [Correções da interface](checkpoint-correcao-ui-head.md): ajustes derivados do feedback de Felipe.

Os demais checkpoints preservam o estado de cada etapa; pendências históricas
não devem ser confundidas com o estado atual acima.

Destino dos testes e verificações reais, incluindo falhas e limites. [Checkpoint Bronze/Silver](checkpoint-bronze-silver.md): reprodução inicial concluída em banco isolado. Isso não valida Gold, interface ou estratégia final.

## Pipeline completo e revisão

- [Execução pelo agente de dados](checkpoint-pipeline-final.md): reprodução histórica, com regras posteriormente corrigidas na interpretação.
- [Revisão do dicionário oficial](checkpoint-revisao-dicionario-oficial.md): prevalece sobre as conclusões antigas.
- [Integração do SQLite](checkpoint-integracao-evidencia.md): hashes e integridade conferidos por Lia.
- [Integração de scripts/documentos](checkpoint-integracao-pipeline.md): verificações desta publicação e pendências do produto.
