# Loop V6: Provider-Backed GEO Agent Loop

Loop V6 extends the V5 UI/provider-access work into a provider-backed GEO agent. It does not replace V5. It starts after V5 has a first usable UI path for running audits and viewing report artifacts.

## Source Principles

- Superpowers: clarify, brainstorm, write plans, TDD/eval-first, request review, finish only after verification.
- GitHub Loop Runner: one milestone, one branch, one PR, CI as VERIFY, progress as state, feedback taxonomy, Loop Trace, long-run growth, handoff prompt, stopper policy.
- GEO product brief: measure AI-answer visibility, diagnose citation failures, produce safe optimization tasks, and retest.

## Product Thesis

The product becomes valuable when it connects provider evidence to the existing GEO audit engine and presents it through an evidence-backed UI:

```text
Desktop UI
  -> Provider Access Layer
  -> Answer/Search/Crawl/Manual Import Providers
  -> AuditRunner Evidence Graph
  -> Reproducible Audit Package
  -> Report UI
  -> Retest Comparison
  -> Skill Learning Records
```

## Active Preconditions

Do not begin V6 implementation until these V5 items are DONE:

- `V5-5`: OpenAI-compatible answer provider behind explicit config.
- `V5-5.5`: Tauri command path for fixture audit.
- `V5-6`: crawler provider abstraction.
- `V5-7`: UI Run Audit and report display path.

A planning or harness repair PR may update V6 docs earlier, but product code should follow V5 order unless Review and Renewal changes `docs/progress.md` with evidence.

## V6 Quality Gates

A V6 milestone is complete only if:

- acceptance criteria map to CI or explicit review evidence;
- tests use fake clients, recorded fixtures, or structural checks;
- no CI path needs live provider credentials;
- raw API keys, OAuth tokens, cookies, request headers, or secrets cannot appear in artifacts, logs, manifests, audit databases, or UI payloads;
- existing fixture and manual-import paths still work;
- provider status labels remain truthful;
- loop trace and feedback evidence are current;
- no unrelated refactors or placeholder files are introduced.

## V6 Backlog

| Slice | Goal | Evidence |
| :--- | :--- | :--- |
| V6-1 | Provider-backed audit orchestration. | Fake answer-provider output reaches `AuditRunner`, evidence store, and package artifacts. |
| V6-2 | Manual import and recorded live-run import UX. | Validated import schema, safe errors, redaction, and package compatibility. |
| V6-3 | Provider output eval harness. | Deterministic eval fixtures for parsing, citations, recommendations, errors, and redaction. |
| V6-4 | Evidence-backed report UI. | UI renders generated package sections and handles partial artifacts honestly. |
| V6-5 | Credential and artifact safety hardening. | Artifact-wide leakage tests and safe command/log behavior. |
| V6-6 | Retest planning workflow. | Baseline/follow-up package comparison and measured deltas. |
| V6-7 | Release-readiness packaging checks. | CI checks desktop structure, package entry points, docs, and no dummy files. |
| V6-8 | Skill-learning records. | Optimization action outcome records by engine, query type, vertical, and result. |

## Per-Milestone Planning Rules

Each milestone plan must include:

1. Product outcome.
2. Files likely to change.
3. Tests/evals to add first.
4. Acceptance criteria.
5. Stopper conditions.
6. Expected PR title and branch name.
7. Loop evidence to append.

## V6-1 Plan: Provider-Backed Audit Orchestration

Branch: `v6-1-provider-backed-audit`

Product outcome: a configured answer provider can feed the audit evidence path without replacing fixtures.

Files likely to change:

- `src/geo_agent/audit_runner.py`
- `src/geo_agent/answer_provider.py`
- `src/geo_agent/evidence_store.py`
- `tests/test_provider_backed_audit.py`
- `docs/progress.md`
- `docs/feedback-log.md`
- `docs/loop-trace.md`

Verification first:

- Add fake provider fixture that returns deterministic answer, mentions, citations, and recommendations.
- Add failing test that expects a provider-backed run to persist answer evidence and produce a package-compatible report.

Stop if provider-backed orchestration requires live credentials or broad refactoring of the fixture path.

## V6-2 Plan: Manual Import and Recorded Live-Run UX

Branch: `v6-2-manual-import-ux`

Product outcome: a user can import recorded evidence safely when live provider access is unavailable.

Verification first:

- Schema tests for valid/invalid answer, citation, page, competitor, and query records.
- Redaction tests for imported fields.

Stop if import bypasses evidence store validation or accepts raw secrets.

## V6-3 Plan: Provider Output Eval Harness

Branch: `v6-3-provider-output-evals`

Product outcome: provider output parsing and citation extraction become regression-tested.

Verification first:

- Eval fixtures for answers with citations, answers without citations, duplicate domains, unsupported regions, provider errors, and malformed payloads.

Stop if evals depend on live network calls.

## V6-4 Plan: Evidence-Backed Report UI

Branch: `v6-4-report-ui`

Product outcome: the desktop UI reads generated package artifacts and renders report sections from evidence.

Verification first:

- Tests or structural checks that load sample `manifest.json` and `report.json`.
- UI copy checks for empty/partial artifact warning states.

Stop if report display duplicates business logic instead of reading package artifacts.

## V6-5 Plan: Credential and Artifact Safety Hardening

Branch: `v6-5-credential-artifact-safety`

Product outcome: artifact-wide redaction guarantees are tested before broader provider use.

Verification first:

- Tests scan generated reports, manifests, audit database rows, log payloads, Tauri command responses, and UI state snapshots for raw key/token patterns.

Stop if raw credentials are needed outside the provider session boundary.

## V6-6 Plan: Retest Planning Workflow

Branch: `v6-6-retest-comparison`

Product outcome: users can compare baseline and follow-up audit packages and see measured changes.

Verification first:

- Fixture package pair with controlled visibility, citation, recommendation, rank, and diagnosis deltas.

Stop if the report claims improvement without measured package deltas.

## V6-7 Plan: Release-Readiness Packaging Checks

Branch: `v6-7-release-readiness-checks`

Product outcome: the repo has deterministic checks for package and desktop release structure.

Verification first:

- CI checks Python entry point, desktop required files, docs, runner files, and no dummy/noop/temp files.

Stop if checks require downloading live desktop dependencies in CI.

## V6-8 Plan: Skill-Learning Records

Branch: `v6-8-optimization-learning-records`

Product outcome: optimization actions can be tied to observed outcomes over time.

Verification first:

- Tests for action/outcome record schema, confidence updates, and non-destructive evidence history.

Stop if learning records overwrite raw audit evidence.

## Review and Renewal

Run Review and Renewal after V5 completion, every 5 merged PRs, when TODO backlog falls below 12, when a deep provider/security boundary changes, or when repeated feedback indicates planning drift.

Renewal may add milestones only if they are specific, useful, non-duplicative, and verifiable. Do not add vague cleanup, UI polish without product path, or broad refactors.

## Hard Stopper Summary

Stop immediately if any milestone would:

- require live credentials in CI;
- leak raw credentials or tokens;
- represent a planned provider as live;
- weaken tests/evals/CI;
- require broad refactoring outside the selected slice;
- merge without loop trace, feedback classification, and progress evidence;
- bypass evidence store/package artifacts for report claims.