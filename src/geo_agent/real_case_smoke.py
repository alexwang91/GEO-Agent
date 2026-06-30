from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = (
    "fixture_kind",
    "fixture_status",
    "source_policy",
    "brand",
    "query_cluster",
    "captures",
    "trust_check",
    "retest_plan",
    "limitations",
)
REQUIRED_CAPTURE_FIELDS = (
    "engine",
    "collection_method",
    "captured_at",
    "query",
    "answer_excerpt",
    "citation_count",
    "evidence_ids",
)
MANUAL_ONLY_ENGINES = {"google_aio", "deepseek", "kimi", "qianwen"}


@dataclass(frozen=True)
class RealCaseSmokeValidation:
    ready: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    capture_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "ready": self.ready,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "capture_count": self.capture_count,
        }


def validate_real_case_smoke_fixture(path: Path) -> RealCaseSmokeValidation:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return validate_real_case_smoke_payload(payload)


def validate_real_case_smoke_payload(payload: dict[str, Any]) -> RealCaseSmokeValidation:
    errors: list[str] = []
    warnings: list[str] = []
    for field in REQUIRED_TOP_LEVEL:
        if field not in payload:
            errors.append(f"missing top-level field: {field}")
    if payload.get("fixture_kind") != "geo-agent real-case smoke":
        errors.append("fixture_kind must identify a real-case smoke fixture")
    if payload.get("fixture_status") != "sanitized_manual_capture":
        errors.append("fixture_status must be sanitized_manual_capture")
    if payload.get("source_policy") != "no_fabricated_engine_answers":
        errors.append("source_policy must prohibit fabricated engine answers")
    captures = payload.get("captures", [])
    if not isinstance(captures, list) or not captures:
        errors.append("captures must be a non-empty list")
        captures = []
    for index, capture in enumerate(captures):
        if not isinstance(capture, dict):
            errors.append(f"capture {index} must be an object")
            continue
        _validate_capture(index, capture, errors, warnings)
    trust_check = payload.get("trust_check", {})
    if isinstance(trust_check, dict):
        if "extraction_precision" not in trust_check:
            errors.append("trust_check missing extraction_precision")
        if "extraction_recall" not in trust_check:
            errors.append("trust_check missing extraction_recall")
        if trust_check.get("status") == "trusted" and not trust_check.get("reviewer_note"):
            errors.append("trusted fixtures require reviewer_note")
    else:
        errors.append("trust_check must be an object")
    retest_plan = payload.get("retest_plan", {})
    if isinstance(retest_plan, dict):
        if not retest_plan.get("noise_floor_note"):
            errors.append("retest_plan missing noise_floor_note")
        if not retest_plan.get("query_cluster"):
            errors.append("retest_plan missing query_cluster")
    else:
        errors.append("retest_plan must be an object")
    limitations = payload.get("limitations", [])
    if not isinstance(limitations, list) or not limitations:
        errors.append("limitations must be a non-empty list")
    return RealCaseSmokeValidation(not errors, tuple(errors), tuple(warnings), len(captures))


def _validate_capture(index: int, capture: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    for field in REQUIRED_CAPTURE_FIELDS:
        if field not in capture:
            errors.append(f"capture {index} missing field: {field}")
    engine = str(capture.get("engine", ""))
    method = str(capture.get("collection_method", ""))
    if engine in MANUAL_ONLY_ENGINES and method != "manual_import":
        errors.append(f"capture {index} manual-only engine must use manual_import")
    if not capture.get("evidence_ids"):
        errors.append(f"capture {index} must preserve evidence_ids")
    excerpt = str(capture.get("answer_excerpt", ""))
    if len(excerpt.split()) < 4:
        warnings.append(f"capture {index} excerpt is short")
    if "api_key" in excerpt.lower() or "cookie" in excerpt.lower() or "token" in excerpt.lower():
        errors.append(f"capture {index} appears to contain secret-like text")
