import unittest

from geo_agent.provider_status_copy import provider_report_status_line, provider_status_copy


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

    def test_planned_simulated_and_unavailable_do_not_claim_execution(self):
        for status in ["planned", "simulated", "unavailable"]:
            copy = provider_status_copy(status)
            self.assertFalse(copy.can_execute)
        self.assertTrue(provider_status_copy("implemented").can_execute)
        self.assertTrue(provider_status_copy("manual").can_execute)
        self.assertTrue(provider_status_copy("manual_only").can_execute)

    def test_report_line_preserves_provider_boundary(self):
        line = provider_report_status_line("Perplexity", "planned")
        self.assertIn("Perplexity", line)
        self.assertIn("Planned provider", line)
        self.assertIn("no evidence", line)
        aio_line = provider_report_status_line("Google AIO", "manual_only")
        self.assertIn("Google AIO", aio_line)
        self.assertIn("Manual-only", aio_line)


if __name__ == "__main__":
    unittest.main()
