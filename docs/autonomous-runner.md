# Autonomous Runner Contract

## Repository

- Repository: `alexwang91/GEO-Agent`
- Base branch: `main`
- Planning branch: `v9-readiness-plan`
- Current loop: V9 real-world readiness
- First TODO: V9-01 concrete-live-crawler-client

## State Source

`docs/progress.md` is the single milestone state source. The runner must read it before choosing work.

## Required Read List

Read these files before starting a milestone:

1. `AGENTS.md`
2. `docs/progress.md`
3. `docs/next-steps-plan.md`
4. `docs/loop-v9.md`
5. `docs/project-evaluation-v9.md`
6. `docs/handoff-decision.md`
7. `docs/runner-prompt.md`
8. `docs/loop-trace.md`
9. `docs/v8-changelog.md`
10. `docs/product-contract.md`
11. `docs/provider-status-language.md`
12. `docs/limitations.md`

## Execution Rules

- Do not bootstrap from scratch.
- Do not re-plan V7 or V8.
- Choose the first TODO from `docs/progress.md`.
- Execute exactly one V9 milestone per branch and PR.
- Update `docs/progress.md` only after the milestone implementation is complete and verified.
- Use GitHub Actions `verify` as the verification gate.
- Keep CI network-free.
- Real network access must be explicit opt-in and tested with fake clients in CI.
- Never persist raw credentials into artifacts, logs, manifests, databases, or UI state.

## Handoff Rule

The external runner reads state from `main`. The planning branch must be merged into `main` before a real V9 execution loop begins.
