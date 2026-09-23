# Catálogo de métricas

| Métrica | Fórmula | Estado | Interpretação permitida |
|---|---|---|---|
| `total_interactions` | `likes + shares + comments_count` | Implementada | Volume das três interações disponíveis |
| `interaction_per_view_pct` | `100 × total_interactions / views` | Implementada | Relação entre interações e views; não é alcance ou retenção |
| `interaction_per_follower_pct` | `100 × total_interactions / follower_count` | Implementada | Relação com a base declarada; não é “engajamento real” |
| `views_per_follower` | `views / follower_count` | Implementada | Sinal de amplificação; não mede pessoas únicas |
| Engajamento por alcance | `interações / alcance` | Ausente | Exige alcance real |
| Engajamento por impressões | `interações / impressões` | Ausente | Exige impressões reais |
| Retenção em 3 segundos | espectadores após 3 s / inícios | Ausente | Não substituir por views |
| Retenção final | conclusões / inícios | Ausente | Exige eventos ou curva de retenção |
| Ponto de 50% | instante em que resta 50% da audiência | Ausente | Exige curva temporal de retenção |
| ROI | `(receita atribuída - gasto) / gasto` | Ausente | Exige gasto, receita e regra de atribuição |

Divisões por zero produzem valor nulo e flag explícita. Nesta versão, os cinco
campos numéricos não apresentam zero. Nenhuma métrica autoriza inferência
causal.
