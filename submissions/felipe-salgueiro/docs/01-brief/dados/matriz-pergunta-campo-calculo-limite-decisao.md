<!-- Snapshot de artefato do agente de dados em 23/09/2026. Estado e limites preservados. -->

# Matriz pergunta → campo → cálculo → limite → decisão

Estado: contrato analítico anterior à camada Silver. Nenhuma linha autoriza causalidade.

| Pergunta | Campo(s) disponível(is) | Cálculo determinístico proposto | Estado | Limite obrigatório | Decisão suportada |
|---|---|---|---|---|---|
| Quantas interações o post recebeu? | `likes`, `shares`, `comments_count` | `total_interactions = likes + shares + comments_count` | Derivável após validação numérica | Não inclui salvamentos, cliques ou reações não listadas | Comparar volume dentro de recortes equivalentes |
| Qual o engajamento por alcance ou impressões? | Nenhum campo de alcance ou impressões | Não calcular | Ausente | `views` não substitui alcance nem impressões | Pedir nova fonte/instrumentação |
| Qual a relação entre interações e views? | Interações + `views` | `interaction_per_view_pct = 100 * total_interactions / views` | Derivável após tratar denominador zero | Views podem repetir pessoas e não medem exposição única | Sinal descritivo inicial; não chamar de alcance nem de retenção |
| Qual a relação entre interações e seguidores? | Interações + `follower_count` | `interaction_per_follower_pct = 100 * total_interactions / follower_count` | Derivável após tratar denominador zero | Seguidores não são espectadores reais do post | Comparar eficiência relativa; não chamar de “engajamento real” |
| O post ultrapassou a base de seguidores? | `views`, `follower_count` | `views_per_follower = views / follower_count` | Derivável após tratar denominador zero | Não identifica usuários únicos nem distribuição paga | Sinal de amplificação, não alcance |
| Patrocinado performa diferente? | `is_sponsored` + métricas | Comparação descritiva estratificada por plataforma, faixa de creator e categoria, sempre com `n` | Derivável com ressalvas | `false` significa “não patrocinado segundo a flag”, não prova orgânico; sem causalidade | Priorizar teste ou medir melhor, nunca atribuir efeito causal |
| Qual plataforma ou categoria funciona melhor? | `platform`, `content_category`, métricas | Estatísticas robustas por estrato com mediana, dispersão e `n` | Derivável com ressalvas | Dataset é simulado; exposição e população podem diferir | Gerar hipótese de teste, não benchmark real |
| Qual frequência de postagem é ideal? | `creator_id`, `platform`, `post_date` | Contagem de posts por creator/plataforma em janelas, somente após validar datas | Parcial | Data do post não garante mesma janela de exposição; sem histórico real | Descrever cadência simulada; não recomendar frequência ótima |
| Qual foi o ROI? | Nenhum gasto, receita, conversão ou lead | Não calcular | Ausente | Patrocínio não informa investimento nem retorno | Pedir gasto, receita e regra de atribuição |
| O gancho segurou mais de 3 segundos? | Nenhum evento de 3 s | Não calcular | Ausente | Views não substituem visualizações de 3 s | Instrumentar vídeo por marco temporal |
| Qual foi a retenção final ou o ponto de 50% da audiência? | Nenhuma curva/evento de retenção | Não calcular | Ausente | `content_length` é duração/tamanho declarado, não tempo assistido | Pedir curva de retenção, conclusão e watch time |
| Quais são gancho, contexto, explicação e CTA? | `content_description`, `comments_text`, `hashtags` | Não classificar automaticamente neste dataset | Não respondível com validade | Não há mídia/transcrição/roteiro; textos auditados são sintéticos e incoerentes com idiomas declarados | Em fonte real, usar texto/transcrição e validação humana |
| Quais dúvidas, objeções e ideias aparecem nos comentários? | `comments_text`, `comments_count`, `content_id` | Possível taxonomia semântica em fonte real | Campo existe, conteúdo inválido para este fim | Texto é amostra sintética sem comentário individual, autor, thread ou separador confiável | Tratar caso Supabase como hipótese externa; pedir export real de comentários |
| A audiência demográfica explica diferenças? | distribuições de idade, gênero e local | Somente após parse, soma e consistência por creator/post | Pendente de auditoria Silver | Pode haver distribuições sintéticas ou inconsistentes; associação não é causal | Descrever segmentos apenas se o contrato passar |

## Regra de promoção

- Bronze: cópia fiel do CSV e proveniência; nenhuma inferência.
- Silver: tipos, flags de qualidade, métricas derivadas nomeadas com precisão e dimensões padronizadas; nunca imputar silenciosamente.
- Gold: tabelas por pergunta e recorte comparável, contendo `n`, medida, dispersão, suficiência, limite e próxima ação (`ampliar`, `testar`, `reduzir` ou `medir melhor`).

JEV está indisponível por falta de novas contas e não integra esta arquitetura. Python realiza transformações e estatística; SQLite armazena Bronze, Silver e Gold reconstruíveis.
