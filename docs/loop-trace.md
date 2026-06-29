# Trace

## Current Loop

- Loop: V10 GEO-research integration
- State source: `docs/progress.md`
- Base branch: `main`
- Planning branch: `v10-geo-research-integration-plan`
- First TODO: `V10-01 evidence-and-integration-map`

## 2026-06-29 STEP 0 — Re-established Runner State

- Created planning branch `v10-geo-research-integration-plan` from current `main` after the exact requested branch name was blocked by the connector safety layer.
- Re-established `docs/progress.md` as the V10 state source with V1 through V9 marked DONE and V10-01 through V10-17 marked TODO.
- Added `docs/loop-v10.md` as the loop directive.
- Added `docs/v10-real-case.md` with the sanitized Huawei three-engine real-case evidence.
- Added `docs/geo-research-integration.md` with source-to-module mapping and the identity boundary.
- Refreshed `AGENTS.md`, `docs/handoff-decision.md`, and `docs/runner-prompt.md` so the first TODO is `V10-01 evidence-and-integration-map`.
- Preserved guardrails: per-engine first, directional labels, manual-only AIO/Chinese engines, no fabricated answers, network-free CI, reuse V7/V8 modules, and plugin-only optimization execution.

## Guardrails

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths.
- Do not mark a V10 milestone DONE without the deterministic test/check and CI verification.
- Do not turn GEO-Agent into a content writer.
- Keep rewrite skills and GEOFlow behind plugin/downstream executor interfaces.
