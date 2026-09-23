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

    def test_reject_missing_sections(self):
        for key in ("overall", "source", "metric", "performance", "coverage", "availability"):
            invalid = copy.deepcopy(self.data)
            del invalid[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_source(invalid)

    def test_reject_historical_fields_and_nonfinite_metrics(self):
        for field in ("creator_profile_eligible", "action_candidate", "measure_better"):
            invalid = copy.deepcopy(self.data)
            invalid["creators"][field] = True
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_source(invalid)
        for number in (float("nan"), float("inf"), float("-inf")):
            invalid = copy.deepcopy(self.data)
            invalid["overall"]["views"]["median"] = number
            with self.subTest(number=number), self.assertRaises(ValueError):
                validate_source(invalid)

    def test_reject_coverage_order_and_injected_id(self):
        invalid = copy.deepcopy(self.data)
        invalid["coverage"].reverse()
        with self.assertRaisesRegex(ValueError, "order"):
            validate_source(invalid)
        invalid = copy.deepcopy(self.data)
        invalid["coverage"][0]["id"] = "injected"
        with self.assertRaisesRegex(ValueError, "coverage fields"):
            validate_source(invalid)

    def test_reject_bad_summary_and_segment_counts(self):
        invalid = copy.deepcopy(self.data)
        invalid["overall"]["views"]["p25"] = 999999
        with self.assertRaisesRegex(ValueError, "quantile"):
            validate_source(invalid)
        invalid = copy.deepcopy(self.data)
        invalid["performance"]["profiles"]["platform"][0]["interaction_per_view_pct"]["n"] += 1
        with self.assertRaisesRegex(ValueError, "reconcile"):
            validate_source(invalid)

    def test_snapshot_changes_with_content_but_ids_are_stable(self):
        before = build_contract(self.data)
        altered = copy.deepcopy(self.data)
        altered["coverage"][0]["basis"] += " Revisão."
        after = build_contract(altered)
        self.assertNotEqual(before["snapshot_id"], after["snapshot_id"])
        self.assertEqual(before["recommendations"][0]["id"], after["recommendations"][0]["id"])

    def test_protect_source_manifest_and_symlink(self):
        with self.assertRaisesRegex(ValueError, "protected"):
            export(SOURCE, DATABASE, SOURCE.parent)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "dashboard.json").symlink_to(SOURCE)
            with self.assertRaisesRegex(ValueError, "protected"):
                export(SOURCE, DATABASE, target)


if __name__ == "__main__":
    unittest.main()
