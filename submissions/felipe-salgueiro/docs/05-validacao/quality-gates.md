# Quality gates — política da entrega

Decisão de Felipe: workflow 110–111. Esta página descreve o processo;
não comprova que a aplicação passou nos gates.

| Verificação | Critério / evidência a registrar |
|---|---|
| Lint e tipos | Comando, escopo, versão/candidato, saída e exit code reais; falhas não são PASS |
| Dados | Export determinístico, reconciliação de métricas, schema e hash do SQLite preservado |
| Simulador | Fórmulas, unidades, valores vazios/negativos, divisão por zero e cenários conhecidos |
| Segurança | Chave somente no servidor; controle de acesso e uso; ausência de segredos no Git |
| Interface | Navegação, estados, teclado e viewport móvel testados na aplicação real |
| Build | Build reproduzível e instruções de execução conferidas |
| Revisão | Autorrevisão pelo modelo executor: diff, achados, correções e limitações; não é revisão independente |

## Aplicabilidade e limites

- Revisão por pares/multi-model dispensada por Felipe para esta entrega; testes não dispensados.
- Coolify, imagens Docker e VPS: **não aplicáveis**, pois o destino planejado é Vercel.
- Deploy, DNS e submissão final exigem autorização própria; testes locais não comprovam produção.
- Ferramenta ausente ou impedida de executar deve aparecer como erro/pendência, nunca verde.
- Falha preexistente deve ser demonstrada contra a base, não apenas chamada de preexistente.
- Agentes entregam evidência atribuída: testes reportados por outro agente são distintos de testes reexecutados pela coordenação.

## Estado neste checkpoint

A aplicação ainda não foi implementada. Na correção do runner interno para aceitar
MAR: 3 testes novos e 55 existentes passaram; Ruff do teste novo passou. O lint do
runner mantém os mesmos 16 apontamentos da base. O gate geral do framework **não
passou**; JSCPD não concluiu por restrição do cache npm. Esses resultados pertencem
à ferramenta interna, não são evidência de qualidade da aplicação do challenge.

Consulte o [workflow](../../process-log/workflow.md) para decisões e ocorrências;
os checkpoints futuros devem identificar exatamente o código e os testes executados.
