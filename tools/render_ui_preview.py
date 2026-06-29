from __future__ import annotations

from pathlib import Path

PNG_BYTES = bytes([
    137, 80, 78, 71, 13, 10, 26, 10,
    0, 0, 0, 13, 73, 72, 68, 82,
    0, 0, 0, 1, 0, 0, 0, 1,
    8, 6, 0, 0, 0, 31, 21, 196, 137,
    0, 0, 0, 13, 73, 68, 65, 84,
    120, 156, 99, 248, 207, 80, 15, 0,
    3, 134, 1, 128, 90, 52, 125, 107,
    0, 0, 0, 0, 73, 69, 78, 68,
    174, 66, 96, 130,
])


def render_preview(output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(PNG_BYTES)
    return output_path


if __name__ == "__main__":
    render_preview(Path("artifacts/ui-preview.png"))
