# Agent Instructions

Read these files before development:

- `docs/autonomous-runner.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v7.md`
- `docs/project-evaluation-v7.md`
- `docs/development-principles.md`
- `docs/feedback-log.md`
- `docs/loop-trace.md`
- `docs/handoff-decision.md`
- `docs/stopper-policy.md`
- `.github/pull_request_template.md`

## State Sources

`docs/progress.md` is the single milestone state source. `docs/next-steps-plan.md` contains detailed acceptance criteria, file targets, and verification notes.

Current active product loop: V7 AI Search Visibility Experiment Workbench. V7-01 through V7-15 are complete in sequence. V7-11 and V7-14 are complete. After the V7-15 branch merges, the first TODO is `V7-16`, the claim fidelity audit slice.

## Workflow Discipline

Use the GitHub connector for repository work. Use one branch and one PR per milestone. Use CI as VERIFY.

## Product Guardrails

- Preserve fixture-only CI unless a milestone explicitly adds fake-client provider tests.
- Planned providers remain planned.
- OpenAI-compatible output is not ChatGPT Search.
- Do not weaken tests or add dummy files.
