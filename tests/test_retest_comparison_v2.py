import unittest

from geo_agent.retest_comparison_v2 import compare_retest_metric, compare_retest_metrics


class RetestComparisonV2Tests(unittest.TestCase):
    def test_status_uses_noise_floor(self):
        improved = compare_retest_metric("visibility", 0.4, 0.6, noise_floor=0.05, task_id="task:1")
        unchanged = compare_retest_metric("visibility", 0.4, 0.43, noise_floor=0.05)
        regressed = compare_retest_metric("visibility", 0.6, 0.4, noise_floor=0.05)
        self.assertEqual("improved", improved.status)
        self.assertEqual("attributed_to:task:1", improved.attribution)
        self.assertEqual("unchanged", unchanged.status)
        self.assertEqual("regressed", regressed.status)

    def test_batch_comparison_uses_shared_keys(self):
        result = compare_retest_metrics({"a": 0.1, "b": 0.2}, {"b": 0.4, "c": 0.9}, noise_floor=0.01)
        self.assertEqual(1, len(result))
        self.assertEqual("b", result[0].metric_name)

    def test_negative_noise_floor_rejected(self):
        with self.assertRaises(ValueError):
            compare_retest_metric("x", 0.1, 0.2, noise_floor=-0.1)


if __name__ == "__main__":
    unittest.main()
