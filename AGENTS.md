# Agent Instructions

Read `docs/autonomous-runner.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `docs/loop-v2.md`, `docs/context.md`, `docs/decision-log.md`, `docs/development-principles.md`, `docs/feedback-taxonomy.md`, `docs/loop-trace.md`, and `docs/loop-hypotheses.md` before development.

`docs/progress.md` is the state source. Select the first unfinished slice from `docs/progress.md` or `docs/next-steps-plan.md`, complete it through one PR into `main`, update state, append trace and feedback evidence when possible, then re-read progress.

## Workflow Discipline

Follow Loop V2: reload state, align terms, slice vertically, plan for exact files and checks, add failing verification first when behavior changes, build surgically, review against evidence, finish only after CI is green, and stop instead of faking unavailable real evidence. Do not weaken tests, evals, assertions, or acceptance criteria.
