# Trace

## Current Loop

- Loop: V10 GEO-research integration
- State source: `docs/progress.md`
- Base branch: `main`
- Planning branch: `v10-geo-research-integration-plan`
- First TODO: `V10-07 citation-level-feature-schema`

## 2026-06-29 STEP 0 — Re-established Runner State

- Created planning branch `v10-geo-research-integration-plan` from current `main` after the exact requested branch name was blocked by the connector safety layer.
- Re-established `docs/progress.md` as the V10 state source with V1 through V9 marked DONE and V10-01 through V10-17 marked TODO.
- Added `docs/loop-v10.md` as the loop directive.
- Added `docs/v10-real-case.md` with the sanitized Huawei three-engine real-case evidence.
- Added `docs/geo-research-integration.md` with source-to-module mapping and the identity boundary.
- Refreshed `AGENTS.md`, `docs/handoff-decision.md`, and `docs/runner-prompt.md` so the first TODO is `V10-01 evidence-and-integration-map`.
- Preserved guardrails: per-engine first, directional labels, manual-only AIO/Chinese engines, no fabricated answers, network-free CI, reuse V7/V8 modules, and plugin-only optimization execution.

## 2026-06-29 V10-01 — Evidence and Integration Map

- Branch: `v10-geo-research-integration-plan`
- PR: #115
- Files changed: runner-facing docs only.
- Added Huawei three-engine real-case matrix and GEO research resource-to-module mapping.
- CI: GitHub Actions `verify` run 332 passed on PR head.
- Merged to `main`.

## 2026-06-29 V10-02 — Recommendation Matching

- Branch: `v10-02-recommendation-matching`
- PR: #116
- Existing implementation: `_same_entity` delegates to `has_entity`, reusing token-boundary entity matching.
- Existing historical coverage: `tests/test_v9f_01_recommendation_matching.py` covers Huawei product recommendation matching, Apple Watch matching, and unrelated-token false positives.
- Added V10-named regression coverage in `tests/test_v10_02_recommendation_matching.py`.
- CI: GitHub Actions `verify` run 334 passed.
- Merged to `main`.

## 2026-06-29 V10-03 — Manual Capture Recommendations and Mention Handling

- Branch: `v10-03-manual-capture-dedup`
- PR: #117
- Existing implementation preserves `recommendations` through manual capture import and `EngineRun` conversion.
- Existing implementation normalizes fallback mentions by longest non-overlapping entity spans.
- Added V10-named regression coverage in `tests/test_v10_03_manual_capture_recommendations_dedup.py`.
- CI: GitHub Actions `verify` run 336 passed.
- Merged to `main`.

## 2026-06-29 V10-04 — Capture To Package Bridge

- Branch: `v10-04-capture-package-bridge`
- PR: #118
- Existing implementation exposes `AuditRunner.run_with_captured_runs()` and CLI `capture-package`.
- Added V10-named regression coverage in `tests/test_v10_04_capture_package_bridge.py` for two manual captures across two engines producing manifest, report, and SQLite package artifacts without query generation.
- CI: GitHub Actions `verify` run 338 passed.
- Merged to `main`.

## 2026-06-29 V10-05 — Position-Adjusted Visibility

- Branch: `v10-05-visibility-metrics`
- PR: #119
- Replaced the naive character-position rank score with sentence-level position-adjusted word-count visibility.
- Added a deterministic subjective-impression-style component based on mention, owned citation, recommendation, and prominence signals.
- Added V10 regression coverage in `tests/test_v10_05_visibility_metrics.py`.
- CI: GitHub Actions `verify` run 340 passed.
- Merged to `main`.

## 2026-06-29 V10-06 — Report Selection Absorption Attribution

- Branch: `v10-06-report-decomposition`
- Added report v2 per-engine decomposition for selection, absorption, and attribution.
- Added a dedicated `Selection Absorption Attribution` report section and carried the three-layer breakdown into the aggregate metric summary.
- Added V10 regression coverage in `tests/test_v10_06_report_decomposition.py`.

## Guardrails

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths.
- Do not mark a V10 milestone DONE without the deterministic test/check and CI verification.
- Do not turn GEO-Agent into a content writer.
- Keep rewrite skills and GEOFlow behind plugin/downstream executor interfaces.
