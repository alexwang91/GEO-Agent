import unittest

from geo_agent.industry_templates import b2b_saas_template


class IndustryTemplatesTests(unittest.TestCase):
    def test_b2b_saas_template_has_expected_dimensions(self):
        template = b2b_saas_template()
        self.assertEqual("industry:b2b_saas", template.template_id)
        self.assertIn("integration use cases", template.query_clusters)
        self.assertIn("review", template.source_priorities)
        self.assertIn("claim_fidelity_gap", template.diagnosis_emphasis)
        self.assertEqual("B2B SaaS", template.to_dict()["name"])


if __name__ == "__main__":
    unittest.main()
