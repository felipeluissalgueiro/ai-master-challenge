#!/usr/bin/env python3
"""Create sample-relative follower-count quartiles at post level."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path


def nearest_rank(sorted_values: list[int], probability: float) -> int:
    rank = max(1, math.ceil(probability * len(sorted_values)))
    return sorted_values[rank - 1]


def band_for(value: int, thresholds: tuple[int, int, int]) -> tuple[int, str]:
    q1, q2, q3 = thresholds
    if value <= q1:
        return 1, "post_followers_q1"
    if value <= q2:
        return 2, "post_followers_q2"
    if value <= q3:
        return 3, "post_followers_q3"
    return 4, "post_followers_q4"


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")
    source_rows = list(
        connection.execute(
            """
            SELECT source_row_number, id, content_id, follower_count, metrics_valid
            FROM silver_posts_metrics
            ORDER BY source_row_number
            """
        )
    )
    invalid_rows = sum(
        1 for *_prefix, follower_count, metrics_valid in source_rows
        if not metrics_valid or follower_count is None
    )
    if invalid_rows:
        raise ValueError(
            f"Cannot create follower bands: {invalid_rows} rows lack valid follower_count"
        )

    sorted_followers = sorted(row[3] for row in source_rows)
    thresholds = (
        nearest_rank(sorted_followers, 0.25),
        nearest_rank(sorted_followers, 0.50),
        nearest_rank(sorted_followers, 0.75),
    )
    prepared_rows = []
    band_counts: Counter[str] = Counter()
    band_values: dict[int, list[int]] = {1: [], 2: [], 3: [], 4: []}
    for source_row_number, row_id, content_id, follower_count, _metrics_valid in source_rows:
        ordinal, label = band_for(follower_count, thresholds)
        band_counts[label] += 1
        band_values[ordinal].append(follower_count)
        prepared_rows.append(
            (
                source_row_number,
                row_id,
                content_id,
                follower_count,
                ordinal,
                label,
                "sample_relative_nearest_rank_quartile",
            )
        )

    definitions = []
    for ordinal in range(1, 5):
        values = band_values[ordinal]
        definitions.append(
            (
                ordinal,
                f"post_followers_q{ordinal}",
                min(values),
                max(values),
                len(values),
                "sample_relative_nearest_rank_quartile",
                "follower_count declared on each post; not a stable creator profile",
            )
        )

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_follower_bands")
        connection.execute("DROP TABLE IF EXISTS silver_follower_band_definitions")
        connection.execute(
            """
            CREATE TABLE silver_follower_band_definitions (
                band_ordinal INTEGER PRIMARY KEY CHECK (band_ordinal BETWEEN 1 AND 4),
                band_label TEXT NOT NULL UNIQUE,
                minimum_follower_count INTEGER NOT NULL,
                maximum_follower_count INTEGER NOT NULL,
                sample_size INTEGER NOT NULL,
                method TEXT NOT NULL,
                interpretation_limit TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            "INSERT INTO silver_follower_band_definitions VALUES (?, ?, ?, ?, ?, ?, ?)",
            definitions,
        )
        connection.execute(
            """
            CREATE TABLE silver_posts_follower_bands (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                follower_count INTEGER NOT NULL CHECK (follower_count >= 0),
                band_ordinal INTEGER NOT NULL CHECK (band_ordinal BETWEEN 1 AND 4),
                band_label TEXT NOT NULL,
                band_method TEXT NOT NULL,
                FOREIGN KEY (band_ordinal)
                    REFERENCES silver_follower_band_definitions(band_ordinal)
            )
            """
        )
        connection.executemany(
            "INSERT INTO silver_posts_follower_bands VALUES (?, ?, ?, ?, ?, ?, ?)",
            prepared_rows,
        )
        stored_rows = connection.execute(
            "SELECT COUNT(*) FROM silver_posts_follower_bands"
        ).fetchone()[0]
        if stored_rows != len(source_rows):
            raise RuntimeError(
                f"Follower band parity failed: source={len(source_rows)}, stored={stored_rows}"
            )
        connection.execute(
            "CREATE INDEX silver_posts_follower_bands_band_idx "
            "ON silver_posts_follower_bands(band_ordinal, follower_count)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "database": str(database_path),
        "rows": len(source_rows),
        "invalid_rows": invalid_rows,
        "method": "sample_relative_nearest_rank_quartile",
        "thresholds": {"q1": thresholds[0], "q2": thresholds[1], "q3": thresholds[2]},
        "bands": [
            {
                "ordinal": ordinal,
                "label": label,
                "minimum": minimum,
                "maximum": maximum,
                "n": sample_size,
            }
            for ordinal, label, minimum, maximum, sample_size, _method, _limit
            in definitions
        ],
        "interpretation_limit": (
            "Bands describe follower_count declared on each post; "
            "they are not stable creator-size tiers."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
