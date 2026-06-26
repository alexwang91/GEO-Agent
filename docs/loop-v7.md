# Loop V7: AI Search Visibility Experiment Workbench

> Status source rule: `docs/progress.md` is the single milestone state source. This file is the
> human-readable design intent for the V7 backlog (`V7-01` through `V7-38`). When this file and
> `docs/progress.md` conflict, stop and run the Review and Renewal Loop.

Loop V7 starts after V6 completed the provider-backed GEO agent core. V7 repositions the product and
hardens it across evidence traceability, real-answer ingestion, statistical credibility, diagnosis
depth, executable tasks, retest loops, and an end-to-end desktop UX, so a non-engineer can run a full
audit → diagnosis → task → retest cycle and trust the result.

## 1. Product Positioning

GEO-Agent is an **AI Search Visibility Experiment Workbench**. It helps a brand discover how users ask
AI engines, sample or import real AI answers, preserve evidence, measure brand/competitor mention,
citation, recommendation, and absorption, diagnose failure causes, generate cross-team tasks
(SEO, content, PR, engineering, product marketing, brand/legal), and verify whether actions worked
through retest comparison.

This matches the original product brief: monitor, diagnose, and improve brand/product/website/third-party
evidence visibility across ChatGPT Search, Perplexity, Google AI Overviews, Gemini, Claude Search, and
Bing Copilot.

### Non-promises (hard product contract)

- No guaranteed ranking improvement — AI answers are non-deterministic.
- The OpenAI-compatible API output is **not** ChatGPT Search UI output. Never equate them.
- No fully automated coverage of all answer engines. Planned providers stay labeled planned.
- No conclusion from insufficient sample size. A single sample is directional only.
- Improving only owned pages is not sufficient — third-party evidence networks matter.

## 2. Competitive and Industry Benchmarks

| Type | Reference | What V7 should learn |
| :--- | :--- | :--- |
| SEO + AI visibility platform | Semrush, Ahrefs | Use traditional SEO data as a GEO base; do not split GEO from SEO. |
| AI visibility enterprise | Profound | Engine coverage, brand mention, crawler interaction, recommendation dashboards. |
| GEO/brand analytics | Evertune | Repeated sampling across query variants and models; statistical recommendation frequency. |
| SEO data base | Ahrefs Brand Radar | Source graph, citation domains, competitor citation/backlink network. |
| Academic/OSS GEO optimizer | cxcscmu/AutoGEO | Engine-preference rule extraction + document rewriting as an optimization plugin; keep GEO and GEU separate so we never trade factual quality for citation. |
| Agent skill workflow | onvoyage-ai/gtm-engineer-skills | Package the system as reusable skills with clear inputs and concrete deliverable files. |
| Research methodology | stanford-oval/storm | Multi-perspective question generation, moderator for unknown-unknowns, outline-before-audit. |

### GitHub references applied

- **gtm-engineer-skills** → package GEO-Agent as a skill pipeline: research-query-space, run-ai-visibility-audit,
  diagnose-citation-failure, build-evidence-network, generate-geo-task-plan, run-retest, learn-optimization-outcomes.
- **AutoGEO** → optimization-rule layer: learn per query/engine/vertical preference rules; optimize for
  visibility without sacrificing utility; keep GEO score and GEU score separate.
- **STORM** → query discovery: multi-perspective generation, moderator for unknown-unknowns, research
  outline before audit; organize brand/competitor/source/query/failure/task as a mind map.

## 3. Brand-Practice Lessons

- **Integration (HubSpot/Semrush data):** do not silo GEO from SEO; output tasks per team
  (SEO, Content, PR, Product Marketing, Engineering, Brand/Legal).
- **Evertune:** require query variants, repeated sampling, confidence intervals, volatility labels,
  baseline/follow-up/holdout; never package one sample as a definite conclusion.
- **Profound:** add AI-crawler access import, source-selection map, engine-by-engine dashboard,
  bot/robots/noindex/sitemap diagnostics, evidence-backed content recommendations.
- **Google AIO research:** AIO/Gemini/organic return different sources and are unstable across runs and
  query rewrites — measure each surface separately; do not use organic ranking as an AIO-citation proxy.
- **AIO claim fidelity:** a meaningful share of AIO atomic claims are not supported by cited pages — add
  a claim-fidelity audit (claim → cited page → does the page support it → omission/unsupported/distorted).

## 4. UX Contract Overview

