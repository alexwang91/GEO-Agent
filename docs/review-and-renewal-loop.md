# Review and Renewal Loop

## Trigger Conditions

Run review when:

- no TODO rows remain;
- a milestone is blocked or repeatedly fails CI;
- feedback repeats `verification_failure`, `scope_violation`, `weak_verification`, `trace_gap`, `harness_defect`, `merge_blocked`, or `regression`;
- Loop Trace is missing required events or decisions lack evidence;
- an active hypothesis reaches validation or invalidation;
- the next step touches release readiness, deployment readiness, credentials, external providers, data removal, or trust boundaries;
- the user asks for review, plan renewal, or stop assessment.

## Review Steps

1. Summarize completed milestones since the last review.
2. Summarize feedback trends since last review.
3. Summarize Loop Trace coverage and missing evidence.
4. Compare repo state against the product goal.
5. Check whether verification and PR evidence remain meaningful.
6. Evaluate active hypotheses and apply Hypothesis-Gated Renewal.
7. Detect missing tests, missing docs, stale plan items, blockers, duplicated work, weak acceptance criteria, architecture drift, harness defects, and inconsistent progress state.
8. Decide whether the plan needs new milestones, split milestones, blocked milestones, cancelled milestones, Harness Repair Loop, or hypothesis validation.
9. Classify the decision with the Feedback Taxonomy.
10. Apply the Stopper Policy.
11. Update `docs/loop-review.md`.
12. Update plan, progress, and hypotheses only when the change is specific, useful, and verifiable.

## Decision Values

- `continue`
- `continue_with_new_milestones`
- `blocked`
- `stop`
