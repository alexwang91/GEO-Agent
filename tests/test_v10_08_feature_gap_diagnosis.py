import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.failure_debugger import CONTENT_FEATURE_TAXONOMY, diagnose_failure_v2
from geo_agent.page_inventory import PageInventoryRecord
from geo_agent.query_space import QueryRecord


class V10FeatureGapDiagnosisTests(unittest.TestCase):
    def test_diagnosis_references_concrete_content_feature_gaps(self):
        run = EngineRun(
            engine="fixture_ai",
            query="best fitness watch",
            timestamp="2026-06-29T12:00:00+00:00",
            region="HU",
            language="en",
            raw_answer="Other Watch is listed as a shortlist option.",
            citations=("source-a",),
            mentions=("Other Watch",),
            recommendations=("Other Watch",),
            source_domains=("third-party.test",),
        )
        query = QueryRecord(
            query=run.query,
            intent_type="category",
            funnel_stage="awareness",
            language="en",
            region="HU",
            target_engine="fixture_ai",
            competitor_entities=("Other Watch",),
            expected_answer_format="shortlist",
            priority_score=1.0,
            cluster="category:fitness-watch",
        )
        page = PageInventoryRecord(
            url="http://owned.test/acme-watch",
            title="Acme Watch",
            h1="Acme Watch",
            schema_types=(),
            last_modified=None,
            canonical_url="http://owned.test/acme-watch",
            content_chunks=("Acme Watch is a lightweight fitness wearable for buyers.",),
        )

        diagnosis = diagnose_failure_v2(run, query, pages=(page,), brand="Acme", brand_domain="owned.test", competitors=("Other Watch",))

        self.assertIn("trust", diagnosis.failure_types)
        self.assertIn("feature_gap=statistics", diagnosis.explanation)
        self.assertIn("feature_gap=quotations", diagnosis.explanation)
        self.assertIn("feature_gap=schema", diagnosis.explanation)
        self.assertIn("Address content feature gaps", diagnosis.next_step)
        self.assertIn("statistics", CONTENT_FEATURE_TAXONOMY)
        self.assertIn("freshness", CONTENT_FEATURE_TAXONOMY)


if __name__ == "__main__":
    unittest.main()
