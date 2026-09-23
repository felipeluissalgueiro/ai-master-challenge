"""Export a versioned UI contract from the audited report, without recomputing metrics."""

import argparse
import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE_HASH = "7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad"
EVIDENCE_HASH = "e4a0b622450b1dbd089bac8e2c910772a817a028fb7fca2f819b56a7eeda6c4f"
SECTIONS = ("overall", "performance", "sponsorship", "audience", "creators", "temporal")
QUESTION_SECTIONS = (
    ("performance",), ("sponsorship",), ("audience",),
    ("performance", "sponsorship"), ("performance", "temporal"),
    ("sponsorship",), ("performance", "sponsorship"), ("overall", "temporal"),
)
ACTIONS = (
    "Testar hipóteses de conteúdo sem declarar vencedor causal.",
    "Medir custos e conversões antes de decidir sobre investimento.",
    "Validar aderência comercial e estabilidade dos recortes de audiência.",
    "Não recomendar cortes financeiros a partir de engajamento isolado.",
    "Desenhar teste confirmatório; não inferir frequência ótima nesta base.",
    "Definir economia e critérios do teste antes de escalar patrocínio.",
    "Suspender conclusões de desperdício sem custo e receita medidos.",
    "Instrumentar campanha, padronizar métricas e registrar hipóteses.",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_source(data):
    if data.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported evidence schema")
    metric = data.get("metric", {})
    if metric.get("unit") != "percent" or metric.get("difference_unit") != "percentage_points":
        raise ValueError("Incompatible metric units")
    if data["overall"]["rows"] != 52214 or len(data["coverage"]) != 8:
        raise ValueError("Unexpected evidence coverage")
    if data["source"]["database_sha256"] != DATABASE_HASH:
        raise ValueError("Unexpected source database")


def build_contract(data):
    validate_source(data)
    evidence = [{"id": f"ev-{key}", "source_pointer": f"/{key}", "data": data[key]}
                for key in SECTIONS]
    recommendations = []
    for index, (coverage, sections, action) in enumerate(
        zip(data["coverage"], QUESTION_SECTIONS, ACTIONS, strict=True), start=1
    ):
        recommendations.append({
            "id": f"rec-q{index}", "rule_id": f"descriptive-q{index}-v1",
            **coverage, "action": action, "action_kind": "proposed_not_validated",
            "evidence_ids": [f"ev-{section}" for section in sections],
        })
    return {
        "schema_version": 1, "snapshot_id": f"g4-{EVIDENCE_HASH[:16]}",
        "source": data["source"], "metric": data["metric"],
        "evidence": evidence, "recommendations": recommendations,
        "availability": data["availability"], "limits": data["interpretation_guards"],
        "commercial": {"revenue": None, "cost_per_sale": None, "cac": None,
                       "reason": "Costs, attributed sales and customers absent from source"},
    }


def export(source, database, output):
    if digest(source) != EVIDENCE_HASH or digest(database) != DATABASE_HASH:
        raise ValueError("Source hash mismatch; review checkpoint before exporting")
    with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
        connection.execute("PRAGMA query_only=ON")
        if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Invalid SQLite integrity")
        if connection.execute("SELECT count(*) FROM bronze_posts_raw").fetchone()[0] != 52214:
            raise ValueError("Unexpected SQLite row count")
    payload = build_contract(json.loads(source.read_text(encoding="utf-8")))
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if digest(database) != DATABASE_HASH:
        raise ValueError("Database changed during export")
    output.mkdir(parents=True, exist_ok=True)
    target = output / "dashboard.json"
    target.write_text(encoded, encoding="utf-8")
    manifest = {"schema_version": 1, "evidence_sha256": EVIDENCE_HASH,
                "database_sha256": DATABASE_HASH, "dashboard_sha256": digest(target),
                "generator_sha256": digest(Path(__file__)), "rows": 52214}
    (output / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )


def main():
    solution = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=solution / "reports/evidence.json")
    parser.add_argument("--database", type=Path, default=solution / "data/evidence/social_media_analysis.sqlite")
    parser.add_argument("--output", type=Path, default=solution / "data/app")
    args = parser.parse_args()
    export(args.source, args.database, args.output)
    print("Export validated: 52214 rows, 8 recommendations, read-only SQLite")


if __name__ == "__main__":
    main()
