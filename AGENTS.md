# Agent Instructions

Read these files before development:

- `docs/autonomous-runner.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v7.md`
- `docs/project-evaluation-v7.md`
- `docs/loop-v8.md`
- `docs/project-evaluation-v8.md`
- `docs/development-principles.md`
- `docs/feedback-log.md`
- `docs/loop-trace.md`
- `docs/handoff-decision.md`
- `docs/stopper-policy.md`
- `.github/pull_request_template.md`

## State Sources

`docs/progress.md` is the single milestone state source. `docs/next-steps-plan.md` contains detailed acceptance criteria, file targets, and verification notes. `docs/loop-v8.md` contains current loop design intent. `docs/project-evaluation-v8.md` contains the code-grounded Review-and-Renewal evaluation.

Current active product loop: V8 foundation hardening. V7-01 through V7-38 are DONE through PR #80. The first product TODO is `V8-01`, the CI and test harness hardening slice.

## Workflow Discipline

Use the GitHub connector for repository work. Use one branch and one PR per milestone. Use CI as VERIFY.

## Product Guardrails

- Preserve fixture-only CI unless a milestone explicitly adds fake-client provider tests.
- Planned providers remain planned.
- OpenAI-compatible output is not ChatGPT Search.
- Do not weaken tests or add dummy files.
