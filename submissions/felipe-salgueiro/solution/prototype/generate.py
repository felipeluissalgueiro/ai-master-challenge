#!/usr/bin/env python3
"""Generate the self-contained exploratory Gold report from SQLite, read-only."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sqlite3
import statistics
from pathlib import Path
from urllib.parse import quote


REQUIRED_TABLES = {
    "gold_segment_summaries",
    "gold_sponsorship_comparisons",
    "gold_numeric_correlations",
}

DIMENSIONS = {
    "platform": "Plataforma",
    "content_type": "Formato",
    "content_category": "Categoria",
    "audience_age_label": "Idade predominante",
    "audience_gender_label": "Gênero predominante",
    "audience_location_label": "Localização principal",
}

SPONSOR_LABELS = {
    "not_sponsored_by_flag": "Não patrocinado segundo a flag",
    "sponsored_true": "Patrocinado",
}


def read_rows(connection: sqlite3.Connection, table: str) -> list[dict[str, object]]:
    cursor = connection.execute(f'SELECT * FROM "{table}"')
    columns = [item[0] for item in cursor.description]
    return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def br_number(value: float, digits: int = 4) -> str:
    rendered = f"{value:,.{digits}f}"
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def json_for_html(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def build_page(database: Path) -> str:
    font_base64 = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "fonts"
        / "manrope-latin-variable.woff2.b64"
    ).read_text(encoding="ascii").strip()
    database = database.resolve()
    uri = f"file:{quote(str(database), safe='/')}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        connection.execute("PRAGMA query_only = ON")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"SQLite integrity_check failed: {integrity}")
        available = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        missing = sorted(REQUIRED_TABLES - available)
        if missing:
            raise RuntimeError(f"Missing Gold tables: {', '.join(missing)}")
        segments = read_rows(connection, "gold_segment_summaries")
        comparisons = read_rows(connection, "gold_sponsorship_comparisons")
        correlations = read_rows(connection, "gold_numeric_correlations")

    visible_segments = [row for row in segments if row["slice_type"] in DIMENSIONS]
    public_comparison_fields = (
        "platform",
        "content_category",
        "post_follower_band",
        "sponsored_n",
        "not_sponsored_n",
        "sponsored_interaction_per_view_pct_median",
        "not_sponsored_interaction_per_view_pct_median",
        "interaction_per_view_pct_median_difference",
    )
    public_comparisons = [
        {field: row[field] for field in public_comparison_fields}
        for row in comparisons
    ]
    overall = {
        row["sponsorship_label"]: row
        for row in segments
        if row["slice_type"] == "overall"
    }
    sponsored = overall["sponsored_true"]
    not_sponsored = overall["not_sponsored_by_flag"]
    total_posts = int(sponsored["n"]) + int(not_sponsored["n"])
    overall_delta = (
        float(sponsored["interaction_per_view_pct_median"])
        - float(not_sponsored["interaction_per_view_pct_median"])
    )

    deltas = [float(row["interaction_per_view_pct_median_difference"]) for row in comparisons]
    median_delta = statistics.median(deltas)
    min_delta = min(deltas)
    max_delta = max(deltas)
    positive = sum(value > 0 for value in deltas)
    negative = sum(value < 0 for value in deltas)
    sample_side_sizes = [
        int(row[key])
        for row in comparisons
        for key in ("sponsored_n", "not_sponsored_n")
    ]

    format_rows = [row for row in segments if row["slice_type"] == "content_type"]
    format_leaders = {}
    for label, display in SPONSOR_LABELS.items():
        candidates = [row for row in format_rows if row["sponsorship_label"] == label]
        leader = max(candidates, key=lambda row: float(row["interaction_per_view_pct_median"]))
        trailer = min(candidates, key=lambda row: float(row["interaction_per_view_pct_median"]))
        format_leaders[label] = {
            "group": display,
            "leader": leader["slice_key"],
            "leader_value": leader["interaction_per_view_pct_median"],
            "trailer": trailer["slice_key"],
            "trailer_value": trailer["interaction_per_view_pct_median"],
            "spread": float(leader["interaction_per_view_pct_median"])
            - float(trailer["interaction_per_view_pct_median"]),
        }

    correlation_index = {
        (row["variable_left"], row["variable_right"]): row
        for row in correlations
    }

    def correlation(left: str, right: str) -> float:
        row = correlation_index.get((left, right)) or correlation_index.get((right, left))
        if row is None or row["spearman_rho"] is None:
            raise RuntimeError(f"Required Gold correlation missing: {left} × {right}")
        return float(row["spearman_rho"])

    sponsor_engagement_rho = correlation("is_sponsored", "interaction_per_view_pct")
    follower_ratio_rho = correlation("follower_count", "interaction_per_follower_pct")

    metadata = {
        "database_sha256": sha256(database),
        "database_name": database.name,
        "integrity_check": integrity,
        "gold_counts": {
            "segment_summaries": len(segments),
            "sponsorship_comparisons": len(comparisons),
            "numeric_correlations": len(correlations),
        },
        "dimensions": DIMENSIONS,
        "sponsor_labels": SPONSOR_LABELS,
        "overall": overall,
        "overall_delta": overall_delta,
        "total_posts": total_posts,
        "comparison_summary": {
            "median_delta": median_delta,
            "min_delta": min_delta,
            "max_delta": max_delta,
            "positive": positive,
            "negative": negative,
            "zero": len(deltas) - positive - negative,
            "min_side_n": min(sample_side_sizes),
            "max_side_n": max(sample_side_sizes),
        },
        "format_leaders": format_leaders,
    }

    template = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Explorador das tabelas Ouro da análise de engajamento e patrocínio do Challenge 004.">
  <title>Explorador de dados — Challenge 004</title>
  <style>
    @font-face {
      font-family: "Manrope";
      font-style: normal;
      font-weight: 200 800;
      font-display: swap;
      src: url("data:font/woff2;base64,__MANROPE_FONT__") format("woff2");
    }
    :root {
      color-scheme: light;
      --paper: #f5f4f3;
      --paper-strong: #ffffff;
      --ink: #031a26;
      --muted: #184560;
      --line: #e5e7eb;
      --line-dark: #184560;
      --gold: #b9915b;
      --gold-dark: #001f35;
      --gold-soft: #f5f4f3;
      --teal: #184560;
      --teal-soft: #f5f4f3;
      --navy: #001f35;
      --sand: #f5f4f3;
      --danger: #184560;
      --shadow: 0 12px 32px rgba(0, 31, 53, .10);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Manrope", Arial, sans-serif;
      font-variant-numeric: tabular-nums;
    }
    a { color: inherit; }
    button, select { font: inherit; }
    .skip-link { position: fixed; left: 12px; top: -50px; z-index: 50; background: var(--gold); color: var(--ink); padding: 10px 14px; font-weight: 850; }
    .skip-link:focus { top: 12px; }
    .shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; }
    .topline { border-bottom: 1px solid rgba(245,244,243,.22); background: var(--navy); color: white; position: sticky; top: 0; z-index: 20; }
    .topline .shell { min-height: 64px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; letter-spacing: -.02em; }
    .brand-mark { width: 28px; height: 28px; display: grid; place-items: center; background: var(--gold); color: var(--ink); font-size: 10px; font-weight: 950; transform: rotate(-4deg); }
    .brand-mark::after { content: "G4"; }
    .status { font-size: 12px; color: #f5f4f3; display: flex; gap: 8px; align-items: center; }
    .status::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--gold); }
    .report-tabs { background: var(--paper-strong); border-bottom: 1px solid var(--line); }
    .report-tabs .shell { display: flex; gap: 8px; overflow-x: auto; padding-top: 10px; padding-bottom: 10px; }
    .report-tabs a { white-space: nowrap; text-decoration: none; border: 1px solid var(--line); border-radius: 8px; padding: 9px 13px; color: var(--muted); font-weight: 750; font-size: 13px; }
    .report-tabs a[aria-current="page"] { background: var(--navy); border-color: var(--navy); color: white; }
    header { width: auto !important; max-width: none !important; padding: 46px max(16px, calc((100% - 1180px) / 2)) 34px; background: var(--navy); color: white; border-bottom: 5px solid var(--gold); }
    .eyebrow { color: var(--gold); font-size: 12px; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    h1 { font-size: clamp(34px, 5vw, 58px); line-height: 1.02; letter-spacing: -.05em; max-width: 900px; margin: 14px 0 18px; font-weight: 800; }
    .lede { font-size: clamp(18px, 2vw, 23px); line-height: 1.45; max-width: 780px; color: #f5f4f3; margin: 0; }
    .summary-grid { display: grid; grid-template-columns: 1.2fr repeat(3, 1fr); gap: 12px; margin-top: 46px; }
    .intro-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
    .intro-actions a { display: inline-flex; align-items: center; padding: 10px 14px; border-radius: 7px; text-decoration: none; font-weight: 800; border: 1px solid rgba(245,244,243,.35); }
    .intro-actions a:first-child { background: var(--gold); color: var(--navy); border-color: var(--gold); }
    .onboarding { padding-top: 48px; }
    .how-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0 18px; }
    .how-card { padding: 18px; border: 1px solid var(--line); border-top: 4px solid var(--gold); border-radius: 9px; background: var(--paper-strong); }
    .how-card b { display: block; color: var(--navy); margin-bottom: 7px; }
    .how-card p { margin: 0; color: var(--muted); line-height: 1.5; font-size: 14px; }
    .reading-note { margin: 16px 0; padding: 16px 18px; background: var(--paper-strong); border-left: 5px solid var(--teal); color: var(--muted); }
    .dictionary { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; overflow: hidden; border: 1px solid var(--line); border-radius: 9px; background: var(--line); }
    .dictionary div { padding: 14px 16px; background: var(--paper-strong); }
    .dictionary strong { display: block; color: var(--navy); margin-bottom: 4px; }
    .dictionary span { color: var(--muted); font-size: 13px; line-height: 1.45; }
    details.guide { margin-top: 14px; border: 1px solid var(--line); border-radius: 9px; background: var(--paper-strong); overflow: hidden; }
    details.guide summary { cursor: pointer; padding: 15px 18px; font-weight: 800; color: var(--navy); }
    details.guide .guide-body { padding: 0 18px 18px; }
    .summary-card { color: var(--ink); background: var(--paper-strong); border: 1px solid var(--line); border-radius: 12px; padding: 22px; min-height: 145px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: var(--shadow); }
    .summary-card.primary { background: var(--navy); color: white; border-top: 5px solid var(--gold); }
    .summary-label { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 800; }
    .primary .summary-label { color: #f5f4f3; }
    .summary-value { font-size: clamp(28px, 4vw, 42px); font-weight: 900; letter-spacing: -.04em; line-height: 1; margin: 12px 0; }
    .summary-note { font-size: 12px; color: var(--muted); line-height: 1.4; }
    .primary .summary-note { color: #f5f4f3; }
    main { padding-bottom: 80px; }
    .section { padding: 68px 0; border-top: 1px solid var(--line); }
    .section-head { display: grid; grid-template-columns: minmax(240px, .8fr) minmax(320px, 1.2fr); gap: 42px; align-items: end; margin-bottom: 32px; }
    .section-index { font-size: 12px; color: var(--gold-dark); font-weight: 900; letter-spacing: .12em; }
    h2 { font-size: clamp(31px, 4vw, 50px); font-weight: 860; letter-spacing: -.045em; line-height: 1.05; margin: 8px 0 0; }
    .section-copy { color: var(--muted); line-height: 1.65; max-width: 660px; margin: 0; }
    .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 22px; }
    .tab { border: 1px solid var(--line); background: var(--paper-strong); color: var(--ink); padding: 9px 13px; cursor: pointer; border-radius: 8px; font-weight: 750; }
    .tab[aria-selected="true"] { background: var(--ink); color: white; border-color: var(--ink); }
    .tab:focus-visible, select:focus-visible, a:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }
    .legend { display: flex; gap: 18px; flex-wrap: wrap; font-size: 12px; color: var(--muted); margin-bottom: 14px; }
    .legend-item { display: flex; align-items: center; gap: 7px; }
    .legend-dot { width: 9px; height: 9px; border-radius: 50%; }
    .legend-dot.organic { background: var(--teal); }
    .legend-dot.sponsored { background: var(--gold); }
    .scale-note { font-size: 12px; padding: 12px 14px; border-left: 4px solid var(--gold); background: var(--gold-soft); margin-bottom: 18px; color: var(--muted); }
    .segment-list { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; background: var(--paper-strong); box-shadow: var(--shadow); }
    .segment-row { display: grid; grid-template-columns: minmax(150px, .7fr) minmax(390px, 1.7fr) minmax(135px, .55fr); gap: 22px; padding: 20px; border-bottom: 1px solid var(--line); align-items: center; }
    .segment-row:last-child { border-bottom: 0; }
    .segment-name { font-weight: 850; letter-spacing: -.01em; }
    .segment-sample { color: var(--muted); font-size: 12px; margin-top: 4px; }
    .range-area { position: relative; height: 62px; }
    .axis { position: absolute; left: 0; right: 0; top: 30px; height: 1px; background: var(--line); }
    .range { position: absolute; height: 4px; border-radius: 4px; transform: translateY(-50%); }
    .range.organic { background: var(--teal-soft); top: 20px; }
    .range.sponsored { background: var(--gold-soft); top: 42px; }
    .point { position: absolute; width: 10px; height: 10px; border-radius: 50%; transform: translate(-50%, -50%); border: 2px solid var(--paper-strong); box-shadow: 0 0 0 1px currentColor; }
    .point.organic { top: 20px; color: var(--teal); background: var(--teal); }
    .point.sponsored { top: 42px; color: var(--gold); background: var(--gold); }
    .range-value { position: absolute; right: 0; font-size: 11px; color: var(--muted); }
    .range-value.organic { top: 5px; }
    .range-value.sponsored { top: 47px; }
    .delta { justify-self: end; text-align: right; }
    .delta-value { font-weight: 900; font-size: 19px; }
    .delta-label { color: var(--muted); font-size: 11px; max-width: 125px; }
    .control-bar { display: grid; grid-template-columns: repeat(3, minmax(150px, 1fr)); gap: 12px; margin: 18px 0; }
    .control { display: grid; gap: 6px; }
    .control label { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); font-weight: 800; }
    select { width: 100%; border: 1px solid var(--line); background: var(--paper-strong); color: var(--ink); padding: 10px 12px; border-radius: 8px; }
    .delta-strip { position: relative; height: 76px; border: 1px solid var(--line); border-radius: 10px; background: var(--paper-strong); overflow: hidden; }
    .zero-line { position: absolute; left: 50%; top: 0; bottom: 0; width: 1px; background: var(--ink); opacity: .35; }
    .strip-dot { position: absolute; top: 50%; width: 9px; height: 9px; transform: translate(-50%, -50%); border-radius: 50%; background: var(--gold); opacity: .82; border: 1px solid var(--paper-strong); }
    .strip-caption { display: flex; justify-content: space-between; color: var(--muted); font-size: 11px; margin-top: 6px; }
    .table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--paper-strong); margin-top: 18px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th { text-align: left; background: var(--ink); color: white; padding: 11px 12px; white-space: nowrap; }
    td { padding: 11px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; }
    tbody tr:last-child td { border-bottom: 0; }
    tbody tr:hover { background: var(--sand); }
    .number { text-align: right; }
    .positive { color: var(--teal); font-weight: 800; }
    .negative { color: var(--danger); font-weight: 800; }
    .decision-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .decision-card { border: 1px solid var(--line); border-radius: 12px; background: var(--paper-strong); padding: 24px; display: flex; flex-direction: column; min-height: 330px; box-shadow: var(--shadow); }
    .decision-kicker { font-size: 11px; color: var(--gold-dark); text-transform: uppercase; letter-spacing: .1em; font-weight: 900; }
    .decision-card h3 { font-size: 26px; font-weight: 850; letter-spacing: -.03em; margin: 12px 0 16px; }
    .decision-block { border-top: 1px solid var(--line); padding-top: 12px; margin-top: 12px; }
    .decision-block strong { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 5px; }
    .decision-block p { color: var(--muted); margin: 0; line-height: 1.5; }
    .trace-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    .trace-card { border: 1px solid var(--line); border-radius: 12px; background: var(--paper-strong); padding: 22px; }
    .trace-card h3 { margin: 0 0 12px; font-size: 17px; }
    .formula { display: block; background: var(--ink); color: #f5f4f3; padding: 12px; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
    .trace-card dl { display: grid; grid-template-columns: 105px 1fr; gap: 8px 12px; font-size: 13px; margin: 16px 0 0; }
    .trace-card dt { color: var(--muted); }
    .trace-card dd { margin: 0; overflow-wrap: anywhere; }
    .warning { margin-top: 18px; border: 1px solid #d8c3a6; border-radius: 10px; background: var(--gold-soft); padding: 18px; display: grid; grid-template-columns: 34px 1fr; gap: 12px; align-items: start; }
    .warning-icon { width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; background: var(--gold); color: var(--ink); font-weight: 900; }
    .warning strong { display: block; margin-bottom: 4px; }
    .warning p { margin: 0; color: var(--muted); line-height: 1.5; }
    footer { background: var(--navy); color: white; padding: 36px 0; }
    .footer-grid { display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: end; }
    .footer-title { font-size: 25px; font-weight: 850; letter-spacing: -.03em; }
    .footer-meta { color: #f5f4f3; font-size: 12px; line-height: 1.7; overflow-wrap: anywhere; }
    .prototype-stamp { border: 1px solid #b9915b; color: #f5f4f3; padding: 9px 11px; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; transform: rotate(-2deg); }
    .empty { padding: 24px; color: var(--muted); }
    @media (max-width: 900px) {
      .summary-grid { grid-template-columns: repeat(2, 1fr); }
      .section-head { grid-template-columns: 1fr; gap: 18px; }
      .segment-row { grid-template-columns: 1fr; gap: 12px; }
      .delta { justify-self: start; text-align: left; }
      .decision-grid, .trace-grid { grid-template-columns: 1fr; }
      .how-grid, .dictionary { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 620px) {
      .shell { width: min(100% - 20px, 1180px); }
      header { padding-top: 46px; }
      .summary-grid { grid-template-columns: 1fr; }
      .how-grid, .dictionary { grid-template-columns: 1fr; }
      .summary-card { min-height: 120px; }
      .control-bar { grid-template-columns: 1fr; }
      .topline .shell { align-items: flex-start; padding: 11px 0; flex-direction: column; gap: 4px; }
      .segment-row { padding: 16px; }
      .footer-grid { grid-template-columns: 1fr; }
      .prototype-stamp { justify-self: start; }
    }
    @media print {
      .topline { position: static; }
      .tabs, .control-bar { display: none; }
      .section { break-inside: avoid; }
      body { background: white; }
      .summary-card, .segment-list, .decision-card, .trace-card, .table-wrap { box-shadow: none; }
    }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  </style>
</head>
<body>
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <div class="topline">
    <div class="shell">
      <div class="brand"><span class="brand-mark" aria-hidden="true"></span>Evidência Social</div>
      <div class="status">Explorador SQLite · dados Ouro</div>
    </div>
  </div>
  <nav class="report-tabs" aria-label="Relatórios disponíveis">
    <div class="shell">
      <a href="../reports/performance-strategy.html">Análise de performance e estratégia</a>
      <a href="index.html" aria-current="page">Explorar dados</a>
    </div>
  </nav>

  <header class="shell">
    <div class="eyebrow">Explorador do banco SQLite · dados Ouro</div>
    <h1>Explore os dados que sustentam o relatório executivo.</h1>
    <p class="lede">Esta página permite navegar, filtrar e comparar os resultados consolidados do banco <strong>social_media_analysis.sqlite</strong>. Ela não é o relatório executivo: é a camada de comprovação para quem deseja verificar os recortes e cálculos.</p>
    <div class="intro-actions"><a href="../reports/performance-strategy.html">Voltar ao relatório executivo</a><a href="#como-usar">Como usar este explorador</a></div>
    <div class="summary-grid" aria-label="Resumo executivo">
      <article class="summary-card primary">
        <div class="summary-label">O que você está consultando</div>
        <div class="summary-value">Resultados consolidados</div>
        <div class="summary-note">Tabelas Ouro geradas do SQLite em modo somente leitura. Nenhum filtro desta página altera o banco.</div>
      </article>
      <article class="summary-card">
        <div class="summary-label">Mediana · patrocinado</div>
        <div class="summary-value">__SPONSORED_MEDIAN__%</div>
        <div class="summary-note">Interações por view · n = __SPONSORED_N__</div>
      </article>
      <article class="summary-card">
        <div class="summary-label">Mediana · não patrocinado</div>
        <div class="summary-value">__NOT_SPONSORED_MEDIAN__%</div>
        <div class="summary-note">Segundo a flag · n = __NOT_SPONSORED_N__</div>
      </article>
      <article class="summary-card">
        <div class="summary-label">Delta geral</div>
        <div class="summary-value">__OVERALL_DELTA__ p.p.</div>
        <div class="summary-note">Patrocinado menos não patrocinado; comparação descritiva, não causal.</div>
      </article>
    </div>
  </header>

  <main id="conteudo">
    <section class="section onboarding" id="como-usar">
      <div class="shell">
        <div class="section-head">
          <div><div class="section-index">GUIA DE LEITURA</div><h2>Como navegar e interpretar as comparações</h2></div>
          <p class="section-copy">Use esta página quando quiser conferir os números apresentados no relatório. Comece escolhendo um recorte; depois compare os grupos e verifique o volume de posts antes de interpretar qualquer diferença.</p>
        </div>
        <div class="how-grid">
          <article class="how-card"><b>1. Escolha a dimensão</b><p>Use as abas para comparar plataforma, formato, categoria, audiência ou tamanho do creator.</p></article>
          <article class="how-card"><b>2. Compare os grupos</b><p>Cada linha coloca posts patrocinados e posts sem a marcação de patrocínio lado a lado.</p></article>
          <article class="how-card"><b>3. Aplique os filtros</b><p>Em patrocínio, refine por plataforma, categoria e faixa de seguidores para comparar contextos equivalentes.</p></article>
          <article class="how-card"><b>4. Verifique o volume</b><p>O número de posts mostra quanta informação sustenta cada comparação. Grupos menores pedem mais cautela.</p></article>
        </div>
        <div class="reading-note"><strong>Como ler os gráficos:</strong> o ponto representa o resultado típico do grupo. A linha mostra onde se concentra a parte central dos resultados. Quanto maior a sobreposição, menor a separação observada. A escala pode mudar entre dimensões; compare os números exibidos, não apenas o comprimento visual.</div>
        <details class="guide"><summary>O que cada categoria representa</summary><div class="guide-body"><div class="dictionary">
          <div><strong>Plataforma</strong><span>Rede em que o post foi publicado: Instagram, TikTok, YouTube, Bilibili ou RedNote.</span></div>
          <div><strong>Formato</strong><span>Tipo do conteúdo: vídeo, imagem, texto ou formato misto.</span></div>
          <div><strong>Categoria</strong><span>Tema atribuído ao post na base: beleza, lifestyle ou tecnologia.</span></div>
          <div><strong>Tamanho do creator</strong><span>Quatro grupos com quantidades semelhantes de posts, ordenados pelos seguidores na data da publicação. Q1 é a menor faixa e Q4 a maior.</span></div>
          <div><strong>Idade e gênero predominantes</strong><span>Rótulos predominantes informados na base; não representam a distribuição completa da audiência.</span></div>
          <div><strong>Localização principal</strong><span>País descrito como principal; não identifica a localização de cada pessoa que interagiu.</span></div>
          <div><strong>Patrocinado</strong><span>Post marcado como patrocinado na fonte. Ausência da marcação não comprova distribuição totalmente orgânica.</span></div>
          <div><strong>Interações por visualização</strong><span>Curtidas, compartilhamentos e comentários em relação às visualizações. São eventos, não pessoas únicas.</span></div>
        </div></div></details>
      </div>
    </section>
    <section class="section" id="engajamento">
      <div class="shell">
        <div class="section-head">
          <div><div class="section-index">01 · DESEMPENHO</div><h2>Compare o desempenho por plataforma, formato e audiência</h2></div>
          <p class="section-copy">Escolha uma dimensão nas abas. Cada linha compara o resultado típico, a faixa central e o volume de posts dos grupos patrocinado e sem marcação de patrocínio.</p>
        </div>
        <div class="tabs" id="dimension-tabs" role="tablist" aria-label="Dimensão analítica"></div>
        <div class="legend" aria-label="Legenda">
          <span class="legend-item"><span class="legend-dot organic"></span>Não patrocinado segundo a flag</span>
          <span class="legend-item"><span class="legend-dot sponsored"></span>Patrocinado</span>
        </div>
        <div class="scale-note" id="scale-note">A escala é ajustada para cada dimensão. Use os números exibidos para comparar; barras próximas indicam pouca separação entre os grupos.</div>
        <div class="segment-list" id="segment-list" aria-live="polite"></div>
      </div>
    </section>

    <section class="section" id="patrocinio">
      <div class="shell">
        <div class="section-head">
          <div><div class="section-index">02 · PATROCÍNIO</div><h2>Verifique onde o patrocínio ficou acima ou abaixo</h2></div>
          <p class="section-copy">As comparações mantêm plataforma, categoria e faixa de seguidores equivalentes. Use os filtros para investigar um contexto específico e observe a diferença entre os grupos — não apenas quem ficou em primeiro.</p>
        </div>
        <div class="summary-grid" aria-label="Resumo das células comparáveis">
          <article class="summary-card primary"><div class="summary-label">Delta mediano nas 60 células</div><div class="summary-value">__MEDIAN_DELTA__ p.p.</div><div class="summary-note">Cada lado tem entre __MIN_SIDE_N__ e __MAX_SIDE_N__ posts.</div></article>
          <article class="summary-card"><div class="summary-label">Células positivas</div><div class="summary-value">__POSITIVE__</div><div class="summary-note">Patrocinado acima no recorte.</div></article>
          <article class="summary-card"><div class="summary-label">Células negativas</div><div class="summary-value">__NEGATIVE__</div><div class="summary-note">Não patrocinado acima no recorte.</div></article>
          <article class="summary-card"><div class="summary-label">Amplitude dos deltas</div><div class="summary-value">__MIN_DELTA__ a __MAX_DELTA__</div><div class="summary-note">Pontos percentuais; extremos não definem política geral.</div></article>
        </div>
        <div class="delta-strip" id="delta-strip" aria-label="Distribuição dos 60 deltas"><span class="zero-line" aria-hidden="true"></span></div>
        <div class="strip-caption"><span id="strip-min"></span><span>0 p.p.</span><span id="strip-max"></span></div>
        <div class="control-bar" aria-label="Filtros da comparação">
          <div class="control"><label for="platform-filter">Plataforma</label><select id="platform-filter"></select></div>
          <div class="control"><label for="category-filter">Categoria</label><select id="category-filter"></select></div>
          <div class="control"><label for="band-filter">Quartil de seguidores</label><select id="band-filter"></select></div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Plataforma</th><th>Categoria</th><th>Faixa</th><th class="number">Posts patrocinados</th><th class="number">Posts sem marcação</th><th class="number">Resultado típico patrocinado</th><th class="number">Resultado típico sem marcação</th><th class="number">Diferença</th></tr></thead>
            <tbody id="comparison-body"></tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section" id="decisao">
      <div class="shell">
        <div class="section-head">
          <div><div class="section-index">03 · INTERPRETAÇÃO</div><h2>O que esta comparação prova — e o que não prova</h2></div>
          <p class="section-copy">Os blocos abaixo ajudam a distinguir resultado observado, limite da fonte e próximo teste. O explorador não recomenda automaticamente cortar ou escalar investimento.</p>
        </div>
        <div class="decision-grid">
          <article class="decision-card">
            <div class="decision-kicker">Formato</div><h3>Uma pista pequena, não um vencedor</h3>
            <div class="decision-block"><strong>Achado descritivo</strong><p id="format-finding"></p></div>
            <div class="decision-block"><strong>Limitação</strong><p>As diferenças entre medianas são estreitas e pertencem a uma simulação; não medem alcance ou retenção.</p></div>
            <div class="decision-block"><strong>Próximo teste</strong><p>Comparar os formatos dentro da mesma plataforma e categoria, com janela de exposição comum e métrica definida antes do teste.</p></div>
          </article>
          <article class="decision-card">
            <div class="decision-kicker">Patrocínio</div><h3>Testar recortes, não criar uma regra geral</h3>
            <div class="decision-block"><strong>Achado descritivo</strong><p>__POSITIVE__ células favorecem patrocinado e __NEGATIVE__ favorecem não patrocinado; o delta mediano é __MEDIAN_DELTA__ p.p.</p></div>
            <div class="decision-block"><strong>Limitação</strong><p>Não há gasto, receita, atribuição, randomização ou alcance. A flag não calcula ROI e não prova distribuição orgânica.</p></div>
            <div class="decision-block"><strong>Próximo teste</strong><p>Escolher uma célula com amostra suficiente, registrar investimento e manter plataforma, categoria, faixa e janela comparáveis.</p></div>
          </article>
          <article class="decision-card">
            <div class="decision-kicker">Audiência</div><h3>Segmento predominante, não preferência individual</h3>
            <div class="decision-block"><strong>Achado descritivo</strong><p>Idade, gênero e localização permitem comparar grupos predominantes associados aos posts.</p></div>
            <div class="decision-block"><strong>Limitação</strong><p>Os campos não são distribuições percentuais nem identificam quem viu, interagiu ou converteu.</p></div>
            <div class="decision-block"><strong>Próximo teste</strong><p>Validar a composição real da audiência e medir resposta por exposição antes de personalizar conteúdo ou investimento.</p></div>
          </article>
        </div>
        <div class="warning">
          <div class="warning-icon" aria-hidden="true">!</div>
          <div><strong>Creators</strong><p>O ranking de creators não aparece nesta página. <code>creator_id</code> é uma chave válida, mas <code>creator_name</code> varia para o mesmo ID e exige tratamento separado.</p></div>
        </div>
      </div>
    </section>

    <section class="section" id="metodo">
      <div class="shell">
        <div class="section-head">
          <div><div class="section-index">04 · RASTREABILIDADE</div><h2>Origem dos dados e regras de cálculo</h2></div>
          <p class="section-copy">Fórmula, tabelas de origem, integridade do SQLite e limites da comparação.</p>
        </div>
        <div class="trace-grid">
          <article class="trace-card">
            <h3>Métrica principal</h3>
            <code class="formula">100 × (likes + shares + comments_count) / views</code>
            <dl><dt>Nome</dt><dd>Interações por view (%)</dd><dt>Origem</dt><dd>`gold_segment_summaries` e `gold_sponsorship_comparisons`</dd><dt>Uso</dt><dd>Proxy descritiva comparável dentro desta amostra</dd><dt>Não mede</dt><dd>Alcance, impressões, pessoas únicas ou retenção</dd></dl>
          </article>
          <article class="trace-card">
            <h3>Contrato da comparação</h3>
            <code class="formula">delta = mediana(patrocinado) − mediana(não patrocinado)</code>
            <dl><dt>Recorte</dt><dd>Plataforma × categoria × quartil de seguidores</dd><dt>Dispersão</dt><dd>p25–p75 nos resumos segmentados</dd><dt>Suficiência</dt><dd>`n` sempre visível</dd><dt>Limite</dt><dd>Associação observacional, sem causalidade ou ROI</dd></dl>
          </article>
          <article class="trace-card">
            <h3>Fonte e natureza</h3>
            <dl><dt>Dataset</dt><dd>Social Media Sponsorship &amp; Engagement Dataset</dd><dt>Publicador</dt><dd>omenkj · Kaggle</dd><dt>Natureza</dt><dd>Simulada, declarada pelo publicador</dd><dt>Licença</dt><dd>MIT</dd><dt>Posts</dt><dd>__TOTAL_POSTS__</dd></dl>
          </article>
          <article class="trace-card">
            <h3>Controles contra falsas conclusões</h3>
            <dl><dt>Patrocínio × métrica</dt><dd>rho de Spearman = __SPONSOR_RHO__</dd><dt>Seguidores × razão</dt><dd>rho de Spearman = __FOLLOWER_RHO__</dd><dt>Leitura</dt><dd>A flag quase não se associa à métrica; a razão por seguidores é dominada pelo denominador.</dd><dt>Origem</dt><dd><code>gold_numeric_correlations</code></dd></dl>
          </article>
          <article class="trace-card">
            <h3>Artefato consultado</h3>
            <dl><dt>SQLite</dt><dd>__DATABASE_NAME__</dd><dt>SHA-256</dt><dd>__DATABASE_SHA__</dd><dt>Integridade</dt><dd>__INTEGRITY__</dd><dt>Tabelas Ouro</dt><dd>__SEGMENT_ROWS__ resumos · __COMPARISON_ROWS__ comparações · __CORRELATION_ROWS__ correlações</dd><dt>Modo</dt><dd>Somente leitura (<code>mode=ro</code> + <code>query_only</code>)</dd></dl>
          </article>
        </div>
        <div class="warning">
          <div class="warning-icon" aria-hidden="true">i</div>
          <div><strong>Como ler as conclusões</strong><p>O dataset simulado é válido para explorar o cenário do desafio, mas não representa benchmark real. Diferença pequena não prova efeito zero — e tampouco autoriza corte, escala ou causalidade.</p></div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="shell footer-grid">
      <div><div class="footer-title">Evidência antes de recomendação.</div><div class="footer-meta">Tabelas Ouro do Challenge 004 · fonte simulada · análise descritiva<br>Projeto independente, sem afiliação com o G4 Educação.</div></div>
      <div class="prototype-stamp">Explorador de dados</div>
    </div>
  </footer>

  <script id="segment-data" type="application/json">__SEGMENTS_JSON__</script>
  <script id="comparison-data" type="application/json">__COMPARISONS_JSON__</script>
  <script id="report-meta" type="application/json">__METADATA_JSON__</script>
  <script>
    (() => {
      "use strict";
      const segments = JSON.parse(document.getElementById("segment-data").textContent);
      const comparisons = JSON.parse(document.getElementById("comparison-data").textContent);
      const meta = JSON.parse(document.getElementById("report-meta").textContent);

      const number = new Intl.NumberFormat("pt-BR");
      const decimal = new Intl.NumberFormat("pt-BR", { minimumFractionDigits: 4, maximumFractionDigits: 4 });
      const signed = value => `${value >= 0 ? "+" : ""}${decimal.format(value)}`;
      const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[character]);
      const displayKey = value => ({video:"Vídeo", image:"Imagem", text:"Texto", mixed:"Misto", beauty:"Beleza", lifestyle:"Lifestyle", tech:"Tecnologia", female:"Feminino", male:"Masculino", "non-binary":"Não binário", unknown:"Desconhecido"})[value] || value;
      const displayBand = value => ({post_followers_q1:"Q1", post_followers_q2:"Q2", post_followers_q3:"Q3", post_followers_q4:"Q4"})[value] || value;

      const tabs = document.getElementById("dimension-tabs");
      const list = document.getElementById("segment-list");
      let currentDimension = "platform";

      function renderTabs() {
        tabs.innerHTML = Object.entries(meta.dimensions).map(([key, label], index) => `<button class="tab" type="button" role="tab" aria-selected="${key === currentDimension}" aria-controls="segment-list" id="tab-${key}" data-dimension="${key}" tabindex="${key === currentDimension ? 0 : -1}">${escapeHtml(label)}</button>`).join("");
        tabs.querySelectorAll("button").forEach(button => button.addEventListener("click", () => {
          currentDimension = button.dataset.dimension;
          renderTabs();
          renderSegments();
        }));
      }

      function renderSegments() {
        const rows = segments.filter(row => row.slice_type === currentDimension);
        const grouped = new Map();
        rows.forEach(row => {
          if (!grouped.has(row.slice_key)) grouped.set(row.slice_key, {});
          grouped.get(row.slice_key)[row.sponsorship_label] = row;
        });
        const complete = [...grouped.entries()].filter(([, pair]) => pair.sponsored_true && pair.not_sponsored_by_flag).map(([key, pair]) => ({ key, pair }));
        if (!complete.length) {
          list.innerHTML = '<div class="empty">Nenhum segmento comparável nesta dimensão.</div>';
          return;
        }
        const allBounds = complete.flatMap(({pair}) => [pair.sponsored_true.interaction_per_view_pct_p25, pair.sponsored_true.interaction_per_view_pct_p75, pair.not_sponsored_by_flag.interaction_per_view_pct_p25, pair.not_sponsored_by_flag.interaction_per_view_pct_p75]);
        const domainMin = Math.min(...allBounds);
        const domainMax = Math.max(...allBounds);
        const width = Math.max(domainMax - domainMin, .0001);
        const position = value => Math.max(0, Math.min(100, 100 * (value - domainMin) / width));
        complete.sort((a, b) => {
          const avgA = (a.pair.sponsored_true.interaction_per_view_pct_median + a.pair.not_sponsored_by_flag.interaction_per_view_pct_median) / 2;
          const avgB = (b.pair.sponsored_true.interaction_per_view_pct_median + b.pair.not_sponsored_by_flag.interaction_per_view_pct_median) / 2;
          return avgB - avgA;
        });
        list.innerHTML = complete.map(({key, pair}) => {
          const sponsored = pair.sponsored_true;
          const organic = pair.not_sponsored_by_flag;
          const delta = sponsored.interaction_per_view_pct_median - organic.interaction_per_view_pct_median;
          const organicLeft = position(organic.interaction_per_view_pct_p25);
          const organicRight = position(organic.interaction_per_view_pct_p75);
          const sponsorLeft = position(sponsored.interaction_per_view_pct_p25);
          const sponsorRight = position(sponsored.interaction_per_view_pct_p75);
          return `<article class="segment-row">
            <div><div class="segment-name">${escapeHtml(displayKey(key))}</div><div class="segment-sample">n = ${number.format(organic.n + sponsored.n)} · dois grupos</div></div>
            <div class="range-area" aria-label="Medianas e intervalos centrais">
              <span class="axis" aria-hidden="true"></span>
              <span class="range organic" style="left:${organicLeft}%;width:${Math.max(organicRight-organicLeft,1)}%"></span>
              <span class="point organic" style="left:${position(organic.interaction_per_view_pct_median)}%"></span>
              <span class="range sponsored" style="left:${sponsorLeft}%;width:${Math.max(sponsorRight-sponsorLeft,1)}%"></span>
              <span class="point sponsored" style="left:${position(sponsored.interaction_per_view_pct_median)}%"></span>
              <span class="range-value organic">${decimal.format(organic.interaction_per_view_pct_median)}% · n ${number.format(organic.n)} · p25–p75 ${decimal.format(organic.interaction_per_view_pct_p25)}–${decimal.format(organic.interaction_per_view_pct_p75)}</span>
              <span class="range-value sponsored">${decimal.format(sponsored.interaction_per_view_pct_median)}% · n ${number.format(sponsored.n)} · p25–p75 ${decimal.format(sponsored.interaction_per_view_pct_p25)}–${decimal.format(sponsored.interaction_per_view_pct_p75)}</span>
            </div>
            <div class="delta"><div class="delta-value ${delta >= 0 ? "positive" : "negative"}">${signed(delta)} p.p.</div><div class="delta-label">patrocinado menos não patrocinado</div></div>
          </article>`;
        }).join("");
        document.getElementById("scale-note").textContent = `Escala ampliada nesta dimensão: ${decimal.format(domainMin)}% a ${decimal.format(domainMax)}%. Compare os valores exatos; o eixo não começa em zero.`;
      }

      function uniqueValues(key) { return [...new Set(comparisons.map(row => row[key]))].sort(); }
      function populateSelect(id, key, formatter = value => value) {
        const select = document.getElementById(id);
        select.innerHTML = `<option value="">Todos</option>` + uniqueValues(key).map(value => `<option value="${escapeHtml(value)}">${escapeHtml(formatter(value))}</option>`).join("");
        select.addEventListener("change", renderComparisonTable);
      }

      function renderStrip() {
        const summary = meta.comparison_summary;
        const bound = Math.max(Math.abs(summary.min_delta), Math.abs(summary.max_delta));
        const strip = document.getElementById("delta-strip");
        strip.querySelectorAll(".strip-dot").forEach(dot => dot.remove());
        comparisons.forEach((row, index) => {
          const dot = document.createElement("span");
          dot.className = "strip-dot";
          dot.style.left = `${50 + 48 * row.interaction_per_view_pct_median_difference / bound}%`;
          dot.style.top = `${18 + (index % 5) * 14}%`;
          dot.title = `${row.platform} · ${row.content_category} · ${displayBand(row.post_follower_band)}: ${signed(row.interaction_per_view_pct_median_difference)} p.p.`;
          strip.appendChild(dot);
        });
        document.getElementById("strip-min").textContent = `${decimal.format(-bound)} p.p.`;
        document.getElementById("strip-max").textContent = `+${decimal.format(bound)} p.p.`;
      }

      function renderComparisonTable() {
        const platform = document.getElementById("platform-filter").value;
        const category = document.getElementById("category-filter").value;
        const band = document.getElementById("band-filter").value;
        const rows = comparisons.filter(row => (!platform || row.platform === platform) && (!category || row.content_category === category) && (!band || row.post_follower_band === band)).sort((a, b) => Math.abs(b.interaction_per_view_pct_median_difference) - Math.abs(a.interaction_per_view_pct_median_difference));
        document.getElementById("comparison-body").innerHTML = rows.map(row => {
          const delta = row.interaction_per_view_pct_median_difference;
          return `<tr><td>${escapeHtml(row.platform)}</td><td>${escapeHtml(displayKey(row.content_category))}</td><td>${escapeHtml(displayBand(row.post_follower_band))}</td><td class="number">${number.format(row.sponsored_n)}</td><td class="number">${number.format(row.not_sponsored_n)}</td><td class="number">${decimal.format(row.sponsored_interaction_per_view_pct_median)}%</td><td class="number">${decimal.format(row.not_sponsored_interaction_per_view_pct_median)}%</td><td class="number ${delta >= 0 ? "positive" : "negative"}">${signed(delta)} p.p.</td></tr>`;
        }).join("") || '<tr><td colspan="8" class="empty">Nenhuma célula para os filtros escolhidos.</td></tr>';
      }

      function renderFinding() {
        const organic = meta.format_leaders.not_sponsored_by_flag;
        const sponsored = meta.format_leaders.sponsored_true;
        document.getElementById("format-finding").textContent = `${displayKey(organic.leader)} lidera entre não patrocinados com ${decimal.format(organic.leader_value)}% (amplitude entre formatos: ${decimal.format(organic.spread)} p.p.); ${displayKey(sponsored.leader)} lidera entre patrocinados com ${decimal.format(sponsored.leader_value)}% (amplitude: ${decimal.format(sponsored.spread)} p.p.).`;
      }

      renderTabs();
      renderSegments();
      populateSelect("platform-filter", "platform");
      populateSelect("category-filter", "content_category", displayKey);
      populateSelect("band-filter", "post_follower_band", displayBand);
      renderStrip();
      renderComparisonTable();
      renderFinding();
    })();
  </script>
</body>
</html>
'''

    replacements = {
        "__MANROPE_FONT__": font_base64,
        "__SPONSORED_MEDIAN__": br_number(float(sponsored["interaction_per_view_pct_median"])),
        "__SPONSORED_N__": f'{int(sponsored["n"]):,}'.replace(",", "."),
        "__NOT_SPONSORED_MEDIAN__": br_number(float(not_sponsored["interaction_per_view_pct_median"])),
        "__NOT_SPONSORED_N__": f'{int(not_sponsored["n"]):,}'.replace(",", "."),
        "__OVERALL_DELTA__": ("+" if overall_delta >= 0 else "") + br_number(overall_delta),
        "__TOTAL_POSTS__": f"{total_posts:,}".replace(",", "."),
        "__MEDIAN_DELTA__": ("+" if median_delta >= 0 else "") + br_number(median_delta),
        "__MIN_DELTA__": br_number(min_delta),
        "__MAX_DELTA__": ("+" if max_delta >= 0 else "") + br_number(max_delta),
        "__POSITIVE__": str(positive),
        "__NEGATIVE__": str(negative),
        "__MIN_SIDE_N__": str(min(sample_side_sizes)),
        "__MAX_SIDE_N__": str(max(sample_side_sizes)),
        "__DATABASE_NAME__": html.escape(database.name),
        "__DATABASE_SHA__": sha256(database),
        "__INTEGRITY__": html.escape(integrity),
        "__SPONSOR_RHO__": br_number(sponsor_engagement_rho, 6),
        "__FOLLOWER_RHO__": br_number(follower_ratio_rho, 6),
        "__SEGMENT_ROWS__": str(len(segments)),
        "__COMPARISON_ROWS__": str(len(comparisons)),
        "__CORRELATION_ROWS__": str(len(correlations)),
        "__SEGMENTS_JSON__": json_for_html(visible_segments),
        "__COMPARISONS_JSON__": json_for_html(public_comparisons),
        "__METADATA_JSON__": json_for_html(metadata),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    unresolved = [token for token in replacements if token in template]
    if unresolved:
        raise RuntimeError(f"Unresolved placeholders: {unresolved}")
    return template


def main() -> None:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate the static exploratory report from Gold SQLite tables."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=base.parent / "data" / "evidence" / "social_media_analysis.sqlite",
    )
    parser.add_argument("--output", type=Path, default=base / "index.html")
    args = parser.parse_args()
    if not args.database.is_file():
        raise SystemExit(f"Database not found: {args.database}")
    page = build_page(args.database)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")
    print(
        json.dumps(
            {
                "database": str(args.database.resolve()),
                "database_sha256": sha256(args.database),
                "output": str(args.output.resolve()),
                "output_bytes": args.output.stat().st_size,
                "gold_tables": sorted(REQUIRED_TABLES),
                "read_only": True,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
