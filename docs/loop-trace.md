# Trace

## Current Loop

- Loop: V9F evidence-driven real-case fixes
- State source: `docs/progress.md`
- Base branch: `main`
- Planning branch: `v9f-real-case-fixes`
- First TODO: `V9F-3 capture-to-package-bridge`

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
- Files changed: `src/geo_agent/manual_capture.py`, `src/geo_agent/engine_sampling.py`, `src/geo_agent/entity_resolution.py`, `tests/test_v9_02_manual_capture.py`, `docs/progress.md`, `docs/loop-trace.md`
- Manual captures now preserve `recommendations` through `EngineRun` conversion.
- Fallback mention extraction now returns unique longest mention text for overlapping aliases.
- Regression coverage checks recommendation scoring through manual capture and deduped Huawei Watch Fit 5 fallback mentions.
- CI: GitHub Actions `verify` run 277 passed on commit `a35a0ab50348b1cd50fefe53db9738d1449274ac` before docs status update.
- Final docs update committed after CI pass; re-run CI on final head before merging.

## Guardrails

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths.
- Do not mark a V9F milestone DONE without the deterministic test/check and CI verification.
- Do not add new analytics modules.
