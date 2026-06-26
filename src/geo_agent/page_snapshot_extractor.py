"""Deterministic page snapshot extractor from static HTML."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from html import unescape
from urllib.parse import urljoin, urlparse


class PageSnapshotExtractionError(ValueError):
    pass


@dataclass(frozen=True)
class ExtractedTable:
    caption: str | None
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def to_dict(self) -> dict[str, object]:
        return {"caption": self.caption, "headers": list(self.headers), "rows": [list(row) for row in self.rows]}


@dataclass(frozen=True)
class ExtractedFAQ:
    question: str
    answer: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ExtractedPageSnapshot:
    url: str
    canonical_url: str
    title: str | None
    meta: dict[str, str]
    headings: tuple[str, ...]
    paragraphs: tuple[str, ...]
    tables: tuple[ExtractedTable, ...]
    faqs: tuple[ExtractedFAQ, ...]
    json_ld_types: tuple[str, ...]
    html_sha256: str
    text_sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "url": self.url,
            "canonical_url": self.canonical_url,
            "title": self.title,
            "meta": dict(self.meta),
            "headings": list(self.headings),
            "paragraphs": list(self.paragraphs),
            "tables": [table.to_dict() for table in self.tables],
            "faqs": [faq.to_dict() for faq in self.faqs],
            "json_ld_types": list(self.json_ld_types),
            "html_sha256": self.html_sha256,
            "text_sha256": self.text_sha256,
        }


def extract_page_snapshot(url: str, html: str) -> ExtractedPageSnapshot:
    if not _valid_url(url):
        raise PageSnapshotExtractionError(f"Invalid snapshot URL: {url}")
    if not isinstance(html, str) or "<" not in html:
        raise PageSnapshotExtractionError("Snapshot HTML must be a non-empty HTML string.")
    canonical = _attr_first(html, "link", "href", required_attr=("rel", "canonical")) or url
    visible = _visible_text(html)
    json_ld = _json_ld_blocks(html)
    return ExtractedPageSnapshot(
        url=url,
        canonical_url=urljoin(url, canonical),
        title=_clean(_first_match(html, r"<title[^>]*>(.*?)</title>")),
        meta=_meta(html),
        headings=tuple(_clean_all(re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", html, flags=re.I | re.S))),
        paragraphs=tuple(_clean_all(re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.I | re.S))),
        tables=tuple(_tables(html)),
        faqs=tuple(_faqs(html, json_ld)),
        json_ld_types=tuple(sorted(_json_ld_types(json_ld))),
        html_sha256=_digest(html),
        text_sha256=_digest(visible),
    )


def _meta(html: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for tag in re.findall(r"<meta\b[^>]*>", html, flags=re.I | re.S):
        key = _attr(tag, "name") or _attr(tag, "property")
        value = _attr(tag, "content")
        if key and value:
            values[key] = _clean(value) or ""
    return values


def _tables(html: str) -> list[ExtractedTable]:
    tables = []
    for table_html in re.findall(r"<table\b[^>]*>(.*?)</table>", html, flags=re.I | re.S):
        caption = _clean(_first_match(table_html, r"<caption[^>]*>(.*?)</caption>"))
        headers = tuple(_clean_all(re.findall(r"<th[^>]*>(.*?)</th>", table_html, flags=re.I | re.S)))
        rows = []
        for row_html in re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, flags=re.I | re.S):
            cells = tuple(_clean_all(re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, flags=re.I | re.S)))
            if cells:
                rows.append(cells)
        tables.append(ExtractedTable(caption, headers, tuple(rows)))
    return tables


def _faqs(html: str, json_ld: tuple[object, ...]) -> list[ExtractedFAQ]:
    faqs: list[ExtractedFAQ] = []
    for item in json_ld:
        nodes = item if isinstance(item, list) else [item]
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                for entity in node.get("mainEntity", []):
                    if not isinstance(entity, dict):
                        continue
                    question = str(entity.get("name", "")).strip()
                    answer_node = entity.get("acceptedAnswer", {})
                    answer = answer_node.get("text", "") if isinstance(answer_node, dict) else ""
                    if question and answer:
                        faqs.append(ExtractedFAQ(_clean(question) or question, _clean(str(answer)) or str(answer)))
    if faqs:
        return faqs
    questions = _clean_all(re.findall(r"<dt[^>]*>(.*?)</dt>", html, flags=re.I | re.S))
    answers = _clean_all(re.findall(r"<dd[^>]*>(.*?)</dd>", html, flags=re.I | re.S))
    return [ExtractedFAQ(q, a) for q, a in zip(questions, answers)]


def _json_ld_blocks(html: str) -> tuple[object, ...]:
    blocks = []
    for raw in re.findall(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", html, flags=re.I | re.S):
        try:
            blocks.append(json.loads(raw.strip()))
        except json.JSONDecodeError:
            continue
    return tuple(blocks)


def _json_ld_types(blocks: tuple[object, ...]) -> set[str]:
    found: set[str] = set()
    def walk(value: object) -> None:
        if isinstance(value, dict):
            item_type = value.get("@type")
            if isinstance(item_type, str):
                found.add(item_type)
            elif isinstance(item_type, list):
                found.update(str(item) for item in item_type)
            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)
    for block in blocks:
        walk(block)
    return found


def _visible_text(html: str) -> str:
    without_scripts = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.I | re.S)
    return _clean(without_scripts) or ""


def _attr_first(html: str, tag: str, attr: str, *, required_attr: tuple[str, str]) -> str | None:
    for tag_text in re.findall(rf"<{tag}\b[^>]*>", html, flags=re.I | re.S):
        if (_attr(tag_text, required_attr[0]) or "").lower() == required_attr[1].lower():
            return _attr(tag_text, attr)
    return None


def _attr(tag: str, name: str) -> str | None:
    match = re.search(rf"\b{name}=[\"']([^\"']+)[\"']", tag, flags=re.I)
    return unescape(match.group(1).strip()) if match else None


def _first_match(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.I | re.S)
    return match.group(1) if match else None


def _clean_all(values: list[str]) -> list[str]:
    return [cleaned for value in values if (cleaned := _clean(value))]


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    text = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
