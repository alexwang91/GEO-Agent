# Harness Repair Loop

## Purpose

Repair runner-protocol failures without mixing product feature work into the repair.

## Trigger Conditions

Run the Harness Repair Loop when any of these conditions appears:

- repeated `protocol_violation`, `trace_gap`, `weak_verification`, `merge_blocked`, or `harness_defect` feedback;
- missing or malformed `docs/progress.md`, `docs/feedback-log.md`, `docs/loop-trace.md`, or `docs/loop-hypotheses.md`;
- inconsistent status between merged PRs and `docs/progress.md`;
- PRs repeatedly lack evidence required by the template;
- CI scaffold cannot verify the generated repository shape;
- review finds stale or contradictory runner instructions;
- active hypotheses cannot be validated because the harness lacks the needed trace or feedback signal.

## Repair Scope

Allowed repair scope:

- runner docs;
- feedback taxonomy;
- loop trace format;
- review loop rules;
- stopper policy;
- PR template;
- CI scaffold;
- milestone slicing rules.

## Forbidden Repairs

- product feature work;
- unrelated refactors;
- weakened verification;
- deleted tests to get green;
- vague process text with no validation criteria;
- changes that require local clone, local package-manager, or local test execution in GitHub-only mode;
- changes that hide or discard blocking evidence.

## Validation Criteria

A valid harness repair must show the specific failure mode, affected harness files, root-cause layer, validation evidence, preserved GitHub-only and CI-only runner contract, no weakened verification, and no product feature work mixed into the repair.
