# Decision Log

Durable product and architecture decisions are recorded here. Use short ADR-style entries.

## D-0001: Loop V2 uses evidence-first vertical slices

- Date: 2026-06-24
- Status: accepted
- Context: M0-M9 created a runnable skeleton, but the project still needs real product capability and stronger evidence gates.
- Decision: Future work follows Loop V2: align, define shared language, slice vertically, plan, test first, build surgically, review, finish only after CI, then re-read state.
- Consequences: Progress can no longer be marked done merely because a module exists. Each slice needs behavior evidence and a verification path.

## D-0002: Raw evidence is a product asset

- Date: 2026-06-24
- Status: accepted
- Context: GEO value depends on preserving query, answer, citation, source, page, diagnosis, action, and retest history.
- Decision: The next engineering slice should add a persistence seam before further scoring or reporting expansion.
- Consequences: Mock adapters remain acceptable for CI, but real or imported evidence must flow through a store-compatible interface.

## D-0003: Shared language is part of the runner contract

- Date: 2026-06-24
- Status: accepted
- Context: Agents can drift into broad or vague terms when continuing a partially built repo.
- Decision: Public APIs and plans should use `docs/context.md` terminology.
- Consequences: Reviews should flag ambiguous new names or duplicate concepts.
