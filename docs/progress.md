# Autonomous Progress

> Base branch: `main`.
>
> State source rule: this file is the single milestone state source. `docs/next-steps-plan.md` provides acceptance criteria and implementation detail.

## Status Legend

- TODO
- IN_PROGRESS
- DONE
- BLOCKED
- DEFERRED
- CANCELLED

## Current Completion Summary

| Area | State | Evidence |
| :--- | :--- | :--- |
| Bootstrap MVP loop | DONE | M0-M9 are complete. |
| Loop V2 evidence/report hardening | DONE | V2-0 through V2-5 are complete. |
| Loop V3 fixture audit productization | DONE | V3-0 through V3-5 are complete. |
| Loop V4 reproducible audit package | DONE | V4-0 through V4-5 are complete. |
| Loop V5 UI and provider access | DONE | V5-0 through V5-7 are complete. |
| Complete loop planning package | DONE | V6 planning, long-run growth, handoff, and runner prompt files are installed. |
| Loop V6 provider-backed GEO agent | DONE | V6-1 through V6-8 are complete. |
| Loop V7 AI visibility workbench | TODO | V7-01 and V7-02 are DONE in this branch; V7-03 through V7-38 remain TODO. |

## Progress

| Milestone | Description | Status |
| :--- | :--- | :--- |
| M0 | Bootstrap runner docs, CI scaffold, product brief, feedback taxonomy, loop trace, and stopper policy. | DONE |
| M1 | Build domain intake and entity profile schema. | DONE |
| M2 | Implement deterministic query records with intent, funnel stage, language, region, engine, competitors, and priority. | DONE |
| M3 | Implement page inventory crawler. | DONE |
| M4 | Implement engine sampling records. | DONE |
| M5 | Implement visibility and citation scoring. | DONE |
| M6 | Implement citation failure debugger. | DONE |
| M7 | Generate optimization task briefs. | DONE |
| M8 | Add experiment planning. | DONE |
| M9 | Ship first dashboard or report view. | DONE |
| V2-0 | Install Loop V2, shared context, and decision log. | DONE |
| V2-1 | Add persistent evidence store for raw query-answer-citation history. | DONE |
| V2-2 | Replace parser-only page inventory with fetch-capable crawler seam. | DONE |
| V2-3 | Upgrade engine sampling adapter contract and recorded-run import path. | DONE |
| V2-4 | Rework scoring into weighted metric components with stronger edge-case tests. | DONE |
| V2-5 | Add evidence-backed operational report artifact and snapshot or JSON tests. | DONE |
| V3-0 | Install Loop V3 and productization plan. | DONE |
| V3-1 | Add `AuditRunner` orchestrating existing modules over fixtures. | DONE |
| V3-2 | Add recorded dataset schema and fixture loader. | DONE |
| V3-3 | Expand EvidenceStore beyond engine runs. | DONE |
| V3-4 | Add Diagnosis V2 using run, page, and competitor evidence. | DONE |
| V3-5 | Add CLI entry point for fixture-based audits. | DONE |
| V4-0 | Install V4 evaluation, loop, and reproducible audit package plan. | DONE |
| V4-1 | Persist the full audit evidence graph during `AuditRunner.run`. | DONE |
| V4-2 | Write reproducible audit package artifacts from CLI. | DONE |
| V4-3 | Add canonical example fixture and usage docs. | DONE |
| V4-4 | Publish recorded dataset schema documentation. | DONE |
| V4-5 | Document live adapter boundary without implementing live calls. | DONE |
| V5-0 | Install V5 evaluation, Tauri + React UI brief, provider access architecture, and loop plan. | DONE |
| V5-1 | Add provider access domain model and registry. | DONE |
| V5-2 | Add Tauri + React app shell. | DONE |
| V5-3 | Add BYOK API key session flow. | DONE |
| V5-4 | Add OAuth framework with fake provider. | DONE |
| PLAN-0 | Install complete Superpowers + GitHub Loop Runner planning package: V6 evaluation, V6 loop plan, long-run growth, handoff, and runner prompt files. | DONE |
| V5-5 | Add first OpenAI-compatible answer provider behind explicit config. | DONE |
| V5-5.5 | Add Tauri command path that runs the existing fixture audit. | DONE |
| V5-6 | Add crawler provider abstraction and first crawler adapter. | DONE |
| V5-7 | Wire UI Run Audit to provider registry, fixture/provider audit paths, and report display. | DONE |
| V6-1 | Add provider-backed audit orchestration that converts configured answer-provider output into existing evidence records. | DONE |
| V6-2 | Add manual import and recorded live-run import UX path with schema validation and redaction checks. | DONE |
| V6-3 | Add provider output eval harness for answer parsing, citation extraction, redaction, and deterministic fake-provider behavior. | DONE |
| V6-4 | Add evidence-backed report UI reading generated package artifacts and showing visibility, citation, diagnosis, and task briefs. | DONE |
| V6-5 | Add access and artifact safety hardening across CLI, Tauri commands, report artifacts, manifests, logs, and tests. | DONE |
| V6-6 | Add retest planning workflow that compares baseline and follow-up audit packages. | DONE |
| V6-7 | Add release-readiness packaging checks for desktop app structure, Python package, and docs. | DONE |
| V6-8 | Add skill-learning record for which optimization actions worked by engine, query type, and vertical. | DONE |
| V7-01 | Audit and reconcile doc state (progress, next-steps, AGENTS, handoff, runner prompt) and add a CI consistency test for stale milestones; mark the alpha/technical-preview boundary. | DONE |
| V7-02 | Add product-contract, provider-status-language, and limitations docs with consistent provider wording across README, UI, and docs. | DONE |
| V7-03 | Add UX contract: personas, user journeys, report copy guidelines, error-state taxonomy, and a copy-contract test. | TODO |
| V7-04 | Add evidence graph schema objects (AuditRun, EngineSample, Citation/Mention/Recommendation, PageSnapshot, Claim, Diagnosis, Task, Retest, SkillOutcome). | TODO |
| V7-05 | Add audit package manifest v2 with metric-to-sample-ID traceability and no-secret tests. | TODO |
| V7-06 | Replace template query builder with STORM-style multi-perspective query discovery and clusters. | TODO |
| V7-07 | Add query ranker, deterministic dedupe, citation-likelihood, and business value scoring. | TODO |
| V7-08 | Add manual-import provider (ChatGPT/Perplexity/Gemini/AIO) into the shared evidence graph. | TODO |
| V7-09 | Add browser-capture schema (structure only, no fragile scraping). | TODO |
| V7-10 | Add provider-status UI/report copy: implemented/manual/simulated/planned/unavailable. | TODO |
| V7-11 | Add crawler provider v2 (sitemap + manual URL + rendered-HTML fallback, per-page status). | TODO |
| V7-12 | Add page snapshot extractor (title/meta/headings/paragraphs/tables/FAQ/JSON-LD + hashes). | TODO |
| V7-13 | Add citation parser v1 (URL normalize, domain extract, dedupe, position). | TODO |
| V7-14 | Add source classifier (owned/competitor/earned/review/community/directory/docs/marketplace/gov/academic/unknown). | TODO |
| V7-15 | Add citation absorption metric (selected vs absorbed: none/weak/material/strong). | TODO |
| V7-16 | Add claim fidelity audit (supported/partially/unsupported/contradicted + evidence span). | TODO |
| V7-17 | Add repeated sampling plan (runs_per_prompt, engines, region/language, sample budget). | TODO |
| V7-18 | Add bootstrap confidence intervals, volatility, noise floor, and improvement judgment. | TODO |
| V7-19 | Add diagnosis taxonomy v3 with root-cause failure types, evidence IDs, confidence, and recommended owner. | TODO |
| V7-20 | Add optimization task engine v2 (owner/target asset/exact change/evidence/expected metric/risk/retest). | TODO |
| V7-21 | Add task owner mapping and Markdown/CSV/JSON export. | TODO |
| V7-22 | Add retest plan (same prompt/engine/region/language + holdout clusters). | TODO |
| V7-23 | Add retest comparison stats and attribution with noise-floor gate (inconclusive when below floor). | TODO |
| V7-24 | Add desktop Project Setup page (6 fields). | TODO |
| V7-25 | Add desktop Query Space Review page (clusters, edit, budget). | TODO |
| V7-26 | Add desktop Evidence Source Setup page with truthful provider status. | TODO |
| V7-27 | Add desktop Run Audit page (product-language progress, failure next steps). | TODO |
| V7-28 | Add desktop Dashboard (four questions + metric cards + confidence). | TODO |
| V7-29 | Add desktop Query Drilldown and Citation Map. | TODO |
| V7-30 | Add desktop Diagnosis, Task Plan, and Export pages. | TODO |
| V7-31 | Add report system v2 (executive/SEO/content/PR/engineering/appendix/retest). | TODO |
| V7-32 | Add secret-redaction hardening across report v2 outputs. | TODO |
| V7-33 | Add skill-learning layer (outcome record + recommender feeding next task generation). | TODO |
| V7-34 | Add B2B SaaS industry template (queries, source weights, tasks, sample report). | TODO |
| V7-35 | Add ecommerce industry template. | TODO |
| V7-36 | Add local-service industry template (and media site as needed). | TODO |
| V7-37 | Add sample audit package and design-partner alpha scaffolding (M16 validation tracked off-loop). | TODO |
| V7-38 | Add public technical preview docs (quickstart, provider-matrix, limitations, examples). | TODO |
