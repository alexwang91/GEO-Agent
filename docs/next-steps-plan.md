# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for Generative Engine Optimization that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Current State

The repository has moved past the initial fixture-based GEO audit core. It now has a Python domain package, fixture audit workflow, reproducible audit package output, provider access model, Tauri + React app shell, BYOK session boundary, and fake OAuth boundary. The active gap is provider-connected execution from the desktop product entry point.

Current completion checkpoint:

- M0-M9: complete baseline GEO workflow.
- V2: complete evidence store, crawler seam, adapter contract, weighted scoring, operational report artifact.
- V3: complete fixture audit runner, recorded dataset loader, evidence graph store, diagnosis V2, CLI.
- V4: complete reproducible audit package with manifest, report, audit database, example fixture, schema docs, live adapter boundary.
- V5-0 through V5-4: complete UI/provider plan, provider registry, Tauri + React shell, BYOK session, fake OAuth flow.
- First product TODO: `V5-5`.

## Methodology Map

| Source | Repo application |
| :--- | :--- |
| Superpowers | Clarify product intent, write concrete plans, define tests/evals first, make the smallest implementation slice, review against evidence, finish only after CI. |
| GitHub Loop Runner | GitHub-only branch/PR loop, `docs/progress.md` as state, CI as VERIFY, feedback classification, loop trace, long-run growth, harness repair, handoff prompt. |
| Existing GEO docs | Preserve product boundary: real AI-answer visibility, citation diagnostics, evidence history, safe optimization tasks, retest plans. |

## Operating Rules

1. Select the first TODO in `docs/progress.md`.
2. Use one branch and one PR per milestone.
3. Add deterministic tests or structural checks before product behavior changes.
4. Keep CI network-free unless a milestone explicitly adds fake-client verification for live-provider boundaries.
5. Never persist raw credentials or tokens.
6. Update progress, loop trace, and feedback evidence in the milestone PR.
7. Merge only after CI is green and acceptance criteria are mapped.
8. Re-read progress before selecting the next milestone.

## Active Loop V5 Backlog

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

## V5-5: OpenAI-Compatible Answer Provider

Goal: implement the first answer-provider boundary without default live calls.

Likely files:

- `src/geo_agent/answer_provider.py`
- `src/geo_agent/provider_access.py`
- `src/geo_agent/__init__.py`
- `tests/test_answer_provider.py`
- `docs/provider-access-architecture.md`
- `docs/next-steps-plan.md`
- `docs/progress.md`

Acceptance criteria:

- Provider interface accepts query text, model/provider config, and an explicit session or platform credential reference.
- OpenAI-compatible adapter accepts an injected fake HTTP client in CI.
- Missing credentials fail with a clear `ProviderAccessError` or equivalent domain error.
- Adapter output converts to existing `EngineRun` or equivalent answer evidence structure.
- No default live calls, no network requirement in CI, no raw key leakage in returned objects or artifacts.

Verification:

- Unit tests cover fake successful answer, missing credential, provider error, redaction, and conversion to evidence.
- Existing test suite remains green.

Stop if:

- The implementation requires real OpenAI credentials for CI.
- Raw request headers, API keys, or response bodies with secrets could enter reports, logs, manifests, or audit databases.
- Existing fixture engine-run contracts would need broad refactors.

## V5-5.5: Tauri Fixture Audit Command Path

Goal: create an early clickable local product loop by letting the Tauri boundary invoke the existing fixture audit path.

Likely files:

- `apps/desktop/src-tauri/src/main.rs`
- `apps/desktop/src/App.jsx`
- `tests/test_tauri_fixture_audit_command.py`
- `src/geo_agent/cli.py` or a thin audit service wrapper if needed
- `docs/ui-tori-brief.md`
- `docs/next-steps-plan.md`
- `docs/progress.md`

Acceptance criteria:

- Command accepts fixture path and output directory.
- Command delegates to existing fixture audit workflow or a narrow wrapper around it.
- Command returns redacted package metadata and report file locations.
- React app exposes a disabled/fixture-only Run Audit path with truthful status text.
- CI verifies command shape or wrapper behavior without installing Tauri dependencies or making network calls.

Verification:

- Structural or Python tests validate command/wrapper contract.
- UI text tests or file checks prove the UI does not claim live provider execution.

Stop if:

- Tauri tests require network dependency installation.
- The UI implies provider-backed audit execution before V5-7.

## V5-6: Crawler Provider Abstraction

Goal: add a crawler-provider boundary that can feed page inventory/evidence without live crawling in CI.

Likely files:

- `src/geo_agent/crawl_provider.py`
- `src/geo_agent/page_inventory.py`
- `src/geo_agent/evidence_store.py`
- `tests/test_crawl_provider.py`
- `docs/provider-access-architecture.md`
- `docs/next-steps-plan.md`
- `docs/progress.md`

Acceptance criteria:

- Crawler provider interface represents URL input, crawl result, page chunks, metadata, and errors.
- Static/fake crawler adapter works in CI.
- Crawl output feeds existing page inventory or evidence store structures.
- Crawl4AI, Firecrawl, or similar live providers remain planned unless explicitly implemented behind config.
- CI remains network-free.

Verification:

