import json
import unittest

from geo_agent.answer_provider import (
    AnswerCredentialRef,
    AnswerProviderConfig,
    OpenAICompatibleAnswerProvider,
)
from geo_agent.audit_runner import AuditRunner
from geo_agent.entity_profile import EntityProfile
from geo_agent.evidence_store import EvidenceStore


class FakeHttpClient:
    def __init__(self) -> None:
        self.calls = []

    def post(self, url, *, headers, json):
        self.calls.append({"url": url, "headers": headers, "json": json})
        query = json["messages"][0]["content"]
        return {
            "created_at": "2026-06-25T00:00:00Z",
            "choices": [{"message": {"content": f"Acme AI is cited for: {query}"}}],
            "geo": {
                "citations": ["https://acme.ai/guide"],
                "mentions": ["Acme AI"],
                "recommendations": ["Acme AI"],
            },
        }


class ProviderBackedAuditTests(unittest.TestCase):
    def test_provider_backed_audit_persists_answer_evidence_and_report(self):
        profile = EntityProfile(
            brand="Acme AI",
            domain="acme.ai",
            aliases=("Acme",),
            competitors=("Globex",),
            target_regions=("US",),
            target_languages=("en",),
            target_customer="marketing teams",
            main_product="AI visibility platform",
            category="GEO software",
            business_goal="improve AI search visibility",
        )
        pages = {
            "https://acme.ai/": "<html><head><title>Acme</title><link rel='canonical' href='https://acme.ai/'></head><body><h1>Acme AI</h1><p>Acme AI helps marketing teams.</p></body></html>"
        }
        client = FakeHttpClient()
        provider = OpenAICompatibleAnswerProvider(http_client=client)
        config = AnswerProviderConfig(
            provider_id="openai_compatible",
            model="fixture-model",
            endpoint_url="https://provider.invalid/chat",
        )
        credential_ref = AnswerCredentialRef(access_method="platform_managed", platform_api_key="sample-platform-value")

        with EvidenceStore() as store:
            artifacts = AuditRunner(store).run_with_answer_provider(
                profile,
                pages=pages,
                answer_provider=provider,
                provider_config=config,
                credential_ref=credential_ref,
                manual_urls=["https://acme.ai/"],
                max_queries=2,
                timestamp="2026-06-25T00:00:00Z",
            )
            runs = store.list_runs(engine="openai_compatible")
            pages_in_store = store.list_page_records()
            reports = store.list_report_artifacts()

        self.assertEqual(len(client.calls), 2)
        self.assertEqual(len(runs), 2)
        self.assertEqual(len(pages_in_store), 1)
        self.assertEqual(len(reports), 2)
        self.assertEqual(artifacts.runs[0].engine, "openai_compatible")
        self.assertEqual(artifacts.runs[0].mentions, ("Acme AI",))
        self.assertEqual(artifacts.runs[0].citations, ("https://acme.ai/guide",))
        self.assertIn("score", json.loads(artifacts.report_json))
        self.assertIn("# GEO Agent Operational Report", artifacts.report_markdown)

    def test_provider_backed_audit_does_not_write_access_values_to_artifacts(self):
        profile = EntityProfile(
            brand="Acme AI",
            domain="acme.ai",
            aliases=(),
            competitors=("Globex",),
            target_regions=("US",),
            target_languages=("en",),
            target_customer="marketing teams",
            main_product="AI visibility platform",
            category="GEO software",
            business_goal="improve AI search visibility",
        )
        pages = {"https://acme.ai/": "<html><body><h1>Acme AI</h1><p>Evidence.</p></body></html>"}
        client = FakeHttpClient()
        provider = OpenAICompatibleAnswerProvider(http_client=client)
        credential_ref = AnswerCredentialRef(access_method="platform_managed", platform_api_key="sample-platform-value")

        with EvidenceStore() as store:
            artifacts = AuditRunner(store).run_with_answer_provider(
                profile,
                pages=pages,
                answer_provider=provider,
                provider_config=AnswerProviderConfig(endpoint_url="https://provider.invalid/chat"),
                credential_ref=credential_ref,
                manual_urls=["https://acme.ai/"],
                max_queries=1,
            )
            stored_reports = "\n".join(item.content for item in store.list_report_artifacts())
            stored_runs = "\n".join(item.raw_answer for item in store.list_runs())

        combined = "\n".join([artifacts.report_json, artifacts.report_markdown, stored_reports, stored_runs])
        self.assertNotIn("sample-platform-value", combined)
        self.assertNotIn("Authorization", combined)
        self.assertEqual(client.calls[0]["headers"]["Authorization"], "Bearer sample-platform-value")


if __name__ == "__main__":
    unittest.main()
