from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REQUIRED_INPUTS = (
    "task_id",
    "method",
    "target_page",
    "query_cluster",
    "evidence_ids",
    "expected_metric",
    "risk",
)
REQUIRED_OUTPUTS = ("artifact_ref", "evidence_ids", "warnings")


@dataclass(frozen=True)
class SkillPackageValidation:
    name: str
    version: str
    valid: bool
    errors: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "version": self.version, "valid": self.valid, "errors": list(self.errors)}


def validate_skill_package(root: Path) -> SkillPackageValidation:
    manifest_path = root / "skill.json"
    errors: list[str] = []
    if not manifest_path.exists():
        return SkillPackageValidation("", "", False, ("missing skill.json",))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    name = str(manifest.get("name", ""))
    version = str(manifest.get("version", ""))
    entrypoint = root / str(manifest.get("entrypoint", ""))
    inputs = tuple(manifest.get("inputs", ()))
    outputs = tuple(manifest.get("outputs", ()))
    boundaries = tuple(manifest.get("boundaries", ()))
    for item in REQUIRED_INPUTS:
        if item not in inputs:
            errors.append(f"missing input: {item}")
    for item in REQUIRED_OUTPUTS:
        if item not in outputs:
            errors.append(f"missing output: {item}")
    if not name:
        errors.append("missing name")
    if not version:
        errors.append("missing version")
    if not entrypoint.exists():
        errors.append("missing entrypoint")
    if not any("core does not generate final content" in str(item) for item in boundaries):
        errors.append("missing core boundary")
    return SkillPackageValidation(name, version, not errors, tuple(errors))
