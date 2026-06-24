import unittest

from geo_agent.evidence_store import EvidenceStore, ReportArtifact
from geo_agent.failure_debugger import FailureDiagnosis
from geo_agent.optimization_tasks import OptimizationTaskBrief
from geo_agent.page_inventory import PageInventoryRecord
from geo_agent.query_space import QueryRecord


class EvidenceGraphStoreTests(unittest.TestCase):
    def test_query_records_save_load_and_filter_by_cluster(self):
        first = query("brand:en:US:recorded")
        second = query("category:en:US:recorded")
        with EvidenceStore() as store:
            store.save_query_records([first, second])
            all_records = store.list_query_records()
            filtered = store.list_query_records(cluster="brand:en:US:recorded")

        self.assertEqual(all_records, [first, second])
        self.assertEqual(filtered, [first])

    def test_page_inventory_save_load_and_filter_by_canonical(self):
        first = page("https://acme.ai/")
        second = page("https://acme.ai/pricing")
        with EvidenceStore() as store:
            store.save_page_records([first, second])
            all_records = store.list_page_records()
            filtered = store.list_page_records(canonical_url="https://acme.ai/")

        self.assertEqual(all_records, [first, second])
        self.assertEqual(filtered, [first])

    def test_diagnoses_save_load_and_filter_by_failure_type(self):
        first = FailureDiagnosis(("attribution",), "missing citation", "Inspect owned page.", ("brand without owned source",))
        second = FailureDiagnosis(("retrieval",), "empty answer", "Inspect sampling.", ("empty answer",))
        with EvidenceStore() as store:
            store.save_diagnoses([first, second])
            all_records = store.list_diagnoses()
            filtered = store.list_diagnoses(failure_type="attribution")

        self.assertEqual(all_records, [first, second])
        self.assertEqual(filtered, [first])

    def test_tasks_save_load_and_filter_by_action_type(self):
        first = task("add_citable_claims")
        second = task("strengthen_page_evidence")
        with EvidenceStore() as store:
            store.save_tasks([first, second])
            all_records = store.list_tasks()
            filtered = store.list_tasks(action_type="add_citable_claims")

        self.assertEqual(all_records, [first, second])
        self.assertEqual(filtered, [first])

    def test_report_artifacts_save_load_and_filter_by_format(self):
        first = ReportArtifact("audit", "json", "{}")
        second = ReportArtifact("audit", "markdown", "# Report")
        with EvidenceStore() as store:
            store.save_report_artifact(first)
            store.save_report_artifact(second)
            all_records = store.list_report_artifacts()
            filtered = store.list_report_artifacts(format="json")

        self.assertEqual(all_records, [first, second])
        self.assertEqual(filtered, [first])


def query(cluster):
    return QueryRecord(
        query="What is Acme AI?",
        intent_type=cluster.split(":")[0],
        funnel_stage="awareness",
        language="en",
        region="US",
        target_engine="recorded",
        competitor_entities=("Globex",),
        expected_answer_format="summary",
        priority_score=0.55,
        cluster=cluster,
    )


def page(url):
    return PageInventoryRecord(
        url=url,
        title="Acme AI",
        h1="Acme AI",
        schema_types=("Organization",),
        last_modified=None,
        canonical_url=url,
        content_chunks=("Acme AI page",),
    )


def task(action_type):
    return OptimizationTaskBrief(
        action_type=action_type,
        target_page="https://acme.ai/",
        query_cluster="brand:en:US:recorded",
        expected_impact="medium",
        confidence=0.72,
        risk="draft_only_no_auto_publish",
        draft_content="Draft update",
        retest_plan="Retest cluster.",
        failure_type="attribution",
    )


if __name__ == "__main__":
    unittest.main()
