import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "render_ui_preview.py"


class V10UIPreviewArtifactTests(unittest.TestCase):
    def test_preview_renderer_writes_png(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT)], cwd=directory, check=True, capture_output=True)
            output = Path(directory) / "artifacts" / "ui-preview.png"
            data = output.read_bytes()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(output.name, "ui-preview.png")
        self.assertEqual(data[:4], b"\x89PNG")


if __name__ == "__main__":
    unittest.main()
