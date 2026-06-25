import unittest

from geo_agent.artifact_safety import assert_artifacts_safe, scan_artifacts_for_access_leaks


class ArtifactSafetyTests(unittest.TestCase):
    def test_safe_artifact_set_passes(self):
        artifacts = {
            "manifest.json": {"package_id": "pkg-1", "files": ["report.json", "audit.sqlite"]},
            "report.json": {"score": {"visibility_score": 0.5}, "cited_sources": ["acme.ai"]},
            "report.md": "# GEO Agent Operational Report\n- cited source: acme.ai",
            "ui_payload": {"provider_status": "Configured boundary", "redacted_label": "sk…ue"},
            "log": "provider configured with redacted label only",
        }

        report = scan_artifacts_for_access_leaks(artifacts, forbidden_values=("sample-access-value",))

        self.assertTrue(report.passed)
        self.assertEqual(report.findings, ())
        assert_artifacts_safe(artifacts, forbidden_values=("sample-access-value",))

    def test_detects_forbidden_value_in_report_artifact(self):
        artifacts = {"report.json": {"summary": "sample-access-value"}}

        report = scan_artifacts_for_access_leaks(artifacts, forbidden_values=("sample-access-value",))

        self.assertFalse(report.passed)
        self.assertEqual(report.findings[0].artifact_name, "report.json")
        self.assertEqual(report.findings[0].reason, "forbidden access value")

    def test_detects_sensitive_key_name_in_manifest(self):
        artifacts = {"manifest.json": {"provider": {"api_key_label": "not allowed"}}}

        report = scan_artifacts_for_access_leaks(artifacts)

        self.assertFalse(report.passed)
        self.assertIn("manifest.json.provider.api_key_label", report.findings[0].path)

    def test_detects_nested_ui_payload_and_log_leakage(self):
        artifacts = {
            "ui_payload": {"providers": [{"label": "ok"}, {"value": "sample-access-value"}]},
            "log": "completed without access values",
        }

        report = scan_artifacts_for_access_leaks(artifacts, forbidden_values=("sample-access-value",))

        self.assertFalse(report.passed)
        self.assertIn("ui_payload.providers[1].value", report.findings[0].path)

    def test_assert_artifacts_safe_raises_actionable_error(self):
        artifacts = {"audit.sqlite.rows": [{"header_value": "sample-access-value"}]}

        with self.assertRaises(AssertionError) as error:
            assert_artifacts_safe(artifacts, forbidden_values=("sample-access-value",))

        self.assertIn("audit.sqlite.rows", str(error.exception))
        self.assertIn("forbidden access value", str(error.exception))


if __name__ == "__main__":
    unittest.main()
