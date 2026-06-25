# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for Generative Engine Optimization that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Current State

The repository has moved past the initial fixture-based GEO audit core. It now has a Python domain package, fixture audit workflow, reproducible audit package output, provider access model, Tauri + React app shell, BYOK session boundary, fake OAuth boundary, the first OpenAI-compatible answer-provider boundary, a fixture-only Tauri command path, and a fixture-backed crawler provider boundary.

Current completion checkpoint:

- M0-M9: complete baseline GEO workflow.
- V2: complete evidence store, crawler seam, adapter contract, weighted scoring, operational report artifact.
- V3: complete fixture audit runner, recorded dataset loader, evidence graph store, diagnosis V2, CLI.
- V4: complete reproducible audit package with manifest, report, audit database, example fixture, schema docs, live adapter boundary.
- V5-0 through V5-6: complete UI/provider plan, provider registry, Tauri + React shell, BYOK session, fake OAuth flow, OpenAI-compatible answer-provider boundary, fixture-only command path, and static crawler provider boundary.
- First product TODO after this branch: `V5-7`.

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
5. Never persist raw access values.
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
| V5-5 | Add first OpenAI-compatible answer provider behind explicit config. | DONE |
| V5-5.5 | Add Tauri command path that runs the existing fixture audit. | DONE |
| V5-6 | Add crawler provider abstraction and first crawler adapter. | DONE |
| V5-7 | Wire UI Run Audit to provider registry, fixture/provider audit paths, and report display. | TODO |

## V5-6: Crawler Provider Abstraction

Goal: add a crawler-provider boundary that can feed page inventory/evidence without live crawling in CI.

Implemented files:

- `src/geo_agent/crawl_provider.py`
- `src/geo_agent/__init__.py`
- `tests/test_crawl_provider.py`
- `docs/provider-access-architecture.md`
- `docs/next-steps-plan.md`
- `docs/progress.md`

Acceptance evidence:

- `CrawlProviderRequest` represents provider id, manual URLs, sitemap URLs, chunk size, and metadata.
- `CrawlProviderResult` represents page records, typed errors, and metadata.
- `StaticCrawlerProvider` works in CI using fixture-backed pages and sitemaps.
- Crawl output converts to existing `PageInventoryRecord` objects and persists through `EvidenceStore.save_page_records()`.
- Crawl4AI and Firecrawl remain planned provider registry entries.
- CI remains network-free.

Verification:

- `tests/test_crawl_provider.py` covers static crawler success, failure, unsupported provider, request validation, redaction-shaped serialization, evidence store conversion, and planned live crawler registry entries.

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
| V6-5 | Access and artifact safety hardening. | Tests prove raw access values cannot appear in reports, manifests, logs, DB rows, or UI payloads. |
| V6-6 | Retest planning workflow. | Baseline and follow-up packages can be compared for visibility/citation/diagnosis deltas. |
| V6-7 | Release-readiness packaging checks. | CI verifies desktop app structure, Python package entry points, docs, and no dummy files. |
| V6-8 | Skill-learning records. | Optimization outcomes are stored by engine, query type, vertical, action, confidence, and result. |

## Review and Renewal Rules

Run Review and Renewal before adding more milestones when:

- V5 backlog completes;
- TODO backlog falls below the configured floor;
- CI or feedback repeats the same failure type;
- trace evidence is stale or missing;
- provider trust boundaries change;
- a milestone becomes too broad for one PR;
- user asks to re-evaluate direction.

New milestones must be specific, useful, verifiable, and non-duplicative. Do not add vague cleanup, polish, placeholder, broad refactor, or churn-only tasks.