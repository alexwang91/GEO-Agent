# Next Steps Plan — Loop V9 Real-World Readiness

## Scope

This planning change re-establishes runner state and encodes the V9 backlog only. It must not implement V9 product milestones.

Execution model after this planning branch is merged:

- one milestone per branch;
- one PR per milestone;
- GitHub Actions `verify` is the verification gate;
- CI remains network-free;
- real network access is opt-in only and covered in CI with fake clients;
- no raw credentials may be persisted in artifacts, logs, manifests, databases, or UI state.

## V9-01 — concrete-live-crawler-client

Acceptance criteria:

- Ship a concrete HTTP implementation satisfying `crawl_provider_v2.FetchClient`.
- Respect robots.txt.
- Support timeout, bounded retry, and explicit error handling.
- Wire or retire any dead `page_inventory.py` `UrlLibPageFetcher` seam.
- Keep live fetch behind `allow_live_fetch=True`.
- CI uses fake clients only; no live network in CI.

Likely file targets:

- `src/geo_agent/crawl_provider_v2.py`
- `src/geo_agent/page_inventory.py`
- `tests/test_v9_01_live_crawler_client.py`
- `docs/limitations.md`

Verification:

- `PYTHONPATH=src python -m unittest discover -s tests -v`
- `python tools/check_python_style.py`
- `python tools/check_type_annotations.py`
- `python tools/check_coverage.py`

## V9-02 — manual-capture-import-ux

Acceptance criteria:

- Add a polished manual-capture import schema for ChatGPT Search, Perplexity, Gemini, and Google AIO evidence.
- Accept answer text, citations, engine, captured_at, region, language, and query metadata.
- Validate imported evidence and route it into the existing evidence graph.
- Redaction-check imported data before persistence or artifact generation.
- Document the manual-capture workflow as the realistic multi-engine path while live APIs remain planned.

Likely file targets:

- `src/geo_agent/recorded_dataset.py`
- `src/geo_agent/engine_sampling.py`
- `src/geo_agent/artifact_safety.py`
- `tests/test_v9_02_manual_capture_import.py`
- `docs/limitations.md`

Verification:

- deterministic fixture tests only;
- no live provider calls;
- redaction tests for raw credential patterns.

## V9-03 — desktop-real-report-loading

Acceptance criteria:

- Replace hardcoded-only desktop rendering with loading a real generated audit package: manifest plus `report.json`.
- Keep demo data available only when explicitly labeled demo.
- Add empty, loading, and error states.
- Preserve provider/status overclaim guardrails.

Likely file targets:

- `apps/desktop/src/App.jsx`
- `apps/desktop/src/reportArtifacts.js`
- `apps/desktop/src/pkgLoader.js`
- desktop tests or deterministic JS helper tests if available

Verification:

- no new live network calls;
- demo artifacts are visibly labeled demo;
- generated artifacts are distinguishable from fixtures.

## V9-04 — desktop-run-flow-wiring

Acceptance criteria:

- Wire truthful `list_providers` status display.
- Add brand-profile form flow.
- Add query-space preview.
- Add run-audit trigger so a user can move project -> audit -> real report inside the app.
- Keep planned providers labeled planned.

Likely file targets:

- `apps/desktop/src/App.jsx`
- `apps/desktop/src/reportArtifacts.js`
- backend/desktop bridge files if present
- provider status copy helpers

Verification:

- deterministic tests or static helper tests;
- no live network in CI;
- UI copy preserves provider truth labels.

## V9-05 — extraction-regression-on-realistic-data

Acceptance criteria:

- Extend extraction eval harness with realistic non-synthetic answer/citation samples.
- Track precision and recall for entity and citation extraction.
- Gate regressions in CI with fixture-backed tests.
- Preserve existing V8 improvements: alias, boundary, diacritics, URL extraction, and substring false-positive prevention.

Likely file targets:

- `tests/fixtures/`
- `tests/test_v9_05_extraction_regression.py`
- `src/geo_agent/entity_resolution.py`
- `src/geo_agent/engine_sampling.py`

Verification:

- network-free fixture tests;
- regression thresholds explicit and stable.

## V9-06 — real-brand-validation-run

Acceptance criteria:

- Perform one consented real-brand end-to-end validation outside CI.
- Use real crawl plus manual-captured answers across engines.
- Run extraction, diagnosis, tasks, and retest planning.
- Record sanitized findings, surprises, and limits in docs.
- Commit no private data, raw answers with sensitive content, credentials, or unredacted customer material.

Likely file targets:

- `docs/v9-real-brand-validation.md`
- sanitized fixture summaries if safe
- `docs/limitations.md`

Verification:

- docs and redaction review;
- CI remains network-free.

## V9-07 — limitations-and-provider-matrix-refresh

Acceptance criteria:

- Update README/showcase, provider matrix, and limitations to state exactly what is real after V9.
- OpenAI-compatible must not be described as ChatGPT Search.
- Planned providers must remain planned unless implemented and verified.
- Single-sample results stay directional.
- Demo, fixture, simulated, manual, and live outputs must be clearly distinguished.

Likely file targets:

- `README.md`
- `docs/provider-status-language.md`
- `docs/limitations.md`
- `docs/v8-changelog.md` or a new V9 changelog if appropriate

Verification:

- product contract tests;
- docs consistency checks;
- full GitHub Actions `verify`.
