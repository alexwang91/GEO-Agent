import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.provider_access import manual_only_provider_matrix
from geo_agent.provider_status_copy import provider_status_copy
from geo_agent.repeated_sampling import summarize_brand_probability


class V10SamplingProviderMatrixTests(unittest.TestCase):
    def test_manual_only_provider_statuses_are_registered(self):
        statuses = {provider.provider_id: provider.implementation_status for provider in manual_only_provider_matrix()}
        methods = {provider.provider_id: provider.access_methods for provider in manual_only_provider_matrix()}

        for provider_id in ("google_aio", "deepseek", "kimi", "qianwen"):
            self.assertEqual(statuses[provider_id], "manual_only")
            self.assertEqual(methods[provider_id], ("manual_import",))
            self.assertEqual(provider_status_copy("manual_only").status, "manual_only")

    def test_repeated_sampling_probability_exposes_n_and_confidence(self):
        runs = (
            EngineRun("manual_import", "best watch", "t1", "HU", "en", "Acme Watch is recommended.", (), ("Acme Watch",), ("Acme Watch",), ()),
            EngineRun("manual_import", "best watch", "t2", "HU", "en", "Other Watch is recommended.", (), ("Other Watch",), ("Other Watch",), ()),
            EngineRun("manual_import", "best watch", "t3", "HU", "en", "Acme Watch appears again.", (), ("Acme Watch",), ("Acme Watch",), ()),
        )

        summary = summarize_brand_probability(runs, brand="Acme", query_cluster="category:best-watch").to_dict()

        self.assertEqual(summary["engine"], "manual_import")
        self.assertEqual(summary["query_cluster"], "category:best-watch")
        self.assertEqual(summary["sample_count"], 3)
        self.assertEqual(summary["positive_count"], 2)
        self.assertGreater(summary["probability"], 0.6)
        self.assertLess(summary["probability"], 0.7)
        self.assertEqual(summary["confidence_label"], "directional")
        self.assertEqual(summary["collection_method"], "manual_or_recorded")


if __name__ == "__main__":
    unittest.main()
