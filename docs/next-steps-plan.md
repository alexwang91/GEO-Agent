# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for GEO that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Methodology Map

- Superpowers: evaluate before implementation, write plans, TDD/eval-first, review, and finish branches after verification.
- Matt Pocock skills: alignment, shared language, ADR-worthy decisions, vertical slices, red-green-refactor, and architecture improvement.
- GitHub Loop Runner: GitHub-only PR loop, progress as state, CI verification, feedback taxonomy, trace, repair, hypotheses, and stoppers.

## Loop V2 Backlog

| Slice | Description | Status |
| :--- | :--- | :--- |
| V2-0 | Install Loop V2, shared context, and decision log. | DONE |
| V2-1 | Add persistent evidence store for raw query-answer-citation history. | DONE |
| V2-2 | Replace parser-only page inventory with fetch-capable crawler seam. | DONE |
| V2-3 | Upgrade engine sampling adapter contract and recorded-run import path. | DONE |
| V2-4 | Rework scoring into weighted metric components with stronger edge-case tests. | DONE |
| V2-5 | Add evidence-backed operational report artifact and snapshot or JSON tests. | DONE |

## Loop V3 Backlog

| Slice | Description | Status |
| :--- | :--- | :--- |
| V3-0 | Install Loop V3 and productization plan. | DONE |
| V3-1 | Add `AuditRunner` orchestrating existing modules over fixtures. | DONE |
| V3-2 | Add recorded dataset schema and fixture loader. | DONE |
| V3-3 | Expand EvidenceStore beyond engine runs. | DONE |
| V3-4 | Add Diagnosis V2 using run, page, and competitor evidence. | DONE |
| V3-5 | Add CLI entry point for fixture-based audits. | DONE |

## Loop V4 Backlog

| Slice | Description | Status |
| :--- | :--- | :--- |
| V4-0 | Install V4 evaluation, loop, and reproducible audit package plan. | DONE |
| V4-1 | Persist the full audit evidence graph during `AuditRunner.run`. | DONE |
| V4-2 | Write reproducible audit package artifacts from CLI. | DONE |
| V4-3 | Add canonical example fixture and usage docs. | DONE |
| V4-4 | Publish recorded dataset schema documentation. | TODO |
| V4-5 | Document live adapter boundary without implementing live calls. | TODO |

## V4-0 Acceptance Criteria

- `docs/project-evaluation-v4.md` evaluates the current project state.
- `docs/loop-v4.md` defines the reproducible audit package loop.
- `AGENTS.md` instructs future agents to read and follow Loop V4.
- `docs/decision-log.md` records the move from report output to reproducible audit package output.
- CI passes.

## V4-1 Acceptance Criteria

- `AuditRunner.run` persists query records, page inventory records, engine runs, diagnoses, tasks, and report artifacts.
- Tests prove the store contains every evidence layer after a fixture audit.
- Existing CLI and report behavior remain unchanged.

## V4-2 Acceptance Criteria

- CLI writes `manifest.json`, `audit.sqlite`, `report.json`, and `report.md`.
- Manifest includes profile brand/domain, engine, query count, page count, run count, generated timestamp, and artifact names.
- CLI tests verify package contents without network or live engine credentials.

## V4-3 Acceptance Criteria

- Repository includes `examples/acme-fixture.json`.
- Usage docs show a fixture audit command and expected outputs.
- CI verifies the example fixture can run through the CLI.

## V4-4 Acceptance Criteria

- Repository includes recorded dataset schema documentation.
- Required sections and field types are documented.
- Tests or docs checks cover the schema file presence and example alignment.

## V4-5 Acceptance Criteria

- Live adapter boundary is documented without adding live calls.
- Docs define required secrets, rate limits, provenance fields, and stopper rules.
- CI remains fully fixture-based.
