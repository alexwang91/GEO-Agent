"""Deterministic provider output eval harness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .answer_provider import _payload_from_openai_response
from .engine_sampling import EngineRun, run_from_payload
from .provider_access import ProviderAccessError


@dataclass(frozen=True)
class ProviderOutputEvalCase:
    name: str
    response: Mapping[str, object]
    query: str = "What is Acme AI?"
    engine: str = "openai_compatible"
    region: str = "US"
    language: str = "en"
    expected_error: str | None = None
    expected_citations: tuple[str, ...] = ()
    expected_mentions: tuple[str, ...] = ()
    expected_recommendations: tuple[str, ...] = ()
    forbidden_substrings: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProviderOutputEvalResult:
    case_name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, object]:
        return {"case_name": self.case_name, "passed": self.passed, "message": self.message}


@dataclass(frozen=True)
class ProviderOutputEvalSummary:
    results: tuple[ProviderOutputEvalResult, ...]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.results if result.passed)

    @property
    def failed_count(self) -> int:
        return len(self.results) - self.passed_count

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "passed_count": self.passed_count,
            "failed_count": self.failed_count,
            "results": [result.to_dict() for result in self.results],
        }


def evaluate_provider_output_cases(cases: tuple[ProviderOutputEvalCase, ...]) -> ProviderOutputEvalSummary:
    return ProviderOutputEvalSummary(results=tuple(_evaluate_case(case) for case in cases))


def _evaluate_case(case: ProviderOutputEvalCase) -> ProviderOutputEvalResult:
    try:
        run = provider_response_to_run(case)
    except ProviderAccessError as exc:
        if case.expected_error and case.expected_error in str(exc):
            return ProviderOutputEvalResult(case.name, True, "expected error")
        return ProviderOutputEvalResult(case.name, False, f"unexpected error: {exc}")

    if case.expected_error:
        return ProviderOutputEvalResult(case.name, False, "expected an error but parsing succeeded")

    checks = [
        _expect_tuple("citations", run.citations, case.expected_citations),
        _expect_tuple("mentions", run.mentions, case.expected_mentions),
        _expect_tuple("recommendations", run.recommendations, case.expected_recommendations),
        _expect_forbidden(run, case.forbidden_substrings),
    ]
    failures = [check for check in checks if check]
    if failures:
        return ProviderOutputEvalResult(case.name, False, "; ".join(failures))
    return ProviderOutputEvalResult(case.name, True, "passed")


def provider_response_to_run(case: ProviderOutputEvalCase) -> EngineRun:
    payload = _payload_from_openai_response(dict(case.response))
    return run_from_payload(
        payload,
        engine=case.engine,
        query=case.query,
        region=case.region,
        language=case.language,
        timestamp=str(payload.get("timestamp", "")),
    )


def _expect_tuple(label: str, actual: tuple[str, ...], expected: tuple[str, ...]) -> str:
    if expected and actual != expected:
        return f"{label} expected {expected!r} got {actual!r}"
    return ""


def _expect_forbidden(run: EngineRun, forbidden: tuple[str, ...]) -> str:
    if not forbidden:
        return ""
    combined = "\n".join(
        [run.raw_answer, *run.citations, *run.mentions, *run.recommendations, *run.source_domains]
    )
    leaked = [item for item in forbidden if item and item in combined]
    if leaked:
        return f"forbidden output substring(s): {', '.join(leaked)}"
    return ""
