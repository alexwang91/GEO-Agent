import unittest

from geo_agent.industry_templates import b2b_saas_template, ecommerce_template, local_service_template


class IndustryTemplatesTests(unittest.TestCase):
    def test_b2b_saas_template_has_expected_dimensions(self):
        template = b2b_saas_template()
        self.assertEqual("industry:b2b_saas", template.template_id)
        self.assertIn("integration use cases", template.query_clusters)
        self.assertIn("review", template.source_priorities)
        self.assertIn("claim_fidelity_gap", template.diagnosis_emphasis)
        self.assertEqual("B2B SaaS", template.to_dict()["name"])

    def test_ecommerce_template_has_expected_dimensions(self):
        template = ecommerce_template()
        self.assertEqual("industry:ecommerce", template.template_id)
        self.assertIn("product comparison", template.query_clusters)
        self.assertIn("marketplace", template.source_priorities)
        self.assertIn("missing_owned_content", template.diagnosis_emphasis)
        self.assertEqual("Ecommerce", template.to_dict()["name"])

    def test_local_service_template_has_expected_dimensions(self):
        template = local_service_template()
        self.assertEqual("industry:local_service", template.template_id)
        self.assertIn("near me intent", template.query_clusters)
        self.assertIn("directory", template.source_priorities)
        self.assertIn("weak_citation_absorption", template.diagnosis_emphasis)
        self.assertEqual("Local Service", template.to_dict()["name"])


if __name__ == "__main__":
    unittest.main()
