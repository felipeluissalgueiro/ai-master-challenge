#!/usr/bin/env python3
"""Rebuild the complete Bronze, Silver and descriptive Gold pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import build_bronze
import build_gold_comparisons
import build_silver_audience
import build_silver_content
import build_silver_creators
import build_silver_dates
import build_silver_dimensions
import build_silver_follower_bands
import build_silver_metrics


def compact(result: dict[str, object], keys: tuple[str, ...]) -> dict[str, object]:
    return {key: result[key] for key in keys if key in result}


def run(csv_path: Path, zip_path: Path, database_path: Path) -> dict[str, object]:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    results = {}

    results["bronze"] = compact(
        build_bronze.build(csv_path, zip_path, database_path),
        ("rows", "source_columns", "csv_sha256", "zip_sha256", "integrity_check"),
    )
    results["silver_metrics"] = compact(
        build_silver_metrics.build(database_path), ("rows",)
    )
    results["silver_dimensions"] = compact(
        build_silver_dimensions.build(database_path),
        ("rows", "valid_rows", "invalid_rows", "quality_flag_counts"),
    )
    results["silver_creators"] = compact(
        build_silver_creators.build(database_path),
        (
            "source_rows",
            "creator_ids",
            "identity_consistent_creators",
            "creator_profile_eligible",
            "audit_flag_counts",
        ),
    )
    results["silver_dates"] = compact(
        build_silver_dates.build(database_path),
        ("rows", "valid_rows", "invalid_rows", "timezone_known_rows", "period"),
    )
    results["silver_audience"] = compact(
        build_silver_audience.build(database_path),
        ("rows", "valid_rows", "invalid_rows", "quality_flag_counts"),
    )
    results["silver_content"] = compact(
        build_silver_content.build(database_path),
        (
            "rows",
            "valid_structure_rows",
            "invalid_structure_rows",
            "quality_flag_counts",
            "duplicates",
        ),
    )
    results["silver_follower_bands"] = compact(
        build_silver_follower_bands.build(database_path),
        ("rows", "invalid_rows", "method", "thresholds", "bands"),
    )
    results["gold"] = compact(
        build_gold_comparisons.build(database_path),
        (
            "source_rows",
            "segment_summary_rows",
            "comparable_sponsorship_cells",
            "correlation_rows",
            "overall_medians",
            "interaction_per_view_pct_median_difference_across_cells",
            "selected_spearman_correlations",
            "decision",
            "limit",
        ),
    )
    return {"database": str(database_path), "stages": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.csv, args.zip, args.database),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
