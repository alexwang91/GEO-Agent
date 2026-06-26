import unittest

from geo_agent.report_v2 import build_report_v2
from geo_agent.report_v2_checks import assert_report_v2_output, validate_report_v2_output


class ReportV2ChecksTests(unittest.TestCase):
    def test_valid_report_has_no_issues(self):
        report = build_report_v2({"visibility": 1}, ({"dx": 1},), ({"task": 1},), ({"retest": 1},)).to_dict()
        self.assertEqual((), validate_report_v2_output(report))
        assert_report_v2_output(report)

    def test_invalid_report_reports_missing_and_empty_parts(self):
        issues = validate_report_v2_output({"sections": [{"title": "Metric Summary", "items": []}], "guardrails": []})
        self.assertIn("missing_title", issues)
        self.assertIn("empty_section:Metric Summary", issues)
        with self.assertRaises(ValueError):
            assert_report_v2_output({})


if __name__ == "__main__":
    unittest.main()
