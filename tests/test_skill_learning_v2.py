import unittest

from geo_agent.skill_learning_v2 import build_learning_signal, summarize_learning_signals


class SkillLearningV2Tests(unittest.TestCase):
    def test_learning_signal_outcomes_and_recommendations(self):
        positive = build_learning_signal("sig:1", "task:1", 0.2)
        negative = build_learning_signal("sig:2", "task:2", -0.1)
        neutral = build_learning_signal("sig:3", "task:3", 0.0)
        self.assertEqual("positive", positive.outcome)
        self.assertIn("Promote", positive.recommendation)
        self.assertEqual("negative", negative.outcome)
        self.assertEqual("neutral", neutral.outcome)
        self.assertEqual({"positive": 1, "negative": 1, "neutral": 1}, summarize_learning_signals((positive, negative, neutral)))


if __name__ == "__main__":
    unittest.main()
