import unittest

from geo_agent.repeated_sampling import build_repeated_sampling_plan


class RepeatedSamplingPlanTests(unittest.TestCase):
    def test_plan_is_deterministic_and_expands_queries_providers_samples(self):
        first = build_repeated_sampling_plan(["q1", "q2"], ["manual", "fixture"], sample_count=3, seed=42)
        second = build_repeated_sampling_plan(["q1", "q2"], ["manual", "fixture"], sample_count=3, seed=42)
        self.assertEqual(first.plan_id, second.plan_id)
        self.assertEqual(12, len(first.items))
        self.assertEqual(first.items[0].seed, second.items[0].seed)
        self.assertEqual("directional", first.directionality)

    def test_low_sample_is_marked_directional(self):
        plan = build_repeated_sampling_plan(["q"], ["manual"], sample_count=1, seed=7)
        self.assertEqual("directional_low_sample", plan.directionality)
        self.assertEqual(1, plan.items[0].sample_index)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            build_repeated_sampling_plan([], ["manual"], sample_count=1, seed=1)
        with self.assertRaises(ValueError):
            build_repeated_sampling_plan(["q"], ["manual"], sample_count=0, seed=1)


if __name__ == "__main__":
    unittest.main()
