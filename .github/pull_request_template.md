## Milestone

- Progress row:
- Base branch:
- Branch:

## What changed

-

## Acceptance evidence

| Acceptance criterion | CI/review evidence |
| --- | --- |
|  |  |

## Verification

- [ ] CI is green.
- [ ] Acceptance criteria mapped to CI or review evidence.
- [ ] `docs/progress.md` is updated to DONE or a progress PR is linked.
- [ ] No live provider credentials are required in CI.

## Loop evidence

- [ ] Loop Trace updated or trace gap explicitly classified.
- [ ] Feedback entries linked when applicable.
- [ ] Root-cause layer classified for blocking feedback.
- [ ] Active hypotheses updated when applicable.
- [ ] Long-Run Growth policy checked when applicable.
- [ ] Handoff Decision respected when applicable.
- [ ] Harness Repair considered when failures repeat.
- [ ] Review and Renewal considered when no TODO remains or backlog is below floor.

## Provider and credential safety

- [ ] No raw API keys, OAuth tokens, cookies, request headers, or provider secrets are persisted.
- [ ] Returned UI/API/report values use redacted labels or opaque session IDs.
- [ ] Planned providers are not represented as live.
- [ ] Fake clients, fixtures, manual imports, or structural checks cover provider behavior in CI.

## Guardrails

- [ ] No weakened tests, evals, assertions, or acceptance criteria.
- [ ] No unrelated refactors.
- [ ] No dummy/noop/temp filler files.
- [ ] Product claims are backed by evidence artifacts or explicit warning states.