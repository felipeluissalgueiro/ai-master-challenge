#!/usr/bin/env python3
"""Build the first Silver segment: validated counts and explicit rate proxies."""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
from pathlib import Path


COUNT_FIELDS = ("views", "likes", "shares", "comments_count", "follower_count")
NON_NEGATIVE_INTEGER = re.compile(r"^(0|[1-9][0-9]*)$")


def parse_count(raw: str) -> int | None:
    if not NON_NEGATIVE_INTEGER.fullmatch(raw):
        return None
    return int(raw)


def quantile(sorted_values: list[int], probability: float) -> float | None:
    if not sorted_values:
        return None
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")
    profiles = {field: [] for field in COUNT_FIELDS}
    invalid_counts = {field: 0 for field in COUNT_FIELDS}
    zero_counts = {field: 0 for field in COUNT_FIELDS}
    inserted = 0

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_metrics")
        connection.execute(
            """
            CREATE TABLE silver_posts_metrics (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                views INTEGER,
                likes INTEGER,
                shares INTEGER,
                comments_count INTEGER,
                follower_count INTEGER,
                total_interactions INTEGER,
                interaction_per_view_pct REAL,
                interaction_per_follower_pct REAL,
                views_per_follower REAL,
                metrics_valid INTEGER NOT NULL CHECK (metrics_valid IN (0, 1)),
                quality_flags TEXT NOT NULL,
                CHECK (views IS NULL OR views >= 0),
                CHECK (likes IS NULL OR likes >= 0),
                CHECK (shares IS NULL OR shares >= 0),
                CHECK (comments_count IS NULL OR comments_count >= 0),
                CHECK (follower_count IS NULL OR follower_count >= 0)
            )
            """
        )

        select_sql = (
            "SELECT source_row_number, id, content_id, "
            + ", ".join(COUNT_FIELDS)
            + " FROM bronze_posts_raw ORDER BY source_row_number"
        )
        insert_sql = """
            INSERT INTO silver_posts_metrics (
                source_row_number, id, content_id,
                views, likes, shares, comments_count, follower_count,
                total_interactions, interaction_per_view_pct,
                interaction_per_follower_pct, views_per_follower,
                metrics_valid, quality_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        batch: list[tuple[object, ...]] = []

        for row in connection.execute(select_sql):
            source_row_number, row_id, content_id, *raw_counts = row
            parsed = {
                field: parse_count(raw)
                for field, raw in zip(COUNT_FIELDS, raw_counts, strict=True)
            }
            flags = []
            for field, value in parsed.items():
                if value is None:
                    invalid_counts[field] += 1
                    flags.append(f"invalid_{field}")
                else:
                    profiles[field].append(value)
                    if value == 0:
                        zero_counts[field] += 1

            metrics_valid = int(not flags)
            total_interactions = None
            interaction_per_view_pct = None
            interaction_per_follower_pct = None
            views_per_follower = None
            if metrics_valid:
                views = parsed["views"]
                likes = parsed["likes"]
                shares = parsed["shares"]
                comments_count = parsed["comments_count"]
                follower_count = parsed["follower_count"]
                assert None not in (views, likes, shares, comments_count, follower_count)
                total_interactions = likes + shares + comments_count
                if views != 0:
                    interaction_per_view_pct = 100.0 * total_interactions / views
                else:
                    flags.append("zero_views")
                if follower_count != 0:
                    interaction_per_follower_pct = (
                        100.0 * total_interactions / follower_count
                    )
                    views_per_follower = views / follower_count
                else:
                    flags.append("zero_follower_count")

            batch.append(
                (
                    source_row_number,
                    row_id,
                    content_id,
                    parsed["views"],
                    parsed["likes"],
                    parsed["shares"],
                    parsed["comments_count"],
                    parsed["follower_count"],
                    total_interactions,
                    interaction_per_view_pct,
                    interaction_per_follower_pct,
                    views_per_follower,
                    metrics_valid,
                    ";".join(flags),
                )
            )
            if len(batch) == 1000:
                connection.executemany(insert_sql, batch)
                inserted += len(batch)
                batch.clear()
        if batch:
            connection.executemany(insert_sql, batch)
            inserted += len(batch)

        bronze_rows = connection.execute(
            "SELECT COUNT(*) FROM bronze_posts_raw"
        ).fetchone()[0]
        silver_rows = connection.execute(
            "SELECT COUNT(*) FROM silver_posts_metrics"
        ).fetchone()[0]
        if bronze_rows != silver_rows or inserted != bronze_rows:
            raise RuntimeError(
                f"Row parity failed: bronze={bronze_rows}, "
                f"silver={silver_rows}, inserted={inserted}"
            )
        connection.execute(
            "CREATE INDEX silver_posts_metrics_content_id_idx "
            "ON silver_posts_metrics(content_id)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    profile_output = {}
    for field, values in profiles.items():
        values.sort()
        profile_output[field] = {
            "invalid": invalid_counts[field],
            "zero": zero_counts[field],
            "min": values[0] if values else None,
            "p01": quantile(values, 0.01),
            "median": quantile(values, 0.50),
            "p99": quantile(values, 0.99),
            "max": values[-1] if values else None,
        }
    return {
        "database": str(database_path),
        "rows": inserted,
        "profiles": profile_output,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
