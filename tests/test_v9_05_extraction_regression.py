import json
import unittest
from pathlib import Path

from geo_agent.entity_resolution import extract_urls, find_entity_matches

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "realistic_answer_samples.json"


def precision_recall(actual, expected):
    actual_set = set(actual)
    expected_set = set(expected)
    true_positive = len(actual_set & expected_set)
    precision = true_positive / len(actual_set) if actual_set else (1.0 if not expected_set else 0.0)
    recall = true_positive / len(expected_set) if expected_set else 1.0
    return precision, recall


class RealisticExtractionRegressionTests(unittest.TestCase):
    def test_realistic_samples_keep_entity_precision_and_recall(self):
        samples = json.loads(FIXTURE.read_text(encoding="utf-8"))
        scores = []
        for sample in samples:
            matches = find_entity_matches(sample["answer"], sample["brand"], tuple(sample.get("aliases", ())))
            actual = [match.matched for match in matches]
            precision, recall = precision_recall(actual, sample["expected_mentions"])
            scores.append((precision, recall))
        mean_precision = sum(score[0] for score in scores) / len(scores)
        mean_recall = sum(score[1] for score in scores) / len(scores)
        self.assertGreaterEqual(mean_precision, 0.8)
        self.assertGreaterEqual(mean_recall, 0.8)

    def test_realistic_samples_keep_url_recall(self):
        samples = json.loads(FIXTURE.read_text(encoding="utf-8"))
        recalls = []
        for sample in samples:
            actual = extract_urls(sample["answer"])
            _precision, recall = precision_recall(actual, sample["expected_urls"])
            recalls.append(recall)
        self.assertGreaterEqual(sum(recalls) / len(recalls), 0.95)


if __name__ == "__main__":
    unittest.main()
