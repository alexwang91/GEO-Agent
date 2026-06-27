# Project Evaluation V8

Evaluation date: 2026-06-27
Base evaluated: current `main` at the start of the Loop V8 planning branch.
Planning branch: `v8-foundation-hardening-plan`

## Executive finding

Loop V7 shipped a large analytical superstructure, but the foundation under that superstructure still needs hardening. Loop V8 should not add another analytics layer. It should retrofit correctness, live-data acquisition, statistical honesty, verification rigor, and a functional desktop path under the existing V7 modules.

## What V7 shipped

V7 completed the AI visibility workbench layer through V7-01..V7-38. The current repo includes or references these capability areas:

- `query_discovery/`
- `citation_parser`
- `source_classifier`
- `citation_absorption`
- `claim_fidelity`
- `repeated_sampling`
- `bootstrap_stats`
- `diagnosis_taxonomy_v3`
- `optimization_tasks_v2` with `evidence_ids`, `owner_hint`, and `effort`
- `retest_*_v2`
- `report_v2`
- `skill_learning_v2`
- `industry_templates`
- `crawl_provider_v2`
- `page_snapshot_extractor`
- an expanded test suite around the V7 workbench surface

That work improved product semantics, traceability, diagnosis vocabulary, task structure, and report organization. It did not fully harden the lower-level primitives that the new analytics depend on.

## Foundation gaps on current main

### 1. Brand and mention extraction remains naive

`src/geo_agent/visibility_scoring.py` still lowercases the brand and uses substring membership for mention detection. `_has_brand` returns true when the brand name appears anywhere in `raw_answer` or when a lowercased item matches the structured mentions set. This creates false positives for substrings, false negatives for aliases and diacritics, and inconsistent behavior between raw answers and structured provider fields.

Affected files to evaluate and retrofit:

- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/engine_sampling.py`
- `src/geo_agent/citation_absorption.py`
- `src/geo_agent/claim_fidelity.py`

Why it matters: absorption, claim fidelity, scoring, recommendation share, competitor-only share, and report language inherit the extraction errors.

### 2. Web crawling is still fixture/static only

`src/geo_agent/crawl_provider_v2.py` declares itself as structured status records without live network work. `StaticCrawlerProviderV2` reads fixture pages, sitemap fixtures, and rendered HTML. It records failures when no fixture or rendered HTML exists, but it does not fetch a live website.

Affected files to evaluate and retrofit:

- `src/geo_agent/crawl_provider_v2.py`
- `src/geo_agent/page_inventory.py`
- crawler tests and fixture/fake-client boundaries

Why it matters: the pipeline cannot validate owned-site content against real pages. Real-data GEO measurement remains blocked or manual.

### 3. CI remains bare

`.github/workflows/verify.yml` currently runs docs checks and `PYTHONPATH=src python -m unittest discover -s tests -v`. It does not enforce coverage, lint, type checks, or deeper invariant/error-path tests.

Affected files to evaluate and retrofit:

- `.github/workflows/verify.yml`
- `pyproject.toml` or equivalent tool configuration if needed
- `tests/`

Why it matters: fragile analytical modules can regress without targeted quality gates.

### 4. Desktop report path still uses hardcoded sample data

`apps/desktop/src/App.jsx` imports `sampleManifestArtifact` and `sampleReportArtifact` from `reportArtifacts` and builds the displayed report from those samples. It also hardcodes provider cards and keeps run buttons disabled.

Affected files to evaluate and retrofit:

- `apps/desktop/src/App.jsx`
- `apps/desktop/src/reportArtifacts.js`
- Tauri command handlers that should expose `list_providers`, generated report loading, brand form handling, and query generation

Why it matters: a non-engineer still cannot run the loop and inspect real generated output through the desktop app.

### 5. Statistics modules exist but appear unwired into reported numbers

`src/geo_agent/repeated_sampling.py` can build deterministic sampling plans. `src/geo_agent/bootstrap_stats.py` can produce mean, confidence interval, noise floor, sample count, and directionality. `src/geo_agent/report_v2.py` accepts a generic `metric_summary` and adds a low-sample guardrail, but it does not itself prove that visibility, citation, and recommendation numbers are distributions with confidence intervals rather than point estimates.

Affected files to evaluate and retrofit:

- `src/geo_agent/repeated_sampling.py`
- `src/geo_agent/bootstrap_stats.py`
- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/report_v2.py`
- retest comparison modules

Why it matters: single-point claims can look more certain than the sampling evidence supports.

### 6. No real-data end-to-end validation has been recorded

The repo has extensive fixture, fake-provider, and recorded-data boundaries, but Loop V8 should add a manually recorded vertical spike that exercises real brand data from acquisition through retest evidence.

Affected docs and evidence:

- `docs/project-evaluation-v8.md`
- a real-data spike note or package reference chosen during V8-07
- regression findings and stop conditions

Why it matters: the workbench can look complete in fixtures while failing on realistic pages, citations, aliases, and UI loading paths.

## Loop V8 decision

Set the first product TODO to `V8-01`. The runner should start with verification rigor, then make extraction quality measurable before replacing extraction logic, then wire statistics, crawling, desktop functionality, and finally one real-data vertical spike.

V8 principle:

> Harden the foundation and retrofit it under the existing V7 modules. Do not add more analytics on top until extraction, crawling, statistics, verification, and UI execution are credible.
