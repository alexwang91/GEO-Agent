"""Artifact-wide safety checks for provider access values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

SENSITIVE_KEY_PARTS = (
    "api_key",
    "authorization",
    "cookie",
    "password",
    "secret",
    "token",
)


@dataclass(frozen=True)
class ArtifactSafetyFinding:
    artifact_name: str
    path: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {"artifact_name": self.artifact_name, "path": self.path, "reason": self.reason}


@dataclass(frozen=True)
class ArtifactSafetyReport:
    findings: tuple[ArtifactSafetyFinding, ...]

    @property
    def passed(self) -> bool:
        return not self.findings

    def to_dict(self) -> dict[str, object]:
        return {"passed": self.passed, "findings": [finding.to_dict() for finding in self.findings]}


def scan_artifacts_for_access_leaks(
    artifacts: Mapping[str, object], *, forbidden_values: Iterable[str] = ()
) -> ArtifactSafetyReport:
    normalized_values = tuple(value for value in forbidden_values if value)
    findings: list[ArtifactSafetyFinding] = []
    for artifact_name, artifact in artifacts.items():
        findings.extend(_scan_value(str(artifact_name), artifact, path=str(artifact_name), forbidden_values=normalized_values))
    return ArtifactSafetyReport(tuple(findings))


def assert_artifacts_safe(artifacts: Mapping[str, object], *, forbidden_values: Iterable[str] = ()) -> None:
    report = scan_artifacts_for_access_leaks(artifacts, forbidden_values=forbidden_values)
    if not report.passed:
        summary = "; ".join(f"{item.artifact_name}:{item.path}:{item.reason}" for item in report.findings)
        raise AssertionError(f"Access value leakage detected: {summary}")


def _scan_value(
    artifact_name: str,
    value: object,
    *,
    path: str,
    forbidden_values: tuple[str, ...],
) -> list[ArtifactSafetyFinding]:
    findings: list[ArtifactSafetyFinding] = []
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}"
            if _sensitive_key(key_text):
                findings.append(ArtifactSafetyFinding(artifact_name, child_path, "sensitive key name"))
            findings.extend(_scan_value(artifact_name, nested, path=child_path, forbidden_values=forbidden_values))
        return findings
    if isinstance(value, list) or isinstance(value, tuple):
        for index, nested in enumerate(value):
            findings.extend(_scan_value(artifact_name, nested, path=f"{path}[{index}]", forbidden_values=forbidden_values))
        return findings
    text = str(value)
    for forbidden in forbidden_values:
        if forbidden in text:
            findings.append(ArtifactSafetyFinding(artifact_name, path, "forbidden access value"))
    return findings


def _sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(part in normalized for part in SENSITIVE_KEY_PARTS)
