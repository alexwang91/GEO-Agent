import unittest

from geo_agent.diagnosis_taxonomy_v3 import create_diagnosis_v3
from geo_agent.optimization_tasks_v2 import tasks_from_diagnoses


class OptimizationTasksV2Tests(unittest.TestCase):
    def test_tasks_map_diagnoses_to_owner_effort_and_priority(self):
        diagnoses = (
            create_diagnosis_v3("dx:1", "provider_unavailable", "critical", ("provider:1",), "Provider failed."),
            create_diagnosis_v3("dx:2", "weak_citation_absorption", "medium", ("metric:1",), "Weak citations."),
        )
        tasks = tasks_from_diagnoses(diagnoses)
        self.assertEqual("dx:1", tasks[0].diagnosis_id)
        self.assertEqual("ops", tasks[0].owner_hint)
        self.assertGreater(tasks[0].priority_score, tasks[1].priority_score)
        self.assertEqual(["provider:1"], tasks[0].to_dict()["evidence_ids"])

    def test_empty_diagnoses_return_empty_tasks(self):
        self.assertEqual((), tasks_from_diagnoses(()))


if __name__ == "__main__":
    unittest.main()
