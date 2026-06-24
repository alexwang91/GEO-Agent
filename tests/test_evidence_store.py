import tempfile
import unittest
from pathlib import Path

from geo_agent.engine_sampling import EngineRun
from geo_agent.evidence_store import EvidenceStore


def run(query="q1", engine="mock"):
    return EngineRun(
        engine=engine,
        query=query,
        timestamp="2026-06-24T00:00:00Z",
        region="US",
        language="en",
        raw_answer=f"answer for {query}",
        citations=("https://acme.ai/a",),
        mentions=("Acme AI",),
        recommendations=("Acme AI",),
        source_domains=("acme.ai",),
    )


class EvidenceStoreTests(unittest.TestCase):
    def test_empty_store_has_no_runs(self):
        with EvidenceStore() as store:
            self.assertEqual(store.count_runs(), 0)
            self.assertEqual(store.list_runs(), [])

    def test_single_run_round_trips_all_fields(self):
        with EvidenceStore() as store:
            row_id = store.save_run(run())
            records = store.list_runs()

        self.assertEqual(row_id, 1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0], run())

    def test_multiple_runs_keep_insert_order(self):
        with EvidenceStore() as store:
            store.save_runs([run("q1", "mock"), run("q2", "mock"), run("q3", "other")])
            records = store.list_runs()

        self.assertEqual([record.query for record in records], ["q1", "q2", "q3"])

    def test_filters_by_query_and_engine(self):
        with EvidenceStore() as store:
            store.save_runs([run("q1", "mock"), run("q1", "other"), run("q2", "mock")])

            by_query = store.list_runs(query="q1")
            by_engine = store.list_runs(engine="mock")
            combined = store.list_runs(query="q1", engine="mock")

        self.assertEqual([record.engine for record in by_query], ["mock", "other"])
        self.assertEqual([record.query for record in by_engine], ["q1", "q2"])
        self.assertEqual(combined, [run("q1", "mock")])

    def test_file_backed_store_persists_after_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs.sqlite3"
            with EvidenceStore(path) as store:
                store.save_run(run("persisted", "mock"))

            with EvidenceStore(path) as reopened:
                self.assertEqual(reopened.list_runs(), [run("persisted", "mock")])


if __name__ == "__main__":
    unittest.main()
