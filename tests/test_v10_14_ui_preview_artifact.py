import tempfile
import unittest
from pathlib import Path

from tools.render_ui_preview import render_preview


class V10UIPreviewArtifactTests(unittest.TestCase):
    def test_preview_renderer_writes_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = render_preview(Path(directory) / "ui-preview.png")
            data = output.read_bytes()

        self.assertEqual(output.name, "ui-preview.png")
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
