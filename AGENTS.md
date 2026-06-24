# Agent Instructions

Read `docs/autonomous-runner.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `docs/loop-v5.md`, `docs/project-evaluation-v5.md`, `docs/ui-tori-brief.md`, `docs/provider-access-architecture.md`, `docs/loop-v4.md`, `docs/project-evaluation-v4.md`, `docs/loop-v3.md`, `docs/loop-v2.md`, `docs/context.md`, `docs/decision-log.md`, `docs/development-principles.md`, `docs/feedback-taxonomy.md`, `docs/loop-trace.md`, and `docs/loop-hypotheses.md` before development.

`docs/progress.md` and `docs/next-steps-plan.md` are state sources. Select the first unfinished slice from the active loop backlog, complete it through one PR into `main`, update state, append trace and feedback evidence when possible, then re-read the plan.

## Workflow Discipline

Follow Loop V5 for UI/provider-access work: reload state, state the product entry or provider boundary being improved, add deterministic verification first, preserve fixture-only CI behavior, avoid credential leakage, finish only after CI is green, and stop instead of faking unavailable live provider evidence. Do not weaken tests, evals, assertions, or acceptance criteria.
