import unittest
from pathlib import Path

from geo_agent.provider_status_copy import provider_report_status_line, provider_status_copy

ROOT = Path(__file__).resolve().parents[1]


class ProviderStatusCopyTests(unittest.TestCase):
    def test_all_user_facing_statuses_have_distinct_copy(self):
        statuses = ["implemented", "manual", "manual_only", "simulated", "planned", "unavailable"]
        labels = [provider_status_copy(status).label for status in statuses]
        self.assertEqual(len(statuses), len(set(labels)))
        for status in statuses:
            copy = provider_status_copy(status)
            self.assertTrue(copy.summary)
            self.assertTrue(copy.report_note)
            self.assertTrue(copy.action_label)

    def test_planned_and_simulated_do_not_claim_execution(self):
        for status in ["planned", "simulated", "unavailable"]:
            copy = provider_status_copy(status)
            self.assertFalse(copy.can_execute)
        self.assertTrue(provider_status_copy("implemented").can_execute)
        self.assertTrue(provider_status_copy("manual").can_execute)
        self.assertTrue(provider_status_copy("manual_only").can_execute)

    def test_manual_only_status_explicitly_blocks_automated_claims(self):
        copy = provider_status_copy("manual_only")
        self.assertEqual(copy.label, "Manual only")
        self.assertIn("explicit manual capture", copy.summary)
        self.assertIn("no automated provider run", copy.report_note)

    def test_manual_only_docs_name_google_aio(self):
        provider_doc = (ROOT / "docs" / "provider-status-language.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("google_aio", provider_doc)
        self.assertIn("manual_only", provider_doc)
        self.assertIn("Google AIO", readme)
        self.assertIn("Manual only", readme)

    def test_report_line_preserves_provider_boundary(self):
        line = provider_report_status_line("Perplexity", "planned")
        self.assertIn("Perplexity", line)
        self.assertIn("Planned provider", line)
        self.assertIn("no evidence", line)


if __name__ == "__main__":
    unittest.main()
