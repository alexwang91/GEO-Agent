# Trace

## Current Loop

- Loop: V9F evidence-driven real-case fixes
- State source: `docs/progress.md`
- Base branch: `main`
- Planning branch: `v9f-real-case-fixes`
- First TODO: `V9F-6 record-evidence-and-honesty`

## 2026-06-29 STEP 0 — Re-established Runner State

- Created planning branch `v9f-real-case-fixes` from current `main`.
- Re-established `docs/progress.md` as the V9F state source with V1 through V9 marked DONE and V9F-1 through V9F-7 marked TODO.
- Added `docs/loop-v9f.md` as the loop directive.
- Replaced `docs/v9-real-case.md` with the sanitized Huawei three-engine real-case evidence.
- Refreshed `AGENTS.md`, `docs/handoff-decision.md`, and `docs/runner-prompt.md` so the first TODO is `V9F-1 fix-recommendation-matching`.
- Guardrails preserved.

## 2026-06-29 V9F-1 — Recommendation Matching

- Branch: `v9f-1-fix-recommendation-matching`
- PR: #105
- CI: GitHub Actions `verify` run 274 passed on final PR head.
- Merged to `main`.

## 2026-06-29 V9F-2 — Manual Capture Recommendations and Mention Dedup

- Branch: `v9f-2-manual-capture-recommendations-dedup`
- PR: #106
- Manual captures now preserve `recommendations` through `EngineRun` conversion.
- Fallback mention extraction now returns unique longest mention text for overlapping aliases.
- CI: GitHub Actions `verify` run 279 passed on final PR head.
- Merged to `main`.

## 2026-06-29 V9F-3 — Capture To Package Bridge

- Branch: `v9f-3-capture-to-package-bridge`
- PR: #107
- Added `AuditRunner.run_with_captured_runs()` for captured `EngineRun` records without query generation.
- Added CLI subcommand `capture-package` for manual capture packages.
- CI: GitHub Actions `verify` run 283 passed on final PR head.
- Merged to `main`.

## 2026-06-29 V9F-4 — Per-Engine Component Report

- Branch: `v9f-4-report-per-engine-component`
- PR: #108
- Added report v2 per-engine component summary and directional aggregate labeling.
- CI: GitHub Actions `verify` run 288 passed on final PR head.
- Merged to `main`.

## 2026-06-29 V9F-5 — Desktop Multi-Engine Render

- Branch: `v9f-5-desktop-render-multi-engine`
- PR: #109
- Desktop artifact loader now parses report v2 `Per-Engine Breakdown` and `Directional Aggregate` sections.
- Desktop report view renders per-engine component metrics before legacy score cards.
- Demo artifacts remain explicitly labeled as demo and emit demo warnings.
- Regression coverage structurally checks per-engine parsing and render ordering.
- CI: GitHub Actions `verify` run 290 passed on commit `4914b1662703e7abb818cc81c803ef1480869848` before docs status update.
- Final docs update committed after CI pass; re-run CI on final head before merging.

## Guardrails

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths.
- Do not mark a V9F milestone DONE without the deterministic test/check and CI verification.
- Do not add new analytics modules.
