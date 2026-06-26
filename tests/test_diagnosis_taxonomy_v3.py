import unittest

from geo_agent.diagnosis_taxonomy_v3 import create_diagnosis_v3, severity_rank


class DiagnosisTaxonomyV3Tests(unittest.TestCase):
    def test_creates_diagnosis_with_default_action(self):
        item = create_diagnosis_v3("dx:1", "weak_citation_absorption", "high", ("metric:1",), "Weak source mix.")
        self.assertEqual("weak_citation_absorption", item.diagnosis_type)
        self.assertEqual("high", item.severity)
        self.assertIn("citation-quality", item.recommended_action)
        self.assertEqual(["metric:1"], item.to_dict()["evidence_ids"])

    def test_custom_action_and_severity_rank(self):
        item = create_diagnosis_v3("dx:2", "provider_unavailable", "critical", ("provider:1",), "Provider failed.", "Reconnect provider.")
        self.assertEqual("Reconnect provider.", item.recommended_action)
        self.assertGreater(severity_rank("critical"), severity_rank("medium"))

    def test_rejects_missing_required_fields(self):
        with self.assertRaises(ValueError):
            create_diagnosis_v3("", "low_query_coverage", "low", ("evidence:1",), "x")
        with self.assertRaises(ValueError):
            create_diagnosis_v3("dx:3", "low_query_coverage", "low", (), "x")


if __name__ == "__main__":
    unittest.main()
