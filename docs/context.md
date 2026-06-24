# GEO Agent Context

This file defines the shared language for future agent work. Update it when a term, module boundary, or product concept becomes durable.

## Product Terms

| Term | Meaning |
| --- | --- |
| Entity Profile | The normalized brand/domain/competitor/customer input record. |
| Query Space | Deterministic set of query records grouped by intent, region, language, and engine. |
| Page Inventory | Structured representation of crawlable owned pages and extracted evidence. |
| Engine Run | One sampled answer for one query, engine, region, and language. |
| Raw Evidence | Unmodified answer text, citations, source domains, mentions, and recommendations. |
| Visibility Score | Aggregated metrics that describe whether the brand appears, is cited, is recommended, and has source diversity. |
| Failure Diagnosis | Evidence-backed label explaining why the brand was absent, uncited, misattributed, or not recommended. |
| Optimization Task | Draft-only action tied to a page, query cluster, failure type, risk, and retest plan. |
| Experiment Plan | Train, validation, and holdout query groups plus paired pre/post retests. |
| Operational Report | A user-facing evidence view with scores, missing queries, competitor map, cited sources, failures, and actions. |

## Naming Rules

- Use `EngineRun` only for recorded answer evidence.
- Use `QueryRecord` only for planned sampling records.
- Use `PageInventoryRecord` only for owned-page evidence.
- Use `ReportView` only for generated output, not for internal scoring.
- Avoid vague names such as `result`, `data`, `thing`, `agent_output`, or `analysis_blob` in public APIs.

## Architecture Seams

| Seam | Purpose |
| --- | --- |
| Intake | Validate and normalize entity profile input. |
| Planner | Generate query records and experiment plans. |
| Evidence Store | Persist raw runs, pages, scores, diagnoses, tasks, and reports. |
| Adapters | Isolate crawling and engine sampling from domain logic. |
| Scoring | Convert stored evidence into deterministic metrics. |
| Diagnosis | Classify failures from evidence and page context. |
| Reporting | Produce operational output for users and retests. |
