#!/usr/bin/env python3
"""Normalize source post dates while preserving their missing-timezone limitation."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path


SOURCE_FORMAT = "%m/%d/%y %I:%M %p"


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

    rows = []
    invalid_examples = []
    parsed_datetimes: list[datetime] = []
    exact_datetime_counts: Counter[str] = Counter()
    daily_counts: Counter[str] = Counter()
    monthly_counts: Counter[str] = Counter()
    yearly_counts: Counter[int] = Counter()
    weekday_counts: Counter[int] = Counter()
    hour_counts: Counter[int] = Counter()
    platform_ranges: dict[str, list[datetime]] = {}
    valid_rows = 0

    source_sql = """
        SELECT source_row_number, id, content_id, platform, post_date
        FROM bronze_posts_raw
        ORDER BY source_row_number
    """
    for source_row_number, row_id, content_id, platform, raw_date in (
        connection.execute(source_sql)
    ):
        flags = []
        parsed = None
        try:
            parsed = datetime.strptime(raw_date, SOURCE_FORMAT)
        except ValueError:
            flags.append("invalid_post_date")
            if len(invalid_examples) < 10:
                invalid_examples.append(
                    {"source_row_number": source_row_number, "value": raw_date}
                )

        if parsed is None:
            rows.append(
                (
                    source_row_number,
                    row_id,
                    content_id,
                    raw_date,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    0,
                    ";".join(flags),
                )
            )
            continue

        valid_rows += 1
        iso_datetime = parsed.strftime("%Y-%m-%d %H:%M:%S")
        iso_date = parsed.strftime("%Y-%m-%d")
        month = parsed.strftime("%Y-%m")
        parsed_datetimes.append(parsed)
        exact_datetime_counts[iso_datetime] += 1
        daily_counts[iso_date] += 1
        monthly_counts[month] += 1
        yearly_counts[parsed.year] += 1
        weekday_counts[parsed.isoweekday()] += 1
        hour_counts[parsed.hour] += 1
        if platform not in platform_ranges:
            platform_ranges[platform] = [parsed, parsed]
        else:
            platform_ranges[platform][0] = min(platform_ranges[platform][0], parsed)
            platform_ranges[platform][1] = max(platform_ranges[platform][1], parsed)

        rows.append(
            (
                source_row_number,
                row_id,
                content_id,
                raw_date,
                iso_datetime,
                iso_date,
                parsed.year,
                parsed.month,
                parsed.hour,
                parsed.isoweekday(),
                0,
                1,
                "",
            )
        )

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_dates")
        connection.execute(
            """
            CREATE TABLE silver_posts_dates (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                post_date_raw TEXT NOT NULL,
                post_datetime_iso TEXT,
                post_date_iso TEXT,
                post_year INTEGER,
                post_month INTEGER CHECK (post_month IS NULL OR post_month BETWEEN 1 AND 12),
                post_hour INTEGER CHECK (post_hour IS NULL OR post_hour BETWEEN 0 AND 23),
                post_weekday_iso INTEGER
                    CHECK (post_weekday_iso IS NULL OR post_weekday_iso BETWEEN 1 AND 7),
                timezone_known INTEGER NOT NULL CHECK (timezone_known IN (0, 1)),
                date_valid INTEGER NOT NULL CHECK (date_valid IN (0, 1)),
                quality_flags TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO silver_posts_dates (
                source_row_number, id, content_id, post_date_raw,
                post_datetime_iso, post_date_iso, post_year, post_month,
                post_hour, post_weekday_iso, timezone_known, date_valid,
                quality_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        bronze_rows = connection.execute(
            "SELECT COUNT(*) FROM bronze_posts_raw"
        ).fetchone()[0]
        stored_rows = connection.execute(
            "SELECT COUNT(*) FROM silver_posts_dates"
        ).fetchone()[0]
        if bronze_rows != stored_rows or stored_rows != len(rows):
            raise RuntimeError(
                f"Date row parity failed: bronze={bronze_rows}, "
                f"stored={stored_rows}, prepared={len(rows)}"
            )
        connection.execute(
            "CREATE INDEX silver_posts_dates_date_idx "
            "ON silver_posts_dates(post_date_iso, post_hour)"
        )
        connection.execute(
            "CREATE INDEX silver_posts_dates_content_id_idx "
            "ON silver_posts_dates(content_id)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    daily_values = sorted(daily_counts.values())
    parsed_datetimes.sort()
    start = parsed_datetimes[0] if parsed_datetimes else None
    end = parsed_datetimes[-1] if parsed_datetimes else None
    return {
        "database": str(database_path),
        "rows": len(rows),
        "valid_rows": valid_rows,
        "invalid_rows": len(rows) - valid_rows,
        "invalid_examples": invalid_examples,
        "timezone_known_rows": 0,
        "source_format": SOURCE_FORMAT,
        "period": {
            "first_datetime": start.strftime("%Y-%m-%d %H:%M:%S") if start else None,
            "last_datetime": end.strftime("%Y-%m-%d %H:%M:%S") if end else None,
            "inclusive_calendar_days": (end.date() - start.date()).days + 1
            if start and end
            else None,
            "dates_with_posts": len(daily_counts),
            "distinct_exact_datetimes": len(exact_datetime_counts),
            "max_posts_same_datetime": max(exact_datetime_counts.values(), default=0),
        },
        "posts_per_calendar_day": {
            "min": daily_values[0] if daily_values else None,
            "median": quantile(daily_values, 0.50),
            "p99": quantile(daily_values, 0.99),
            "max": daily_values[-1] if daily_values else None,
        },
        "year_counts": {str(key): value for key, value in sorted(yearly_counts.items())},
        "month_counts": dict(sorted(monthly_counts.items())),
        "weekday_iso_counts": {
            str(key): value for key, value in sorted(weekday_counts.items())
        },
        "hour_counts": {str(key): value for key, value in sorted(hour_counts.items())},
        "platform_periods": {
            platform: {
                "first_datetime": limits[0].strftime("%Y-%m-%d %H:%M:%S"),
                "last_datetime": limits[1].strftime("%Y-%m-%d %H:%M:%S"),
            }
            for platform, limits in sorted(platform_ranges.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
