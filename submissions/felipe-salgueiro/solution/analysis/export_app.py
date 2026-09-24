"""Export a versioned UI contract from the audited report, without recomputing metrics."""

import argparse
import hashlib
import json
import math
import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE_HASH = "7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad"
EVIDENCE_HASH = "de0502d33bec4b09fe6970686196f4c83c1fe484b659c40fc607b75d6d1ddf1d"
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
FORBIDDEN_FIELDS = {"creator_profile_eligible", "action_candidate", "measure_better"}
COVERAGE_FIELDS = {"question", "status", "status_label", "basis", "limit"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_tree(value):
    """Reject legacy policy fields and values JSON consumers cannot represent."""
    if isinstance(value, dict):
        require(not FORBIDDEN_FIELDS.intersection(value), "Historical policy field rejected")
        for child in value.values():
            validate_tree(child)
    elif isinstance(value, list):
        for child in value:
            validate_tree(child)
    elif isinstance(value, float):
        require(math.isfinite(value), "Non-finite metric rejected")


def validate_summary(summary):
    require(isinstance(summary, dict), "Invalid metric summary")
    require(type(summary.get("n")) is int and summary["n"] > 0, "Invalid sample size")
    points = [summary.get(key) for key in ("minimum", "p25", "median", "p75", "maximum")]
    require(all(type(value) in (int, float) for value in points), "Missing numeric summary")
    require(points == sorted(points), "Invalid quantile order")
    spread = summary.get("iqr")
    require(type(spread) in (int, float), "Missing IQR")
    require(math.isclose(spread, points[3] - points[1], abs_tol=1e-10), "Invalid IQR")


def validate_profiles(data):
    profiles = data["performance"].get("profiles", {})
    require(isinstance(profiles, dict), "Invalid profiles")
    for dimension in ("platform", "content_type", "content_category", "follower_band"):
        groups = profiles.get(dimension)
        require(isinstance(groups, list) and bool(groups), f"Missing dimension: {dimension}")
        require(all(isinstance(group, dict) for group in groups), "Invalid segment object")
        labels = [group.get("label") for group in groups]
        require(all(isinstance(label, str) and label for label in labels), "Invalid labels")
        require(len(set(labels)) == len(labels), "Duplicate segment label")
        for group in groups:
            validate_summary(group.get("interaction_per_view_pct"))
        require(sum(group["interaction_per_view_pct"]["n"] for group in groups) == 52214,
                "Segment coverage does not reconcile")


def validate_coverage(coverage_items):
    for index, coverage in enumerate(coverage_items, start=1):
        require(isinstance(coverage, dict) and set(coverage) == COVERAGE_FIELDS,
                "Invalid coverage fields")
        require(all(isinstance(value, str) and value for value in coverage.values()),
                "Empty coverage text")
        require(coverage["question"].startswith(f"{index}. "), "Coverage order changed")


def validate_source(data):
    require(isinstance(data, dict), "Evidence must be an object")
    validate_tree(data)
    for key in (*SECTIONS, "source", "metric", "availability"):
        require(isinstance(data.get(key), dict), f"Missing object: {key}")
    require(isinstance(data.get("coverage"), list), "Missing coverage")
    require(isinstance(data.get("interpretation_guards"), list), "Missing limits")
    if data.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported evidence schema")
    metric = data.get("metric", {})
    if metric.get("unit") != "percent" or metric.get("difference_unit") != "percentage_points":
        raise ValueError("Incompatible metric units")
    if data["overall"].get("rows") != 52214 or len(data["coverage"]) != 8:
        raise ValueError("Unexpected evidence coverage")
    if data["source"].get("database_sha256") != DATABASE_HASH:
        raise ValueError("Unexpected source database")
    validate_coverage(data["coverage"])
    for key in ("views", "total_interactions", "interaction_per_view_pct"):
        validate_summary(data["overall"].get(key))
    validate_profiles(data)


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
    payload = {
        "schema_version": 1,
        "source": data["source"], "metric": data["metric"],
        "evidence": evidence, "recommendations": recommendations,
        "availability": data["availability"], "limits": data["interpretation_guards"],
        "commercial": {"revenue": None, "cost_per_sale": None, "cac": None,
                       "reason": "Costs, attributed sales and customers absent from source"},
    }
    content = json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False)
    payload["snapshot_id"] = "g4-" + hashlib.sha256(content.encode()).hexdigest()[:24]
    return payload


def export(source, database, output):
    protected = {source.resolve(), database.resolve(), source.parent.resolve() / "manifest.json"}
    for filename in ("dashboard.json", "manifest.json"):
        target = output / filename
        require(not target.is_symlink() and target.resolve() not in protected,
                "Output conflicts with protected evidence")
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
