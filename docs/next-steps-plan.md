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
- V5: complete UI/provider plan, provider registry, Tauri + React shell, BYOK session, fake OAuth flow, OpenAI-compatible answer-provider boundary, fixture-only command path, static crawler provider boundary, and Run Audit/report display wiring (V5-0 through V5-7).
- V6: complete provider-backed orchestration, manual/recorded import, provider output eval harness, evidence-backed report UI, access/artifact safety hardening, retest planning, release-readiness checks, and skill-learning records (V6-1 through V6-8).
- V7-01: complete state-source audit, stale-milestone consistency test, current-agent handoff reconciliation, and alpha/technical-preview README boundary.
- First product TODO: `V7-02` (see Loop V7 Backlog below and `docs/loop-v7.md`).

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

## Loop V7 Backlog: AI Search Visibility Experiment Workbench

V7 starts after V6. It repositions the product as an AI Search Visibility Experiment Workbench and
hardens evidence traceability, real-answer ingestion, statistical credibility, diagnosis depth,
executable owner-mapped tasks, retest loops, desktop UX, and reports. Design intent and the full
slice-to-PR mapping live in `docs/loop-v7.md`. The first TODO is `V7-02` after V7-01 merges.

Each slice is one branch and one PR. Keep CI network-free unless a slice explicitly adds fake-client
verification. Never persist raw access values. Add deterministic tests or structural checks before
behavior changes.

