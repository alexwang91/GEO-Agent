import unittest

from geo_agent.bootstrap_stats import bootstrap_mean_interval
from geo_agent.report_v2 import compare_metric_delta, summarize_metric_samples


class StatisticsWiringTests(unittest.TestCase):
    def test_metric_samples_include_confidence_and_directionality(self):
        summary = summarize_metric_samples({"visibility": [0.2, 0.4, 0.6]}, seed=1)
        item = summary["visibility"]
        self.assertIn("mean", item)
        self.assertIn("lower", item)
        self.assertIn("upper", item)
        self.assertIn("noise_floor", item)
        self.assertEqual(3, item["sample_count"])
        self.assertIn("directional", item["interpretation"])

    def test_delta_under_noise_floor_is_inconclusive(self):
        before = bootstrap_mean_interval([0.40, 0.41, 0.39], iterations=100, seed=2)
        after = bootstrap_mean_interval([0.405, 0.415, 0.395], iterations=100, seed=2)
        comparison = compare_metric_delta(before, after)
        self.assertEqual("inconclusive_below_noise_floor", comparison["conclusion"])


if __name__ == "__main__":
    unittest.main()
