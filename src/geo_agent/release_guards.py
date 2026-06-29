from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REQUIRED_DONE = tuple(f"V10-{index:02d}" for index in range(1, 18))
REQUIRED_FILES = (
    "docs/release-guards.md",
    "skills/geo-rewrite-skill/skill.json",
    "skills/geo-rewrite-skill/skill.md",
)
FORBIDDEN_COPY_PARTS = (
    ("google aio", "automated"),
    ("deepseek", "live provider"),
    ("kimi", "live provider"),
    ("qianwen", "live provider"),
)


@dataclass(frozen=True)
class ReleaseGuardResult:
    passed: bool
    failures: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {"passed": self.passed, "failures": list(self.failures)}


def evaluate_release_guards(root: Path) -> ReleaseGuardResult:
    failures: list[str] = []
    progress = (root / "docs" / "progress.md").read_text(encoding="utf-8")
    repo_text = _repo_text(root)
    for milestone in REQUIRED_DONE:
        if f"| {milestone} | DONE |" not in progress:
            failures.append(f"milestone not done: {milestone}")
    for path in REQUIRED_FILES:
        if not (root / path).exists():
            failures.append(f"missing release file: {path}")
    for parts in FORBIDDEN_COPY_PARTS:
        phrase = " ".join(parts)
        if phrase in repo_text:
            failures.append(f"forbidden copy: {phrase}")
    return ReleaseGuardResult(not failures, tuple(failures))


def _repo_text(root: Path) -> str:
    chunks: list[str] = []
    for directory in ("docs", "src", "skills"):
        base = root / directory
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".json"}:
                chunks.append(path.read_text(encoding="utf-8").lower())
    return "\n".join(chunks)
