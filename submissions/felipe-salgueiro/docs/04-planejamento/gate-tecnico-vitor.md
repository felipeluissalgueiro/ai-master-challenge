# Gate técnico — Vitor — 23/09/2026

PRD v0.5 consolidado. Parecer do subagente Vitor: **viável com ajustes identificados**. Arquitetura proposta, ainda dependente de RFC; não é aprovação de execução ou deploy. Epics abaixo são agrupamentos propostos, ainda sem issues.

## Três Epics verticais

1. **Evidência e comparações:** snapshot imutável → exportação Ouro versionada → panorama, filtros e rankings por creator_id. Aceite: valores reconciliados, proveniência, n, dispersão e limites; camada nova não usa elegibilidade superada nem measure_better fixo como motor.
2. **Decisão e simulador:** recomendações rastreáveis e custos hipotéticos por mil views, interação e venda. Depende do contrato de evidências do primeiro bloco. Aceite: justificativas ligadas aos números; cenários separados das observações; custo/venda distinto de CAC; zeros/vazios tratados. Benchmark apenas com fonte comparável, sem bloquear o núcleo.
3. **Chat protegido e validação:** contexto da recomendação montado no servidor, OpenRouter explicativo, referências e tratamento de indisponibilidade. Depende das recomendações e dos controles de acesso/custo. Aceite: sem chave no cliente, sem endpoint de inferência aberto, limites aplicados e jornadas verificadas.

## Arquitetura proposta

Python/SQLite offline → JSON estático → Next.js/TypeScript na Vercel, com uma rota servidor para OpenRouter. Sem banco no runtime, VPS, login próprio ou migração Cadência. HTML exploratório pode fornecer elementos visuais sem bloquear o trabalho.

## Caminho crítico e pendências

RFC/contrato Ouro → exports corrigidos → UI e simulador → chat → validação. Entitlement da proteção Vercel, acesso dos avaliadores e configuração da chave/modelo podem ser verificados em paralelo. Nada disso está declarado executado por este parecer.

Prazo de hoje é prioridade, não garantia. Não retirar requisitos ou expor credenciais para cumpri-lo. Deploy e submissão exigem autorização própria. Projeto permanece P-MAR-55 no time Marketing por decisão de Felipe.
