# Conversas do projeto — índice multiagente

Export sanitizado de **15 sessões identificadas como vinculadas ao Challenge**:
1.013 mensagens visíveis no total. Não é apenas a conversa principal, nem um
dump de toda a máquina. Identificação por metadados de sessão, relação de
subagente, worktree e tarefa inicial. Processos internos de segurança/guardian
e sessões de outros projetos não entram no pacote.

Para uma leitura rápida, comece pelo [workflow](../workflow.md).
As conversas são evidência complementar, não leitura obrigatória sequencial.
Veja a [legenda das personas e do PD Framework](../README.md#quem-são-as-personas-mencionadas).

| Sessão / frente | Mensagens | Export |
|---|---:|---|
| Lia — coordenação principal | 534 | [Conversa principal](conversa-sanitizada.md) |
| Pesquisa das PRs públicas | 18 | [Pesquisa](pesquisa-prs.md) |
| Maria — escolha dos cases | 7 | [Parecer Marketing](maria-cases.md) |
| Vitor — escolha dos cases | 14 | [Parecer técnico](vitor-cases.md) |
| Agente de capturas, posteriormente retirado | 9 | [Capturas](capturas.md) |
| g4-dados — auditoria e relatórios | 264 | [Dados](dados.md) |
| Catarina — contexto Cadência | 14 | [Produto](catarina.md) |
| Agente de logs, posteriormente retirado | 9 | [Registro](registro-logs.md) |
| Paloma — PRD | 3 | [Requisitos](paloma-prd.md) |
| Vitor — arquitetura e gate técnico | 8 | [Arquitetura](vitor-arquitetura.md) |
| Sofia — UX | 26 | [Usabilidade](sofia-ux.md) |
| g4-ui — implementação da interface | 56 | [Interface](ui.md) |
| Maria — revisão do relatório, sessão derivada | 15 | [Relatório](maria-relatorio.md) |
| Maria — revisão do dashboard | 3 | [Dashboard](maria-dashboard.md) |
| Camila — QA e retestes Brave | 33 | [QA](camila-qa.md) |

## O que o export contém e omite

- Pedidos visíveis, instruções de coordenação, handoffs colados e respostas públicas dos assistentes, em ordem dentro de cada sessão.
- O canal de entrada pode conter mensagem de Felipe **ou de outro agente**; o export não atribui automaticamente todos os prompts a Felipe.
- Sessões derivadas podem conter contexto herdado; mensagens repetidas não são prova de execuções independentes adicionais.
- Instruções de sistema/desenvolvedor, raciocínio interno, ferramentas, imagens binárias e notificações automáticas não são exportados.
- Caminhos privados, e-mails, identificadores internos e padrões de credenciais são substituídos por marcadores. Espaços no fim das linhas normalizados. Redação restante preservada, sem reescrever erros ou promessas antigas como resultados.
- Cada arquivo informa início/fim UTC e hash do snapshot privado de origem. A fonte bruta não é publicada.
- São snapshots até o momento da extração; não incluem automaticamente novas mensagens, outras instalações ou sessões não localizadas. Rafael não ganhou um export fictício: sua perspectiva final foi simulada na conversa principal.

Extração por [script reproduzível](export_chat.py). Execução requer o JSONL privado
correspondente, que não é necessário para avaliar ou executar a solução.
A sanitização automatizada não é garantia universal de ausência de informações
sensíveis. Este pacote exclui deliberadamente conteúdos internos não necessários
para demonstrar o trabalho solicitado.
