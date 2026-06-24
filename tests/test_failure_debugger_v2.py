import unittest

from geo_agent.engine_sampling import EngineRun
from geo_agent.failure_debugger import diagnose_failure_v2
from geo_agent.page_inventory import PageInventoryRecord
from geo_agent.query_space import QueryRecord


class FailureDebuggerV2Tests(unittest.TestCase):
    def test_attribution_failure_uses_run_page_and_source_evidence(self):
        diagnosis = diagnose_failure_v2(
            run("Acme AI is mentioned", domains=("news.example",), mentions=("Acme AI",)),
            query("brand"),
            pages=(page(),),
            brand="Acme AI",
            brand_domain="acme.ai",
            competitors=("Globex",),
        )

        self.assertIn("attribution", diagnosis.failure_types)
        self.assertIn("owned_pages=1", diagnosis.evidence)
        self.assertIn("brand appears without owned citation", diagnosis.evidence)

    def test_retrieval_failure_when_owned_page_exists_but_answer_empty(self):
        diagnosis = diagnose_failure_v2(
            run(""),
            query("category"),
            pages=(page(),),
            brand="Acme AI",
            brand_domain="acme.ai",
            competitors=("Globex",),
        )

        self.assertIn("retrieval", diagnosis.failure_types)
        self.assertIn("empty answer", diagnosis.evidence)

    def test_competitor_source_dominance_is_explicit(self):
        diagnosis = diagnose_failure_v2(
            run("Globex is cited as the category leader", domains=("globex.com",), mentions=("Globex",)),
            query("category"),
            pages=(page(),),
            brand="Acme AI",
            brand_domain="acme.ai",
            competitors=("Globex",),
        )

        self.assertIn("competitor_source", diagnosis.failure_types)
        self.assertTrue(any("competitor mentioned" in item for item in diagnosis.evidence))

    def test_entity_failure_when_text_mention_is_not_parsed(self):
        diagnosis = diagnose_failure_v2(
            run("Acme AI appears in the answer", domains=("acme.ai",), mentions=()),
            query("brand"),
            pages=(page(),),
            brand="Acme AI",
            brand_domain="acme.ai",
            competitors=("Globex",),
        )

        self.assertIn("entity", diagnosis.failure_types)
        self.assertIn("brand text mention was not parsed as entity mention", diagnosis.evidence)

    def test_intent_mismatch_for_buying_query_without_recommendation(self):
        diagnosis = diagnose_failure_v2(
            run("Acme AI is one option", domains=("acme.ai",), mentions=("Acme AI",), recommendations=()),
            query("buying_intent"),
            pages=(page(),),
            brand="Acme AI",
            brand_domain="acme.ai",
            competitors=("Globex",),
        )

        self.assertIn("intent_mismatch", diagnosis.failure_types)
        self.assertIn("buying-intent query did not recommend the brand", diagnosis.evidence)


def run(answer, *, domains=(), mentions=(), recommendations=()):
    return EngineRun(
        engine="recorded",
        query="q",
        timestamp="2026-06-24T00:00:00Z",
        region="US",
        language="en",
        raw_answer=answer,
        citations=tuple(f"https://{domain}/source" for domain in domains),
        mentions=tuple(mentions),
        recommendations=tuple(recommendations),
        source_domains=tuple(domains),
    )


def query(intent):
    return QueryRecord(
        query="q",
        intent_type=intent,
        funnel_stage="conversion" if intent == "buying_intent" else "awareness",
        language="en",
        region="US",
        target_engine="recorded",
        competitor_entities=("Globex",),
        expected_answer_format="recommendation" if intent == "buying_intent" else "summary",
        priority_score=0.9,
        cluster=f"{intent}:en:US:recorded",
    )


def page():
    return PageInventoryRecord(
        url="https://acme.ai/",
        title="Acme AI",
        h1="Acme AI evidence hub",
        schema_types=("Organization",),
        last_modified=None,
        canonical_url="https://acme.ai/",
        content_chunks=("Acme AI helps marketing teams improve AI search visibility.",),
    )


if __name__ == "__main__":
    unittest.main()
