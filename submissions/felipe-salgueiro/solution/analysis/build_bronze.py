#!/usr/bin/env python3
"""Build a lossless Bronze SQLite copy of the supplied CSV using stdlib only."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sqlite3
from pathlib import Path


EXPECTED_COLUMNS = (
    "id",
    "platform",
    "content_id",
    "creator_id",
    "creator_name",
    "content_url",
    "content_type",
    "content_category",
    "post_date",
    "language",
    "content_length",
    "content_description",
    "hashtags",
    "views",
    "likes",
    "shares",
    "comments_count",
    "comments_text",
    "follower_count",
    "is_sponsored",
    "disclosure_type",
    "sponsor_name",
    "sponsor_category",
    "disclosure_location",
    "audience_age_distribution",
    "audience_gender_distribution",
    "audience_location",
)

SOURCE_URL = (
    "https://www.kaggle.com/datasets/omenkj/"
    "social-media-sponsorship-and-engagement-dataset/data"
)
METADATA_URL = (
    "https://www.kaggle.com/api/v1/datasets/view/omenkj/"
    "social-media-sponsorship-and-engagement-dataset"
)
EXPECTED_ZIP_SHA256 = (
    "ce78ea3352fe1ae6093e6f5d48b506ad591c6e6ca90fbab6ac91866a8c34202e"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quoted(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def build(csv_path: Path, zip_path: Path, output_path: Path) -> dict[str, object]:
    csv_hash = sha256(csv_path)
    zip_hash = sha256(zip_path)
    if zip_hash != EXPECTED_ZIP_SHA256:
        raise ValueError(
            f"ZIP SHA256 mismatch: expected {EXPECTED_ZIP_SHA256}, got {zip_hash}"
        )

    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    if temporary_path.exists():
        temporary_path.unlink()

    connection = sqlite3.connect(temporary_path)
    row_count = 0
    try:
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute(
            "CREATE TABLE bronze_manifest (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        raw_columns = ",\n".join(
            f"    {quoted(column)} TEXT NOT NULL" for column in EXPECTED_COLUMNS
        )
        connection.execute(
            "CREATE TABLE bronze_posts_raw (\n"
            "    source_row_number INTEGER PRIMARY KEY,\n"
            f"{raw_columns}\n"
            ")"
        )
        connection.execute(
            "CREATE TABLE bronze_columns ("
            "ordinal INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, "
            "sqlite_type TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT INTO bronze_columns (ordinal, name, sqlite_type) VALUES (?, ?, ?)",
            ((index, column, "TEXT") for index, column in enumerate(EXPECTED_COLUMNS, 1)),
        )

        csv.field_size_limit(16 * 1024 * 1024)
        placeholders = ",".join("?" for _ in range(len(EXPECTED_COLUMNS) + 1))
        insert_sql = "INSERT INTO bronze_posts_raw VALUES (" + placeholders + ")"
        batch: list[tuple[object, ...]] = []
        with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            header = tuple(next(reader))
            if header != EXPECTED_COLUMNS:
                raise ValueError(
                    "Unexpected CSV header:\n"
                    f"expected={EXPECTED_COLUMNS}\nactual={header}"
                )
            for source_row_number, row in enumerate(reader, start=2):
                if len(row) != len(EXPECTED_COLUMNS):
                    raise ValueError(
                        f"Row {source_row_number} has {len(row)} fields; "
                        f"expected {len(EXPECTED_COLUMNS)}"
                    )
                batch.append((source_row_number, *row))
                if len(batch) == 1000:
                    connection.executemany(insert_sql, batch)
                    row_count += len(batch)
                    batch.clear()
            if batch:
                connection.executemany(insert_sql, batch)
                row_count += len(batch)

        manifest = {
            "dataset_name": "Social Media Sponsorship and Engagement Dataset",
            "source_url": SOURCE_URL,
            "metadata_url": METADATA_URL,
            "license": "MIT",
            "source_nature": "simulated_dataset_as_declared_by_publisher",
            "csv_filename": csv_path.name,
            "csv_sha256": csv_hash,
            "zip_filename": zip_path.name,
            "zip_sha256": zip_hash,
            "row_count": str(row_count),
            "source_column_count": str(len(EXPECTED_COLUMNS)),
            "empty_string_policy": "preserved_as_empty_string",
            "type_policy": "all_source_columns_preserved_as_text",
        }
        connection.executemany(
            "INSERT INTO bronze_manifest (key, value) VALUES (?, ?)", manifest.items()
        )
        connection.commit()

        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        stored_rows = connection.execute(
            "SELECT COUNT(*) FROM bronze_posts_raw"
        ).fetchone()[0]
        if integrity != "ok" or stored_rows != row_count:
            raise RuntimeError(
                f"Bronze validation failed: integrity={integrity}, "
                f"stored_rows={stored_rows}, source_rows={row_count}"
            )
    except Exception:
        connection.close()
        temporary_path.unlink(missing_ok=True)
        raise
    else:
        connection.close()

    os.replace(temporary_path, output_path)
    return {
        "output": str(output_path),
        "rows": row_count,
        "source_columns": len(EXPECTED_COLUMNS),
        "csv_sha256": csv_hash,
        "zip_sha256": zip_hash,
        "integrity_check": "ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(args.csv, args.zip, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
