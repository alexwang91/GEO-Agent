import unittest

from geo_agent import EntityProfile, EntityProfileValidationError, validate_entity_profile


VALID_PROFILE = {
    "brand": "Acme AI",
    "aliases": ["Acme", "Acme Intelligence"],
    "domain": "https://www.acme.ai",
    "competitors": ["Globex AI", "Initech Search"],
    "target_regions": ["US", "GB"],
    "target_languages": ["en"],
    "target_customer": "B2B marketing teams",
    "main_product": "AI search visibility platform",
    "category": "Generative Engine Optimization",
    "business_goal": "Increase qualified demo requests from AI-search referrals",
}


class EntityProfileTests(unittest.TestCase):
    def test_valid_profile_normalizes_domain_and_lists(self):
        profile = validate_entity_profile(VALID_PROFILE)

        self.assertIsInstance(profile, EntityProfile)
        self.assertEqual(profile.brand, "Acme AI")
        self.assertEqual(profile.domain, "acme.ai")
        self.assertEqual(profile.aliases, ("Acme", "Acme Intelligence"))
        self.assertEqual(profile.competitors, ("Globex AI", "Initech Search"))
        self.assertEqual(profile.to_dict()["target_regions"], ["US", "GB"])

    def test_missing_required_fields_return_actionable_errors(self):
        incomplete = {"brand": "Acme AI"}

        with self.assertRaises(EntityProfileValidationError) as raised:
            validate_entity_profile(incomplete)

        issues = raised.exception.to_dict()["issues"]
        fields = {issue["field"] for issue in issues}
        self.assertIn("domain", fields)
        self.assertIn("competitors", fields)
        self.assertIn("business_goal", fields)
        self.assertTrue(all(issue["remediation"] for issue in issues))

    def test_invalid_field_types_are_reported_by_field(self):
        invalid = dict(VALID_PROFILE)
        invalid.update(
            {
                "aliases": "Acme",
                "domain": "not a domain",
                "competitors": [],
                "target_languages": ["en", ""],
                "business_goal": " ",
            }
        )

        with self.assertRaises(EntityProfileValidationError) as raised:
            EntityProfile.from_mapping(invalid)

        issues = raised.exception.to_dict()["issues"]
        by_field = {issue["field"]: issue for issue in issues}
        self.assertEqual(by_field["aliases"]["expected"], "list[str]")
        self.assertEqual(by_field["competitors"]["expected"], "non-empty list[str]")
        self.assertEqual(by_field["target_languages[1]"]["expected"], "non-empty string")
        self.assertEqual(by_field["business_goal"]["expected"], "non-empty string")
        self.assertIn("valid host", by_field["domain"]["message"])

    def test_profile_payload_must_be_mapping(self):
        with self.assertRaises(EntityProfileValidationError) as raised:
            validate_entity_profile(["not", "a", "mapping"])

        self.assertEqual(raised.exception.issues[0].field, "profile")
        self.assertIn("dictionary-like", raised.exception.issues[0].remediation)


if __name__ == "__main__":
    unittest.main()
