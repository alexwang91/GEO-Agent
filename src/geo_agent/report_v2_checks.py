"""Output checks for report v2."""

from __future__ import annotations

REQUIRED_SECTIONS = ("Metric Summary", "Diagnoses", "Optimization Tasks", "Retest Plan")
REQUIRED_GUARDRAILS = ("Low-sample results are directional.", "Planned providers remain planned.")


def validate_report_v2_output(report_payload: dict[str, object]) -> tuple[str, ...]:
    issues = []
    title = report_payload.get("title")
    if not title:
        issues.append("missing_title")
    sections = report_payload.get("sections") or []
    section_titles = [section.get("title") for section in sections if isinstance(section, dict)]
    for required in REQUIRED_SECTIONS:
        if required not in section_titles:
            issues.append(f"missing_section:{required}")
    for section in sections:
        if isinstance(section, dict) and not section.get("items"):
            issues.append(f"empty_section:{section.get('title')}")
    guardrails = report_payload.get("guardrails") or []
    for guardrail in REQUIRED_GUARDRAILS:
        if guardrail not in guardrails:
            issues.append(f"missing_guardrail:{guardrail}")
    return tuple(issues)


def assert_report_v2_output(report_payload: dict[str, object]) -> None:
    issues = validate_report_v2_output(report_payload)
    if issues:
        raise ValueError("report_v2_output_invalid:" + ",".join(issues))
