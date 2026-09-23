#!/usr/bin/env python3
"""Audit creator identity repetition without inventing canonical profiles."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path


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


def distribution(values: list[int]) -> dict[str, int]:
    return {
        str(value): count for value, count in sorted(Counter(values).items())
    }


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")

    creators: defaultdict[str, dict[str, object]] = defaultdict(
        lambda: {
            "posts": 0,
            "names": set(),
            "platforms": set(),
            "follower_counts": set(),
            "missing_names": 0,
            "invalid_follower_rows": 0,
        }
    )
    name_to_creator_ids: defaultdict[str, set[str]] = defaultdict(set)
    empty_creator_id_rows = 0

    source_sql = """
        SELECT
            b.creator_id,
            b.creator_name,
            b.platform,
            m.follower_count,
            m.metrics_valid
        FROM bronze_posts_raw AS b
        JOIN silver_posts_metrics AS m
          ON m.source_row_number = b.source_row_number
        ORDER BY b.source_row_number
    """
    for creator_id, creator_name, platform, follower_count, metrics_valid in (
        connection.execute(source_sql)
    ):
        if not creator_id.strip():
            empty_creator_id_rows += 1
            continue
        profile = creators[creator_id]
        profile["posts"] += 1
        profile["platforms"].add(platform)
        if creator_name.strip():
            profile["names"].add(creator_name)
            name_to_creator_ids[creator_name].add(creator_id)
        else:
            profile["missing_names"] += 1
        if metrics_valid and follower_count is not None:
            profile["follower_counts"].add(follower_count)
        else:
            profile["invalid_follower_rows"] += 1

    posts_per_creator = []
    names_per_creator = []
    platforms_per_creator = []
    followers_per_creator = []
    follower_spreads = []
    identity_consistent_creators = 0
    profile_eligible_creators = 0
    flag_counts: Counter[str] = Counter()

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_creator_profiles")
        connection.execute(
            """
            CREATE TABLE silver_creator_profiles (
                creator_id TEXT PRIMARY KEY,
                posts INTEGER NOT NULL CHECK (posts > 0),
                distinct_creator_names INTEGER NOT NULL,
                distinct_platforms INTEGER NOT NULL,
                distinct_follower_counts INTEGER NOT NULL,
                min_follower_count INTEGER,
                max_follower_count INTEGER,
                follower_count_spread INTEGER,
                canonical_creator_name TEXT,
                identity_consistent INTEGER NOT NULL
                    CHECK (identity_consistent IN (0, 1)),
                creator_profile_eligible INTEGER NOT NULL
                    CHECK (creator_profile_eligible IN (0, 1)),
                audit_flags TEXT NOT NULL
            )
            """
        )
        insert_sql = """
            INSERT INTO silver_creator_profiles (
                creator_id, posts, distinct_creator_names, distinct_platforms,
                distinct_follower_counts, min_follower_count,
                max_follower_count, follower_count_spread,
                canonical_creator_name, identity_consistent,
                creator_profile_eligible, audit_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        rows = []
        for creator_id, profile in sorted(creators.items()):
            names = profile["names"]
            platforms = profile["platforms"]
            follower_counts = profile["follower_counts"]
            posts = profile["posts"]
            flags = []

            if profile["missing_names"]:
                flags.append("missing_creator_name")
            if len(names) != 1:
                flags.append("multiple_creator_names")
            if profile["invalid_follower_rows"]:
                flags.append("invalid_follower_rows")
            if len(follower_counts) > 1:
                flags.append("follower_count_varies")

            for flag in flags:
                flag_counts[flag] += 1

            identity_consistent = int(
                profile["missing_names"] == 0 and len(names) == 1
            )
            profile_eligible = int(
                identity_consistent == 1
                and profile["invalid_follower_rows"] == 0
                and len(follower_counts) >= 1
            )
            identity_consistent_creators += identity_consistent
            profile_eligible_creators += profile_eligible

            canonical_name = next(iter(names)) if identity_consistent else None
            minimum = min(follower_counts) if follower_counts else None
            maximum = max(follower_counts) if follower_counts else None
            spread = maximum - minimum if minimum is not None else None

            posts_per_creator.append(posts)
            names_per_creator.append(len(names))
            platforms_per_creator.append(len(platforms))
            followers_per_creator.append(len(follower_counts))
            if spread is not None:
                follower_spreads.append(spread)

            rows.append(
                (
                    creator_id,
                    posts,
                    len(names),
                    len(platforms),
                    len(follower_counts),
                    minimum,
                    maximum,
                    spread,
                    canonical_name,
                    identity_consistent,
                    profile_eligible,
                    ";".join(flags),
                )
            )

        connection.executemany(insert_sql, rows)
        stored_creators = connection.execute(
            "SELECT COUNT(*) FROM silver_creator_profiles"
        ).fetchone()[0]
        if stored_creators != len(creators):
            raise RuntimeError(
                f"Creator parity failed: expected={len(creators)}, "
                f"stored={stored_creators}"
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    ambiguous_names = {
        name: creator_ids
        for name, creator_ids in name_to_creator_ids.items()
        if len(creator_ids) > 1
    }
    follower_spreads.sort()
    return {
        "database": str(database_path),
        "source_rows": sum(posts_per_creator),
        "empty_creator_id_rows": empty_creator_id_rows,
        "creator_ids": len(creators),
        "identity_consistent_creators": identity_consistent_creators,
        "creator_profile_eligible": profile_eligible_creators,
        "audit_flag_counts": dict(sorted(flag_counts.items())),
        "posts_per_creator": distribution(posts_per_creator),
        "distinct_names_per_creator": distribution(names_per_creator),
        "distinct_platforms_per_creator": distribution(platforms_per_creator),
        "distinct_follower_counts_per_creator": distribution(
            followers_per_creator
        ),
        "follower_count_spread": {
            "min": follower_spreads[0] if follower_spreads else None,
            "median": quantile(follower_spreads, 0.50),
            "p99": quantile(follower_spreads, 0.99),
            "max": follower_spreads[-1] if follower_spreads else None,
        },
        "creator_name_reuse": {
            "distinct_names": len(name_to_creator_ids),
            "names_mapped_to_multiple_creator_ids": len(ambiguous_names),
            "max_creator_ids_per_name": max(
                (len(ids) for ids in name_to_creator_ids.values()), default=0
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
