import json
import unittest

from geo_agent.evidence_store import EvidenceStore, ReportArtifact
from geo_agent.provider_access import ProviderAccessError, ProviderDefinition, ProviderRegistry
from geo_agent.provider_auth_flow import AuthorizationSessionStore, FakeAuthorizationProvider


class ProviderAuthFlowTests(unittest.TestCase):
    def test_start_returns_authorization_url_and_state(self):
        store = AuthorizationSessionStore(fake_registry())

        start = store.start("fake_analytics", redirect_uri="http://localhost/callback", scopes=("read",))

        payload = start.to_dict()
        self.assertEqual(payload["provider_id"], "fake_analytics")
        self.assertIn("state=", payload["authorization_url"])
        self.assertIn("redirect_uri=http%3A%2F%2Flocalhost%2Fcallback", payload["authorization_url"])
        self.assertTrue(payload["state"])

    def test_callback_validates_state_and_returns_redacted_session(self):
        store = AuthorizationSessionStore(fake_registry(), FakeAuthorizationProvider())
        start = store.start("fake_analytics", redirect_uri="http://localhost/callback", scopes=("read", "site"))

        session = store.callback(state=start.state, code="abc123")

        payload = session.to_dict()
        self.assertEqual(payload["provider_id"], "fake_analytics")
        self.assertEqual(payload["scopes"], ["read", "site"])
        self.assertEqual(payload["redacted_label"], "fa…23")
        self.assertNotIn("fake-token-abc123", json.dumps(payload))
        self.assertEqual(store.get_token(session.session_id), "fake-token-abc123")

    def test_callback_rejects_invalid_state(self):
        store = AuthorizationSessionStore(fake_registry())

        with self.assertRaisesRegex(ProviderAccessError, "Invalid authorization state"):
            store.callback(state="wrong", code="abc123")

    def test_callback_rejects_empty_code(self):
        store = AuthorizationSessionStore(fake_registry())
        start = store.start("fake_analytics", redirect_uri="http://localhost/callback")

        with self.assertRaisesRegex(ProviderAccessError, "Authorization code is required"):
            store.callback(state=start.state, code="")

    def test_start_rejects_non_authorization_provider(self):
        store = AuthorizationSessionStore(fake_registry())

        with self.assertRaisesRegex(ProviderAccessError, "does not support authorization flow"):
            store.start("manual_import", redirect_uri="http://localhost/callback")

    def test_disconnect_removes_token_session(self):
        store = AuthorizationSessionStore(fake_registry())
        start = store.start("fake_analytics", redirect_uri="http://localhost/callback")
        session = store.callback(state=start.state, code="abc123")

        store.disconnect(session.session_id)

        with self.assertRaisesRegex(ProviderAccessError, "Unknown authorization session"):
            store.get_token(session.session_id)

    def test_token_does_not_enter_report_artifacts(self):
        store = AuthorizationSessionStore(fake_registry())
        start = store.start("fake_analytics", redirect_uri="http://localhost/callback")
        session = store.callback(state=start.state, code="abc123")
        token = store.get_token(session.session_id)

        with EvidenceStore() as evidence:
            evidence.save_report_artifact(ReportArtifact("auth-state", "json", json.dumps(session.to_dict())))
            artifact = evidence.list_report_artifacts()[0]

        payload = json.loads(artifact.content)
        self.assertNotIn(token, artifact.content)
        self.assertEqual(payload["redacted_label"], "fa…23")


def fake_registry():
    return ProviderRegistry(
        (
            ProviderDefinition(
                "fake_analytics",
                "Fake Analytics",
                "analytics",
                ("analytics",),
                ("oauth",),
                "implemented",
            ),
            ProviderDefinition(
                "manual_import",
                "Manual Import",
                "answer",
                ("manual_import",),
                ("manual_import",),
                "implemented",
            ),
        )
    )


if __name__ == "__main__":
    unittest.main()
