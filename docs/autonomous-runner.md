# Autonomous Runner Protocol

Goal: move each `docs/progress.md` TODO row to DONE through one CI-verified PR into `main`, while preserving provider security, evidence quality, and loop traceability.

## Required State Read

Before selecting work, fetch:

- `AGENTS.md`
- `README.md`
- `docs/product-brief.md`
- `docs/autonomous-runner.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v7.md`
- `docs/project-evaluation-v7.md`
- `docs/development-principles.md`
- `docs/long-run-growth-loop.md`
- `docs/feedback-taxonomy.md`
- `docs/feedback-log.md`
- `docs/loop-trace.md`
- `docs/handoff-decision.md`
- `docs/review-and-renewal-loop.md`
- `docs/harness-repair-loop.md`
- `docs/loop-hypotheses.md`
- `docs/stopper-policy.md`
- `docs/loop-review.md`
- `.github/pull_request_template.md`
- `.github/workflows/verify.yml`

## Handoff Decision

If `docs/handoff-decision.md` selects `external_agent_development`, return the complete prompt from `docs/runner-prompt.md` and stop product work in the current session unless the user explicitly asks this agent to continue.

If it selects `current_agent_development`, continue with the Loop Workflow.

If it is pending or contradictory, stop and ask for the handoff decision. Do not silently begin product work.

## Long-Run Growth Mode

Before selecting work, apply `docs/long-run-growth-loop.md`:

1. Count merged PRs since the last deep review.
2. Count TODO backlog rows in `docs/progress.md`.
3. Determine whether growth review, deep review, hypothesis validation, or harness repair is due.
4. If the backlog is below floor before final-review eligibility, run Review and Renewal instead of stopping.

## Autonomous Loop

1. Probe GitHub connector access. If it works, continue; if not, report missing repository, permission, or GitHub App installation.
2. Fetch fresh state files from `main` or the approved base branch.
3. Report current state: first TODO, backlog count, review due, repair due, active hypotheses, stopper status.
4. Select the first TODO from `docs/progress.md`. Skip DONE, BLOCKED, DEFERRED, and CANCELLED.
5. Create one branch for that milestone.
6. Plan the smallest vertical slice with acceptance criteria mapped to CI or review evidence.
7. Add or update deterministic verification before product behavior changes when possible.
8. Implement only files required by the selected milestone.
9. Update `docs/progress.md`, `docs/feedback-log.md`, and `docs/loop-trace.md` with factual evidence.
10. Open one PR.
11. Use CI as VERIFY. Do not weaken tests or assertions to get green.
12. Run review against the plan and PR template.
13. Merge only after CI is green, acceptance criteria are mapped, loop evidence is complete, active hypotheses are updated, and no stopper applies.
14. Re-fetch `docs/progress.md` before choosing any next milestone.

## Required Trace Events

Record compact, factual entries for:

- `selected_milestone`
- `branch_created`
- `pr_opened`
- `ci_observed`
- `feedback_classified`
- `merge_attempted`
- `progress_updated`
- `growth_review`
- `deep_review`
- `review_run`
- `harness_repair_run`
- `hypothesis_updated`
- `handoff_decision`
- `stop`

Missing material trace evidence becomes `trace_gap` feedback.

## Repository Mode

This repository is bootstrapped for GitHub-only milestone execution. Use GitHub branches, PRs, and CI as the verification channel. Local execution can inform reasoning only when available, but it cannot replace CI evidence for merge readiness.

## Stop Conditions

Stop rather than force progress when:

- connector read/write access is unavailable;
- CI has no usable verification path;
- the next step needs live provider credentials that are not approved for the milestone;
- a provider would be represented as live without deterministic fake-client verification;
- raw credentials or tokens could leak into artifacts, logs, manifests, reports, database files, or UI state;
- progress, trace, feedback, or PR evidence conflicts and cannot be reconciled safely;
- repeated harness defects require repair before product work;
- the remaining work is vague, duplicated, or unverifiable.
