# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for Generative Engine Optimization that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Current State

The repository has moved past the initial fixture-based GEO audit core. It now has a Python domain package, fixture audit workflow, reproducible audit package output, provider access model, Tauri + React app shell, BYOK session boundary, fake OAuth boundary, the first OpenAI-compatible answer-provider boundary, a fixture-only Tauri command path, a fixture-backed crawler provider boundary, product contract docs, provider-status language, limitations, and the first UX/copy contract.

Current completion checkpoint:

- M0-M9: complete baseline GEO workflow.
- V2: complete evidence store, crawler seam, adapter contract, weighted scoring, operational report artifact.
- V3: complete fixture audit runner, recorded dataset loader, evidence graph store, diagnosis V2, CLI.
- V4: complete reproducible audit package with manifest, report, audit database, example fixture, schema docs, live adapter boundary.
- V5: complete UI/provider plan, provider registry, Tauri + React shell, BYOK session, fake OAuth flow, OpenAI-compatible answer-provider boundary, fixture-only Tauri command path, static crawler provider boundary, and Run Audit/report display wiring.
- V6: complete provider-backed orchestration, manual/recorded import, provider output eval harness, evidence-backed report UI, access/artifact safety hardening, retest planning, release-readiness checks, and skill-learning records.
- V7-01: complete state-source audit, stale-milestone consistency test, current-agent handoff reconciliation, and alpha/technical-preview README boundary.
- V7-02: complete product contract, provider status language, limitations docs, and consistency checks across README, UI copy, docs, and provider registry labels.
- V7-03: complete personas, 10-step user journey, UX contract, report copy guidelines, error-state taxonomy, UI copy note, and copy-contract test.
- First product TODO: `V7-04` (see Loop V7 Backlog below and `docs/loop-v7.md`).

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
| V5-7 | Wire UI Run Audit to provider registry, fixture/provider audit paths, and report display. | DONE |

## V5-6: Crawler Provider Abstraction

Goal: add a crawler-provider boundary that can feed page inventory/evidence without live crawling in CI.

Verification: `tests/test_crawl_provider.py` covers static crawler success, failure, unsupported provider, request validation, redaction-shaped serialization, evidence store conversion, and planned live crawler registry entries.

## V5-7: UI Run Audit and Report Display

Goal: connect the UI to fixture and fake-provider audit paths and display report artifacts.

Acceptance criteria: UI can select fixture/manual-import path and fake-provider path, display generated report artifacts, represent export actions truthfully, distinguish provider status, and require no live credentials in CI.

## V6 Complete Development Plan

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

## Loop V7 Backlog: AI Search Visibility Experiment Workbench

V7 starts after V6. It repositions the product as an AI Search Visibility Experiment Workbench and hardens evidence traceability, real-answer ingestion, statistical credibility, diagnosis depth, executable owner-mapped tasks, retest loops, desktop UX, and reports. Design intent and the full slice-to-PR mapping live in `docs/loop-v7.md`. The first TODO is `V7-04` after V7-03 merges.

Each slice is one branch and one PR. Keep CI network-free unless a slice explicitly adds fake-client verification. Never persist raw access values. Add deterministic tests or structural checks before behavior changes.

### M0 - State source repair and product contract

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-01 | State docs agree on completed milestones and the first TODO; a CI test fails on stale/contradictory milestone state; README states the alpha/technical-preview boundary. | `docs/state-audit.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `README.md`, `tests/test_docs_state_consistency.py` | Test asserts no milestone is DONE in one state file and TODO in another, and that the declared first TODO exists and is TODO. |
| V7-02 | Product contract, provider-status language, and limitations docs exist; wording is consistent across README, UI copy, and docs. | `docs/product-contract.md`, `docs/provider-status-language.md`, `docs/limitations.md`, `docs/progress.md` | Structural test checks that provider status vocabulary matches registry labels. |

### M1 - UX contract

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-03 | Personas, the 10-step user journey, report copy guidelines, and an error-state taxonomy are documented; a copy-contract test enforces that report/UI copy distinguishes manual/simulated/live/planned and never states low-sample conclusions as definite. | `docs/ux-contract.md`, `docs/user-journeys.md`, `docs/personas.md`, `docs/report-copy-guidelines.md`, `docs/error-state-taxonomy.md`, `tests/test_ux_copy_contract.py` | Copy-contract test scans report/copy surfaces for overclaim phrasing and required provider-status labels. |

### M2 - Evidence graph

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-04 | Frozen dataclasses exist for AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord; each metric/diagnosis/task can reference the sample/prompt/citation/page IDs it derives from. | `src/geo_agent/evidence_store.py`, `src/geo_agent/schema.py`, `src/geo_agent/audit_runner.py`, `tests/test_evidence_graph.py` | Tests prove a fixture audit produces a complete evidence package and IDs link metrics back to samples. |
| V7-05 | Audit package manifest v2 records traceability from each metric to sample IDs; `audit.sqlite`, `manifest.json`, and `report.json` contain no secrets. | `src/geo_agent/fixture_package.py`, `src/geo_agent/report.py`, `tests/test_audit_package_manifest.py`, `tests/test_artifact_safety.py` | Manifest test asserts metric-to-sample-ID links; safety test asserts no credentials in any artifact. |

### M3-M17 - Remaining V7 backlog

V7-06 through V7-38 remain tracked in `docs/progress.md` and `docs/loop-v7.md`. The runner must select them from fresh progress state one milestone at a time.

## Review and Renewal Rules

Run Review and Renewal before adding more milestones when:

- V5 backlog completes;
- TODO backlog falls below the configured floor;
- CI or feedback repeats the same failure type;
- trace evidence is stale or missing;
- product direction changes.
