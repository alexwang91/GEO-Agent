import json
import unittest

from geo_agent.optimization_tasks_v2 import OptimizationTaskV2
from geo_agent.task_exports import export_tasks_csv, export_tasks_json, group_tasks_by_owner


def task(task_id, owner, priority):
    return OptimizationTaskV2(task_id, "Title", "dx:1", owner, 3, 2, priority, ("evidence:1",))


class TaskExportsTests(unittest.TestCase):
    def test_group_tasks_by_owner_sorts_groups_and_tasks(self):
        groups = group_tasks_by_owner((task("task:2", "seo", 1.0), task("task:1", "content", 2.0), task("task:3", "seo", 3.0)))
        self.assertEqual(["content", "seo"], [group.owner_hint for group in groups])
        self.assertEqual("task:3", groups[1].tasks[0].task_id)

    def test_json_and_csv_exports_include_evidence_ids(self):
        tasks = (task("task:1", "content", 2.0),)
        payload = json.loads(export_tasks_json(tasks))
        csv_text = export_tasks_csv(tasks)
        self.assertEqual(["evidence:1"], payload[0]["evidence_ids"])
        self.assertIn("task_id,owner_hint", csv_text)
        self.assertIn("evidence:1", csv_text)


if __name__ == "__main__":
    unittest.main()