- Tests cover static crawler success, failure, unsupported method, redaction, and evidence conversion.

Stop if:

- The abstraction bypasses existing page inventory/evidence structures.
- CI needs live crawling or external service credentials.

## V5-7: UI Run Audit and Report Display

Goal: connect the UI to fixture and fake-provider audit paths and display report artifacts.

Likely files:

- `apps/desktop/src/App.jsx`
- `apps/desktop/src/styles.css`
- `apps/desktop/src-tauri/src/main.rs`
- `tests/test_ui_run_audit_flow.py`
- `src/geo_agent/audit_runner.py`
- `docs/ui-tori-brief.md`
- `docs/next-steps-plan.md`
- `docs/progress.md`

Acceptance criteria:

- UI can select fixture/manual-import path and fake-provider path.
- UI can display generated report summary, visibility score, citation map, diagnosis, and task brief sections from package artifacts.
- Download/export actions are represented truthfully.
- Provider status clearly distinguishes implemented, fake/test, planned, and unavailable.
- No live credentials are required in CI.

Verification:

- Tests or structural checks cover navigation, state labels, report artifact parsing, and no-live-claim copy.

Stop if:

- The UI masks provider failure as successful audit execution.
- Report display is disconnected from generated package artifacts.

## V6 Complete Development Plan

V6 starts after V5-7 completes the first usable desktop loop. V6 turns the product from a fixture-capable shell into a safer provider-backed GEO agent.

| Milestone | Goal | Acceptance evidence |
| :--- | :--- | :--- |
| V6-1 | Provider-backed audit orchestration. | Fake answer provider output flows into `AuditRunner` evidence records with tests. |
| V6-2 | Manual import and recorded live-run import UX. | UI/import schema validates recorded answer/citation datasets and rejects unsafe fields. |
| V6-3 | Provider output eval harness. | Deterministic evals test answer parsing, citation extraction, redaction, and error handling. |
| V6-4 | Evidence-backed report UI. | UI reads generated artifacts and renders score, citations, diagnoses, and task briefs. |
| V6-5 | Credential and artifact safety hardening. | Tests prove raw credentials/tokens cannot appear in reports, manifests, logs, DB rows, or UI payloads. |
| V6-6 | Retest planning workflow. | Baseline and follow-up packages can be compared for visibility/citation/diagnosis deltas. |
| V6-7 | Release-readiness packaging checks. | CI verifies desktop app structure, Python package entry points, docs, and no dummy files. |
| V6-8 | Skill-learning records. | Optimization outcomes are stored by engine, query type, vertical, action, confidence, and result. |

## V6-1 Acceptance Criteria

- Provider-backed run path accepts provider config and answer-provider session reference.
- Fake provider can produce deterministic answers, citations, and recommendations.
- Output persists to the existing evidence store and audit package.
- Existing fixture path remains unchanged.
- No live calls by default.

## V6-2 Acceptance Criteria

- Manual import UX can load recorded evidence datasets.
- Schema validation rejects malformed query, answer, citation, page, and competitor records.
- Redaction rules run before persistence.
- Import path produces an audit package compatible with report rendering.

## V6-3 Acceptance Criteria

- Eval fixtures cover answer mention extraction, citation parsing, recommendation rank, source domain normalization, error handling, and redaction.
- Eval results can block regressions in CI.
- Provider output parser handles missing citations, duplicate citations, and unsupported regions without crashing.

## V6-4 Acceptance Criteria

- Report UI reads generated `manifest.json`, `report.json`, `report.md`, and database/package metadata when available.
- UI sections map to product outputs: AI Visibility Score, missing high-value queries, competitor citation map, diagnosis, website audit, optimization tasks, expected impact/confidence, retest plan.
- Empty or partial artifact states show explicit warnings.

## V6-5 Acceptance Criteria

- Redaction tests scan report artifacts, manifests, logs, database rows, UI payloads, and command responses.
- Sensitive provider values are represented by opaque session IDs or redacted labels only.
- Failure logs avoid raw request headers and tokens.

## V6-6 Acceptance Criteria

- Retest plan can compare two audit packages.
- Deltas include mention share, citation share, recommendation share, rank, sentiment framing, and claim accuracy when available.
- Report output separates measured improvement from unverified recommendations.

## V6-7 Acceptance Criteria

- CI checks Python package entry points, desktop app file structure, docs, no dummy/noop/temp files, and runner docs.
- Release docs explain fixture mode, manual import mode, and provider-config mode.
- No packaging step depends on live credentials.

## V6-8 Acceptance Criteria

- Optimization action records store action type, source evidence, engine, query type, vertical, expected impact, observed outcome, and confidence.
- Retest outcomes can update action effectiveness without overwriting raw evidence.
- Report can identify reusable actions and actions that failed.

## Review and Renewal Rules

Run Review and Renewal before adding more milestones when:

- V5 backlog completes;
- TODO backlog falls below the configured floor;
- CI or feedback repeats the same failure type;
- trace evidence is stale or missing;
- credential or provider trust boundaries change;
- a milestone becomes too broad for one PR;
- user asks to re-evaluate direction.

New milestones must be specific, useful, verifiable, and non-duplicative. Do not add vague cleanup, polish, placeholder, broad refactor, or churn-only tasks.