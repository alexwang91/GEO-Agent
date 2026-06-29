# Handoff Decision

## Decision

- Mode: `external_agent_development`
- Repository: `alexwang91/GEO-Agent`
- Base branch: `main`
- Planning branch: `v9f-real-case-fixes`
- Current loop: `Loop V9F evidence-driven real-case fixes`
- First TODO: `V9F-1 fix-recommendation-matching`

## Reason

A real three-engine Huawei validation run surfaced concrete product bugs and reporting gaps. The next loop must fix those bugs in priority order using existing V7/V8 code, deterministic tests, and CI verification. This is not a new analytics-module loop.

## Required Merge Before Execution

The external runner reads state from `main`. Merge `v9f-real-case-fixes` into `main` before starting the V9F implementation loop.

## No Bootstrap

Do not bootstrap from scratch. Do not re-plan V7, V8, or V9. Use `docs/progress.md` as the state source and implement only the first TODO milestone.

## Guardrails

- One milestone equals one branch, one PR, and CI verification.
- CI is VERIFY; never weaken tests.
- Keep CI network-free.
- Reuse existing V7/V8 code and `entity_resolution` helpers.
- Do not add new analytics modules.
- Do not fabricate engine samples.
- Keep Google AIO `manual_only`.
- Keep single-sample and aggregate results labeled directional.
- No raw credentials in artifacts.
