# Stopper Policy

## Hard Stoppers

Stop when a required repository access path is unavailable, CI has no usable verification signal, missing trace evidence prevents a factual merge or progress decision, repeated harness defects remain after repair attempts, an invalidated active hypothesis has no rollback path, inconsistent progress state cannot be reconciled from PR and trace evidence, a merged milestone regresses, or the next step needs a decision outside the approved plan.

## Soft Stoppers

Run one review before stopping when no TODO rows remain, review finds no meaningful new work, PR evidence is incomplete, Loop Trace has reconstructable gaps, repeated harness defects appear before a repair loop has run, an active hypothesis needs validation, configured limits are reached, or remaining work is duplicated, vague, or unverifiable.

## Default Limits

```yaml
stopper_policy:
  max_review_cycles: 5
  max_total_milestones: 30
  max_total_prs: 30
  max_harness_repair_attempts_per_failure: 2
  stop_when_no_meaningful_new_work: true
  max_fix_attempts_per_milestone: 3
  max_ci_reruns_per_failure: 1
```

## Stopper Report

Report the stopper reason, completed work, blocked work, unresolved human decisions, missing trace evidence, feedback root-cause layers, active or invalidated hypotheses, harness repairs attempted, and safe next actions.
