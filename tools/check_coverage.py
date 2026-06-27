from __future__ import annotations

import runpy
import sys
import trace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "geo_agent"
MIN_PERCENT = 20.0


def executable_lines(path: Path) -> set[int]:
    lines = set()
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.add(index)
    return lines


def main() -> None:
    sys.path.insert(0, str(ROOT / "src"))
    tracer = trace.Trace(count=True, trace=False)
    old_argv = sys.argv[:]
    sys.argv = ["unittest", "discover", "-s", str(ROOT / "tests"), "-v"]
    try:
        tracer.runctx("runpy.run_module('unittest', run_name='__main__', alter_sys=True)", {"runpy": runpy}, {})
    finally:
        sys.argv = old_argv
    counts = tracer.results().counts
    executable = 0
    covered = 0
    for path in SRC.rglob("*.py"):
        lines = executable_lines(path)
        executable += len(lines)
        filename = str(path)
        covered += len({lineno for (counted_path, lineno), _count in counts.items() if counted_path == filename and lineno in lines})
    percent = round((covered / executable) * 100, 2) if executable else 100.0
    print(f"coverage: {covered}/{executable} lines = {percent}%")
    if percent < MIN_PERCENT:
        raise SystemExit(f"coverage below threshold: {percent}%")


if __name__ == "__main__":
    main()