Personas: Founder/CMO, SEO Manager, Content Lead, PR Lead, Engineer, Agency. Each sees role-appropriate
output; none is forced to read provider schemas or raw JSON.

First-use journey (10 minutes to a sample audit):

1. Create Project — 6 fields only: brand, domain, competitors, region, language, business goal.
2. Review Query Space — clusters (not 300 raw prompts); user can delete/add/reprioritize/budget.
3. Choose Evidence Sources — plain-language provider status (manual / simulated / live / planned / unavailable).
4. Run Audit — product-language progress; failures give a next step, not a dead end.
5. Dashboard — answers four questions: where do I appear, where do competitors win, why am I missing,
   what next; core cards: visibility, mention/citation/recommendation share, absorption, competitor-only,
   coverage, confidence.
6. Query Drilldown — prompt, engine, result, cited sources, owned pages, diagnosis, recommended task, retest.
7. Task Handoff — grouped by owner (Content/SEO/PR/Engineering/Product Marketing/Legal-Brand).
8. Retest — experiment framing with baseline vs follow-up and confidence-aware judgments.

Every conclusion must link to raw evidence; low-sample conclusions must never read as definite.

## 5. Technical Architecture

```
Project Intake
  -> STORM-style Query Discovery
  -> Sampling Plan
  -> Provider Layer (Manual Import, OpenAI-compatible, Perplexity, Gemini, Google AIO capture, Browser capture schema)
  -> Crawler Layer (Static, Sitemap, Crawl4AI/Firecrawl, Page snapshot extractor)
  -> Evidence Graph (Prompts, Engine samples, Raw answers, Citations, Mentions, Page snapshots, Source network, Claims)
  -> Metrics (Mention/Citation/Recommendation share, Absorption, Claim fidelity, Sentiment, Competitor-only share, Confidence)
  -> Diagnosis Engine
  -> Optimization Task Engine
  -> Retest / Experiment Layer
  -> Skill Learning
  -> UI Workbench + Reports
```

## 6. Milestone Breakdown (Backlog V7-01 .. V7-38)

The runner executes one PR-sized slice per branch/PR. Slices map to the planning PRs (PR-001..PR-038)
and group under planning Milestones M0–M17. Acceptance criteria, file targets, and verification per slice
live in `docs/next-steps-plan.md`.

