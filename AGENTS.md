# Agent Notes

## Required read list

1. `docs/progress.md`
2. `docs/loop-v10.md`
3. `docs/v10-real-case.md`
4. `docs/geo-research-integration.md`
5. `docs/handoff-decision.md`
6. `docs/runner-prompt.md`
7. `docs/loop-trace.md`
8. `docs/v8-changelog.md`
9. `docs/product-contract.md`
10. `docs/provider-status-language.md`
11. `docs/limitations.md`

## Current state

- This is an existing advanced repo. Do not bootstrap from scratch.
- V1 through V9 are DONE history.
- Current loop is Loop V10: GEO-research integration.
- First TODO is `V10-01 evidence-and-integration-map`.
- State source is `docs/progress.md`.
- Planning branch is `v10-geo-research-integration-plan`.
- External implementation branches must start from current `main` after the planning branch is merged.

## Product boundary

- GEO-Agent is an AI search visibility measurement, diagnosis, and experiment workbench.
- Measurement research belongs in the core.
- Rewrite resources and distribution systems belong behind plugin or downstream-executor interfaces.
- The core product must not generate final marketing copy.

## Guardrails

- One milestone equals one branch, one PR, and CI verification.
- Fix V10 milestones in priority order.
- Reuse existing V7/V8 modules where applicable.
- Keep CI network-free.
- Use only explicit captured or sanctioned provider evidence for engine answers.
- Keep per-engine results primary.
- Label single-sample and aggregate results as directional.
- Keep Google AIO and Chinese AI engines manual-only unless a sanctioned provider path is added later.
- Do not store secrets in artifacts, logs, manifests, databases, or UI state.
