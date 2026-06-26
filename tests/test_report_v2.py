import unittest

from geo_agent.report_v2 import build_report_v2


class ReportV2Tests(unittest.TestCase):
    def test_build_report_has_required_sections_and_guardrails(self):
        report = build_report_v2({"visibility": 0.5}, ({"dx": "1"},), ({"task": "1"},), ({"retest": "1"},))
        payload = report.to_dict()
        self.assertEqual("AI Visibility Audit Report", payload["title"])
        self.assertEqual(["Metric Summary", "Diagnoses", "Optimization Tasks", "Retest Plan"], [section["title"] for section in payload["sections"]])
        self.assertIn("Low-sample results are directional.", payload["guardrails"])


if __name__ == "__main__":
    unittest.main()
