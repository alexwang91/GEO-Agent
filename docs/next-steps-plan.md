# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for GEO that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Methodology Map

- Superpowers: brainstorm before code, write plans, TDD/eval-first, review, and finish branches after verification.
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
| V3-4 | Add Diagnosis V2 using run, page, and competitor evidence. | TODO |
| V3-5 | Add CLI entry point for fixture-based audits. | TODO |

## V3-0 Acceptance Criteria

- `docs/loop-v3.md` defines the demo-ready evidence loop.
- `AGENTS.md` instructs future agents to read and follow Loop V3.
- `docs/decision-log.md` records why the project is moving from seams to productized audit workflow.
- CI passes.

## V3-1 Acceptance Criteria

- An `AuditRunner` or equivalent orchestrator accepts an `EntityProfile`, page evidence, and recorded or mock engine evidence.
- The runner executes query planning, page inventory, engine sampling, evidence storage, scoring, diagnosis, tasks, and report rendering.
- Tests prove a fixture-based audit produces a JSON or Markdown report with score, missing queries, competitor map, sources, failures, actions, and retest plan.
- The runner does not claim live engine support.

## V3-2 Acceptance Criteria

- A recorded dataset schema exists for entity profile, pages, recorded engine runs, and expected audit metadata.
- Loader tests accept a valid fixture and reject missing required sections, malformed URLs, and malformed recorded runs.
- Dataset loading produces objects compatible with `AuditRunner` without changing scoring code.

## V3-3 Acceptance Criteria

- EvidenceStore can persist query records, page inventory records, failure diagnoses, optimization tasks, and report artifacts.
- Tests cover save/load/filter behavior for each new evidence type.
- Existing engine-run persistence remains backward compatible.

## V3-4 Acceptance Criteria

- Diagnosis V2 uses engine runs, page inventory, source domains, competitors, and query intent.
- Tests cover attribution failure, retrieval failure, competitor-source dominance, entity parsing failure, and intent mismatch.
- Diagnoses include evidence fields usable by reports and task generation.

## V3-5 Acceptance Criteria

- A CLI command can run a fixture-based audit.
- CLI accepts input fixture path and output directory.
- CLI writes stable JSON and Markdown report artifacts.
- CLI tests run in CI without network or live engine credentials.
