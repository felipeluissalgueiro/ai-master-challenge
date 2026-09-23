#!/usr/bin/env python3
"""Build descriptive Gold comparisons with sample sizes and explicit limits."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import defaultdict
from pathlib import Path


METRICS = (
    "views",
    "total_interactions",
    "interaction_per_view_pct",
    "interaction_per_follower_pct",
)
CORRELATION_VARIABLES = (
    "is_sponsored",
    "views",
    "likes",
    "shares",
    "comments_count",
    "follower_count",
    "total_interactions",
    "interaction_per_view_pct",
    "interaction_per_follower_pct",
    "views_per_follower",
)


def quantile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def profile(values: list[float]) -> tuple[float, float, float]:
    q1 = quantile(values, 0.25)
    median = quantile(values, 0.50)
    q3 = quantile(values, 0.75)
    assert q1 is not None and median is not None and q3 is not None
    return q1, median, q3


def average_ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    index = 0
    while index < len(indexed):
        end = index + 1
        while end < len(indexed) and indexed[end][1] == indexed[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        for offset in range(index, end):
            ranks[indexed[offset][0]] = average_rank
        index = end
    return ranks


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right, strict=True)
    )
    left_variance = sum((value - left_mean) ** 2 for value in left)
    right_variance = sum((value - right_mean) ** 2 for value in right)
    denominator = math.sqrt(left_variance * right_variance)
    if denominator == 0:
        return None
    return numerator / denominator


def spearman(left: list[float], right: list[float]) -> float | None:
    return pearson(average_ranks(left), average_ranks(right))


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")

    query = """
        SELECT
            m.source_row_number,
            d.platform,
            d.content_type,
            d.content_category,
            d.is_sponsored,
            d.sponsorship_label,
            f.band_label,
            a.audience_age_label,
            a.audience_gender_label,
            a.audience_location_label,
            m.views,
            m.likes,
            m.shares,
            m.comments_count,
            m.follower_count,
            m.total_interactions,
            m.interaction_per_view_pct,
            m.interaction_per_follower_pct,
            m.views_per_follower
        FROM silver_posts_metrics AS m
        JOIN silver_posts_dimensions AS d USING (source_row_number)
        JOIN silver_posts_follower_bands AS f USING (source_row_number)
        JOIN silver_posts_audience AS a USING (source_row_number)
        WHERE m.metrics_valid = 1
          AND d.dimensions_valid = 1
          AND a.audience_valid = 1
        ORDER BY m.source_row_number
    """
    source_rows = list(connection.execute(query))
    columns = (
        "source_row_number",
        "platform",
        "content_type",
        "content_category",
        "is_sponsored",
        "sponsorship_label",
        "band_label",
        "audience_age_label",
        "audience_gender_label",
        "audience_location_label",
        "views",
        "likes",
        "shares",
        "comments_count",
        "follower_count",
        "total_interactions",
        "interaction_per_view_pct",
        "interaction_per_follower_pct",
        "views_per_follower",
    )

    segment_groups: defaultdict[
        tuple[str, str, str], dict[str, list[float]]
    ] = defaultdict(lambda: {metric: [] for metric in METRICS})
    comparable_groups: defaultdict[
        tuple[str, str, str, str], dict[str, list[float]]
    ] = defaultdict(lambda: {metric: [] for metric in METRICS})
    correlation_values = {variable: [] for variable in CORRELATION_VARIABLES}

    for raw_row in source_rows:
        row = dict(zip(columns, raw_row, strict=True))
        slices = (
            ("overall", "all"),
            ("platform", row["platform"]),
            ("content_type", row["content_type"]),
            ("content_category", row["content_category"]),
            ("post_follower_band", row["band_label"]),
            ("audience_age_label", row["audience_age_label"]),
            ("audience_gender_label", row["audience_gender_label"]),
            ("audience_location_label", row["audience_location_label"]),
        )
        for slice_type, slice_key in slices:
            bucket = segment_groups[
                (slice_type, slice_key, row["sponsorship_label"])
            ]
            for metric in METRICS:
                bucket[metric].append(float(row[metric]))

        comparable_bucket = comparable_groups[
            (
                row["platform"],
                row["content_category"],
                row["band_label"],
                row["sponsorship_label"],
            )
        ]
        for metric in METRICS:
            comparable_bucket[metric].append(float(row[metric]))
        for variable in CORRELATION_VARIABLES:
            correlation_values[variable].append(float(row[variable]))

    summary_rows = []
    for (slice_type, slice_key, sponsorship_label), values in sorted(
        segment_groups.items()
    ):
        metric_profiles = {metric: profile(values[metric]) for metric in METRICS}
        summary_rows.append(
            (
                slice_type,
                slice_key,
                sponsorship_label,
                len(values["views"]),
                *metric_profiles["views"],
                *metric_profiles["total_interactions"],
                *metric_profiles["interaction_per_view_pct"],
                *metric_profiles["interaction_per_follower_pct"],
                "descriptive_association_only",
            )
        )

    comparison_rows = []
    comparison_differences = []
    comparison_sample_sizes = []
    comparison_keys = sorted(
        {
            (platform, category, band)
            for platform, category, band, _sponsorship in comparable_groups
        }
    )
    for platform, category, band in comparison_keys:
        sponsored = comparable_groups[(platform, category, band, "sponsored_true")]
        not_sponsored = comparable_groups[
            (platform, category, band, "not_sponsored_by_flag")
        ]
        sponsored_n = len(sponsored["views"])
        not_sponsored_n = len(not_sponsored["views"])
        sponsored_medians = {
            metric: profile(sponsored[metric])[1] for metric in METRICS
        }
        not_sponsored_medians = {
            metric: profile(not_sponsored[metric])[1] for metric in METRICS
        }
        differences = {
            metric: sponsored_medians[metric] - not_sponsored_medians[metric]
            for metric in METRICS
        }
        comparison_differences.append(differences["interaction_per_view_pct"])
        comparison_sample_sizes.extend((sponsored_n, not_sponsored_n))
        comparison_rows.append(
            (
                platform,
                category,
                band,
                sponsored_n,
                not_sponsored_n,
                sponsored_medians["views"],
                not_sponsored_medians["views"],
                differences["views"],
                sponsored_medians["total_interactions"],
                not_sponsored_medians["total_interactions"],
                differences["total_interactions"],
                sponsored_medians["interaction_per_view_pct"],
                not_sponsored_medians["interaction_per_view_pct"],
                differences["interaction_per_view_pct"],
                sponsored_medians["interaction_per_follower_pct"],
                not_sponsored_medians["interaction_per_follower_pct"],
                differences["interaction_per_follower_pct"],
                "measure_better",
                "synthetic source; sponsorship flag is not causal treatment",
            )
        )

    correlation_rows = []
    correlation_lookup = {}
    for left_index, left_name in enumerate(CORRELATION_VARIABLES):
        for right_name in CORRELATION_VARIABLES[left_index + 1 :]:
            coefficient = spearman(
                correlation_values[left_name], correlation_values[right_name]
            )
            correlation_rows.append(
                (
                    left_name,
                    right_name,
                    len(source_rows),
                    coefficient,
                    "association_only; derived ratios may create mechanical correlation",
                )
            )
            correlation_lookup[f"{left_name}__{right_name}"] = coefficient

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS gold_segment_summaries")
        connection.execute("DROP TABLE IF EXISTS gold_sponsorship_comparisons")
        connection.execute("DROP TABLE IF EXISTS gold_numeric_correlations")
        connection.execute(
            """
            CREATE TABLE gold_segment_summaries (
                slice_type TEXT NOT NULL,
                slice_key TEXT NOT NULL,
                sponsorship_label TEXT NOT NULL,
                n INTEGER NOT NULL,
                views_p25 REAL NOT NULL,
                views_median REAL NOT NULL,
                views_p75 REAL NOT NULL,
                total_interactions_p25 REAL NOT NULL,
                total_interactions_median REAL NOT NULL,
                total_interactions_p75 REAL NOT NULL,
                interaction_per_view_pct_p25 REAL NOT NULL,
                interaction_per_view_pct_median REAL NOT NULL,
                interaction_per_view_pct_p75 REAL NOT NULL,
                interaction_per_follower_pct_p25 REAL NOT NULL,
                interaction_per_follower_pct_median REAL NOT NULL,
                interaction_per_follower_pct_p75 REAL NOT NULL,
                interpretation_limit TEXT NOT NULL,
                PRIMARY KEY (slice_type, slice_key, sponsorship_label)
            )
            """
        )
        connection.executemany(
            "INSERT INTO gold_segment_summaries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            summary_rows,
        )
        connection.execute(
            """
            CREATE TABLE gold_sponsorship_comparisons (
                platform TEXT NOT NULL,
                content_category TEXT NOT NULL,
                post_follower_band TEXT NOT NULL,
                sponsored_n INTEGER NOT NULL,
                not_sponsored_n INTEGER NOT NULL,
                sponsored_views_median REAL NOT NULL,
                not_sponsored_views_median REAL NOT NULL,
                views_median_difference REAL NOT NULL,
                sponsored_total_interactions_median REAL NOT NULL,
                not_sponsored_total_interactions_median REAL NOT NULL,
                total_interactions_median_difference REAL NOT NULL,
                sponsored_interaction_per_view_pct_median REAL NOT NULL,
                not_sponsored_interaction_per_view_pct_median REAL NOT NULL,
                interaction_per_view_pct_median_difference REAL NOT NULL,
                sponsored_interaction_per_follower_pct_median REAL NOT NULL,
                not_sponsored_interaction_per_follower_pct_median REAL NOT NULL,
                interaction_per_follower_pct_median_difference REAL NOT NULL,
                action_candidate TEXT NOT NULL,
                interpretation_limit TEXT NOT NULL,
                PRIMARY KEY (platform, content_category, post_follower_band)
            )
            """
        )
        connection.executemany(
            "INSERT INTO gold_sponsorship_comparisons VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            comparison_rows,
        )
        connection.execute(
            """
            CREATE TABLE gold_numeric_correlations (
                variable_left TEXT NOT NULL,
                variable_right TEXT NOT NULL,
                n INTEGER NOT NULL,
                spearman_rho REAL,
                interpretation_limit TEXT NOT NULL,
                PRIMARY KEY (variable_left, variable_right)
            )
            """
        )
        connection.executemany(
            "INSERT INTO gold_numeric_correlations VALUES (?, ?, ?, ?, ?)",
            correlation_rows,
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    overall = {
        sponsorship: {
            metric: profile(
                segment_groups[("overall", "all", sponsorship)][metric]
            )[1]
            for metric in METRICS
        }
        for sponsorship in ("not_sponsored_by_flag", "sponsored_true")
    }
    absolute_differences = sorted(abs(value) for value in comparison_differences)
    return {
        "database": str(database_path),
        "source_rows": len(source_rows),
        "segment_summary_rows": len(summary_rows),
        "comparable_sponsorship_cells": len(comparison_rows),
        "correlation_rows": len(correlation_rows),
        "overall_medians": overall,
        "comparable_cell_sample_sizes": {
            "min": min(comparison_sample_sizes),
            "median": quantile([float(value) for value in comparison_sample_sizes], 0.50),
            "max": max(comparison_sample_sizes),
        },
        "interaction_per_view_pct_median_difference_across_cells": {
            "min": min(comparison_differences),
            "median": quantile(comparison_differences, 0.50),
            "max": max(comparison_differences),
            "median_absolute": quantile(absolute_differences, 0.50),
            "positive_cells": sum(value > 0 for value in comparison_differences),
            "negative_cells": sum(value < 0 for value in comparison_differences),
            "zero_cells": sum(value == 0 for value in comparison_differences),
        },
        "selected_spearman_correlations": {
            key: correlation_lookup[key]
            for key in (
                "is_sponsored__views",
                "is_sponsored__total_interactions",
                "is_sponsored__interaction_per_view_pct",
                "follower_count__interaction_per_follower_pct",
                "follower_count__views_per_follower",
                "views__interaction_per_view_pct",
                "total_interactions__interaction_per_view_pct",
            )
        },
        "decision": "measure_better",
        "limit": "Synthetic data supports method demonstration, not causal marketing action.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
