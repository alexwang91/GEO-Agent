import unittest

from geo_agent.browser_capture import (
    BrowserCaptureError,
    BrowserCaptureRecord,
    BrowserViewport,
    artifact_digest,
    make_capture_artifact,
)


class BrowserCaptureSchemaTests(unittest.TestCase):
    def test_capture_record_serializes_structure_without_live_scraping(self):
        artifact = make_capture_artifact("artifact:html:1", "html", "text/html", "<html><body>Acme</body></html>")
        record = BrowserCaptureRecord(
            capture_id="capture:1",
            url="https://acme.ai/",
            provider="manual",
            status="captured",
            captured_at="2026-06-24T00:00:00Z",
            viewport=BrowserViewport(1440, 900),
            artifacts=(artifact,),
            notes=("imported from manual browser export",),
        )
        payload = record.to_dict()
        self.assertEqual("https://acme.ai/", payload["url"])
        self.assertEqual("manual", payload["provider"])
        self.assertEqual("captured", payload["status"])
        self.assertEqual(1440, payload["viewport"]["width"])
        self.assertEqual(1, len(payload["artifacts"]))
        self.assertTrue(payload["artifacts"][0]["redacted"])

    def test_invalid_url_is_rejected(self):
        artifact = make_capture_artifact("artifact:html:1", "html", "text/html", "<html></html>")
        with self.assertRaises(BrowserCaptureError):
            BrowserCaptureRecord("capture:bad", "ftp://example.com", "manual", "captured", "2026-06-24T00:00:00Z", BrowserViewport(800, 600), (artifact,))

    def test_captured_status_requires_artifact(self):
        with self.assertRaises(BrowserCaptureError):
            BrowserCaptureRecord("capture:empty", "https://acme.ai/", "recorded_fixture", "captured", "2026-06-24T00:00:00Z", BrowserViewport(800, 600), ())

    def test_digest_is_deterministic(self):
        self.assertEqual(artifact_digest("same"), artifact_digest(b"same"))
        self.assertEqual(64, len(artifact_digest("same")))


if __name__ == "__main__":
    unittest.main()
