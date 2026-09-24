"""Export visible dialogue only; never export reasoning, tools or system prompts."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sanitize(text):
    rules = [
        (r"sk-(?:or-v1-)?[A-Za-z0-9_-]{16,}", "[credencial omitida]"),
        (r"Bearer\s+[A-Za-z0-9._-]+", "[autorização omitida]"),
        (r"(?i)(?:password|senha|token|api_key)\s*[=:]\s*[^\s,;]+", "[atribuição sensível omitida]"),
        (r"(?:/home/|/tmp/|/run/)[^\s`\)\]\"<>]+", "[caminho local omitido]"),
        (r"[A-Za-z]:\\[^\s`\)\]\"<>]+", "[caminho local omitido]"),
        (r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[e-mail omitido]"),
        (r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", "[ID interno omitido]"),
    ]
    for pattern, replacement in rules:
        text = re.sub(pattern, replacement, text)
    return "\n".join(line.rstrip() for line in text.splitlines())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--all-visible", action="store_true", help="Use only for a session already verified as dedicated to this project")
    parser.add_argument("--label", default="Conversa principal")
    args = parser.parse_args()
    raw = args.source.read_bytes()
    messages = []
    started = args.all_visible
    omitted = 0
    for line in raw.splitlines():
        event = json.loads(line)
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or payload.get("type") != "message":
            continue
        role = payload.get("role")
        if role not in ("user", "assistant"):
            continue
        if role == "assistant" and payload.get("phase") not in ("commentary", "final_answer"):
            continue
        text = "\n".join(c.get("text", "") for c in payload.get("content", [])
                         if c.get("type") in ("input_text", "output_text"))
        if role == "user" and "fui selecionado para o processo seletivo dessa vaga" in text:
            started = True
        if not started or not text.strip():
            continue
        if any(marker in text for marker in ("# AGENTS.md instructions", "<environment_context>",
                                            "<subagent_notification>", "<turn_aborted>")):
            omitted += 1
            continue
        messages.append((event.get("timestamp", ""), role, sanitize(text)))
    if not messages:
        raise SystemExit("No task dialogue found; refusing empty export")
    out = [f"# Export sanitizado — {args.label} — Challenge 004\n",
           "Snapshot de mensagens visíveis da sessão identificada no índice. Inclui pedidos de Felipe, "
           "instruções de coordenação e handoffs no canal do usuário e respostas públicas da IA; não atribui "
           "todos os prompts a falas autorais de Felipe. Horários em UTC. Sessões derivadas podem conter contexto herdado; isso não é execução independente repetida.\n",
           "Foram excluídos bootstrap, instruções de sistema/desenvolvedor, ferramentas, "
           "raciocínio interno, imagens binárias e notificações automáticas. Caminhos locais, "
           "e-mails, IDs e padrões de credenciais foram substituídos. Não é transcript bruto "
           "integral. As outras sessões estão separadas no índice. Propostas e estados históricos "
           "não comprovam a execução; consulte workflow e checkpoints.\n",
           f"Mensagens: {len(messages)}. Início: {messages[0][0]}. Fim: {messages[-1][0]}.\n",
           f"SHA-256 do snapshot de origem privado: `{hashlib.sha256(raw).hexdigest()}`. "
           "O hash identifica o snapshot, não oferece acesso à origem nem prova suas alegações.\n",
           f"Blocos automáticos de usuário omitidos após início: {omitted}.\n"]
    for number, (timestamp, role, text) in enumerate(messages, 1):
        label = "Entrada — Felipe / coordenação / handoff" if role == "user" else "Assistente — resposta pública"
        longest = max((len(s) for s in re.findall(r"`+", text)), default=0)
        fence = "`" * max(3, longest + 1)
        out.append(f"## {number}. {label} · {timestamp}\n\n{fence}text\n{text}\n{fence}\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(out), encoding="utf-8")
    print(json.dumps({"messages": len(messages), "bytes": args.output.stat().st_size,
                      "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
