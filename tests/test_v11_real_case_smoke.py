import unittest
from pathlib import Path

from geo_agent.real_case_smoke import validate_real_case_smoke_fixture, validate_real_case_smoke_payload

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "smoke" / "template.json"
REPORT = ROOT / "docs" / "v11-real-case-smoke-report.md"


class V11RealCaseSmokeTests(unittest.TestCase):
    def test_smoke_fixture_contract_passes(self):
        result = validate_real_case_smoke_fixture(FIXTURE).to_dict()

        self.assertTrue(result["ready"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["capture_count"], 1)

    def test_manual_only_engine_requires_manual_import(self):
        payload = {
            "fixture_kind": "geo-agent real-case smoke",
            "fixture_status": "sanitized_manual_capture",
            "source_policy": "no_fabricated_engine_answers",
            "brand": {"name": "GEO-Agent"},
            "query_cluster": "geo measurement workbench",
            "captures": [
                {
                    "engine": "google_aio",
                    "collection_method": "automated",
                    "captured_at": "2026-06-29T00:00:00Z",
                    "query": "example query",
                    "answer_excerpt": "Sanitized excerpt with enough words for validation.",
                    "citation_count": 1,
                    "evidence_ids": ["evidence-smoke-001"],
                }
            ],
            "trust_check": {"status": "reviewed", "extraction_precision": 1.0, "extraction_recall": 1.0},
            "retest_plan": {"query_cluster": "geo measurement workbench", "noise_floor_note": "directional"},
            "limitations": ["single sample"],
        }

        result = validate_real_case_smoke_payload(payload).to_dict()

        self.assertFalse(result["ready"])
        self.assertIn("capture 0 manual-only engine must use manual_import", result["errors"])

    def test_report_keeps_template_boundary(self):
        report = REPORT.read_text(encoding="utf-8")

        self.assertIn("Status: template only", report)
        self.assertIn("Pending actual sanitized capture", report)
        self.assertIn("Single-sample results remain directional", report)


if __name__ == "__main__":
    unittest.main()
