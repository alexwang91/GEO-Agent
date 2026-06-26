import unittest

from geo_agent.optimization_tasks_v2 import OptimizationTaskV2
from geo_agent.retest_plan_v2 import build_retest_plan_v2


def task(task_id, owner, impact, effort, priority):
    return OptimizationTaskV2(task_id, "Title", "dx:1", owner, impact, effort, priority, ("evidence:1",))


class RetestPlanV2Tests(unittest.TestCase):
    def test_builds_retest_items_from_tasks(self):
        plan = build_retest_plan_v2((task("task:1", "content", 3, 2, 2.5), task("task:2", "ops", 4, 1, 5.0)), base_queries=12)
        self.assertEqual("task:2", plan[0].task_id)
        self.assertEqual(1, plan[0].provider_count)
        self.assertEqual(5, plan[0].sample_count)
        self.assertEqual("metric improves beyond noise floor", plan[0].success_condition)

    def test_invalid_base_queries_rejected(self):
        with self.assertRaises(ValueError):
            build_retest_plan_v2((), base_queries=0)


if __name__ == "__main__":
    unittest.main()
