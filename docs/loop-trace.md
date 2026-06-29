# Trace

## Current Loop

- Loop: V9F evidence-driven real-case fixes
- State source: `docs/progress.md`
- Base branch: `main`
- Planning branch: `v9f-real-case-fixes`
- First TODO: `V9F-2 fix-manual-capture-recommendations-and-mention-dedup`

## 2026-06-29 STEP 0 — Re-established Runner State

- Created planning branch `v9f-real-case-fixes` from current `main`.
- Re-established `docs/progress.md` as the V9F state source with V1 through V9 marked DONE and V9F-1 through V9F-7 marked TODO.
- Added `docs/loop-v9f.md` as the loop directive.
- Replaced `docs/v9-real-case.md` with the sanitized Huawei three-engine real-case evidence.
- Refreshed `AGENTS.md`, `docs/handoff-decision.md`, and `docs/runner-prompt.md` so the first TODO is `V9F-1 fix-recommendation-matching`.
- Guardrails preserved: one milestone/one PR, CI verifies, network-free CI, reuse V7/V8 code, no fabricated engine samples, Google AIO manual-only, directional labeling for small samples and aggregate scores, no raw credentials.

## 2026-06-29 V9F-1 — Recommendation Matching

- Branch: `v9f-1-fix-recommendation-matching`
- PR: #105
- Files changed: `src/geo_agent/visibility_scoring.py`, `tests/test_v9f_01_recommendation_matching.py`, `docs/progress.md`, `docs/loop-trace.md`
- Bug fixed: recommendation matching no longer requires exact full-string equality.
- Implementation: `_same_entity` now delegates to existing token-boundary entity matching through `has_entity`.
- Regression coverage:
  - `Huawei` matches `Huawei Watch GT 6 Pro` as a recommendation.
  - `Apple Watch` still matches as a recommendation.
  - `Huawei` does not match inside unrelated token `MegaHuaweiX`.
- CI: GitHub Actions `verify` run 272 passed on commit `11de3337b2bc95242e8841689ae40b6a7df0cd23` before docs status update.
- Final docs update committed after CI pass; re-run CI on final head before merging.

## Guardrails

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths, not fabricated model/web-search output.
- Do not mark a V9F milestone DONE without the deterministic test/check and CI verification.
- Do not add new analytics modules.
