# Agent Instructions

Read `docs/autonomous-runner.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `docs/loop-v3.md`, `docs/loop-v2.md`, `docs/context.md`, `docs/decision-log.md`, `docs/development-principles.md`, `docs/feedback-taxonomy.md`, `docs/loop-trace.md`, and `docs/loop-hypotheses.md` before development.

`docs/progress.md` and `docs/next-steps-plan.md` are state sources. Select the first unfinished slice from the active loop backlog, complete it through one PR into `main`, update state, append trace and feedback evidence when possible, then re-read the plan.

## Workflow Discipline

Follow Loop V3 for productization work: reload state, state the evidence contract, slice through the audit path, verify before implementation, preserve adapter/persistence/rendering seams, review for product truth, finish only after CI is green, and stop instead of faking unavailable live evidence. Do not weaken tests, evals, assertions, or acceptance criteria.
