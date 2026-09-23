#!/usr/bin/env python3
"""Build validated categorical dimensions and sponsorship consistency flags."""

from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path


ALLOWED_VALUES = {
    "platform": {"Bilibili", "Instagram", "RedNote", "TikTok", "YouTube"},
    "content_type": {"image", "mixed", "text", "video"},
    "content_category": {"beauty", "lifestyle", "tech"},
    "disclosure_type": {"explicit", "implicit", "none"},
    "sponsor_category": {
        "Not sponsors",
        "cosmetics",
        "electronics",
        "fashion",
        "food",
        "gaming",
        "travel",
    },
    "disclosure_location": {"caption", "hashtags", "none", "video"},
}


def sponsorship_value(raw: str) -> int | None:
    if raw == "TRUE":
        return 1
    if raw == "FALSE":
        return 0
    return None


def categorical_flags(values: dict[str, str], is_sponsored: int | None) -> list[str]:
    flags = []
    for field, allowed in ALLOWED_VALUES.items():
        if values[field] not in allowed:
            flags.append(f"unexpected_{field}")

    sponsor_name = values["sponsor_name"]
    if not sponsor_name.strip():
        flags.append("empty_sponsor_name")

    if is_sponsored is None:
        flags.append("invalid_is_sponsored")
    elif is_sponsored == 0:
        expected = {
            "disclosure_type": "none",
            "sponsor_name": "Not sponsors",
            "sponsor_category": "Not sponsors",
            "disclosure_location": "none",
        }
        for field, expected_value in expected.items():
            if values[field] != expected_value:
                flags.append(f"not_sponsored_unexpected_{field}")
    else:
        if values["disclosure_type"] not in {"explicit", "implicit"}:
            flags.append("sponsored_invalid_disclosure_type")
        if sponsor_name == "Not sponsors":
            flags.append("sponsored_missing_sponsor_name")
        if values["sponsor_category"] == "Not sponsors":
            flags.append("sponsored_missing_sponsor_category")
        if values["disclosure_location"] == "none":
            flags.append("sponsored_missing_disclosure_location")
    return flags


def nested_counts(counter: Counter[tuple[str, str]]) -> dict[str, dict[str, int]]:
    output: defaultdict[str, dict[str, int]] = defaultdict(dict)
    for (dimension, sponsorship), count in sorted(counter.items()):
        output[dimension][sponsorship] = count
    return dict(output)


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")

    fields = (
        "platform",
        "content_type",
        "content_category",
        "is_sponsored",
        "disclosure_type",
        "sponsor_name",
        "sponsor_category",
        "disclosure_location",
    )
    value_counts = {field: Counter() for field in fields if field != "sponsor_name"}
    cross_counts = {
        "platform": Counter(),
        "content_type": Counter(),
        "content_category": Counter(),
    }
    sponsor_names = {0: set(), 1: set()}
    flag_counts: Counter[str] = Counter()
    valid_rows = 0
    inserted = 0

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_dimensions")
        connection.execute(
            """
            CREATE TABLE silver_posts_dimensions (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                content_type TEXT NOT NULL,
                content_category TEXT NOT NULL,
                is_sponsored INTEGER CHECK (is_sponsored IN (0, 1)),
                sponsorship_label TEXT,
                disclosure_type TEXT NOT NULL,
                sponsor_name TEXT NOT NULL,
                sponsor_category TEXT NOT NULL,
                disclosure_location TEXT NOT NULL,
                dimensions_valid INTEGER NOT NULL CHECK (dimensions_valid IN (0, 1)),
                quality_flags TEXT NOT NULL
            )
            """
        )

        select_sql = (
            "SELECT source_row_number, id, content_id, "
            + ", ".join(fields)
            + " FROM bronze_posts_raw ORDER BY source_row_number"
        )
        insert_sql = """
            INSERT INTO silver_posts_dimensions (
                source_row_number, id, content_id, platform, content_type,
                content_category, is_sponsored, sponsorship_label,
                disclosure_type, sponsor_name, sponsor_category,
                disclosure_location, dimensions_valid, quality_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        batch: list[tuple[object, ...]] = []

        for row in connection.execute(select_sql):
            source_row_number, row_id, content_id, *raw_values = row
            values = dict(zip(fields, raw_values, strict=True))
            is_sponsored = sponsorship_value(values["is_sponsored"])
            flags = categorical_flags(values, is_sponsored)
            for flag in flags:
                flag_counts[flag] += 1

            dimensions_valid = int(not flags)
            valid_rows += dimensions_valid
            sponsorship_label = None
            if is_sponsored == 1:
                sponsorship_label = "sponsored_true"
            elif is_sponsored == 0:
                sponsorship_label = "not_sponsored_by_flag"

            for field, counter in value_counts.items():
                counter[values[field]] += 1
            if is_sponsored is not None:
                sponsor_names[is_sponsored].add(values["sponsor_name"])
                for field, counter in cross_counts.items():
                    counter[(values[field], sponsorship_label)] += 1

            batch.append(
                (
                    source_row_number,
                    row_id,
                    content_id,
                    values["platform"],
                    values["content_type"],
                    values["content_category"],
                    is_sponsored,
                    sponsorship_label,
                    values["disclosure_type"],
                    values["sponsor_name"],
                    values["sponsor_category"],
                    values["disclosure_location"],
                    dimensions_valid,
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
            "SELECT COUNT(*) FROM silver_posts_dimensions"
        ).fetchone()[0]
        if bronze_rows != silver_rows or inserted != bronze_rows:
            raise RuntimeError(
                f"Row parity failed: bronze={bronze_rows}, "
                f"silver={silver_rows}, inserted={inserted}"
            )

        connection.execute(
            "CREATE INDEX silver_posts_dimensions_slice_idx ON "
            "silver_posts_dimensions(platform, content_type, "
            "content_category, is_sponsored)"
        )
        connection.execute(
            "CREATE INDEX silver_posts_dimensions_content_id_idx ON "
            "silver_posts_dimensions(content_id)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "database": str(database_path),
        "rows": inserted,
        "valid_rows": valid_rows,
        "invalid_rows": inserted - valid_rows,
        "quality_flag_counts": dict(sorted(flag_counts.items())),
        "distinct_sponsor_names": {
            "not_sponsored_by_flag": len(sponsor_names[0]),
            "sponsored_true": len(sponsor_names[1]),
        },
        "value_counts": {
            field: dict(sorted(counter.items()))
            for field, counter in value_counts.items()
        },
        "sample_sizes_by_sponsorship": {
            field: nested_counts(counter) for field, counter in cross_counts.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
