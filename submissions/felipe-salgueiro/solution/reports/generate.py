#!/usr/bin/env python3
"""Generate the Challenge 004 executive report from read-only SQLite evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Iterable


REPORT_STATUS = "executive_report_for_head_of_marketing"
DATABASE_SHA256 = "7279027727b912c4c4ad8ec49704164f86e0eeb039218d8ee2b00d0ab78d7bad"
TABLES_READ = (
    "bronze_posts_raw",
    "silver_posts_metrics",
    "silver_posts_dimensions",
    "silver_posts_audience",
    "silver_posts_follower_bands",
    "silver_posts_dates",
    "silver_creator_profiles",
    "gold_sponsorship_comparisons",
    "gold_numeric_correlations",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quantile(values: Iterable[float], probability: float) -> float | None:
    ordered = sorted(float(value) for value in values)
    if not ordered:
        return None
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def describe(values: Iterable[float]) -> dict[str, float | int | None]:
    materialized = list(values)
    q1 = quantile(materialized, 0.25)
    median = quantile(materialized, 0.50)
    q3 = quantile(materialized, 0.75)
    return {
        "n": len(materialized),
        "minimum": min(materialized) if materialized else None,
        "p25": q1,
        "median": median,
        "p75": q3,
        "maximum": max(materialized) if materialized else None,
        "iqr": None if q1 is None or q3 is None else q3 - q1,
    }


def grouped_profiles(rows: list[sqlite3.Row], key: str) -> list[dict[str, object]]:
    buckets: defaultdict[str, list[sqlite3.Row]] = defaultdict(list)
    for row in rows:
        buckets[str(row[key])].append(row)
    profiles = []
    for label, bucket in sorted(buckets.items()):
        profiles.append(
            {
                "label": label,
                "interaction_per_view_pct": describe(
                    row["interaction_per_view_pct"] for row in bucket
                ),
                "views": describe(row["views"] for row in bucket),
                "total_interactions": describe(
                    row["total_interactions"] for row in bucket
                ),
                "interaction_per_follower_pct": describe(
                    row["interaction_per_follower_pct"] for row in bucket
                ),
            }
        )
    return profiles


def rank_context(profiles: list[dict[str, object]]) -> dict[str, object]:
    ordered = sorted(
        profiles,
        key=lambda item: float(item["interaction_per_view_pct"]["median"]),
        reverse=True,
    )
    highest = ordered[0]
    lowest = ordered[-1]
    return {
        "highest": highest,
        "lowest": lowest,
        "median_spread_percentage_points": (
            float(highest["interaction_per_view_pct"]["median"])
            - float(lowest["interaction_per_view_pct"]["median"])
        ),
    }


def audience_cross(
    rows: list[sqlite3.Row], context_key: str, audience_key: str
) -> dict[str, object]:
    buckets: defaultdict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        buckets[(str(row[context_key]), str(row[audience_key]))].append(
            float(row["interaction_per_view_pct"])
        )
    contexts: defaultdict[str, list[dict[str, object]]] = defaultdict(list)
    for (context, audience), values in sorted(buckets.items()):
        contexts[context].append(
            {
                "audience": audience,
                "interaction_per_view_pct": describe(values),
            }
        )
    details = []
    for context, cells in sorted(contexts.items()):
        ordered = sorted(
            cells,
            key=lambda item: float(item["interaction_per_view_pct"]["median"]),
            reverse=True,
        )
        details.append(
            {
                "context": context,
                "highest": ordered[0],
                "lowest": ordered[-1],
                "median_spread_percentage_points": (
                    float(ordered[0]["interaction_per_view_pct"]["median"])
                    - float(ordered[-1]["interaction_per_view_pct"]["median"])
                ),
                "minimum_cell_n": min(
                    int(cell["interaction_per_view_pct"]["n"]) for cell in cells
                ),
                "cells": cells,
            }
        )
    return {
        "context_dimension": context_key,
        "audience_dimension": audience_key,
        "contexts": details,
        "median_context_spread_percentage_points": quantile(
            [item["median_spread_percentage_points"] for item in details], 0.50
        ),
        "maximum_context_spread": max(
            details, key=lambda item: float(item["median_spread_percentage_points"])
        ),
    }


def sponsorship_evidence(
    connection: sqlite3.Connection, rows: list[sqlite3.Row]
) -> dict[str, object]:
    overall_buckets: defaultdict[str, list[sqlite3.Row]] = defaultdict(list)
    for row in rows:
        overall_buckets[str(row["sponsorship_label"])].append(row)
    overall = {
        label: {
            "views": describe(row["views"] for row in bucket),
            "total_interactions": describe(
                row["total_interactions"] for row in bucket
            ),
            "interaction_per_view_pct": describe(
                row["interaction_per_view_pct"] for row in bucket
            ),
        }
        for label, bucket in sorted(overall_buckets.items())
    }
    cells = [
        dict(row)
        for row in connection.execute(
            """
            SELECT
                platform,
                content_category,
                post_follower_band,
                sponsored_n,
                not_sponsored_n,
                sponsored_views_median,
                not_sponsored_views_median,
                views_median_difference,
                sponsored_total_interactions_median,
                not_sponsored_total_interactions_median,
                total_interactions_median_difference,
                sponsored_interaction_per_view_pct_median,
                not_sponsored_interaction_per_view_pct_median,
                interaction_per_view_pct_median_difference,
                sponsored_interaction_per_follower_pct_median,
                not_sponsored_interaction_per_follower_pct_median,
                interaction_per_follower_pct_median_difference,
                interpretation_limit
            FROM gold_sponsorship_comparisons
            ORDER BY platform, content_category, post_follower_band
            """
        )
    ]
    delta_key = "interaction_per_view_pct_median_difference"
    pairs: defaultdict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for cell in cells:
        pairs[(str(cell["platform"]), str(cell["content_category"]))].append(cell)
    patterns = []
    for (platform, category), pair_cells in sorted(pairs.items()):
        signs = [
            1 if float(cell[delta_key]) > 0 else -1 if float(cell[delta_key]) < 0 else 0
            for cell in pair_cells
        ]
        pattern = (
            "all_positive"
            if all(sign > 0 for sign in signs)
            else "all_negative"
            if all(sign < 0 for sign in signs)
            else "mixed"
        )
        patterns.append(
            {
                "platform": platform,
                "content_category": category,
                "pattern_across_follower_bands": pattern,
                "positive_bands": sum(sign > 0 for sign in signs),
                "negative_bands": sum(sign < 0 for sign in signs),
                "cells": pair_cells,
            }
        )
    selected_after_scan = next(
        pair
        for pair in patterns
        if pair["platform"] == "Instagram" and pair["content_category"] == "tech"
    )
    deltas = [float(cell[delta_key]) for cell in cells]
    return {
        "overall": overall,
        "matched_cell_summary": {
            "cells": len(cells),
            "platform_category_pairs_scanned": len(patterns),
            "positive_cells": sum(delta > 0 for delta in deltas),
            "negative_cells": sum(delta < 0 for delta in deltas),
            "median_delta_percentage_points": quantile(deltas, 0.50),
            "median_absolute_delta_percentage_points": quantile(
                [abs(delta) for delta in deltas], 0.50
            ),
            "minimum_delta_percentage_points": min(deltas),
            "maximum_delta_percentage_points": max(deltas),
            "pair_pattern_counts": {
                label: sum(
                    pair["pattern_across_follower_bands"] == label
                    for pair in patterns
                )
                for label in ("all_positive", "all_negative", "mixed")
            },
        },
        "post_hoc_example": {
            **selected_after_scan,
            "status": "exploratory_example_not_validated_priority",
            "selection_warning": (
                "Selecionado após inspecionar 15 pares plataforma-categoria e 60 "
                "células; exige confirmação independente e aderência comercial."
            ),
        },
        "all_cells": cells,
    }


def creator_evidence(connection: sqlite3.Connection) -> dict[str, object]:
    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS creator_count,
            MIN(posts) AS minimum_posts,
            MAX(posts) AS maximum_posts,
            SUM(CASE WHEN distinct_creator_names > 1 THEN 1 ELSE 0 END)
                AS creators_with_multiple_names
        FROM silver_creator_profiles
        """
    ).fetchone()
    return dict(summary)


def correlations(connection: sqlite3.Connection) -> list[dict[str, object]]:
    wanted = {
        ("is_sponsored", "views"),
        ("is_sponsored", "total_interactions"),
        ("is_sponsored", "interaction_per_view_pct"),
        ("follower_count", "interaction_per_follower_pct"),
        ("follower_count", "views_per_follower"),
        ("views", "total_interactions"),
    }
    rows = [dict(row) for row in connection.execute("SELECT * FROM gold_numeric_correlations")]
    return [
        row
        for row in rows
        if (str(row["variable_left"]), str(row["variable_right"])) in wanted
        or (str(row["variable_right"]), str(row["variable_left"])) in wanted
    ]


