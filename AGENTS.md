# Agent Notes

## Required read list

1. `docs/progress.md`
2. `docs/next-steps-plan.md`
3. `docs/loop-v9.md`
4. `docs/handoff-decision.md`
5. `docs/runner-prompt.md`
6. `docs/loop-trace.md`
7. `docs/v8-changelog.md`
8. `docs/product-contract.md`
9. `docs/provider-status-language.md`
10. `docs/limitations.md`

## Current state

- V1 through V8 are DONE history.
- V9 is one vertical slice.
- First TODO is V9-1 minimal real FetchClient.
- State source is `docs/progress.md`.
- Actual planning branch is `v9-slice-plan`.
- Requested planning branch was `v9-vertical-slice-plan`.

## Guardrails

- Do not bootstrap from scratch.
- Do not re-plan V7 or V8.
- Do not add analytics modules.
- Real network access is opt-in and never in CI.
- DONE requires real-case evidence in docs.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
