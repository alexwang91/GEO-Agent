"""Manual answer-capture import for multi-engine evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .artifact_safety import assert_artifacts_safe
from .engine_sampling import EngineRun, run_from_payload
from .provider_access import ProviderAccessError

ManualCaptureEngine = Literal["chatgpt_search", "perplexity", "gemini", "google_aio", "manual_import"]
_ALLOWED_ENGINES = {"chatgpt_search", "perplexity", "gemini", "google_aio", "manual_import"}
_REQUIRED_FIELDS = ("engine", "query", "answer_text", "captured_at")


@dataclass(frozen=True)
class ManualCaptureRecord:
    engine: ManualCaptureEngine
    query: str
    answer_text: str
    citations: tuple[str, ...]
    captured_at: str
    region: str = "unknown"
    language: str = "unknown"
    brand: str | None = None
    brand_aliases: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "engine": self.engine,
            "query": self.query,
            "raw_answer": self.answer_text,
            "citations": list(self.citations),
            "timestamp": self.captured_at,
            "region": self.region,
            "language": self.language,
        }
        if self.brand:
            payload["brand"] = self.brand
        if self.brand_aliases:
            payload["brand_aliases"] = list(self.brand_aliases)
        if self.recommendations:
            payload["recommendations"] = list(self.recommendations)
        return payload

    def to_engine_run(self) -> EngineRun:
        return run_from_payload(
            self.to_payload(),
            engine=self.engine,
            query=self.query,
            region=self.region,
            language=self.language,
            timestamp=self.captured_at,
        )


def import_manual_capture(payload: dict[str, object], *, forbidden_values: tuple[str, ...] = ()) -> ManualCaptureRecord:
    """Validate a pasted-answer capture and return a normalized record.

    This is the realistic bridge for ChatGPT Search, Perplexity, Gemini, and Google AIO evidence while live provider APIs remain planned.
    """

    assert_artifacts_safe({"manual_capture": payload}, forbidden_values=forbidden_values)
    _require_fields(payload)
    engine = _engine(payload["engine"])
    captured_at = _timestamp(str(payload["captured_at"]))
    query = _non_empty(payload["query"], "query")
    answer_text = _non_empty(payload["answer_text"], "answer_text")
    citations = _string_tuple(payload.get("citations", ()), "citations")
    brand_aliases = _string_tuple(payload.get("brand_aliases", ()), "brand_aliases")
    recommendations = _string_tuple(payload.get("recommendations", ()), "recommendations")
    brand = str(payload.get("brand", "")).strip() or None
    region = str(payload.get("region", "unknown")).strip() or "unknown"
    language = str(payload.get("language", "unknown")).strip() or "unknown"
    record = ManualCaptureRecord(
        engine,
        query,
        answer_text,
        citations,
        captured_at,
        region,
        language,
        brand,
        brand_aliases,
        recommendations,
    )
    assert_artifacts_safe({"manual_capture_normalized": record.to_payload()}, forbidden_values=forbidden_values)
    return record


def import_manual_captures(payloads: list[dict[str, object]], *, forbidden_values: tuple[str, ...] = ()) -> tuple[ManualCaptureRecord, ...]:
    return tuple(import_manual_capture(payload, forbidden_values=forbidden_values) for payload in payloads)


def manual_captures_to_engine_runs(records: tuple[ManualCaptureRecord, ...]) -> tuple[EngineRun, ...]:
    return tuple(record.to_engine_run() for record in records)


def _require_fields(payload: dict[str, object]) -> None:
    missing = [field for field in _REQUIRED_FIELDS if not payload.get(field)]
    if missing:
        raise ProviderAccessError(f"Manual capture missing required fields: {', '.join(missing)}")


def _engine(value: object) -> ManualCaptureEngine:
    engine = str(value).strip().lower()
    if engine not in _ALLOWED_ENGINES:
        raise ProviderAccessError(f"Unsupported manual capture engine: {value}")
    return engine  # type: ignore[return-value]


def _timestamp(value: str) -> str:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ProviderAccessError("captured_at must be ISO-8601.") from exc
    return value


def _non_empty(value: object, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ProviderAccessError(f"{field} is required.")
    return text


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if not isinstance(value, (list, tuple)):
        raise ProviderAccessError(f"{field} must be a list of strings.")
    output = tuple(str(item).strip() for item in value if str(item).strip())
    return output
