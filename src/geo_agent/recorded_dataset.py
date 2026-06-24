"""Recorded audit dataset loader for fixture-based GEO audits."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from .engine_sampling import RecordedRunAdapter
from .entity_profile import EntityProfile, validate_entity_profile


class RecordedDatasetError(ValueError):
    pass


@dataclass(frozen=True)
class RecordedAuditDataset:
    profile: EntityProfile
    pages: dict[str, str]
    engine_adapter: RecordedRunAdapter
    manual_urls: list[str]
    sitemap_urls: list[str]
    max_queries: int | None
    metadata: dict[str, object]


def load_recorded_dataset(path: str | Path) -> RecordedAuditDataset:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return load_recorded_dataset_from_mapping(payload)


def load_recorded_dataset_from_mapping(payload: Mapping[str, Any]) -> RecordedAuditDataset:
    if not isinstance(payload, Mapping):
        raise RecordedDatasetError("Recorded dataset must be a mapping/object.")
    _require_sections(payload, ("profile", "pages", "recorded_runs", "audit"))
    profile = validate_entity_profile(payload["profile"])
    pages = _pages(payload["pages"])
    audit = _audit(payload["audit"])
    recorded = _recorded_runs(payload["recorded_runs"])
    return RecordedAuditDataset(
        profile=profile,
        pages=pages,
        engine_adapter=RecordedRunAdapter(recorded["engine"], recorded["runs"]),
        manual_urls=audit["manual_urls"],
        sitemap_urls=audit["sitemap_urls"],
        max_queries=audit["max_queries"],
        metadata=dict(payload.get("metadata", {})),
    )


def _require_sections(payload: Mapping[str, Any], sections: tuple[str, ...]) -> None:
    missing = [section for section in sections if section not in payload]
    if missing:
        raise RecordedDatasetError(f"Recorded dataset missing required section(s): {', '.join(missing)}")


def _pages(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise RecordedDatasetError("pages must be a mapping of URL to HTML.")
    pages: dict[str, str] = {}
    for url, html in value.items():
        if not isinstance(url, str) or not _valid_url(url):
            raise RecordedDatasetError(f"Invalid page URL: {url}")
        if not isinstance(html, str) or "<" not in html:
            raise RecordedDatasetError(f"Page HTML must be a string for {url}")
        pages[url] = html
    if not pages:
        raise RecordedDatasetError("pages must contain at least one page.")
    return pages


def _audit(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RecordedDatasetError("audit must be a mapping/object.")
    manual_urls = _url_list(value.get("manual_urls", []), "audit.manual_urls")
    sitemap_urls = _url_list(value.get("sitemap_urls", []), "audit.sitemap_urls")
    max_queries = value.get("max_queries")
    if max_queries is not None and (not isinstance(max_queries, int) or max_queries <= 0):
        raise RecordedDatasetError("audit.max_queries must be a positive integer when present.")
    return {"manual_urls": manual_urls, "sitemap_urls": sitemap_urls, "max_queries": max_queries}


def _recorded_runs(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RecordedDatasetError("recorded_runs must be a mapping/object.")
    engine = value.get("engine")
    runs = value.get("runs")
    if not isinstance(engine, str) or not engine.strip():
        raise RecordedDatasetError("recorded_runs.engine must be a non-empty string.")
    if not isinstance(runs, Mapping) or not runs:
        raise RecordedDatasetError("recorded_runs.runs must be a non-empty query-to-run mapping.")
    normalized: dict[str, dict[str, object]] = {}
    for query, run in runs.items():
        if not isinstance(query, str) or not query.strip():
            raise RecordedDatasetError("recorded run query keys must be non-empty strings.")
        if not isinstance(run, Mapping):
            raise RecordedDatasetError(f"recorded run for {query} must be a mapping/object.")
        if not isinstance(run.get("raw_answer"), str):
            raise RecordedDatasetError(f"recorded run for {query} must include raw_answer string.")
        normalized[query] = {
            "timestamp": run.get("timestamp"),
            "raw_answer": run.get("raw_answer", ""),
            "citations": _string_list(run.get("citations", []), f"recorded_runs.runs[{query}].citations"),
            "mentions": _string_list(run.get("mentions", []), f"recorded_runs.runs[{query}].mentions"),
            "recommendations": _string_list(run.get("recommendations", []), f"recorded_runs.runs[{query}].recommendations"),
        }
    return {"engine": engine.strip(), "runs": normalized}


def _url_list(value: object, field: str) -> list[str]:
    values = _string_list(value, field)
    for item in values:
        if not _valid_url(item):
            raise RecordedDatasetError(f"{field} contains invalid URL: {item}")
    return values


def _string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list):
        raise RecordedDatasetError(f"{field} must be a list of strings.")
    if any(not isinstance(item, str) for item in value):
        raise RecordedDatasetError(f"{field} must contain only strings.")
    return [item for item in value]


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