def build_evidence(database: Path) -> dict[str, object]:
    if sha256(database) != DATABASE_SHA256:
        raise RuntimeError("SQLite hash differs from the validated evidence snapshot")
    uri = f"file:{database.resolve()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    query_only = int(connection.execute("PRAGMA query_only").fetchone()[0])
    integrity = str(connection.execute("PRAGMA integrity_check").fetchone()[0])
    if query_only != 1 or integrity != "ok":
        raise RuntimeError("read-only or integrity guard failed")
    existing = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    missing = sorted(set(TABLES_READ) - existing)
    if missing:
        raise RuntimeError(f"missing required tables: {', '.join(missing)}")

    rows = list(
        connection.execute(
            """
            SELECT
                m.source_row_number,
                d.platform,
                d.content_type,
                d.content_category,
                d.sponsorship_label,
                f.band_label AS follower_band,
                a.audience_age_label,
                a.audience_gender_label,
                a.audience_location_label,
                m.views,
                m.total_interactions,
                m.interaction_per_view_pct,
                m.interaction_per_follower_pct
            FROM silver_posts_metrics AS m
            JOIN silver_posts_dimensions AS d USING (source_row_number)
            JOIN silver_posts_follower_bands AS f USING (source_row_number)
            JOIN silver_posts_audience AS a USING (source_row_number)
            WHERE m.metrics_valid = 1
              AND d.dimensions_valid = 1
              AND a.audience_valid = 1
            ORDER BY m.source_row_number
            """
        )
    )
    dimensions = (
        "platform",
        "content_type",
        "content_category",
        "follower_band",
        "audience_age_label",
        "audience_gender_label",
        "audience_location_label",
    )
    profiles = {dimension: grouped_profiles(rows, dimension) for dimension in dimensions}
    audience_crosses = {
        f"{context}__{audience}": audience_cross(rows, context, audience)
        for context in ("platform", "content_type", "content_category")
        for audience in (
            "audience_age_label",
            "audience_gender_label",
            "audience_location_label",
        )
    }
    temporal = dict(
        connection.execute(
            """
            SELECT
                COUNT(*) AS posts,
                COUNT(DISTINCT post_date_iso) AS covered_calendar_days,
                MIN(post_date_iso) AS first_date,
                MAX(post_date_iso) AS last_date,
                SUM(timezone_known) AS timezone_known_posts
            FROM silver_posts_dates
            WHERE date_valid = 1
            """
        ).fetchone()
    )
    evidence = {
        "schema_version": "1.0.0",
        "status": REPORT_STATUS,
        "source": {
            "dataset": "Social Media Sponsorship & Engagement Dataset",
            "publisher": "omenkj",
            "source_url": "https://www.kaggle.com/datasets/omenkj/social-media-sponsorship-and-engagement-dataset/data",
            "metadata_url": "https://www.kaggle.com/api/v1/datasets/view/omenkj/social-media-sponsorship-and-engagement-dataset",
            "nature": "simulated_dataset_as_declared_by_publisher",
            "license": "MIT",
            "database_relative_path": "../data/evidence/social_media_analysis.sqlite",
            "database_sha256": DATABASE_SHA256,
            "tables_read": list(TABLES_READ),
            "sqlite_uri_mode": "ro",
            "pragma_query_only": query_only,
            "integrity_check": integrity,
        },
        "metric": {
            "name": "interaction_per_view_pct",
            "plain_portuguese": "interações em relação às views",
            "formula": "100 × (likes + shares + comments_count) / views",
            "unit": "percent",
            "difference_unit": "percentage_points",
            "origin_tables": ["silver_posts_metrics", "bronze_posts_raw"],
            "interpretation": (
                "Conta interações e views, não pessoas únicas, alcance ou retenção."
            ),
        },
        "overall": {
            "rows": len(rows),
            "zero_view_posts": sum(float(row["views"]) == 0 for row in rows),
            "zero_interaction_posts": sum(
                float(row["total_interactions"]) == 0 for row in rows
            ),
            "views": describe(row["views"] for row in rows),
            "total_interactions": describe(
                row["total_interactions"] for row in rows
            ),
            "interaction_per_view_pct": describe(
                row["interaction_per_view_pct"] for row in rows
            ),
        },
        "performance": {
            "profiles": profiles,
            "rank_context": {
                dimension: rank_context(dimension_profiles)
                for dimension, dimension_profiles in profiles.items()
            },
        },
        "sponsorship": sponsorship_evidence(connection, rows),
        "audience": {"crosses": audience_crosses},
        "creators": creator_evidence(connection),
        "temporal": {
            **temporal,
            "generation_rule": "random_dates_declared_by_publisher",
            "interpretation": "Descreve cobertura da amostra; não identifica frequência editorial eficaz.",
        },
        "correlations": correlations(connection),
        "coverage": [
            {
                "question": "1. O que gera engajamento?",
                "status": "answered_descriptively",
                "status_label": "Respondida descritivamente",
                "basis": "Perfis por plataforma, formato, categoria e faixa de seguidores",
                "limit": "Sem vencedor causal ou sinal de qualidade criativa",
            },
            {
                "question": "2. Patrocínio funciona?",
                "status": "partially_answered",
                "status_label": "Respondida parcialmente",
                "basis": "Comparação da flag em 60 células descritivas comparáveis",
                "limit": "Sem alcance, custo, conversão ou tratamento causal",
            },
            {
                "question": "3. Qual audiência engaja?",
                "status": "answered_descriptively",
                "status_label": "Respondida descritivamente",
                "basis": "Rótulos predominantes de audiência cruzados por contexto",
                "limit": "Os rótulos não são distribuições percentuais da audiência",
            },
            {
                "question": "4. O que não funciona?",
                "status": "no_waste_proven",
                "status_label": "Sem desperdício comprovado",
                "basis": "Diferenças observadas pequenas e instáveis",
                "limit": "Custo e receita ausentes",
            },
            {
                "question": "5. Onde concentrar e com qual frequência?",
                "status": "partially_answered",
                "status_label": "Respondida parcialmente",
                "basis": "O ranking não sustenta realocação exclusiva",
                "limit": "Datas aleatórias não identificam frequência eficaz",
            },
            {
                "question": "6. Política e limiares de patrocínio?",
                "status": "proposed_policy_not_finding",
                "status_label": "Política proposta",
                "basis": "Governança de testar antes de escalar",
                "limit": "O limiar econômico depende da economia do negócio",
            },
            {
                "question": "7. O que parar?",
                "status": "no_operational_cut_supported",
                "status_label": "Sem corte operacional sustentado",
                "basis": "Nenhum canal ou formato tem desperdício comprovado",
                "limit": "As práticas operacionais do G4 não estão na base",
            },
            {
                "question": "8. Quick wins da semana?",
                "status": "proposed_actions",
                "status_label": "Ações propostas",
                "basis": "Contrato da métrica, ficha de campanha e desenho confirmatório",
                "limit": "As propostas não são achados validados",
            },
        ],
        "availability": {
            "absent_fields": [
                "alcance",
                "impressões",
                "gasto",
                "custo do creator",
                "conversões",
                "receita",
                "visualização de vídeo após 3 segundos",
                "tempo assistido",
                "curva de retenção",
                "conclusão do vídeo",
                "gancho, contexto, explicação e CTA anotados",
                "janela uniforme de exposição",
            ],
            "existing_with_limits": [
                "views são contagens, não alcance, pessoas únicas ou retenção",
                "is_sponsored falso não comprova distribuição orgânica",
                "os campos de audiência são rótulos predominantes",
                "as datas são aleatórias pelo desenho do dataset",
                "creator_id é válido; creator_name é inconsistente",
            ],
            "analyses_pending_not_absent": [
                "ranking por creator_id com validação de estabilidade",
                "padrões de hashtags, idioma e comprimento sem misturar unidades",
                "temas dos comentários sintéticos",
                "decomposição dos componentes de interação",
            ],
        },
        "interpretation_guards": [
            "Diferenças descritivas não são efeitos causais.",
            "Diferença menor que o IQR é contexto, não teste de equivalência ou limiar econômico.",
            "O exemplo Instagram-Tech é pós-hoc e exige validação independente.",
            "Nenhum portfólio, cadência ou prática operacional atual do G4 é presumido.",
            "Política e limiares de teste são propostas, não achados do dataset.",
        ],
    }
    connection.close()
    return evidence


def fmt_int(value: float | int) -> str:
    return f"{int(round(float(value))):,}".replace(",", ".")


def fmt_pct(value: float, digits: int = 2) -> str:
    return f"{float(value):.{digits}f}".replace(".", ",") + "%"


def fmt_pp(value: float, digits: int = 3, signed: bool = False) -> str:
    pattern = f"{{:{'+' if signed else ''}.{digits}f}}"
    return pattern.format(float(value)).replace(".", ",") + " pp"


def esc(value: object) -> str:
    return html.escape(str(value))


DIMENSION_LABELS = {
    "platform": "Plataforma",
    "content_type": "Formato",
    "content_category": "Categoria",
    "follower_band": "Seguidores declarados no post",
    "audience_age_label": "Idade predominante",
    "audience_gender_label": "Gênero predominante",
    "audience_location_label": "Localização principal",
}

VALUE_LABELS = {
    "post_followers_q1": "Q1 · 1.013–250.811",
    "post_followers_q2": "Q2 · 250.838–498.488",
    "post_followers_q3": "Q3 · 498.492–749.826",
    "post_followers_q4": "Q4 · 749.841–999.998",
    "not_sponsored_by_flag": "Não patrocinado segundo a flag",
    "sponsored_true": "Patrocinado",
    "content_type": "Formato",
    "content_category": "Categoria",
}


def value_label(value: object) -> str:
    return VALUE_LABELS.get(str(value), str(value).replace("_", " ").title())


