#!/usr/bin/env python3
"""Audit source structure and derive observable content features only."""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


INTEGER = re.compile(r"^(0|[1-9][0-9]*)$")
TOKEN = re.compile(r"^[A-Za-z0-9_'-]+$")
SENTENCE_MARK = re.compile(r"[.!?]+")


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


def numeric_profile(values: list[int]) -> dict[str, float | int | None]:
    values.sort()
    return {
        "min": values[0] if values else None,
        "p01": quantile(values, 0.01),
        "median": quantile(values, 0.50),
        "p99": quantile(values, 0.99),
        "max": values[-1] if values else None,
    }


def build(database_path: Path) -> dict[str, object]:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys=ON")
    columns = [
        row[1]
        for row in connection.execute("PRAGMA table_info(bronze_posts_raw)")
        if row[1] != "source_row_number"
    ]
    select_sql = (
        "SELECT source_row_number, " + ", ".join(columns) + " "
        "FROM bronze_posts_raw ORDER BY source_row_number"
    )

    empty_counts: Counter[str] = Counter()
    ids = set()
    content_ids = set()
    full_rows = set()
    duplicate_ids = 0
    duplicate_content_ids = 0
    duplicate_full_rows = 0
    value_sets = {
        "content_description": set(),
        "comments_text": set(),
        "hashtags": set(),
        "content_url": set(),
    }
    length_by_type: defaultdict[str, list[int]] = defaultdict(list)
    language_rows: Counter[str] = Counter()
    language_non_ascii_description: Counter[str] = Counter()
    language_non_ascii_comments: Counter[str] = Counter()
    hashtag_counts: list[int] = []
    description_chars: list[int] = []
    description_words: list[int] = []
    comments_chars: list[int] = []
    comments_words: list[int] = []
    comments_sentence_marks: list[int] = []
    url_schemes: Counter[str] = Counter()
    url_hosts = set()
    flag_counts: Counter[str] = Counter()
    rows = []
    valid_rows = 0

    for database_row in connection.execute(select_sql):
        source_row_number = database_row[0]
        values = dict(zip(columns, database_row[1:], strict=True))
        raw_tuple = tuple(database_row[1:])
        if raw_tuple in full_rows:
            duplicate_full_rows += 1
        else:
            full_rows.add(raw_tuple)

        row_id = values["id"]
        content_id = values["content_id"]
        if row_id in ids:
            duplicate_ids += 1
        ids.add(row_id)
        if content_id in content_ids:
            duplicate_content_ids += 1
        content_ids.add(content_id)

        for column, value in values.items():
            if value == "":
                empty_counts[column] += 1

        flags = []
        raw_length = values["content_length"]
        content_length = int(raw_length) if INTEGER.fullmatch(raw_length) else None
        if content_length is None:
            flags.append("invalid_content_length")
        else:
            length_by_type[values["content_type"]].append(content_length)

        description = values["content_description"]
        description_char_count = len(description)
        description_word_count = len(description.split())
        description_non_ascii = int(any(ord(char) > 127 for char in description))
        description_chars.append(description_char_count)
        description_words.append(description_word_count)

        hashtags_raw = values["hashtags"]
        hashtag_tokens = [] if hashtags_raw == "" else hashtags_raw.split(",")
        hashtag_count = len(hashtag_tokens)
        hashtag_counts.append(hashtag_count)
        if any(token == "" or token.strip() != token or not TOKEN.fullmatch(token) for token in hashtag_tokens):
            flags.append("invalid_hashtag_format")
        if any(token.startswith("#") for token in hashtag_tokens):
            flags.append("unexpected_hashtag_prefix")

        comments = values["comments_text"]
        comments_present = int(comments != "")
        comments_char_count = len(comments)
        comments_word_count = len(comments.split())
        comments_mark_count = len(SENTENCE_MARK.findall(comments))
        comments_non_ascii = int(any(ord(char) > 127 for char in comments))
        if comments_present:
            comments_chars.append(comments_char_count)
            comments_words.append(comments_word_count)
            comments_sentence_marks.append(comments_mark_count)

        parsed_url = urlparse(values["content_url"])
        url_valid = int(parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc))
        if not url_valid:
            flags.append("invalid_content_url")
        else:
            url_schemes[parsed_url.scheme] += 1
            url_hosts.add(parsed_url.netloc.lower())

        language = values["language"]
        language_rows[language] += 1
        language_non_ascii_description[language] += description_non_ascii
        language_non_ascii_comments[language] += comments_non_ascii
        for field in value_sets:
            if values[field] != "":
                value_sets[field].add(values[field])
        for flag in flags:
            flag_counts[flag] += 1
        content_valid = int(not flags)
        valid_rows += content_valid

        rows.append(
            (
                source_row_number,
                row_id,
                content_id,
                content_length,
                description_char_count,
                description_word_count,
                description_non_ascii,
                hashtag_count,
                comments_present,
                comments_char_count,
                comments_word_count,
                comments_mark_count,
                comments_non_ascii,
                url_valid,
                content_valid,
                ";".join(flags),
            )
        )

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS silver_posts_content")
        connection.execute(
            """
            CREATE TABLE silver_posts_content (
                source_row_number INTEGER PRIMARY KEY
                    REFERENCES bronze_posts_raw(source_row_number),
                id TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_length_value INTEGER,
                description_char_count INTEGER NOT NULL,
                description_word_count INTEGER NOT NULL,
                description_has_non_ascii INTEGER NOT NULL CHECK (description_has_non_ascii IN (0, 1)),
                hashtag_count INTEGER NOT NULL,
                comments_text_present INTEGER NOT NULL CHECK (comments_text_present IN (0, 1)),
                comments_char_count INTEGER NOT NULL,
                comments_word_count INTEGER NOT NULL,
                comments_sentence_mark_count INTEGER NOT NULL,
                comments_has_non_ascii INTEGER NOT NULL CHECK (comments_has_non_ascii IN (0, 1)),
                content_url_valid INTEGER NOT NULL CHECK (content_url_valid IN (0, 1)),
                content_structure_valid INTEGER NOT NULL CHECK (content_structure_valid IN (0, 1)),
                quality_flags TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            """
            INSERT INTO silver_posts_content (
                source_row_number, id, content_id, content_length_value,
                description_char_count, description_word_count,
                description_has_non_ascii, hashtag_count,
                comments_text_present, comments_char_count,
                comments_word_count, comments_sentence_mark_count,
                comments_has_non_ascii, content_url_valid,
                content_structure_valid, quality_flags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        bronze_rows = connection.execute(
            "SELECT COUNT(*) FROM bronze_posts_raw"
        ).fetchone()[0]
        stored_rows = connection.execute(
            "SELECT COUNT(*) FROM silver_posts_content"
        ).fetchone()[0]
        if bronze_rows != stored_rows or stored_rows != len(rows):
            raise RuntimeError(
                f"Content row parity failed: bronze={bronze_rows}, "
                f"stored={stored_rows}, prepared={len(rows)}"
            )
        connection.execute(
            "CREATE INDEX silver_posts_content_content_id_idx "
            "ON silver_posts_content(content_id)"
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "database": str(database_path),
        "rows": len(rows),
        "source_columns": len(columns),
        "valid_structure_rows": valid_rows,
        "invalid_structure_rows": len(rows) - valid_rows,
        "quality_flag_counts": dict(sorted(flag_counts.items())),
        "empty_string_counts": {
            column: empty_counts[column] for column in columns
        },
        "duplicates": {
            "duplicate_id_rows": duplicate_ids,
            "duplicate_content_id_rows": duplicate_content_ids,
            "duplicate_full_source_rows": duplicate_full_rows,
        },
        "unique_nonempty_values": {
            field: len(values) for field, values in value_sets.items()
        },
        "content_length_by_type": {
            content_type: {
                "distinct_values": len(set(values)),
                **numeric_profile(values),
            }
            for content_type, values in sorted(length_by_type.items())
        },
        "description_chars": numeric_profile(description_chars),
        "description_words": numeric_profile(description_words),
        "hashtag_count": numeric_profile(hashtag_counts),
        "comments_text_present": len(comments_chars),
        "comments_text_missing": len(rows) - len(comments_chars),
        "comments_chars_when_present": numeric_profile(comments_chars),
        "comments_words_when_present": numeric_profile(comments_words),
        "comments_sentence_marks_when_present": numeric_profile(
            comments_sentence_marks
        ),
        "language_rows": dict(sorted(language_rows.items())),
        "non_ascii_description_rows_by_declared_language": dict(
            sorted(language_non_ascii_description.items())
        ),
        "non_ascii_comment_rows_by_declared_language": dict(
            sorted(language_non_ascii_comments.items())
        ),
        "content_urls": {
            "schemes": dict(sorted(url_schemes.items())),
            "distinct_hosts": len(url_hosts),
        },
        "content_length_unit": "not declared in the CSV",
        "semantic_quality": "not inferred by this deterministic script",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.database), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
