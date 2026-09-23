#!/usr/bin/env python3
"""Validate audience labels without treating them as numeric distributions."""

from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter
from pathlib import Path


ALLOWED_AGES = {"13-18", "19-25", "26-35", "36-50", "50+"}
ALLOWED_GENDERS = {"female", "male", "non-binary", "unknown"}
ALLOWED_LOCATIONS = {
    "Brazil",
    "China",
    "Germany",
    "India",
    "Japan",
    "Russia",
    "UK",
    "USA",
}


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")

    age_counts: Counter[str] = Counter()
    gender_counts: Counter[str] = Counter()
    location_counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    platform_age: Counter[tuple[str, str]] = Counter()
    platform_gender: Counter[tuple[str, str]] = Counter()
    platform_location: Counter[tuple[str, str]] = Counter()
    rows = []
    valid_rows = 0

    source_sql = """
        SELECT source_row_number, id, content_id, platform,
               audience_age_distribution,
               audience_gender_distribution,
               audience_location
        FROM bronze_posts_raw
        ORDER BY source_row_number
    """
    for source_row_number, row_id, content_id, platform, age, gender, location in (
        connection.execute(source_sql)
    ):
        flags = []
        if age not in ALLOWED_AGES:
            flags.append("unexpected_audience_age")
        if gender not in ALLOWED_GENDERS:
            flags.append("unexpected_audience_gender")
        if location not in ALLOWED_LOCATIONS:
            flags.append("unexpected_audience_location")
        for flag in flags:
            flag_counts[flag] += 1

        valid = int(not flags)
        valid_rows += valid
        age_counts[age] += 1
        gender_counts[gender] += 1
        location_counts[location] += 1
        platform_age[(platform, age)] += 1
        platform_gender[(platform, gender)] += 1
        platform_location[(platform, location)] += 1
        rows.append(
            (
                source_row_number,
                row_id,
                content_id,
                age,
                gender,
                location,
                "single_label_per_post",
                valid,
                ";".join(flags),
            )
        )

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_audience")
        connection.execute(
            """
            CREATE TABLE silver_posts_audience (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                audience_age_label TEXT NOT NULL,
                audience_gender_label TEXT NOT NULL,
                audience_location_label TEXT NOT NULL,
                source_granularity TEXT NOT NULL
                    CHECK (source_granularity = 'single_label_per_post'),
                audience_valid INTEGER NOT NULL CHECK (audience_valid IN (0, 1)),
                quality_flags TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO silver_posts_audience (
                source_row_number, id, content_id, audience_age_label,
                audience_gender_label, audience_location_label,
                source_granularity, audience_valid, quality_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        bronze_rows = connection.execute(
            "SELECT COUNT(*) FROM bronze_posts_raw"
        ).fetchone()[0]
        stored_rows = connection.execute(
            "SELECT COUNT(*) FROM silver_posts_audience"
        ).fetchone()[0]
        if bronze_rows != stored_rows or stored_rows != len(rows):
            raise RuntimeError(
                f"Audience row parity failed: bronze={bronze_rows}, "
                f"stored={stored_rows}, prepared={len(rows)}"
            )
        connection.execute(
            "CREATE INDEX silver_posts_audience_slice_idx ON "
            "silver_posts_audience(audience_age_label, "
            "audience_gender_label, audience_location_label)"
        )
        connection.execute(
            "CREATE INDEX silver_posts_audience_content_id_idx ON "
            "silver_posts_audience(content_id)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    def platform_range(counter: Counter[tuple[str, str]], labels: set[str]) -> dict[str, object]:
        totals: Counter[str] = Counter()
        for (platform, _label), count in counter.items():
            totals[platform] += count
        percentages = []
        for (platform, label), count in counter.items():
            if label in labels:
                percentages.append(100.0 * count / totals[platform])
        return {
            "min_cell_pct": min(percentages) if percentages else None,
            "max_cell_pct": max(percentages) if percentages else None,
        }

    return {
        "database": str(database_path),
        "rows": len(rows),
        "valid_rows": valid_rows,
        "invalid_rows": len(rows) - valid_rows,
        "quality_flag_counts": dict(sorted(flag_counts.items())),
        "source_semantics": {
            "age": "single categorical label per post, not a distribution",
            "gender": "single categorical label per post, not a distribution",
            "location": "single country label per post, not a distribution",
        },
        "age_counts": dict(sorted(age_counts.items())),
        "gender_counts": dict(sorted(gender_counts.items())),
        "location_counts": dict(sorted(location_counts.items())),
        "platform_cell_percentage_ranges": {
            "age": platform_range(platform_age, ALLOWED_AGES),
            "gender": platform_range(platform_gender, ALLOWED_GENDERS),
            "location": platform_range(platform_location, ALLOWED_LOCATIONS),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