def profile_table(dimension: str, profiles: list[dict[str, object]]) -> str:
    body = []
    for profile in profiles:
        metric = profile["interaction_per_view_pct"]
        body.append(
            "<tr>"
            f"<td>{esc(value_label(profile['label']))}</td>"
            f"<td>{fmt_int(metric['n'])}</td>"
            f"<td>{fmt_pct(metric['median'], 3)}</td>"
            f"<td>{fmt_pct(metric['p25'], 3)}–{fmt_pct(metric['p75'], 3)}</td>"
            f"<td>{fmt_int(profile['views']['median'])}</td>"
            "</tr>"
        )
    return (
        f"<h4>{esc(DIMENSION_LABELS[dimension])}</h4>"
        '<div class="table-wrap"><table><thead><tr>'
        "<th>Recorte</th><th>n</th><th>Mediana interações/views</th>"
        "<th>P25–P75</th><th>Views medianas</th>"
        "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


def segment_dot_plot(
    dimension: str,
    profiles: list[dict[str, object]],
    scale_min: float,
    scale_max: float,
) -> str:
    rows = []
    scale_width = scale_max - scale_min
    for profile in sorted(
        profiles,
        key=lambda item: float(item["interaction_per_view_pct"]["median"]),
        reverse=True,
    ):
        metric = profile["interaction_per_view_pct"]
        position = (
            50.0
            if scale_width == 0
            else max(
                0.0,
                min(100.0, (float(metric["median"]) - scale_min) / scale_width * 100),
            )
        )
        rows.append(
            "<div class='dot-row'>"
            f"<span class='dot-label'>{esc(value_label(profile['label']))}</span>"
            "<span class='dot-track' aria-hidden='true'>"
            f"<span class='dot-marker' style='left:{position:.3f}%'></span>"
            "</span>"
            f"<strong>{fmt_pct(metric['median'], 3)}</strong>"
            f"<small>n={fmt_int(metric['n'])}</small>"
            "</div>"
        )
    return (
        "<article class='chart-card'>"
        f"<div class='chart-title'><h3>{esc(DIMENSION_LABELS[dimension])}</h3>"
        f"<span>{fmt_pp(max(float(row['interaction_per_view_pct']['median']) for row in profiles) - min(float(row['interaction_per_view_pct']['median']) for row in profiles))} entre extremos</span></div>"
        + "".join(rows)
        + "</article>"
    )


def answer_card(
    number: int,
    decision_type: str,
    conclusion: str,
    evidence: str,
    implication: str,
    action: str,
    limit: str,
    proofs: tuple[tuple[str, str, str], ...],
    source_tables: str,
    calculation: str,
    evidence_id: str,
) -> str:
    proof_html = "".join(
        "<div class='proof-tile'>"
        f"<strong>{esc(value)}</strong>"
        f"<span>{esc(label)}</span>"
        f"<small>Fonte: {esc(source)}</small>"
        "</div>"
        for value, label, source in proofs
    )
    return f"""
      <article class="answer-card" id="q{number}">
        <div class="answer-number">{number:02d}</div>
        <div>
          <p class="eyebrow">{esc(decision_type)}</p>
          <h3>{esc(conclusion)}</h3>
          <div class="proof-grid" aria-label="Números que sustentam a conclusão">{proof_html}</div>
          <dl class="answer-flow">
            <div><dt>Evidência</dt><dd>{evidence}</dd></div>
            <div><dt>Decisão para o gestor</dt><dd>{implication}</dd></div>
            <div class="action"><dt>Próxima ação</dt><dd>{action}</dd></div>
            <div class="limit"><dt>Até onde o dado permite ir</dt><dd>{limit}</dd></div>
          </dl>
          <div class="source-strip"><strong>Como comprovamos</strong><span>Tabelas: <code>{esc(source_tables)}</code></span><span>Cálculo: {esc(calculation)}</span><a href="evidence.json">Abrir evidência JSON</a><code>{esc(evidence_id)}</code></div>
        </div>
      </article>
    """


def render_html(evidence: dict[str, object]) -> str:
    overall = evidence["overall"]
    performance = evidence["performance"]
    sponsor = evidence["sponsorship"]
    matched = sponsor["matched_cell_summary"]
    post_hoc = sponsor["post_hoc_example"]
    profiles = performance["profiles"]
    ranks = performance["rank_context"]
    non_sponsored = sponsor["overall"]["not_sponsored_by_flag"]
    sponsored = sponsor["overall"]["sponsored_true"]
    creators = evidence["creators"]
    temporal = evidence["temporal"]
    audience_crosses = evidence["audience"]["crosses"]

    def rho(left: str, right: str) -> float:
        for row in evidence["correlations"]:
            pair = {str(row["variable_left"]), str(row["variable_right"])}
            if pair == {left, right}:
                return float(row["spearman_rho"])
        raise KeyError(f"correlation not found: {left} x {right}")

    follower_ratio_rho = rho("follower_count", "interaction_per_follower_pct")
    location_rank = ranks["audience_location_label"]
    text_location = audience_crosses[
        "content_type__audience_location_label"
    ]["maximum_context_spread"]
    max_primary_spread = max(
        float(ranks[dimension]["median_spread_percentage_points"])
        for dimension in ("platform", "content_type", "content_category", "follower_band")
    )
    overall_rate = overall["interaction_per_view_pct"]
    visual_scale_min = float(overall_rate["p25"])
    visual_scale_max = float(overall_rate["p75"])
    segment_charts = "".join(
        segment_dot_plot(
            dimension,
            profiles[dimension],
            visual_scale_min,
            visual_scale_max,
        )
        for dimension in (
            "platform",
            "content_type",
            "content_category",
            "follower_band",
        )
    )
    positive_share = float(matched["positive_cells"]) / float(matched["cells"]) * 100
    negative_share = float(matched["negative_cells"]) / float(matched["cells"]) * 100
    audience_dashboard = "".join(
        "<article class='audience-card'>"
        f"<span>{esc(DIMENSION_LABELS[dimension])}</span>"
        f"<strong>{fmt_pp(ranks[dimension]['median_spread_percentage_points'])}</strong>"
        f"<small>{esc(value_label(ranks[dimension]['highest']['label']))} acima de "
        f"{esc(value_label(ranks[dimension]['lowest']['label']))} no agregado</small>"
        "</article>"
        for dimension in (
            "audience_age_label",
            "audience_gender_label",
            "audience_location_label",
        )
    )

    q1_evidence = (
        f"O post mediano registra {fmt_int(overall['views']['median'])} views e "
        f"{fmt_int(overall['total_interactions']['median'])} interações. A maior distância "
        f"entre formatos é {fmt_pp(ranks['content_type']['median_spread_percentage_points'])}; "
        f"entre plataformas, {fmt_pp(ranks['platform']['median_spread_percentage_points'])}."
    )
    q2_evidence = (
        f"Patrocinados e não patrocinados segundo a flag têm {fmt_int(sponsored['views']['median'])} "
        f"views e {fmt_int(sponsored['total_interactions']['median'])} interações medianas. "
        f"Nas {fmt_int(matched['cells'])} células comparáveis, há {fmt_int(matched['positive_cells'])} "
        f"diferenças positivas e {fmt_int(matched['negative_cells'])} negativas."
    )
    q3_evidence = (
        f"No agregado, {value_label(location_rank['highest']['label'])} aparece acima e "
        f"{value_label(location_rank['lowest']['label'])} abaixo por apenas "
        f"{fmt_pp(location_rank['median_spread_percentage_points'])}. Em conteúdo de texto, "
        f"{value_label(text_location['highest']['audience'])} aparece acima e "
        f"{value_label(text_location['lowest']['audience'])} abaixo: a posição muda com o contexto."
    )
    q4_evidence = (
        f"A amostra tem {fmt_int(overall['zero_view_posts'])} posts com zero views e "
        f"{fmt_int(overall['zero_interaction_posts'])} com zero interações; views variam apenas de "
        f"{fmt_int(overall['views']['minimum'])} a {fmt_int(overall['views']['maximum'])}. "
        "Sem cauda de falha, custo ou receita, não há base para provar desperdício."
    )
    q5_evidence = (
        f"O ranking separa formatos por somente {fmt_pp(ranks['content_type']['median_spread_percentage_points'])}. "
        f"A amostra cobre {fmt_int(temporal['covered_calendar_days'])} dias, mas o publicador declara "
        "que as datas foram geradas aleatoriamente; cobertura temporal não é frequência eficaz."
    )
    q6_evidence = (
        f"Em {fmt_int(matched['cells'])} células comparáveis, {fmt_int(matched['positive_cells'])} "
        f"favorecem patrocinado e {fmt_int(matched['negative_cells'])} não patrocinado segundo a flag. "
        "Gasto, margem, alcance, conversão e receita não estão no arquivo."
    )
    q7_evidence = (
        f"O maior intervalo entre medianas de plataforma é {fmt_pp(ranks['platform']['median_spread_percentage_points'])}; "
        f"a base tem {fmt_int(overall['zero_interaction_posts'])} posts com zero interações. "
        "Isso não identifica investimento de baixo retorno nem descreve as práticas atuais do G4."
    )
    q8_evidence = (
        f"A base já organiza {fmt_int(overall['rows'])} posts e {fmt_int(creators['creator_count'])} "
        "creator_ids. O ganho imediato é usar esse contrato para pré-registrar a próxima comparação "
        "e acrescentar custo, entrega e resultado de negócio."
    )

    cards = {
        1: answer_card(
            1,
            "Achado observado",
            "Nenhuma plataforma, formato, categoria ou faixa de seguidores se separa como vencedora.",
            q1_evidence,
            "O ranking não deve, sozinho, decidir orçamento ou volume de produção.",
            "Escolher a próxima hipótese por aderência comercial e compará-la dentro do mesmo contexto.",
            "Views e interações são eventos, não pessoas. A análise não testa equivalência nem qualidade criativa.",
            (
                (
                    f"{fmt_int(overall['views']['median'])} / {fmt_int(overall['total_interactions']['median'])}",
                    "views / interações no post mediano",
                    f"silver_posts_metrics · n={fmt_int(overall['rows'])}",
                ),
                (
                    fmt_pp(ranks["content_type"]["median_spread_percentage_points"]),
                    "distância entre formatos extremos",
                    "silver_posts_metrics + silver_posts_dimensions",
                ),
            ),
            "silver_posts_metrics; silver_posts_dimensions; silver_posts_follower_bands",
            "mediana por post; distância = maior mediana − menor mediana",
            "EV-PERF-01",
        ),
        2: answer_card(
            2,
            "Resposta parcial",
            "A vantagem econômica do patrocínio não está demonstrada nesta base.",
            q2_evidence,
            "Não existe respaldo para uma regra geral de ampliar ou cortar patrocínio.",
            "Testar somente uma hipótese com aderência comercial, controle comparável e resultado econômico definido antes da campanha.",
            (
                f"Instagram/Tech apareceu positivo após examinar {fmt_int(matched['platform_category_pairs_scanned'])} combinações e "
                f"{fmt_int(matched['cells'])} células. É uma seleção pós-hoc, não uma prioridade comprovada."
            ),
            (
                (
                    f"{fmt_int(sponsored['views']['median'])} = {fmt_int(non_sponsored['views']['median'])}",
                    "views medianas: patrocinado = não patrocinado segundo a flag",
                    "silver_posts_metrics + silver_posts_dimensions",
                ),
                (
                    f"{fmt_int(matched['positive_cells'])} × {fmt_int(matched['negative_cells'])}",
                    "células positivas × negativas",
                    "gold_sponsorship_comparisons",
                ),
            ),
            "gold_sponsorship_comparisons; silver_posts_metrics; silver_posts_dimensions",
            "delta = mediana patrocinado − mediana não patrocinado, dentro de plataforma × categoria × quartil",
            "EV-SPONS-01",
        ),
        3: answer_card(
            3,
            "Achado observado",
            "A base não revela um perfil de audiência que lidere de forma estável.",
            q3_evidence,
            "Audiência deve ser usada para formular hipóteses, não para excluir ou priorizar públicos automaticamente.",
            "Validar a segmentação em exposição real e observar resposta por contexto antes de personalizar investimento.",
            "Idade, gênero e localização são rótulos predominantes do post, não percentuais nem identidade de quem interagiu.",
            (
                (
                    fmt_pp(location_rank["median_spread_percentage_points"]),
                    "distância agregada entre localizações",
                    "silver_posts_audience + silver_posts_metrics",
                ),
                (
                    fmt_pp(text_location["median_spread_percentage_points"]),
                    "maior distância por localização em conteúdo de texto",
                    "cruzamento Prata: formato × localização",
                ),
            ),
            "silver_posts_audience; silver_posts_metrics; silver_posts_dimensions",
            "medianas por rótulo predominante; comparação repetida por plataforma, formato e categoria",
            "EV-AUD-01",
        ),
        4: answer_card(
            4,
            "Limite demonstrado",
            "Não foi possível provar desperdício de canal ou formato.",
            q4_evidence,
            "O relatório não classifica um recorte como fracasso sem observar retorno econômico e cauda de baixo desempenho.",
            "Não usar seguidores isolados, taxa por seguidores entre faixas diferentes ou centésimos de ponto como regra de corte.",
            f"A correlação entre seguidores e interações/seguidores é {follower_ratio_rho:.4f}; a razão é dominada pelo denominador.",
            (
                (
                    f"{fmt_int(overall['zero_view_posts'])} / {fmt_int(overall['zero_interaction_posts'])}",
                    "posts com zero views / zero interações",
                    "silver_posts_metrics",
                ),
                (
                    f"{fmt_int(overall['views']['minimum'])}–{fmt_int(overall['views']['maximum'])}",
                    "intervalo completo de views",
                    "silver_posts_metrics",
                ),
            ),
            "silver_posts_metrics; gold_numeric_correlations; bronze_columns",
            "contagem de zeros, mínimo/máximo e rho de Spearman",
            "EV-RISK-01",
        ),
        5: answer_card(
            5,
            "Decisão possível",
            "Concentre o próximo esforço em aprender uma hipótese comercial, não em perseguir o primeiro colocado do ranking.",
            q5_evidence,
            "A estratégia de conteúdo deve começar pelo objetivo e pela hipótese criativa, mantendo plataforma, categoria e exposição comparáveis no teste.",
            "Selecionar uma decisão real — canal, formato ou tema — e executar uma comparação prospectiva com janela comum.",
            "A base não informa a operação atual e as datas aleatórias não permitem recomendar frequência ou horário.",
            (
                (
                    fmt_pp(ranks["content_type"]["median_spread_percentage_points"]),
                    "distância entre formatos extremos",
                    "silver_posts_metrics + silver_posts_dimensions",
                ),
                (
                    fmt_int(temporal["covered_calendar_days"]),
                    "dias cobertos por datas aleatórias",
                    "silver_posts_dates + dicionário oficial Kaggle",
                ),
            ),
            "silver_posts_metrics; silver_posts_dimensions; silver_posts_dates",
            "ranking por mediana; cobertura temporal distinta de frequência eficaz",
            "EV-STRAT-01",
        ),
        6: answer_card(
            6,
            "Política proposta",
            "Patrocínio deve entrar como experimento com critério de escala definido antes do resultado.",
            q6_evidence,
            "Sem gasto e resultado de negócio, qualquer threshold de seguidores ou engagement seria arbitrário.",
            "Exigir objetivo, creator_id, grupo comparável, gasto, alcance/impressões e conversão/receita; escalar somente acima do limite econômico do negócio.",
            "A política é recomendação de governança, não um threshold descoberto na base.",
            (
                (
                    fmt_int(matched["cells"]),
                    "células comparáveis examinadas",
                    "gold_sponsorship_comparisons",
                ),
                (
                    "Ausentes",
                    "gasto, alcance, conversão e receita",
                    "bronze_columns + manifest de evidência",
                ),
            ),
            "gold_sponsorship_comparisons; bronze_columns; manifest.json",
            "política proposta a partir das lacunas; não é estimativa de ROI",
            "EV-POLICY-01",
        ),
        7: answer_card(
            7,
            "Decisão possível",
            "Não interrompa um canal, formato ou faixa de creator com base neste ranking.",
            q7_evidence,
            "A base não identifica investimento com baixo retorno; ela identifica critérios que não são suficientes para decidir um corte.",
            "Condicionar qualquer corte futuro a custo, resultado e comparação equivalente — não à posição isolada na tabela.",
            "Isso não afirma que o G4 pratica hoje uma decisão errada; é o limite seguro para usar este dataset.",
            (
                (
                    fmt_pp(ranks["platform"]["median_spread_percentage_points"]),
                    "distância entre plataformas extremas",
                    "silver_posts_metrics + silver_posts_dimensions",
                ),
                (
                    "Não calculável",
                    "ROI por canal ou formato",
                    "campos de custo e receita ausentes",
                ),
            ),
            "silver_posts_metrics; silver_posts_dimensions; bronze_columns",
            "comparação de medianas; retorno exige receita e gasto atribuídos",
            "EV-STOP-01",
        ),
        8: answer_card(
            8,
            "Plano de execução",
            "Nesta semana, prepare um teste que possa responder a decisão de investimento.",
            q8_evidence,
            "A empresa passa a acumular evidência operacional em vez de repetir rankings inconclusivos.",
            "Definir KPI e limite econômico; criar ficha de campanha; escolher hipótese comercial; pré-registrar comparação; usar creator_id como chave.",
            "São ações recomendadas. O dataset não valida antecipadamente qual hipótese criativa vencerá.",
            (
                (
                    fmt_int(overall["rows"]),
                    "posts já estruturados como referência",
                    "silver_posts_metrics",
                ),
                (
                    f"{fmt_int(creators['creator_count'])} IDs",
                    f"{fmt_int(creators['minimum_posts'])}–{fmt_int(creators['maximum_posts'])} posts por creator_id",
                    "silver_creator_profiles",
                ),
            ),
            "silver_posts_metrics; silver_creator_profiles; evidence.json",
            "contagens de base + proposta de desenho prospectivo",
            "EV-QUICK-01",
        ),
    }
    engagement_cards = "".join(cards[number] for number in (1, 3, 4))
    sponsorship_cards = "".join(cards[number] for number in (2, 6))
    strategy_cards = "".join(cards[number] for number in (5, 7, 8))

    coverage_rows = "".join(
        f"<tr><td>{esc(item['question'])}</td><td><span class='status'>{esc(item['status_label'])}</span></td>"
        f"<td>{esc(item['basis'])}</td><td>{esc(item['limit'])}</td></tr>"
        for item in evidence["coverage"]
    )
    absent_items = "".join(
        f"<li>{esc(item.replace('_', ' '))}</li>"
        for item in evidence["availability"]["absent_fields"]
    )
    pending_items = "".join(
        f"<li>{esc(item)}</li>"
        for item in evidence["availability"]["analyses_pending_not_absent"]
    )
    limited_items = "".join(
        f"<li>{esc(item)}</li>"
        for item in evidence["availability"]["existing_with_limits"]
    )
    dimension_tables = "".join(
        profile_table(dimension, profiles[dimension])
        for dimension in (
            "platform",
            "content_type",
            "content_category",
            "follower_band",
        )
    )
    audience_rows = []
    for cross in audience_crosses.values():
        maximum = cross["maximum_context_spread"]
        audience_rows.append(
            "<tr>"
            f"<td>{esc(DIMENSION_LABELS[cross['context_dimension']])}</td>"
            f"<td>{esc(DIMENSION_LABELS[cross['audience_dimension']])}</td>"
            f"<td>{esc(value_label(maximum['context']))}</td>"
            f"<td>{fmt_pp(maximum['median_spread_percentage_points'])}</td>"
            f"<td>{fmt_int(maximum['minimum_cell_n'])}</td>"
            "</tr>"
        )
    correlation_rows = "".join(
        "<tr>"
        f"<td>{esc(row['variable_left'])}</td><td>{esc(row['variable_right'])}</td>"
        f"<td>{float(row['spearman_rho']):.4f}</td><td>{fmt_int(row['n'])}</td>"
        "</tr>"
        for row in evidence["correlations"]
    )
    instagram_rows = "".join(
        "<tr>"
        f"<td>{esc(value_label(cell['post_follower_band']))}</td>"
        f"<td>{fmt_int(cell['sponsored_n'])}</td>"
        f"<td>{fmt_int(cell['not_sponsored_n'])}</td>"
        f"<td>{fmt_pp(cell['interaction_per_view_pct_median_difference'], signed=True)}</td>"
        "</tr>"
        for cell in post_hoc["cells"]
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Relatório executivo de performance e estratégia social media do Challenge 004.">
  <title>Análise de performance e estratégia · Challenge 004</title>
  <style>
    :root {{
      --g4-navy-950: #111827; --g4-navy-800: #1e293b; --g4-coral-500: #f2675c;
      --g4-coral-100: #fff0ee; --g4-surface: #ffffff; --g4-surface-muted: #f5f6f8;
      --g4-border: #d9dde5; --g4-ink: #111827; --g4-muted: #5d6676;
      --g4-blue-soft: #e8eef6; --radius: 14px; --shadow: 0 12px 32px rgba(17,24,39,.08);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; color: var(--g4-ink); background: var(--g4-surface-muted); font: 16px/1.58 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-variant-numeric: tabular-nums; }}
    a {{ color: inherit; }}
    .skip-link {{ position: fixed; left: 16px; top: -60px; z-index: 100; background: var(--g4-coral-500); color: var(--g4-navy-950); padding: 10px 14px; font-weight: 800; }}
    .skip-link:focus {{ top: 16px; }}
    .wrap {{ width: min(1180px, calc(100% - 40px)); margin: 0 auto; }}
    .topbar {{ background: var(--g4-navy-950); color: white; border-bottom: 1px solid #334155; }}
    .topbar .wrap {{ min-height: 66px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 850; letter-spacing: -.02em; }}
    .brand-mark {{ width: 28px; height: 28px; display: grid; place-items: center; background: var(--g4-coral-500); color: var(--g4-navy-950); font-size: .72rem; font-weight: 950; transform: rotate(-4deg); }}
    .topbar-meta {{ color: #cbd5e1; font-size: .8rem; }}
    .report-tabs {{ background: var(--g4-surface); border-bottom: 1px solid var(--g4-border); }}
    .report-tabs .wrap {{ display: flex; gap: 8px; overflow-x: auto; padding-top: 10px; padding-bottom: 10px; }}
    .report-tabs a {{ white-space: nowrap; text-decoration: none; border: 1px solid var(--g4-border); border-radius: 8px; padding: 9px 13px; color: var(--g4-muted); font-weight: 750; font-size: .86rem; }}
    .report-tabs a[aria-current="page"] {{ background: var(--g4-navy-950); border-color: var(--g4-navy-950); color: white; }}
    .hero {{ padding: 64px 0 48px; background: var(--g4-navy-950); color: white; border-bottom: 5px solid var(--g4-coral-500); }}
    .badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }}
    .badge {{ border: 1px solid #475569; border-radius: 999px; padding: 5px 10px; font-size: .72rem; font-weight: 800; letter-spacing: .055em; text-transform: uppercase; background: var(--g4-navy-800); color: #e2e8f0; }}
    .badge.coral {{ border-color: var(--g4-coral-500); background: var(--g4-coral-500); color: var(--g4-navy-950); }}
    h1 {{ font-size: clamp(2.35rem, 6vw, 4.7rem); line-height: 1.02; letter-spacing: -.055em; max-width: 970px; margin: 0 0 22px; font-weight: 880; }}
    .dek {{ max-width: 900px; font-size: clamp(1.08rem, 2vw, 1.35rem); color: #d8e0ea; margin: 0 0 32px; }}
    .hero-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
    .hero-note {{ background: var(--g4-navy-800); border: 1px solid #3c4a5e; border-radius: 10px; padding: 20px; color: #e2e8f0; }}
    .hero-note strong {{ display: block; color: white; margin-bottom: 7px; font-size: 1.02rem; }}
    .hero-note .number {{ display: block; color: var(--g4-coral-500); font-size: 1.65rem; font-weight: 900; margin-bottom: 4px; }}
    nav.section-nav {{ position: sticky; top: 0; z-index: 10; background: rgba(255,255,255,.96); backdrop-filter: blur(12px); border-bottom: 1px solid var(--g4-border); }}
    nav.section-nav .wrap {{ display: flex; gap: 20px; overflow-x: auto; padding-top: 13px; padding-bottom: 13px; white-space: nowrap; }}
    nav.section-nav a {{ text-decoration: none; font-weight: 750; font-size: .85rem; color: var(--g4-navy-800); }}
    main {{ padding: 48px 0 80px; }}
    .executive-call {{ display: grid; grid-template-columns: .8fr 1.2fr; gap: 28px; padding: 28px; background: var(--g4-surface); border: 1px solid var(--g4-border); border-left: 6px solid var(--g4-coral-500); border-radius: var(--radius); box-shadow: var(--shadow); margin-bottom: 56px; }}
    .executive-call h2 {{ margin: 0; }}
    .priority-list {{ counter-reset: priority; display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }}
    .priority-list li {{ counter-increment: priority; display: grid; grid-template-columns: 32px 1fr; gap: 10px; align-items: start; }}
    .priority-list li::before {{ content: counter(priority); width: 28px; height: 28px; display: grid; place-items: center; background: var(--g4-coral-500); color: var(--g4-navy-950); font-weight: 900; border-radius: 6px; }}
    .dashboard-section {{ margin: 0 0 68px; }}
    .dashboard-intro {{ display: grid; grid-template-columns: .9fr 1.1fr; gap: 24px; align-items: end; margin-bottom: 20px; }}
    .dashboard-intro p {{ margin: 0; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; margin-bottom: 16px; }}
    .kpi-card {{ min-height: 165px; padding: 20px; border-radius: 12px; color: white; background: var(--g4-navy-950); border-top: 5px solid var(--g4-coral-500); display: flex; flex-direction: column; }}
    .kpi-card strong {{ display: block; color: var(--g4-coral-500); font-size: clamp(1.65rem, 3vw, 2.4rem); line-height: 1; letter-spacing: -.04em; margin: 10px 0 8px; }}
    .kpi-card span {{ font-weight: 800; }}
    .kpi-card small {{ color: #cbd5e1; margin-top: auto; padding-top: 10px; }}
    .chart-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px; }}
    .chart-card {{ padding: 22px; background: var(--g4-surface); border: 1px solid var(--g4-border); border-radius: 12px; box-shadow: var(--shadow); }}
    .chart-title {{ display: flex; justify-content: space-between; gap: 12px; align-items: baseline; margin-bottom: 18px; }}
    .chart-title h3 {{ margin: 0; font-size: 1.1rem; }}
    .chart-title span {{ color: var(--g4-muted); font-size: .76rem; white-space: nowrap; }}
    .dot-row {{ display: grid; grid-template-columns: minmax(88px,1fr) minmax(110px,1.6fr) 64px 58px; gap: 10px; align-items: center; min-height: 36px; border-top: 1px solid #edf0f4; }}
    .dot-row:first-of-type {{ border-top: 0; }}
    .dot-label {{ font-size: .78rem; font-weight: 750; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .dot-track {{ position: relative; display: block; height: 4px; border-radius: 999px; background: #dfe4eb; }}
    .dot-track::before {{ content: ""; position: absolute; left: 50%; top: -4px; width: 1px; height: 12px; background: #9aa4b2; }}
    .dot-marker {{ position: absolute; top: 50%; width: 12px; height: 12px; border: 3px solid white; border-radius: 50%; background: var(--g4-coral-500); box-shadow: 0 0 0 1px var(--g4-navy-950); transform: translate(-50%,-50%); }}
    .dot-row strong {{ text-align: right; font-size: .8rem; }}
    .dot-row small {{ color: var(--g4-muted); text-align: right; }}
    .scale-caption {{ display: flex; justify-content: space-between; gap: 20px; margin: 10px 0 22px; padding: 11px 14px; border-left: 4px solid var(--g4-coral-500); background: var(--g4-coral-100); color: var(--g4-muted); font-size: .77rem; }}
    .sponsor-board {{ display: grid; grid-template-columns: 1.05fr .95fr; gap: 14px; margin-top: 16px; }}
    .visual-card {{ padding: 22px; background: var(--g4-surface); border: 1px solid var(--g4-border); border-radius: 12px; box-shadow: var(--shadow); }}
    .visual-card h3 {{ font-size: 1.15rem; margin-bottom: 7px; }}
    .sponsor-values {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 10px; margin: 16px 0; }}
    .sponsor-values div {{ padding: 14px; background: var(--g4-blue-soft); border-radius: 8px; }}
    .sponsor-values strong {{ display: block; font-size: 1.45rem; }}
    .sponsor-values span {{ color: var(--g4-muted); font-size: .75rem; }}
    .split-bar {{ display: flex; height: 34px; overflow: hidden; border-radius: 8px; margin: 18px 0 8px; color: white; font-size: .75rem; font-weight: 900; }}
    .split-positive, .split-negative {{ display: grid; place-items: center; }}
    .split-positive {{ background: var(--g4-navy-800); }}
    .split-negative {{ background: var(--g4-coral-500); color: var(--g4-navy-950); }}
    .split-legend {{ display: flex; justify-content: space-between; gap: 14px; color: var(--g4-muted); font-size: .74rem; }}
    .audience-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-top: 16px; }}
    .audience-card {{ padding: 16px; border: 1px solid var(--g4-border); border-radius: 9px; background: var(--g4-surface-muted); }}
    .audience-card span, .audience-card small {{ display: block; color: var(--g4-muted); }}
    .audience-card strong {{ display: block; font-size: 1.55rem; color: var(--g4-navy-950); margin: 5px 0; }}
    .strategy-plan {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin: 22px 0 18px; }}
    .strategy-step {{ position: relative; padding: 22px; border-radius: 12px; background: var(--g4-navy-950); color: white; border-top: 5px solid var(--g4-coral-500); }}
    .strategy-step > span {{ display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 6px; background: var(--g4-coral-500); color: var(--g4-navy-950); font-weight: 950; }}
    .strategy-step h3 {{ margin: 14px 0 8px; font-size: 1.18rem; }}
    .strategy-step p {{ margin: 0; color: #d8e0ea; font-size: .9rem; }}
    .strategy-step small {{ display: block; margin-top: 14px; color: #aebacc; }}
    .section-heading {{ margin: 0 0 24px; max-width: 780px; }}
    .eyebrow {{ margin: 0 0 7px; color: var(--g4-coral-500); font-size: .73rem; font-weight: 900; letter-spacing: .1em; text-transform: uppercase; }}
    h2 {{ font-size: clamp(1.9rem, 4vw, 3rem); line-height: 1.08; letter-spacing: -.04em; margin: 0 0 10px; font-weight: 860; }}
    h3 {{ font-size: clamp(1.25rem, 2.4vw, 1.75rem); line-height: 1.22; margin: 0 0 18px; letter-spacing: -.025em; }}
    h4 {{ margin: 28px 0 10px; }}
    .muted {{ color: var(--g4-muted); }}
    .pillar {{ margin-top: 64px; }}
    .pillar-head {{ display: grid; grid-template-columns: 170px 1fr; gap: 24px; align-items: start; margin-bottom: 22px; }}
    .pillar-index {{ color: var(--g4-coral-500); font-size: .8rem; font-weight: 900; text-transform: uppercase; letter-spacing: .1em; border-top: 3px solid var(--g4-coral-500); padding-top: 10px; }}
    .answers {{ display: grid; gap: 18px; }}
    .answer-card {{ display: grid; grid-template-columns: 52px 1fr; gap: 20px; padding: 28px; background: var(--g4-surface); border: 1px solid var(--g4-border); border-radius: var(--radius); box-shadow: var(--shadow); }}
    .answer-number {{ width: 44px; height: 44px; display: grid; place-items: center; border-radius: 8px; background: var(--g4-navy-950); color: white; font-weight: 900; }}
    .proof-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; margin: 18px 0; }}
    .proof-tile {{ display: flex; flex-direction: column; gap: 3px; background: var(--g4-blue-soft); border-left: 4px solid var(--g4-navy-800); border-radius: 6px; padding: 14px; }}
    .proof-tile strong {{ font-size: 1.35rem; color: var(--g4-navy-950); }}
    .proof-tile span {{ font-weight: 750; }}
    .proof-tile small {{ color: var(--g4-muted); }}
    .answer-flow {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 0; }}
    .answer-flow div {{ padding: 14px; border-radius: 8px; background: var(--g4-surface-muted); border: 1px solid var(--g4-border); }}
    .answer-flow .action {{ background: var(--g4-navy-950); color: white; border-color: var(--g4-navy-950); }}
    .answer-flow .action dt {{ color: var(--g4-coral-500); }}
    .answer-flow .limit {{ background: var(--g4-coral-100); border-color: #f4c5c0; }}
    dt {{ font-size: .7rem; font-weight: 900; letter-spacing: .07em; text-transform: uppercase; color: var(--g4-navy-800); margin-bottom: 5px; }}
    dd {{ margin: 0; }}
    .source-strip {{ display: flex; gap: 10px 16px; flex-wrap: wrap; align-items: center; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--g4-border); color: var(--g4-muted); font-size: .76rem; }}
    .source-strip strong {{ color: var(--g4-navy-950); }}
    .source-strip a {{ color: var(--g4-navy-800); font-weight: 800; }}
    .section-block {{ margin-top: 64px; }}
    .coverage {{ background: var(--g4-navy-950); color: white; padding: 34px; border-radius: var(--radius); }}
    .coverage h2, .coverage .eyebrow {{ color: white; }}
    .coverage .table-wrap {{ border-color: rgba(255,255,255,.22); }}
    .coverage table {{ background: transparent; color: white; }}
    .coverage th, .coverage td {{ border-color: rgba(255,255,255,.18); }}
    .status {{ display: inline-block; border: 1px solid rgba(255,255,255,.42); border-radius: 999px; padding: 3px 8px; font-size: .72rem; }}
    .availability {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
    .availability article {{ padding: 22px; border: 1px solid var(--g4-border); border-radius: var(--radius); background: var(--g4-surface); }}
    .availability ul {{ padding-left: 20px; margin-bottom: 0; }}
    details {{ margin-top: 14px; border: 1px solid var(--g4-border); border-radius: 10px; background: var(--g4-surface); overflow: hidden; }}
    summary {{ cursor: pointer; padding: 18px 20px; font-weight: 850; background: #e9edf3; }}
    summary:focus-visible, a:focus-visible {{ outline: 3px solid var(--g4-coral-500); outline-offset: 3px; }}
    .details-body {{ padding: 4px 20px 24px; }}
    .callout {{ margin: 18px 0; padding: 18px; border-left: 5px solid var(--g4-coral-500); background: var(--g4-coral-100); border-radius: 4px 10px 10px 4px; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--g4-border); border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--g4-surface); font-size: .86rem; }}
    th, td {{ padding: 11px 13px; text-align: left; border-bottom: 1px solid var(--g4-border); vertical-align: top; }}
    th {{ color: white; background: var(--g4-navy-800); font-size: .72rem; text-transform: uppercase; letter-spacing: .035em; }}
    tbody tr:last-child td {{ border-bottom: 0; }}
    code {{ font: .84em ui-monospace, SFMono-Regular, Menlo, monospace; background: #e8ebf0; padding: 2px 5px; border-radius: 4px; }}
    footer {{ background: var(--g4-navy-950); color: #cbd5e1; padding: 32px 0 46px; font-size: .84rem; }}
    footer strong {{ color: white; }}
    @media (max-width: 920px) {{ .kpi-grid {{ grid-template-columns: repeat(2,1fr); }} .chart-grid, .sponsor-board, .strategy-plan {{ grid-template-columns: 1fr; }} }}
    @media (max-width: 820px) {{ .hero-grid, .availability, .answer-flow, .proof-grid, .executive-call, .dashboard-intro {{ grid-template-columns: 1fr; }} .answer-card {{ grid-template-columns: 1fr; }} .pillar-head {{ grid-template-columns: 1fr; gap: 8px; }} .topbar-meta {{ display: none; }} }}
    @media (max-width: 640px) {{ .kpi-grid, .audience-grid {{ grid-template-columns: 1fr; }} .dot-row {{ grid-template-columns: minmax(80px,1fr) minmax(90px,1fr) 60px; }} .dot-row small {{ display: none; }} .scale-caption {{ display: block; }} .scale-caption span {{ display: block; }} }}
    @media (max-width: 560px) {{ .wrap {{ width: min(100% - 24px, 1180px); }} .topbar .wrap {{ min-height: 58px; }} .hero {{ padding-top: 44px; }} .answer-card {{ padding: 20px; }} }}
    @media print {{ .topbar, .report-tabs, nav.section-nav {{ display: none; }} body {{ background: white; }} .answer-card, details, .availability article, .executive-call {{ box-shadow: none; break-inside: avoid; }} details {{ break-inside: auto; }} details > * {{ display: block; }} .hero {{ padding-top: 28px; background: white; color: var(--g4-ink); border-top: 6px solid var(--g4-coral-500); }} .dek {{ color: var(--g4-muted); }} }}
  </style>
</head>
<body>
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <div class="topbar">
    <div class="wrap">
      <div class="brand"><span class="brand-mark" aria-hidden="true">G4</span><span>Challenge 004 · Social Media</span></div>
      <div class="topbar-meta">Relatório para decisão do Head de Marketing</div>
    </div>
  </div>
  <div class="report-tabs" aria-label="Relatórios disponíveis">
    <div class="wrap">
      <a href="performance-strategy.html" aria-current="page">Análise de performance e estratégia</a>
      <a href="../prototype/index.html">Explorar dados</a>
    </div>
  </div>
  <header class="hero">
    <div class="wrap">
      <div class="badges"><span class="badge coral">Decisão executiva</span><span class="badge">Dataset simulado</span><span class="badge">52.214 posts analisados</span></div>
      <h1>Não há um canal vencedor. Patrocínio precisa provar retorno antes de ganhar escala.</h1>
      <p class="dek">Plataformas, formatos, categorias e faixas de seguidores ficaram muito próximos em interações por view. A estratégia mais segura é não realocar investimento só pelo ranking e transformar a próxima campanha em um teste comparável, com custo e resultado de negócio registrados.</p>
      <div class="hero-grid">
        <div class="hero-note"><span class="number">{fmt_pp(max_primary_spread)}</span><strong>Maior distância nos recortes principais</strong>Plataforma, formato, categoria e faixa de seguidores não se separam o bastante para escolher um vencedor. <small>Fonte: tabelas Prata · mediana maior − menor</small></div>
        <div class="hero-note"><span class="number">{fmt_int(sponsored['views']['median'])} = {fmt_int(non_sponsored['views']['median'])}</span><strong>Views medianas por patrocínio</strong>Patrocinado e não patrocinado segundo a flag chegam ao mesmo valor mediano. <small>Fonte: silver_posts_metrics + dimensions</small></div>
        <div class="hero-note"><span class="number">Teste antes de escalar</span><strong>Estratégia recomendada</strong>Objetivo, comparação, gasto, entrega e conversão devem ser definidos antes da campanha. <small>Política proposta; não é achado causal</small></div>
      </div>
    </div>
  </header>
  <nav class="section-nav" aria-label="Navegação do relatório"><div class="wrap"><a href="#decisao">Decisão em 60 segundos</a><a href="#painel">Painel visual</a><a href="#engajamento">1. Engajamento</a><a href="#patrocinio">2. Patrocínio</a><a href="#estrategia">3. Estratégia</a><a href="#coverage">8 perguntas</a><a href="#appendix">Evidências</a></div></nav>
  <main id="conteudo" class="wrap">
    <section id="decisao" class="executive-call">
      <div><p class="eyebrow">Decisão em 60 segundos</p><h2>O que fazer com este diagnóstico</h2><p class="muted">Três decisões para reduzir risco sem transformar diferenças pequenas em certeza.</p></div>
      <ol class="priority-list">
        <li><div><strong>Não escolher canal ou formato só pela posição no ranking.</strong><br>As diferenças entre os grandes recortes são estreitas e não demonstram retorno econômico.</div></li>
        <li><div><strong>Não ampliar patrocínio sem teste comparável.</strong><br>Defina objetivo, controle, gasto, entrega e conversão antes de veicular.</div></li>
        <li><div><strong>Usar a próxima campanha para produzir a evidência que falta.</strong><br>Escolha uma hipótese com aderência comercial e um limite econômico acordado previamente.</div></li>
      </ol>
    </section>

    <section id="painel" class="dashboard-section" aria-labelledby="painel-title">
      <div class="dashboard-intro">
        <div><p class="eyebrow">Painel de decisão</p><h2 id="painel-title">Os sinais existem, mas estão comprimidos.</h2></div>
        <p class="muted">Os gráficos usam a mesma escala — o intervalo P25–P75 dos {fmt_int(overall_rate['n'])} posts — para não ampliar visualmente diferenças de centésimos. Cada ponto mostra a mediana do recorte e seu tamanho de amostra.</p>
      </div>
      <div class="kpi-grid" aria-label="Números centrais">
        <article class="kpi-card"><span>Post mediano</span><strong>{fmt_pct(overall_rate['median'], 2)}</strong><small>{fmt_int(overall['total_interactions']['median'])} interações para {fmt_int(overall['views']['median'])} views · n={fmt_int(overall_rate['n'])}</small></article>
        <article class="kpi-card"><span>Dispersão central</span><strong>{fmt_pct(overall_rate['p25'], 2)}–{fmt_pct(overall_rate['p75'], 2)}</strong><small>P25–P75 da métrica em todos os posts · amplitude {fmt_pp(float(overall_rate['p75']) - float(overall_rate['p25']))}</small></article>
        <article class="kpi-card"><span>Patrocínio comparável</span><strong>{fmt_pp(matched['median_delta_percentage_points'], signed=True)}</strong><small>Diferença mediana em {fmt_int(matched['cells'])} células controladas por plataforma × categoria × quartil</small></article>
        <article class="kpi-card"><span>Retorno financeiro</span><strong>Não calculável</strong><small>Gasto, custo do creator, conversão e receita não existem na fonte</small></article>
      </div>
      <div class="scale-caption"><span><strong>Escala comum:</strong> {fmt_pct(visual_scale_min, 3)} a {fmt_pct(visual_scale_max, 3)} — P25–P75 global.</span><span>A linha central é apenas referência visual; não é meta.</span></div>
      <div class="chart-grid" aria-label="Comparações de engajamento por recorte">{segment_charts}</div>
      <div class="sponsor-board">
        <article class="visual-card">
          <p class="eyebrow">Patrocinado versus flag não patrocinada</p><h3>As medianas quase coincidem.</h3>
          <div class="sponsor-values"><div><strong>{fmt_pct(sponsored['interaction_per_view_pct']['median'], 3)}</strong><span>patrocinado · n={fmt_int(sponsored['interaction_per_view_pct']['n'])}</span></div><div><strong>{fmt_pct(non_sponsored['interaction_per_view_pct']['median'], 3)}</strong><span>não patrocinado segundo a flag · n={fmt_int(non_sponsored['interaction_per_view_pct']['n'])}</span></div></div>
          <div class="split-bar" aria-label="33 células positivas e 27 negativas"><span class="split-positive" style="width:{positive_share:.3f}%">{fmt_int(matched['positive_cells'])}</span><span class="split-negative" style="width:{negative_share:.3f}%">{fmt_int(matched['negative_cells'])}</span></div>
          <div class="split-legend"><span>Patrocinado acima</span><span>Não patrocinado acima</span></div>
          <p class="muted">Fonte: <code>gold_sponsorship_comparisons</code>. É associação descritiva; não mede alcance, custo ou ROI.</p>
        </article>
        <article class="visual-card">
          <p class="eyebrow">Perfil predominante de audiência</p><h3>A liderança muda conforme o contexto.</h3>
          <div class="audience-grid">{audience_dashboard}</div>
          <p class="muted">Em conteúdo de texto, a distância máxima por localização é {fmt_pp(text_location['median_spread_percentage_points'])}; no agregado, outro rótulo lidera. Fonte: <code>silver_posts_audience</code> + métricas e dimensões.</p>
        </article>
      </div>
    </section>

    <section id="engajamento" class="pillar">
      <div class="pillar-head"><div class="pillar-index">Pilar 1</div><div><p class="eyebrow">O que gera engajamento de verdade</p><h2>O ranking descreve a base, mas não revela um vencedor confiável.</h2><p class="muted">A métrica utilizável é interações em relação às views. Ela compara eventos por post; não mede pessoas, alcance ou retenção.</p></div></div>
      <div class="answers">{engagement_cards}</div>
    </section>

    <section id="patrocinio" class="pillar">
      <div class="pillar-head"><div class="pillar-index">Pilar 2</div><div><p class="eyebrow">Vale a pena patrocinar influenciadores?</p><h2>A base não demonstra vantagem econômica; ela define como testar com menos risco.</h2><p class="muted">O desempenho observado é comparável dentro de plataforma, categoria e faixa de seguidores. ROI continua não calculável porque custo, alcance e conversão não existem no arquivo.</p></div></div>
      <div class="answers">{sponsorship_cards}</div>
    </section>

    <section id="estrategia" class="pillar">
      <div class="pillar-head"><div class="pillar-index">Pilar 3</div><div><p class="eyebrow">Qual deve ser a estratégia de conteúdo?</p><h2>Trocar a busca por um “campeão” por um sistema de testes com decisão econômica.</h2><p class="muted">A estratégia abaixo transforma os resultados em prioridade, política de patrocínio, regra de corte e quick wins para a próxima semana.</p></div></div>
      <div class="strategy-plan" aria-label="Estratégia recomendada em três etapas">
        <article class="strategy-step"><span>1</span><h3>Uma hipótese comercial</h3><p>Escolha um tema ligado ao objetivo do negócio e aplique a mesma proposta em variações comparáveis de canal ou formato.</p><small>Decisão apoiada pela proximidade descritiva dos rankings; não é um tema vencedor descoberto.</small></article>
        <article class="strategy-step"><span>2</span><h3>Conteúdo instrumentado</h3><p>Registre Gancho → Contexto → Explicação → CTA e capture retenção após 3s, ponto de 50%, conclusão e resposta ao CTA.</p><small>Método proposto. Esses campos não existem no dataset atual.</small></article>
        <article class="strategy-step"><span>3</span><h3>Escala condicionada</h3><p>Patrocine apenas como teste controlado; amplie somente quando entrega, custo e resultado de negócio superarem o limite definido antes.</p><small>Política recomendada; nenhum threshold econômico foi inferido da simulação.</small></article>
      </div>
      <div class="answers">{strategy_cards}</div>
    </section>
    <section id="coverage" class="section-block coverage">
      <p class="eyebrow">Controle de escopo</p><h2>As oito perguntas, sem esconder o que falta</h2>
      <div class="table-wrap"><table><thead><tr><th>Pergunta</th><th>Estado</th><th>Base usada</th><th>Limite</th></tr></thead><tbody>{coverage_rows}</tbody></table></div>
    </section>
    <section id="availability" class="section-block">
      <div class="section-heading"><p class="eyebrow">Cobertura dos dados</p><h2>Ausente não é a mesma coisa que pendente</h2></div>
      <div class="availability">
        <article><h3>Campos ausentes</h3><p>Não podem ser inferidos desta tabela.</p><ul>{absent_items}</ul></article>
        <article><h3>Existem, com limite</h3><p>Podem contextualizar, sem receber outro significado.</p><ul>{limited_items}</ul></article>
        <article><h3>Análises pendentes</h3><p>São possíveis com os campos existentes, mas ainda não viraram recomendação.</p><ul>{pending_items}</ul></article>
      </div>
    </section>
    <section id="appendix" class="section-block">
      <div class="section-heading"><p class="eyebrow">Apêndice recolhível</p><h2>Evidência técnica e rastreabilidade</h2><p class="muted">Detalhes para avaliadores e LLMs. O corpo principal permanece orientado à decisão.</p></div>
      <details><summary>Definição da métrica e exemplo humano</summary><div class="details-body"><p><strong>Interações totais</strong> = likes + shares + comentários. <strong>Interações em relação às views</strong> = 100 × interações totais / views.</p><div class="callout">Na mediana dos {fmt_int(overall['rows'])} posts, são {fmt_int(overall['total_interactions']['median'])} eventos de interação para {fmt_int(overall['views']['median'])} views, ou {fmt_pct(overall['interaction_per_view_pct']['median'], 2)}. Isso não significa pessoas únicas: uma pessoa pode produzir mais de um evento e views não são alcance.</div><p>Origem: <code>silver_posts_metrics</code>, derivada de <code>bronze_posts_raw</code>.</p></div></details>
      <details><summary>n, mediana e IQR por plataforma, formato, categoria e seguidores</summary><div class="details-body">{dimension_tables}<p class="muted">Os quartis são relativos à amostra e representam seguidores declarados na data do post; não são categorias de mercado nem tamanho estável do creator.</p></div></details>
      <details><summary>Patrocínio: comparação geral, células e seleção pós-hoc</summary><div class="details-body"><div class="table-wrap"><table><thead><tr><th>Grupo</th><th>n</th><th>Views medianas</th><th>Interações medianas</th><th>Interações/views</th></tr></thead><tbody><tr><td>Patrocinado</td><td>{fmt_int(sponsored['views']['n'])}</td><td>{fmt_int(sponsored['views']['median'])}</td><td>{fmt_int(sponsored['total_interactions']['median'])}</td><td>{fmt_pct(sponsored['interaction_per_view_pct']['median'], 3)}</td></tr><tr><td>Não patrocinado segundo a flag</td><td>{fmt_int(non_sponsored['views']['n'])}</td><td>{fmt_int(non_sponsored['views']['median'])}</td><td>{fmt_int(non_sponsored['total_interactions']['median'])}</td><td>{fmt_pct(non_sponsored['interaction_per_view_pct']['median'], 3)}</td></tr></tbody></table></div><p>Nas {fmt_int(matched['cells'])} células: diferença mediana {fmt_pp(matched['median_delta_percentage_points'], signed=True)}; mediana absoluta {fmt_pp(matched['median_absolute_delta_percentage_points'])}; extremos de {fmt_pp(matched['minimum_delta_percentage_points'], signed=True)} a {fmt_pp(matched['maximum_delta_percentage_points'], signed=True)}. Isso descreve a amostra; não testa causalidade, equivalência ou retorno.</p><h4>Instagram/Tech — exemplo exploratório encontrado após a varredura</h4><div class="table-wrap"><table><thead><tr><th>Faixa no post</th><th>n patrocinado</th><th>n não patrocinado</th><th>Diferença de mediana</th></tr></thead><tbody>{instagram_rows}</tbody></table></div><div class="callout">A combinação foi selecionada depois de inspecionar {fmt_int(matched['platform_category_pairs_scanned'])} pares e {fmt_int(matched['cells'])} células. Portanto, sofre risco de seleção pós-hoc e precisa de validação independente. Só é um exemplo de teste se também houver aderência comercial.</div></div></details>
      <details><summary>Audiência cruzada: maiores amplitudes observadas</summary><div class="details-body"><div class="table-wrap"><table><thead><tr><th>Contexto</th><th>Audiência</th><th>Recorte da maior amplitude</th><th>Amplitude</th><th>Menor n da célula</th></tr></thead><tbody>{''.join(audience_rows)}</tbody></table></div><p class="muted">Mostrar a maior amplitude de cada cruzamento é diagnóstico, não confirmação de um perfil vencedor. A posição dos rótulos muda entre contextos.</p></div></details>
      <details><summary>Correlações de controle</summary><div class="details-body"><div class="table-wrap"><table><thead><tr><th>Variável A</th><th>Variável B</th><th>rho de Spearman</th><th>n</th></tr></thead><tbody>{correlation_rows}</tbody></table></div><p class="muted">Correlação não demonstra causalidade. A relação quase perfeita entre seguidores e razões que usam seguidores no denominador é um alerta matemático.</p></div></details>
      <details><summary>Proveniência, arquivos e limites</summary><div class="details-body"><ul><li>Fonte: Social Media Sponsorship &amp; Engagement Dataset, omenKJ/Kaggle.</li><li>Natureza: dataset simulado declarado pelo publicador; licença MIT.</li><li>SQLite: <code>../data/evidence/social_media_analysis.sqlite</code>.</li><li>SHA-256: <code>{esc(evidence['source']['database_sha256'])}</code>.</li><li>Leitura: SQLite URI <code>mode=ro</code>, <code>PRAGMA query_only=ON</code>, <code>integrity_check=ok</code>.</li><li>Evidência estruturada: <a href="evidence.json">evidence.json</a>; linhagem: <a href="manifest.json">manifest.json</a>; instruções: <a href="README.md">README.md</a>.</li></ul></div></details>
    </section>
  </main>
  <footer><div class="wrap"><strong>Challenge 004 · análise de performance e estratégia.</strong><br>Relatório executivo estático, separado do visualizador de dados. Projeto desenvolvido para o Challenge 004; não é produto oficial e não implica afiliação com o G4 Educação. Dataset simulado · sem login, LLM, backend ou deploy.</div></footer>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database",
        type=Path,
        default=script_dir.parent / "data" / "evidence" / "social_media_analysis.sqlite",
    )
    parser.add_argument("--evidence", type=Path, default=script_dir / "evidence.json")
    parser.add_argument(
        "--output", type=Path, default=script_dir / "performance-strategy.html"
    )
    parser.add_argument("--manifest", type=Path, default=script_dir / "manifest.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    script_path = Path(__file__).resolve()
    evidence = build_evidence(args.database.resolve())
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence_text = json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    args.evidence.write_text(evidence_text, encoding="utf-8")
    report_text = render_html(evidence)
    args.output.write_text(report_text, encoding="utf-8")
    readme = script_path.parent / "README.md"
    manifest = {
        "schema_version": "1.0.0",
        "status": REPORT_STATUS,
        "artifact": "executive_performance_and_strategy_report",
        "lineage": {
            "database": {
                "relative_path": "../data/evidence/social_media_analysis.sqlite",
                "sha256": sha256(args.database.resolve()),
                "access": "sqlite_uri_mode_ro_and_pragma_query_only",
                "integrity_check": evidence["source"]["integrity_check"],
            },
            "tables_read": list(TABLES_READ),
            "generator": {"relative_path": "generate.py", "sha256": sha256(script_path)},
        },
        "outputs": {
            "evidence": {
                "relative_path": "evidence.json",
                "sha256": sha256(args.evidence),
                "rows_analyzed": evidence["overall"]["rows"],
            },
            "html": {
                "relative_path": "performance-strategy.html",
                "sha256": sha256(args.output),
                "self_contained": True,
                "external_assets": 0,
            },
            "readme": {
                "relative_path": "README.md",
                "sha256": sha256(readme) if readme.exists() else None,
            },
        },
        "separation_of_concerns": {
            "executive_report": "performance-strategy.html",
            "exploratory_viewer": "../prototype/index.html",
            "prototype_preserved": True,
        },
        "interpretation_guards": evidence["interpretation_guards"],
    }
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "database": str(args.database.resolve()),
                "rows": evidence["overall"]["rows"],
                "evidence": str(args.evidence.resolve()),
                "html": str(args.output.resolve()),
                "manifest": str(args.manifest.resolve()),
                "query_only": evidence["source"]["pragma_query_only"],
                "integrity_check": evidence["source"]["integrity_check"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
