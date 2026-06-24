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

## D-0004: Loop V3 productizes the audit path

- Date: 2026-06-24
- Status: accepted
- Context: Loop V2 completed the main seams: persistence, crawler fetcher, engine adapter, weighted scoring, and report artifacts. The project now needs a user-observable workflow rather than more isolated modules.
- Decision: Future work follows Loop V3. The first priority is an `AuditRunner` that creates a deterministic audit report from fixture evidence without claiming live engine support.
- Consequences: New slices must move the end-to-end audit path forward and include an artifact or persisted evidence. Isolated helpers are deferred unless immediately consumed by the audit workflow.

## D-0005: Loop V4 makes audits reproducible packages

- Date: 2026-06-24
- Status: accepted
- Context: Loop V3 created a fixture audit CLI that writes reports, but reviewers still need a complete package containing evidence, metadata, and artifacts.
- Decision: Future work follows Loop V4. Each audit should become a reproducible package with a manifest, report artifacts, and an inspectable evidence database.
- Consequences: New slices must improve package reproducibility and evidence reviewability. Live engine work remains out of scope until the adapter boundary is documented.

## D-0006: Loop V5 prioritizes Tauri + React provider access

- Date: 2026-06-24
- Status: accepted
- Context: The reproducible CLI package is useful, but the original product needs a user-facing app that connects answer, search, crawl, model, and analytics providers.
- Decision: Future work follows Loop V5. The product entry point is a Tauri + React desktop UI with a provider access layer supporting API key, OAuth, platform-managed access, and manual import.
- Consequences: UI and provider access become first-class. New slices must prevent credential leakage and keep CI fixture-based while moving toward real provider-connected audits.
