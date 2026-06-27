from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "src", ROOT / "tests"]


def iter_python_files() -> list[Path]:
    files: list[Path] = []
    for target in TARGETS:
        if target.exists():
            files.extend(sorted(target.rglob("*.py")))
    return files


def main() -> None:
    failures: list[str] = []
    for path in iter_python_files():
        text = path.read_text(encoding="utf-8")
        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path.relative_to(ROOT)}:{exc.lineno}: syntax error: {exc.msg}")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
