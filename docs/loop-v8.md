# Loop V8: Foundation Hardening

Status: planned
First TODO: `V8-01`
Base branch: `main`
Planning branch: `v8-foundation-hardening-plan`

## Purpose

Loop V8 is a Review-and-Renewal loop after V7. It does not re-plan V7 and does not bootstrap the repo from scratch. V7 is complete through `V7-38`. V8 starts from current `main` and hardens the foundation under the existing V7 analytical modules.

## Design principle

Harden the foundation first:

1. extraction correctness;
2. real data acquisition;
3. statistical honesty;
4. verification rigor;
5. functional desktop execution;
6. one real-data vertical spike.

Retrofit those foundations under the existing V7 modules instead of adding another analytics layer.

## As-built V7 assessment

V7 added the AI visibility workbench superstructure:

- query discovery and query-space expansion;
- citation parsing and source classification;
- citation absorption and claim fidelity;
- repeated sampling and bootstrap statistics helpers;
- diagnosis taxonomy v3;
- optimization task v2 records with evidence IDs, owner hints, and effort;
- retest v2 records;
- report v2 structures;
- skill-learning v2 records;
- industry templates;
- crawler provider v2 and page snapshot extraction;
- a larger test surface.

Those additions improved the product shape. They did not yet prove that the lower-level inputs are correct enough for the analytics to be trusted.

## Foundation gaps to retrofit

| Gap | Current risk | Retrofit target |
| :--- | :--- | :--- |
| Brand extraction | Substring matching creates false positives and false negatives. | Tokenized, normalized entity resolution across scoring, sampling, absorption, and claim fidelity. |
| Crawling | Static fixture/rendered HTML path cannot fetch a live site. | Opt-in HTTP fetcher with robots, timeout, and error status records; fake-client CI boundary. |
| CI | Bare unittest discovery lacks coverage, lint, typing, and invariant/error-path checks. | `verify.yml` becomes a meaningful verification harness before behavior changes. |
| Desktop UI | Report view loads hardcoded sample artifacts and disabled controls. | Desktop loads real generated packages, lists providers, and lets a user run the loop end-to-end. |
| Statistics | Sampling and bootstrap helpers exist, but reports may still show point estimates. | Mean plus confidence interval reporting, directional labels for single/low sample, inconclusive deltas under noise floor. |
| Real data | No recorded real-data vertical spike proves end-to-end behavior. | One real brand spike from crawl/import through extraction, diagnosis, task, retest, and findings record. |

## V8 backlog

Each slice is one branch and one PR. CI is VERIFY. Keep CI network-free unless the slice explicitly adds fake-client verification. Real crawling must never run in CI.

### V8-01 ci-and-test-harness-hardening

Goal: add verification rigor before changing product behavior.

Acceptance:

- `.github/workflows/verify.yml` runs unit tests with coverage and adds ruff lint plus mypy or an equivalent type check.
- Invariant and error-path tests cover scoring, extraction inputs, citation absorption, and unsafe/empty provider data.
- Existing tests still pass.
- CI remains network-free.

Primary file targets:

- `.github/workflows/verify.yml`
- `pyproject.toml` or equivalent tool config
- `tests/`
- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/citation_absorption.py`

Stop if:

- CI requires live network access.
- The slice rewrites product behavior instead of hardening verification.

### V8-02 extraction-eval-harness

Goal: make extraction quality measurable before replacing extraction logic.

Acceptance:

- Gold-set fixtures cover multi-word names, aliases, acronyms, diacritics, false-positive domains, competitor mentions, and citation extraction edge cases.
- Eval output reports precision, recall, false positives, and false negatives for brand mentions and citation extraction.
- Tests fail when substring-only matching passes obvious false-positive cases.

Primary file targets:

- `tests/fixtures/` or equivalent eval fixture path
- `tests/test_*extraction*`
- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/engine_sampling.py`

Stop if:

- The harness bakes in implementation-specific shortcuts.
- It cannot fail against the current naive substring behavior.

### V8-03 entity-resolution-brand-normalization

Goal: replace substring matching with tokenized, normalized entity resolution.

Acceptance:

- Brand, alias, and competitor matching handles token boundaries, case, punctuation, Unicode normalization, acronyms, aliases, and diacritics.
- `visibility_scoring.py` and `engine_sampling.py` stop relying on raw substring checks for brand presence.
- A fallback mention/citation parser runs when the provider returns no structured fields.
- `citation_absorption.py` and `claim_fidelity.py` use the shared normalized parser/resolver where relevant.
- V8-02 eval fixtures pass.

Primary file targets:

