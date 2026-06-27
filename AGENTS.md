# Agent Notes

## Required read list

Read these files before choosing or executing work:

1. `docs/progress.md`
2. `docs/next-steps-plan.md`
3. `docs/loop-v9.md`
4. `docs/project-evaluation-v9.md`
5. `docs/autonomous-runner.md`
6. `docs/handoff-decision.md`
7. `docs/runner-prompt.md`
8. `docs/loop-trace.md`
9. `docs/v8-changelog.md`
10. `docs/product-contract.md`
11. `docs/provider-status-language.md`
12. `docs/limitations.md`

## Current state

- V1 through V8 are DONE history.
- Loop V9 real-world readiness is active planning state.
- First TODO is V9-01 concrete-live-crawler-client.
- `docs/progress.md` is the single milestone state source.
- Planning branch is `v9-readiness-plan`.

## Guardrails

- Do not bootstrap from scratch.
- Do not re-plan V7 or V8.
- Use one branch and one PR per V9 milestone.
- Keep CI network-free.
- Real network access must be explicit opt-in and covered with fake clients in CI.
- Never persist raw credentials into artifacts, logs, manifests, databases, or UI state.
- Planned providers remain planned until implemented and verified.
