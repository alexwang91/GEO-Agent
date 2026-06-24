# Feedback Taxonomy

## Feedback Sources

- `parser`
- `protocol`
- `git_diff`
- `ci`
- `pr_review`
- `mergeability`
- `progress_state`
- `loop_trace`
- `review_loop`
- `harness_repair`
- `loop_hypothesis`
- `stopper_policy`

## Feedback Types

| Type | Default severity | Meaning |
| --- | --- | --- |
| `invalid_action` | blocking | Runner output is incomplete or cannot be parsed. |
| `protocol_violation` | blocking | Runner skipped or violated the repo protocol. |
| `scope_violation` | blocking | PR changes exceed milestone scope. |
| `verification_failure` | blocking | CI, tests, lint, build, or eval failed. |
| `weak_verification` | warning/blocking | Checks pass but do not prove the milestone. |
| `trace_gap` | warning/blocking | Loop Trace is missing, malformed, or inconsistent. |
| `harness_defect` | blocking | Runner harness caused repeated failure. |
| `hypothesis_invalidated` | blocking/terminal | Evidence disproved an active process hypothesis. |
| `repair_validated` | info | A harness repair has evidence that it fixed the failure. |
| `review_failure` | blocking | PR does not satisfy acceptance criteria or review. |
| `merge_blocked` | blocking | Merge is blocked by conflict, check, review, or permission. |
| `blocked_dependency` | blocking | Work needs missing setup or human decision. |
| `regression` | blocking | Previously completed work regressed. |
| `success` | info | PR merged, CI green, progress updated, and trace evidence present. |
| `no_meaningful_work` | terminal | Review found no useful verifiable work. |

## Root-Cause Layers

| Layer | Meaning |
| --- | --- |
| `observation` | Needed signal was not observed or recorded. |
| `context` | Repository, product, or milestone context was missing or stale. |
| `planning` | Plan, acceptance criteria, or milestone slice was wrong. |
| `control_loop` | Runner chose the wrong next action or skipped a step. |
| `tool_action` | Connector/tool failed, was unavailable, or had wrong inputs. |
| `state_store` | Progress, feedback, trace, hypothesis, or review state was inconsistent. |
| `verification` | CI, tests, evals, or PR evidence was missing, weak, or red. |
| `governance` | Work crossed review, approval, or access boundaries. |
| `product_code` | Product implementation caused the failure. |
| `unknown` | Evidence does not support a specific layer yet. |

## Feedback Entry Format

```yaml
feedback:
  id: F-0001
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"
  source: ci
  type: verification_failure
  severity: blocking
  milestone: M0
  branch: m0-example
  pr: 1
  summary: "Short factual summary."
  evidence:
    checks: []
    files: []
    review_comments: []
    trace_ids: []
    hypothesis_ids: []
  root_cause:
    layer: verification
    category: unknown
    confidence: low
    explanation: "What the evidence supports."
  allowed_next_actions: []
  forbidden_next_actions: []
  runner_decision:
    action: inspect_failure
    reason: "Why this action is allowed."
```

## Allowed Action Map

| Feedback type | Allowed actions | Forbidden actions |
| --- | --- | --- |
| `verification_failure` | `inspect_ci_failure`, `fix_true_cause`, `add_missing_in_scope_test` | `weaken_test`, `remove_assertion`, `mark_done` |
| `weak_verification` | `add_stronger_test`, `add_eval`, `create_verification_hardening_milestone` | `claim_complete_without_evidence` |
| `trace_gap` | `append_missing_trace_entry`, `repair_trace_format`, `run_harness_repair_loop` | `merge_without_trace_evidence` |
| `harness_defect` | `run_harness_repair_loop`, `repair_runner_docs`, `repair_ci_scaffold`, `repair_pr_template` | `ship_product_work_in_repair`, `weaken_verification` |
| `hypothesis_invalidated` | `rollback_hypothesis`, `run_review_loop`, `stop_if_no_safe_rollback` | `promote_invalidated_hypothesis` |
| `repair_validated` | `record_repair_evidence`, `continue_loop`, `check_review_due` | `repeat_same_repair_without_new_evidence` |
| `success` | `mark_done`, `update_feedback_log`, `append_trace_entry`, `continue_loop` | none |
| `no_meaningful_work` | `stop_with_loop_review` | `create_vague_cleanup`, `create_placeholder_milestone` |
