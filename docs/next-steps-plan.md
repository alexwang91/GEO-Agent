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
| V2-2 | Replace parser-only page inventory with fetch-capable crawler seam. | TODO |
| V2-3 | Upgrade engine sampling adapter contract and recorded-run import path. | TODO |
| V2-4 | Rework scoring into weighted metric components with stronger edge-case tests. | TODO |
| V2-5 | Add evidence-backed operational report artifact and snapshot or JSON tests. | TODO |

## V2-0 Acceptance Criteria

- `docs/loop-v2.md` defines the new operating loop.
- `docs/context.md` defines shared project language.
- `docs/decision-log.md` records durable loop decisions.
- `AGENTS.md` instructs future agents to read and follow Loop V2.
- CI passes.

## V2-1 Acceptance Criteria

- A storage module persists raw `EngineRun` records with query, engine, region, language, timestamp, answer text, citations, mentions, recommendations, and source domains.
- The store can save and load runs deterministically in CI.
- Tests cover empty store, single run, multiple runs, and query/engine filtering.
- The design keeps a seam for future page, diagnosis, task, and report persistence.

## V2-2 Acceptance Criteria

- Page inventory has a fetch-capable adapter interface separate from parser logic.
- Sitemap index and URL sitemap inputs are supported through fixtures.
- Canonical dedupe and malformed page handling are tested.
- Network behavior remains mockable in CI.

## V2-3 Acceptance Criteria

- Engine adapters share a protocol that can support live, recorded, and mock modes.
- Recorded-run import can turn saved answer fixtures into `EngineRun` records.
- Tests prove real adapters can be added without changing scoring code.

## V2-4 Acceptance Criteria

- Scoring exposes metric components before aggregate score.
- Weighting is configurable and deterministic.
- Tests cover brand mention without citation, citation without recommendation, competitor-only answer, empty answer, and source diversity.

## V2-5 Acceptance Criteria

- Report generation produces a stable JSON or Markdown artifact.
- Report includes score, missing queries, competitor map, cited sources, failures, recommended actions, and retest plan.
- Snapshot or structured assertions verify the artifact shape.
