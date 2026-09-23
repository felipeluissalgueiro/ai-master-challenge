"""Unit and real-snapshot contract checks (standard library only)."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from solution.analysis.export_app import build_contract, digest, export, validate_source

SOLUTION = Path(__file__).resolve().parents[1]
SOURCE = SOLUTION / "reports/evidence.json"
DATABASE = SOLUTION / "data/evidence/social_media_analysis.sqlite"


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_references_and_missing_commercial_values(self):
        result = build_contract(self.data)
        ids = {entry["id"] for entry in result["evidence"]}
        self.assertEqual(len(result["recommendations"]), 8)
        for recommendation in result["recommendations"]:
            self.assertTrue(set(recommendation["evidence_ids"]) <= ids)
        self.assertIsNone(result["commercial"]["cost_per_sale"])
        self.assertEqual(result["evidence"][0]["data"], self.data["overall"])

    def test_reject_bad_schema_and_units(self):
        for key, value in (("schema_version", 99), ("metric", {"unit": "percentage_points"})):
            invalid = copy.deepcopy(self.data)
            invalid[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_source(invalid)

    def test_real_snapshot_is_deterministic_and_unchanged(self):
        before = digest(DATABASE)
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "a", Path(directory) / "b"
            export(SOURCE, DATABASE, first)
            export(SOURCE, DATABASE, second)
            for name in ("dashboard.json", "manifest.json"):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
        self.assertEqual(digest(DATABASE), before)

    def test_reject_wrong_hash_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "output"
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                export(SOLUTION / "reports/README.md", DATABASE, target)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
