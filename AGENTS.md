# Agent Notes

## Required read list

1. `docs/progress.md`
2. `docs/loop-v9f.md`
3. `docs/v9-real-case.md`
4. `docs/handoff-decision.md`
5. `docs/runner-prompt.md`
6. `docs/loop-trace.md`
7. `docs/v8-changelog.md`
8. `docs/product-contract.md`
9. `docs/provider-status-language.md`
10. `docs/limitations.md`

## Current state

- This is an existing advanced repo. Do not bootstrap from scratch.
- V1 through V9 are DONE history.
- Current loop is Loop V9F: evidence-driven real-case fixes from the Huawei three-engine validation run.
- First TODO is `V9F-1 fix-recommendation-matching`.
- State source is `docs/progress.md`.
- Planning branch is `v9f-real-case-fixes`.
- External implementation branches must start from current `main` after the planning branch is merged.

## Guardrails

- One milestone equals one branch, one PR, and CI verification.
- Fix V9F milestones in priority order.
- Do not add new analytics modules.
- Reuse existing V7/V8 code and entity-resolution helpers.
- CI must remain network-free.
- Never fabricate AI-engine answers or treat model/web-search output as a real engine sample.
- Google AIO remains `manual_only`; AIO share links are gated and not auto-capturable.
- Single-sample and aggregate results must be labeled directional.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