- new entity-resolution module under `src/geo_agent/`
- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/engine_sampling.py`
- `src/geo_agent/citation_absorption.py`
- `src/geo_agent/claim_fidelity.py`
- extraction eval tests

Stop if:

- Matching becomes opaque or non-deterministic.
- The change reduces precision or recall against V8-02 fixtures without an explicit documented tradeoff.

### V8-04 statistics-wiring

Goal: make reported numbers statistically honest.

Acceptance:

- `repeated_sampling.py` and `bootstrap_stats.py` drive reported visibility, citation, and recommendation metrics as mean plus confidence interval where repeated samples exist.
- Single-sample results are labeled directional-only.
- Deltas inside the noise floor are reported as inconclusive, not wins/losses.
- `report_v2.py` exposes metric summaries that include sample count, directionality, confidence interval, and noise-floor language.

Primary file targets:

- `src/geo_agent/repeated_sampling.py`
- `src/geo_agent/bootstrap_stats.py`
- `src/geo_agent/visibility_scoring.py`
- `src/geo_agent/report_v2.py`
- retest v2 comparison modules
- report/statistics tests

Stop if:

- Reports still render only point estimates where repeated samples exist.
- Low-sample outputs use decisive language.

### V8-05 crawler-real-fetch

Goal: add real opt-in crawling while keeping CI fixture-safe.

Acceptance:

- `crawl_provider_v2.py` includes an opt-in HTTP fetcher with timeout, robots/error handling, status records, and deterministic fake-client tests.
- The old dead `page_inventory.py` `UrlLibPageFetcher` seam is retired or clearly superseded.
- CI never performs live network calls.
- Manual/local usage can fetch real pages when explicitly configured.

Primary file targets:

- `src/geo_agent/crawl_provider_v2.py`
- `src/geo_agent/page_inventory.py`
- crawler provider tests
- docs for local opt-in behavior

Stop if:

- Any CI path performs live HTTP.
- Fetch errors get swallowed without structured status records.

### V8-06 desktop-backend-wiring

Goal: make the desktop app load real generated results instead of sample artifacts.

Acceptance:

- `apps/desktop/src/App.jsx` no longer imports hardcoded `sampleManifestArtifact` and `sampleReportArtifact` as the active report source.
- The app can load a generated report package from backend/Tauri handlers.
- `list_providers` is wired to the UI.
- Brand form and query-generation handlers are real enough for a non-engineer to start an end-to-end loop.
- Sample data may remain only as an explicit demo/fallback state, labeled as such.

Primary file targets:

- `apps/desktop/src/App.jsx`
- `apps/desktop/src/reportArtifacts.js`
- Tauri command/backend files
- provider registry/list-provider integration
- desktop tests or structural checks

Stop if:

- The report page still defaults to pretending sample data is a generated package.
- Credentials or raw access values can enter persisted artifacts.

### V8-07 real-data-vertical-spike

Goal: run one real brand end-to-end and record what breaks.

Acceptance:

- One real brand is exercised through real/manual import, real crawl, real extraction, diagnosis, optimization task generation, and retest planning or retest evidence.
- Findings, regressions, and manual caveats are recorded in `docs/project-evaluation-v8.md`.
- Any bugs found become explicit follow-up TODOs or stop conditions.
- The spike does not add secrets or private raw access values to repo artifacts.

Primary file targets:

- `docs/project-evaluation-v8.md`
- spike notes or sanitized evidence references
- relevant tests/regression fixtures from observed failures

Stop if:

- The spike requires committing private credentials, private customer data, or unsanitized provider output.
- The run cannot be reproduced or audited enough to inform product decisions.

## Retrofit mapping

| Existing V7 module | V8 retrofit |
| :--- | :--- |
| `visibility_scoring.py` | Replace substring matching, add statistical summaries where repeated samples exist. |
| `engine_sampling.py` | Normalize provider outputs and fallback parse missing mentions/citations. |
| `citation_absorption.py` | Use normalized citation/source identity and extraction fixtures. |
| `claim_fidelity.py` | Share normalized text/entity parsing where claim support depends on entity identity. |
| `repeated_sampling.py` | Feed report metrics instead of remaining a planning helper only. |
| `bootstrap_stats.py` | Feed mean/CI/noise-floor summaries into reports and retest deltas. |
| `report_v2.py` | Render statistical honesty and low-sample language in metric summaries. |
| `crawl_provider_v2.py` | Add opt-in live fetch with fake-client verification. |
| `apps/desktop/src/App.jsx` | Load generated artifacts and backend provider state instead of hardcoded samples. |

## State rule

`docs/progress.md` remains the single milestone state source. `docs/next-steps-plan.md` contains acceptance detail. This file explains design intent and retrofit mapping only.