| Slice | PR | M | Title | Intent |
| :-- | :-- | :-- | :-- | :-- |
| V7-01 | PR-001 | M0 | docs-state-cleanup | State audit + CI consistency test so progress/next-steps/AGENTS agree; mark alpha/preview boundary. |
| V7-02 | PR-002 | M0 | product-contract-provider-status | product-contract, provider-status-language, limitations docs; consistent provider wording. |
| V7-03 | PR-003 | M1 | ux-contract-user-journeys | personas, user journeys, report copy guidelines, error-state taxonomy + copy contract test. |
| V7-04 | PR-004 | M2 | evidence-graph-schema | AuditRun, EngineSample, Citation/Mention/Recommendation, PageSnapshot, Claim, Diagnosis, Task, Retest, SkillOutcome objects. |
| V7-05 | PR-005 | M2 | audit-package-manifest-v2 | metric→sample-ID traceability; manifest/report/db carry no secrets. |
| V7-06 | PR-006 | M3 | query-discovery-perspectives | STORM multi-perspective generation + clusters. |
| V7-07 | PR-007 | M3 | query-ranker-dedupe | deterministic dedupe, ranker, citation-likelihood, business value. |
| V7-08 | PR-008 | M4 | manual-import-provider | manual ChatGPT/Perplexity/Gemini/AIO import into shared evidence graph. |
| V7-09 | PR-009 | M4 | browser-capture-schema | capture structure only; no fragile scraping. |
| V7-10 | PR-010 | M4 | provider-status-ui-copy | implemented/manual/simulated/planned/unavailable copy in UI + report. |
| V7-11 | PR-011 | M5 | crawler-provider-v2 | sitemap + manual URL + rendered-HTML fallback; per-page status. |
| V7-12 | PR-012 | M5 | page-snapshot-extractor | title/meta/headings/paragraphs/tables/FAQ/JSON-LD + hashes. |
| V7-13 | PR-013 | M6 | citation-parser-v1 | URL normalize, domain extract, dedupe, position. |
| V7-14 | PR-014 | M6 | source-classifier | owned/competitor/earned/review/community/directory/docs/marketplace/gov/academic/unknown. |
| V7-15 | PR-015 | M7 | citation-absorption-metric | selected vs absorbed (none/weak/material/strong). |
| V7-16 | PR-016 | M7 | claim-fidelity-audit | supported/partially/unsupported/contradicted + evidence span. |
| V7-17 | PR-017 | M8 | repeated-sampling-plan | runs_per_prompt, engines, region/language, sample budget. |
| V7-18 | PR-018 | M8 | bootstrap-confidence-interval | mean/CI, volatility, noise floor, improvement judgment. |
| V7-19 | PR-019 | M9 | diagnosis-taxonomy-v3 | root-cause failure types with evidence IDs + confidence + recommended owner. |
| V7-20 | PR-020 | M10 | optimization-task-engine-v2 | owner/target asset/exact change/evidence/expected metric/risk/retest. |
| V7-21 | PR-021 | M10 | task-owner-export | owner mapping + Markdown/CSV/JSON export. |
| V7-22 | PR-022 | M11 | retest-plan | same prompt/engine/region/language + holdout clusters. |
| V7-23 | PR-023 | M11 | retest-comparison-stats | delta + attribution; no false attribution; noise-floor → inconclusive. |
| V7-24 | PR-024 | M12 | desktop-project-setup | Project Setup page (6 fields). |
| V7-25 | PR-025 | M12 | desktop-query-space-review | Query Space Review page (clusters, edit/budget). |
| V7-26 | PR-026 | M12 | desktop-evidence-source-setup | Evidence Source Setup page with truthful status. |
| V7-27 | PR-027 | M12 | desktop-run-audit | Run Audit page (product-language progress, failure next steps). |
| V7-28 | PR-028 | M12 | desktop-dashboard | Dashboard: four questions + metric cards + confidence. |
| V7-29 | PR-029 | M12 | desktop-query-drilldown | Query Drilldown + Citation Map. |
| V7-30 | PR-030 | M12 | desktop-diagnosis-task-plan | Diagnosis + Task Plan + Export pages. |
| V7-31 | PR-031 | M13 | report-system-v2 | executive/SEO/content/PR/engineering/appendix/retest reports. |
| V7-32 | PR-032 | M13 | secret-redaction-hardening | no secret leakage across report v2 outputs. |
| V7-33 | PR-033 | M14 | skill-learning-layer | outcome record + recommender feeding next task generation. |
| V7-34 | PR-034 | M15 | industry-template-b2b-saas | B2B SaaS template (queries, source weights, tasks, sample report). |
| V7-35 | PR-035 | M15 | industry-template-ecommerce | ecommerce template. |
| V7-36 | PR-036 | M15 | industry-template-local-service | local-service template (+ media site as needed). |
| V7-37 | PR-037 | M16 | sample-audit-package | sample package + design-partner alpha scaffolding (M16 validation tracked off-loop). |
| V7-38 | PR-038 | M17 | public-preview-docs | quickstart, provider-matrix, limitations, examples for public technical preview. |

> Off-loop note: M16 design-partner alpha is a real-world validation activity (run 3 brands, collect
> feedback), not a CI-verifiable code PR. Its code/doc scaffolding lives in V7-37; the validation itself
> is tracked here and in the long-run growth loop, not as a runner milestone.

## 7. Differentiation

Do not fight Semrush/Ahrefs on SEO data, Profound/Evertune on enterprise coverage, or AutoGEO on
algorithm papers. V7's edge: explainable + locally reproducible + raw-evidence traceability + deep
diagnosis + executable owner-mapped tasks + repeated-sampling credibility + retest loop + skill learning,
with AutoGEO-style optimization as a plugin rather than the whole product.

## 8. Recommended Sequence

The backlog order is already dependency-ordered and Alpha-first: fix docs/contract (V7-01..02) → UX
contract (V7-03) → evidence graph (V7-04..05) → STORM query discovery (V7-06..07) → manual import +
provider status (V7-08..10) → crawler/snapshot (V7-11..12) → citation parsing/classification
(V7-13..14) → absorption + claim fidelity (V7-15..16) → repeated sampling + stats (V7-17..18) →
diagnosis (V7-19) → tasks (V7-20..21) → retest (V7-22..23) → desktop UX (V7-24..30) → reports +
redaction (V7-31..32) → skill learning (V7-33) → industry templates (V7-34..36) → sample package +
preview docs (V7-37..38).

First principle: not "help users write GEO content," but "help users use evidence to understand why AI
mentions others and not them, then change that result with repeatable, retestable actions."
