import unittest

from geo_agent.bootstrap_stats import bootstrap_mean_interval


class BootstrapStatsTests(unittest.TestCase):
    def test_bootstrap_is_deterministic(self):
        first = bootstrap_mean_interval([0.2, 0.4, 0.6, 0.8], iterations=100, seed=9)
        second = bootstrap_mean_interval([0.2, 0.4, 0.6, 0.8], iterations=100, seed=9)
        self.assertEqual(first, second)
        self.assertEqual(0.5, first.mean)
        self.assertGreaterEqual(first.upper, first.lower)
        self.assertGreaterEqual(first.noise_floor, 0)
        self.assertEqual("directional", first.directionality)

    def test_low_sample_directionality(self):
        result = bootstrap_mean_interval([0.5], iterations=10, seed=1)
        self.assertEqual("directional_low_sample", result.directionality)
        self.assertEqual(0.0, result.noise_floor)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            bootstrap_mean_interval([])
        with self.assertRaises(ValueError):
            bootstrap_mean_interval([1], iterations=0)


if __name__ == "__main__":
    unittest.main()
