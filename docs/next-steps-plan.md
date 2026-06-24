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
| V4-4 | Publish recorded dataset schema documentation. | DONE |
| V4-5 | Document live adapter boundary without implementing live calls. | DONE |

## Loop V5 Backlog

| Slice | Description | Status |
| :--- | :--- | :--- |
| V5-0 | Install V5 evaluation, Tauri + React UI brief, provider access architecture, and loop plan. | DONE |
| V5-1 | Add provider access domain model and registry. | DONE |
| V5-2 | Add Tauri + React app shell. | DONE |
| V5-3 | Add BYOK API key session flow. | DONE |
| V5-4 | Add OAuth framework with fake provider. | DONE |
| V5-5 | Add first OpenAI-compatible answer provider behind explicit config. | TODO |
| V5-5.5 | Add Tauri command path that runs the existing fixture audit. | TODO |
| V5-6 | Add crawler provider abstraction and first crawler adapter. | TODO |
| V5-7 | Wire UI Run Audit to provider registry, fixture/provider audit paths, and report display. | TODO |

## V5-0 Acceptance Criteria

- `docs/project-evaluation-v5.md` evaluates the UI/provider access product gap.
- `docs/loop-v5.md` defines the UI-first provider access loop.
- `docs/ui-tori-brief.md` describes the Tauri + React UI workflow.
- `docs/provider-access-architecture.md` defines provider types, access methods, security rules, and initial matrix.
- `AGENTS.md` instructs future agents to read and follow Loop V5.
- `docs/decision-log.md` records the shift from CLI package to UI/provider access product entry.
- CI passes.

## V5-1 Acceptance Criteria

- Provider access domain model supports provider types, capabilities, access methods, implementation status, and redacted connection state.
- Registry exposes initial provider matrix.
- Tests reject unsupported access methods and prove credentials are redacted.
- No live provider calls.

## V5-2 Acceptance Criteria

- Repository includes a Tauri + React app shell.
- UI includes Providers, Brand Profile, Queries, Audit Run, Report, and Evidence Package navigation shells.
- CI verifies app structure without requiring network install.
- UI does not claim live provider support.

## V5-3 Acceptance Criteria

- API key session flow accepts a key through a backend/session boundary.
- Key is redacted from responses, reports, manifests, audit DB, and logs.
- Missing key gives clear error.
- No live provider calls.

## V5-4 Acceptance Criteria

- OAuth start/callback/disconnect framework exists with fake provider.
- State validation is tested.
- Tokens are redacted and never enter artifacts.
- No live OAuth provider calls in CI.

## V5-5 Acceptance Criteria

- OpenAI-compatible answer provider interface exists behind explicit config.
- CI uses fake HTTP client.
- Missing credentials fail clearly.
- Output converts to `EngineRun` or equivalent answer evidence.
- No default live calls.

## V5-5.5 Acceptance Criteria

- Tauri command boundary can invoke the existing fixture audit path without live provider credentials.
- The command accepts a fixture path and output directory.
- The command returns redacted package metadata and report file locations.
- CI verifies command shape or wrapper behavior without installing Tauri dependencies or making network calls.
- This slice does not replace provider-backed audit execution; it creates an early clickable local product loop.

## V5-6 Acceptance Criteria

- Crawler provider abstraction exists.
- First crawler adapter boundary is documented and testable with fake/static crawler.
- Crawl output feeds page inventory/evidence store.
- CI remains network-free.

## V5-7 Acceptance Criteria

- UI Run Audit can execute fixture audit and fake-provider audit paths.
- UI can display report data from generated package artifacts.
- Download actions are represented.
- No live credentials required in CI.
