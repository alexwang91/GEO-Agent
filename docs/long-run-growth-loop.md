# Long-Run Growth Loop

## Purpose

Prevent the runner from treating a short initial backlog as the whole product. GEO Agent needs a sustained loop because provider access, evidence quality, UI execution, report review, credential safety, retest comparison, and learning records mature across multiple milestones.

## Configuration

```yaml
long_run_growth:
  enabled: true
  target_merged_prs: 50
  minimum_merged_prs_before_final_review: 40
  review_interval_prs: 5
  deep_review_interval_prs: 10
  minimum_open_todo_backlog: 12
  preferred_open_todo_backlog: 20
  expansion_batch_min: 5
  expansion_batch_max: 10
  empty_deep_reviews_before_final_review: 3
```

## Growth Review Trigger

Run a growth review when any condition is true:

- TODO backlog in `docs/progress.md` falls below `minimum_open_todo_backlog` before final-review eligibility.
- No TODO remains and fewer than `minimum_merged_prs_before_final_review` PRs have been merged.
- The active loop completes, such as V5 completion before V6 product work.
- A provider/security boundary changes.
- The user asks to check progress or renew the plan.
- Review finds repeated `weak_verification`, `trace_gap`, `verification_failure`, `harness_defect`, `scope_violation`, `merge_blocked`, or `regression` feedback.

## Deep Review Trigger

Run a deep review when:

- merged PR count since last deep review reaches `deep_review_interval_prs`;
- a loop finishes;
- repeated feedback indicates architecture or harness drift;
- a milestone proposes live provider access, credential persistence, desktop packaging, or release readiness;
- final-review eligibility is being considered.

## Growth Review Steps

1. Re-read `docs/product-brief.md`, `docs/project-evaluation-v6.md`, `docs/loop-v6.md`, `docs/progress.md`, and `docs/next-steps-plan.md`.
2. Count DONE, TODO, BLOCKED, DEFERRED, and CANCELLED rows.
3. Compare the current backlog to the product goal and active risks.
4. Identify the next smallest useful vertical slices.
5. Reject vague cleanup, broad refactors, placeholder UI polish, and unverifiable tasks.
6. Add only milestones with acceptance criteria, likely files, verification, and stoppers.
7. Update `docs/progress.md`, `docs/next-steps-plan.md`, `docs/loop-review.md`, and `docs/loop-trace.md`.
8. Classify the review result in `docs/feedback-log.md` when it changes the runner decision.

## Expansion Rules

A new milestone is allowed only when it is:

- directly tied to GEO product value;
- independently reviewable in one PR;
- verifiable by CI, deterministic fixture, fake client, structural check, or explicit review evidence;
- safe under credential and provider-access guardrails;
- non-duplicative with existing TODO rows;
- small enough for a single vertical slice.

## Forbidden Expansions

Do not add milestones for:

- generic cleanup;
- unspecified refactors;
- dummy files;
- UI polish not connected to audit execution or report review;
- live provider calls without fake-client CI boundary;
- credential persistence without redaction/encryption decision;
- broad rewrites of the audit core;
- work that cannot update trace, progress, and verification evidence.

## Final Review Eligibility

Final review may recommend stopping only when all conditions are true:

- at least `minimum_merged_prs_before_final_review` PRs have merged;
- TODO backlog is empty after growth review;
- the last three deep reviews found no specific useful verifiable work;
- no active hypothesis needs validation;
- no blocking feedback remains;
- no hard stopper is being ignored;
- the product has a usable provider/manual-import audit path, evidence-backed report UI, artifact safety checks, and retest comparison path.

## Output Contract

Each growth or deep review must report:

- trigger;
- merged PR count;
- TODO backlog count;
- completed milestones since last review;
- feedback trends;
- trace gaps;
- active hypotheses;
- proposed new milestones or reason none were added;
- stopper decision;
- next first TODO from fresh `docs/progress.md`.