# Handoff Decision

## Decision

- Mode: `external_agent_development`
- Repository: `alexwang91/GEO-Agent`
- Base branch: `main`
- Planning branch: `v10-geo-research-integration-plan`
- Current loop: `Loop V10 GEO-research integration`
- First TODO: `V10-01 evidence-and-integration-map`

## Reason

Loop V10 integrates GEO measurement research into the core product while preserving GEO-Agent as a measurement, diagnosis, experiment, task-planning, and retest workbench. The loop starts with documentation-only evidence mapping before code changes.

## Required Merge Before Execution

The external runner reads state from `main`. Merge `v10-geo-research-integration-plan` into `main` before starting the V10 implementation loop.

## No Bootstrap

Do not bootstrap from scratch. Do not re-plan V1 through V9. Use `docs/progress.md` as the state source and implement only the first TODO milestone.

## Guardrails

- One milestone equals one branch, one PR, and CI verification.
- CI is VERIFY; never weaken tests.
- Keep CI network-free.
- Reuse existing V7/V8 code and `entity_resolution` helpers.
- Do not fabricate engine samples.
- Keep per-engine results primary; aggregates are directional.
- Keep single-sample results labeled directional.
- Keep Google AIO and Chinese AI engines manual-only unless sanctioned provider paths are added later.
- Keep content rewriting and GEOFlow behind plugin or downstream executor interfaces.
- Do not store secrets in artifacts.