### M0 - State source repair and product contract

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-01 | `docs/progress.md`, `docs/next-steps-plan.md`, `AGENTS.md`, `docs/handoff-decision.md`, and `docs/runner-prompt.md` agree on completed milestones and the first TODO; a CI test fails on stale/contradictory milestone state; README states the alpha/technical-preview boundary. | `docs/state-audit.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `README.md`, `tests/test_docs_state_consistency.py` | Test asserts no milestone is DONE in one state file and TODO in another, and that the declared first TODO exists and is TODO. Stop if state cannot be reconciled safely. |
| V7-02 | `product-contract.md` lists product promises and non-promises; `provider-status-language.md` defines the status vocabulary; `limitations.md` lists known limits; wording is consistent across README, UI copy, and docs. | `docs/product-contract.md`, `docs/provider-status-language.md`, `docs/limitations.md`, `docs/progress.md` | Structural test or doc check that the status vocabulary matches the provider registry labels. Stop if UI/docs claim more than the implemented boundary. |

### M1 - UX contract

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-03 | Personas, the 10-step user journey, report copy guidelines, and an error-state taxonomy are documented; a copy-contract test enforces that report/UI copy distinguishes manual/simulated/live/planned and never states low-sample conclusions as definite. | `docs/ux-contract.md`, `docs/user-journeys.md`, `docs/personas.md`, `docs/report-copy-guidelines.md`, `docs/error-state-taxonomy.md`, `tests/test_ux_copy_contract.py` | Copy-contract test scans report/copy fixtures for forbidden definite-conclusion phrasing and required provider-status labels. |

### M2 - Evidence graph

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-04 | Frozen dataclasses exist for AuditRun, PromptRecord, EngineSample, CitationRecord, MentionRecord, RecommendationRecord, PageSnapshot, ClaimRecord, DiagnosisRecord, OptimizationTask, RetestRecord, SkillOutcomeRecord; each metric/diagnosis/task can reference the sample/prompt/citation/page IDs it derives from. | `src/geo_agent/evidence_store.py`, `src/geo_agent/schema.py`, `src/geo_agent/audit_runner.py`, `tests/test_evidence_graph.py` | Tests prove a fixture audit produces a complete evidence package and IDs link metrics back to samples. |
| V7-05 | Audit package manifest v2 records traceability from each metric to sample IDs; `audit.sqlite`, `manifest.json`, and `report.json` contain no secrets. | `src/geo_agent/fixture_package.py`, `src/geo_agent/report.py`, `tests/test_audit_package_manifest.py`, `tests/test_artifact_safety.py` | Manifest test asserts metric→sample-ID links; safety test asserts no credentials in any artifact. |

### M3 - STORM-style query discovery

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-06 | Multi-perspective generator produces queries tagged with cluster and perspective across the documented clusters; supports a no-LLM fixture mode. | `src/geo_agent/query_discovery/perspectives.py`, `.../cluster_schema.py`, `.../generator.py`, `.../seed_sources.py`, `tests/test_query_discovery.py`, `docs/query-space-v2.md` | Deterministic fixture test covers perspectives, clusters, and no-LLM mode. |
| V7-07 | Default run yields 80-300 queries; each has cluster, perspective, business value, citation likelihood, and priority; dedupe is deterministic; users can review/delete/add/reprioritize. | `src/geo_agent/query_discovery/dedupe.py`, `.../ranker.py`, `.../citation_likelihood.py`, `tests/test_query_discovery.py` | Deterministic dedupe and ranking tests; range assertion on default output size. |

### M4 - Provider layer v2

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-08 | Manual-import provider validates the import schema (engine, capture_mode, captured_at, query, answer_text, citations, region, language) and feeds the shared evidence graph; rejects unsafe fields. | `src/geo_agent/providers/manual_import.py`, `src/geo_agent/manual_import.py`, `tests/test_manual_import_provider.py` | Tests cover valid import, schema rejection, and evidence-graph entry. Stop if import bypasses redaction. |
| V7-09 | Browser capture schema is defined as a structure (no scraping logic); documented as planned-live. | `src/geo_agent/providers/browser_capture.py`, `tests/test_browser_capture_schema.py` | Schema/serialization test only; no live calls. |
| V7-10 | Provider status copy uses implemented/manual_only/simulated/planned/unavailable in UI and report; OpenAI-compatible provider is never labeled ChatGPT Search; provider failure never renders as audit success. | `apps/desktop/src/components/ProviderStatusBadge.jsx`, `src/geo_agent/provider_access.py`, `tests/test_provider_status.py`, `tests/test_openai_compatible_copy.py` | Copy tests assert status literals and the no-ChatGPT-Search-equivalence rule. |

### M5 - Crawler provider v2

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-11 | Crawler v2 supports sitemap.xml (incl. nested), manual URLs, and rendered-HTML with fallback; per-page crawl status is surfaced; crawl failure does not block the audit; live crawler off by default in CI. | `src/geo_agent/crawlers/sitemap.py`, `.../static.py`, `.../base.py`, `tests/test_crawler_provider_v2.py` | Fixture-backed tests for sitemap parse, fallback, and failure isolation. |
| V7-12 | Page extractor produces PageSnapshot (title, meta, H1-H6, paragraphs, tables, FAQ, JSON-LD, schema types, html_hash, text_hash, fetched_at). | `src/geo_agent/crawlers/page_extractor.py`, `.../page_snapshot.py`, `tests/test_page_extractor.py`, `tests/fixtures/pages/` | Extraction tests against fixture pages. |

### M6 - Citation parser

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-13 | Parser normalizes URLs (param-insensitive), extracts domains, dedupes, and records citation position. | `src/geo_agent/citations/parser.py`, `.../normalize.py`, `.../answer_span.py`, `tests/test_citation_parser.py` | >=50 fixture samples; normalization and position tests. |
| V7-14 | Source classifier labels owned/competitor_owned/earned_media/review_site/community/directory/documentation/marketplace/government/academic/unknown with explainable reasons. | `src/geo_agent/citations/source_classifier.py`, `tests/test_source_classifier.py` | Classification tests including owned vs competitor domain detection. |

### M7 - Citation absorption and claim fidelity

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-15 | Absorption metric distinguishes cited-but-not-absorbed, weakly, materially, and strongly absorbed, with answer_overlap and claim_support scores and a none/weak/material/strong label. | `src/geo_agent/absorption/aligner.py`, `.../metric.py`, `tests/test_absorption_metric.py` | Tests cover each absorption label; report shows selection and absorption separately. |
| V7-16 | Claim fidelity audit extracts atomic claims and labels supported/partially_supported/unsupported/contradicted with an evidence span and confidence. | `src/geo_agent/absorption/claim_extractor.py`, `.../claim_verifier.py`, `tests/test_claim_fidelity.py` | Each fidelity result carries an evidence span; fixtures cover each label. |

### M8 - Repeated sampling and statistics

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-17 | RepeatedSamplingPlan captures prompts, engines, runs_per_prompt, region, language, sample budget, and schedule window. | `src/geo_agent/stats/repeated_sampling.py`, `tests/test_repeated_sampling.py` | Plan construction and budget tests. |
| V7-18 | Metric estimates report mean/median/CI/sample size/volatility/noise floor/judgment; single-sample reports are flagged directional only; deltas under the noise floor read inconclusive; low sample size lowers task confidence. | `src/geo_agent/stats/bootstrap.py`, `.../volatility.py`, `.../noise_floor.py`, `.../comparison.py`, `tests/test_bootstrap_ci.py`, `tests/test_retest_comparison_stats.py` | Bootstrap CI and comparison tests; directional-only and inconclusive gating asserted. |

### M9 - Diagnosis engine v3

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-19 | Diagnosis classifies the documented root-cause failure types, each result carries evidence IDs, a recommended owner, an action type, a retest plan, and a confidence; low confidence outputs needs_more_sampling. | `src/geo_agent/diagnosis/taxonomy.py`, `.../classifier.py`, `.../evidence_rules.py`, `.../confidence.py`, `tests/test_diagnosis_taxonomy.py`, `tests/test_diagnosis_evidence_links.py` | >=5 fixture cases per failure type; every diagnosis links evidence IDs. |

### M10 - Optimization task engine v2

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-20 | Tasks carry target cluster/engine, failure type, owner, target asset, action type, exact change, evidence IDs, expected metric/impact, confidence, risk, effort, and retest plan; no vague "write more content" output. | `src/geo_agent/tasks/schema.py`, `.../generator.py`, `.../risk.py`, `.../retest_plan.py`, `tests/test_task_generation.py` | Tests assert each task has owner, evidence, expected metric, risk, and retest; reject empty-advice output. |
| V7-21 | Owner mapping assigns each task to Content/SEO/PR/Engineering/Product Marketing/Legal-Brand; export to Markdown/CSV/JSON. | `src/geo_agent/tasks/owner_mapper.py`, `tests/test_task_owner_mapping.py` | Owner-mapping and export-format tests. |

### M11 - Retest / experiment layer

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-22 | Retest plan reuses the same prompts/engines/region/language and supports holdout clusters and changed-task/page references. | `src/geo_agent/retest/plan.py`, `tests/test_retest_plan.py` | Plan-equivalence tests for prompt/engine/region/language. |
| V7-23 | Comparison reports baseline vs follow-up with CI and a judgment; does not attribute success to unexecuted tasks; deltas under the noise floor read inconclusive; report is exportable. | `src/geo_agent/retest/compare.py`, `.../attribution.py`, `.../report.py`, `tests/test_retest_comparison.py`, `tests/test_task_attribution.py` | Attribution test rejects crediting unexecuted tasks; noise-floor gating asserted. |

### M12 - Desktop UI workbench

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-24 | Project Setup page collects brand, domain, competitors, region, language, goal. | `apps/desktop/src/pages/ProjectSetup.jsx` | UI flow test/structural check. |
| V7-25 | Query Space Review page shows clusters with edit/add/delete/reprioritize and sampling budget. | `apps/desktop/src/pages/QuerySpace.jsx` | UI flow test/structural check. |
| V7-26 | Evidence Source Setup page shows truthful provider status via ProviderStatusBadge. | `apps/desktop/src/pages/EvidenceSources.jsx`, `apps/desktop/src/components/ProviderStatusBadge.jsx` | Status-label test; provider failure not shown as success. |
| V7-27 | Run Audit page shows product-language progress and gives a next step on failure. | `apps/desktop/src/pages/RunAudit.jsx` | UI flow test; failure-state copy test. |
| V7-28 | Dashboard answers the four questions and shows metric cards plus a confidence badge; every conclusion links to evidence. | `apps/desktop/src/pages/Dashboard.jsx`, `apps/desktop/src/components/MetricCard.jsx`, `.../ConfidenceBadge.jsx`, `.../EvidenceLink.jsx` | Structural test that conclusions carry evidence links and low-confidence cues. |
| V7-29 | Query Drilldown and Citation Map render prompt, engine samples, raw answers, mentions, citations, absorption, competitor comparison, diagnosis, and task. | `apps/desktop/src/pages/QueryDrilldown.jsx`, `.../CitationMap.jsx` | Drilldown render test from package artifacts. |
| V7-30 | Diagnosis, Task Plan (grouped by owner), and Export pages let a user export the task plan. | `apps/desktop/src/pages/Diagnosis.jsx`, `.../TaskPlan.jsx`, `.../Export.jsx`, `apps/desktop/src/components/FailureTypeChart.jsx` | Export and owner-grouping tests. |

### M13 - Report system v2

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-31 | Executive, SEO/GEO, content brief, PR plan, engineering issues, evidence appendix, and retest reports generate in Markdown and JSON; each conclusion carries evidence references and states sample size/confidence. | `src/geo_agent/reports/executive.py`, `.../seo_report.py`, `.../content_brief.py`, `.../pr_plan.py`, `.../engineering_issues.py`, `.../evidence_appendix.py`, `.../retest_report.py`, `tests/test_report_v2.py`, `tests/test_report_evidence_links.py` | Evidence-link and confidence-statement tests. PDF deferred. |
| V7-32 | No secret leakage across report v2 outputs. | `src/geo_agent/reports/*`, `tests/test_report_no_secret_leakage.py` | Leakage test across all report outputs. |

### M14 - Skill learning layer

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-33 | After retest, an outcome record is generated (action_type, failure_type, vertical, engine, query_cluster, before/after metric, confidence, result_label); next task generation can reference history; without significance the result is not recorded as worked; outcomes are exportable. | `src/geo_agent/skill_learning/schema.py`, `.../recorder.py`, `.../recommender.py`, `.../outcome_store.py`, `tests/test_skill_outcome_record.py`, `tests/test_skill_recommender.py` | Recorder and recommender tests; significance gate asserted. |

### M15 - Industry templates

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-34 | B2B SaaS template generates 80+ queries with default source-type weights, task examples, and a sample report. | `templates/b2b_saas.yaml`, `tests/test_industry_templates.py` | Template generation test (>=80 queries, weights present). |
| V7-35 | Ecommerce template meets the same bar. | `templates/ecommerce.yaml`, `tests/test_industry_templates.py` | Same template test. |
| V7-36 | Local-service template (and media-site template as needed) meets the same bar. | `templates/local_service.yaml`, `templates/media_site.yaml`, `tests/test_industry_templates.py` | Same template test. |

### M16-M17 - Sample package and public preview

| Slice | Acceptance criteria | Likely files | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V7-37 | A sample audit package and a manual-import example exist; alpha scaffolding supports a 3-case design-partner run. The design-partner validation itself is tracked off-loop in `docs/loop-v7.md` and the growth loop, not as a runner milestone. | `examples/sample-audit-package/`, `examples/sample-report.md`, `examples/manual-import/` | Package-structure test; sample report renders. |
| V7-38 | Public technical preview docs are complete and do not overstate support: README implemented/not-implemented lists, quickstart, provider matrix, limitations, examples. | `README.md`, `docs/quickstart.md`, `docs/provider-matrix.md`, `docs/sample-audit.md`, `docs/limitations.md`, `examples/` | Doc-consistency check against the provider registry and product contract. |

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
