import json
import unittest

from geo_agent.answer_provider import (
    AnswerCredentialRef,
    AnswerProviderConfig,
    AnswerProviderRequest,
    OpenAICompatibleAnswerProvider,
)
from geo_agent.engine_sampling import EngineRun
from geo_agent.evidence_store import EvidenceStore, ReportArtifact
from geo_agent.provider_access import ApiKeySessionStore, ProviderAccessError


class AnswerProviderTests(unittest.TestCase):
    def test_openai_compatible_provider_converts_fake_response_to_engine_run(self):
        session_store = ApiKeySessionStore()
        session = session_store.create_session("openai_compatible", "sk-test-secret", label="sk-test-secret")
        client = FakeHttpClient(
            {
                "choices": [{"message": {"content": "Acme is cited for GEO audits."}}],
                "geo": {
                    "citations": ["https://example.com/acme-guide"],
                    "mentions": ["Acme"],
                    "recommendations": ["Acme"],
                },
                "created_at": "2026-06-25T15:40:00Z",
            }
        )
        provider = OpenAICompatibleAnswerProvider(http_client=client, session_store=session_store)

        run = provider.sample(
            AnswerProviderRequest(
                query="best GEO audit tools",
                region="US",
                language="en",
                config=AnswerProviderConfig(model="test-model"),
                credential_ref=AnswerCredentialRef("api_key", session_id=session.session_id),
            )
        )

        self.assertIsInstance(run, EngineRun)
        self.assertEqual(run.engine, "openai_compatible")
        self.assertEqual(run.query, "best GEO audit tools")
        self.assertEqual(run.raw_answer, "Acme is cited for GEO audits.")
        self.assertEqual(run.citations, ("https://example.com/acme-guide",))
        self.assertEqual(run.source_domains, ("example.com",))
        self.assertEqual(client.calls[0]["json"]["model"], "test-model")
        self.assertNotIn("sk-test-secret", json.dumps(run.to_dict()))

    def test_missing_session_id_fails_clearly(self):
        provider = OpenAICompatibleAnswerProvider(http_client=FakeHttpClient({}))

        with self.assertRaisesRegex(ProviderAccessError, "session id is required"):
            provider.sample(
                AnswerProviderRequest(
                    query="best GEO audit tools",
                    region="US",
                    language="en",
                    config=AnswerProviderConfig(),
                    credential_ref=AnswerCredentialRef("api_key"),
                )
            )

    def test_missing_platform_key_fails_clearly(self):
        provider = OpenAICompatibleAnswerProvider(http_client=FakeHttpClient({}))

        with self.assertRaisesRegex(ProviderAccessError, "Platform-managed API key is required"):
            provider.sample(
                AnswerProviderRequest(
                    query="best GEO audit tools",
                    region="US",
                    language="en",
                    config=AnswerProviderConfig(),
                    credential_ref=AnswerCredentialRef("platform_managed"),
                )
            )

    def test_provider_error_is_reported_as_access_error(self):
        session_store = ApiKeySessionStore()
        session = session_store.create_session("openai_compatible", "sk-test-secret")
        provider = OpenAICompatibleAnswerProvider(
            http_client=FakeHttpClient({"error": {"message": "provider unavailable"}}),
            session_store=session_store,
        )

        with self.assertRaisesRegex(ProviderAccessError, "provider unavailable"):
            provider.sample(
                AnswerProviderRequest(
                    query="best GEO audit tools",
                    region="US",
                    language="en",
                    config=AnswerProviderConfig(),
                    credential_ref=AnswerCredentialRef("api_key", session_id=session.session_id),
                )
            )

    def test_request_and_report_artifacts_do_not_expose_raw_credentials(self):
        secret = "sk-test-secret"
        request = AnswerProviderRequest(
            query="best GEO audit tools",
            region="US",
            language="en",
            config=AnswerProviderConfig(),
            credential_ref=AnswerCredentialRef("platform_managed", platform_api_key=secret),
        )

        with EvidenceStore() as evidence:
            evidence.save_report_artifact(ReportArtifact("answer-request", "json", json.dumps(request.to_dict())))
            artifact = evidence.list_report_artifacts()[0]

        self.assertNotIn(secret, artifact.content)
        self.assertIn("sk…et", artifact.content)

    def test_malformed_geo_metadata_fails_without_network_retry(self):
        session_store = ApiKeySessionStore()
        session = session_store.create_session("openai_compatible", "sk-test-secret")
        provider = OpenAICompatibleAnswerProvider(
            http_client=FakeHttpClient(
                {
                    "choices": [{"message": {"content": "Answer text"}}],
                    "geo": {"citations": "not-a-list"},
                }
            ),
            session_store=session_store,
        )

        with self.assertRaisesRegex(ProviderAccessError, "metadata lists must be arrays"):
            provider.sample(
                AnswerProviderRequest(
                    query="best GEO audit tools",
                    region="US",
                    language="en",
                    config=AnswerProviderConfig(),
                    credential_ref=AnswerCredentialRef("api_key", session_id=session.session_id),
                )
            )


class FakeHttpClient:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post(self, url, *, headers, json):
        self.calls.append({"url": url, "headers": headers, "json": json})
        return self.response


if __name__ == "__main__":
    unittest.main()