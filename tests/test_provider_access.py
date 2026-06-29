import json
import unittest

from geo_agent.evidence_store import EvidenceStore, ReportArtifact
from geo_agent.provider_access import (
    ApiKeySessionStore,
    ProviderAccessError,
    ProviderDefinition,
    ProviderRegistry,
    default_provider_registry,
    manual_only_provider_matrix,
    redact_credential_label,
)


class ProviderAccessTests(unittest.TestCase):
    def test_default_registry_exposes_initial_provider_matrix(self):
        registry = default_provider_registry()
        definitions = {item.provider_id: item for item in registry.list_definitions()}

        self.assertIn("openai_compatible", definitions)
        self.assertIn("google_search_console", definitions)
        self.assertIn("manual_import", definitions)
        self.assertNotIn("google_aio", definitions)
        self.assertEqual(definitions["openai_compatible"].access_methods, ("api_key", "platform_managed"))
        self.assertEqual(definitions["openai_compatible"].implementation_status, "implemented")
        self.assertEqual(definitions["google_search_console"].access_methods, ("oauth",))
        self.assertEqual(definitions["manual_import"].implementation_status, "implemented")

    def test_manual_only_provider_matrix_is_explicit(self):
        definitions = {item.provider_id: item for item in manual_only_provider_matrix()}

        self.assertEqual(set(definitions), {"google_aio", "deepseek", "kimi", "qianwen"})
        self.assertEqual(definitions["google_aio"].implementation_status, "manual_only")
        self.assertEqual(definitions["google_aio"].access_methods, ("manual_import",))

    def test_registry_rejects_unsupported_access_method(self):
        registry = default_provider_registry()

        with self.assertRaisesRegex(ProviderAccessError, "does not support"):
            registry.connect("manual_import", "oauth")

    def test_connections_redact_credentials(self):
        registry = default_provider_registry()

        connection = registry.connect("manual_import", "manual_import", credential_label="sk-secret-value")

        payload = connection.to_dict()
        self.assertEqual(payload["redacted_label"], "sk…ue")
        self.assertNotIn("sk-secret-value", str(payload))

    def test_manual_only_provider_connects_only_through_manual_import(self):
        registry = ProviderRegistry(manual_only_provider_matrix())

        connection = registry.connect("google_aio", "manual_import")

        self.assertEqual(connection.auth_status, "connected")
        self.assertEqual(connection.access_method, "manual_import")
        with self.assertRaisesRegex(ProviderAccessError, "does not support"):
            registry.connect("google_aio", "api_key")

    def test_implemented_openai_provider_can_connect_with_redacted_credential(self):
        registry = default_provider_registry()

        connection = registry.connect("openai_compatible", "api_key", credential_label="sk-live-value")

        self.assertEqual(connection.auth_status, "connected")
        self.assertEqual(connection.redacted_label, "sk…ue")
        self.assertNotIn("sk-live-value", json.dumps(connection.to_dict()))

    def test_planned_provider_is_visible_but_not_connected(self):
        registry = default_provider_registry()

        connection = registry.connect("perplexity", "api_key", credential_label="pplx-live-value")

        self.assertEqual(connection.auth_status, "planned")
        self.assertEqual(connection.redacted_label, "planned")

    def test_redaction_for_short_or_empty_values(self):
        self.assertEqual(redact_credential_label(""), "redacted")
        self.assertEqual(redact_credential_label("abc"), "****")

    def test_api_key_session_accepts_key_and_returns_only_redacted_state(self):
        store = ApiKeySessionStore(fake_registry())

        session = store.create_session("fake_answer", "pplx-secret-key", label="pplx-secret-key")

        payload = session.to_dict()
        self.assertEqual(payload["provider_id"], "fake_answer")
        self.assertEqual(payload["redacted_label"], "pp…ey")
        self.assertNotIn("pplx-secret-key", json.dumps(payload))
        self.assertEqual(store.get_key(session.session_id), "pplx-secret-key")

    def test_api_key_session_rejects_missing_key(self):
        store = ApiKeySessionStore(fake_registry())

        with self.assertRaisesRegex(ProviderAccessError, "API key is required"):
            store.create_session("fake_answer", "")

    def test_api_key_session_rejects_non_api_key_provider(self):
        store = ApiKeySessionStore()

        with self.assertRaisesRegex(ProviderAccessError, "does not support API key"):
            store.create_session("google_search_console", "secret")

    def test_api_key_session_rejects_planned_provider(self):
        store = ApiKeySessionStore()

        with self.assertRaisesRegex(ProviderAccessError, "not implemented"):
            store.create_session("perplexity", "secret")

    def test_api_key_does_not_enter_report_artifacts(self):
        secret = "pplx-secret-key"
        store = ApiKeySessionStore(fake_registry())
        session = store.create_session("fake_answer", secret, label=secret)
        with EvidenceStore() as evidence:
            evidence.save_report_artifact(ReportArtifact("provider-state", "json", json.dumps(session.to_dict())))
            artifact = evidence.list_report_artifacts()[0]

        payload = json.loads(artifact.content)
        self.assertNotIn(secret, artifact.content)
        self.assertEqual(payload["redacted_label"], "pp…ey")


def fake_registry():
    return ProviderRegistry(
        (
            ProviderDefinition(
                "fake_answer",
                "Fake Answer Provider",
                "answer",
                ("answer",),
                ("api_key",),
                "implemented",
            ),
        )
    )


if __name__ == "__main__":
    unittest.main()
