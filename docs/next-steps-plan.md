# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for Generative Engine Optimization that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Current State

M0-M9 and Loops V2 through V6 are complete. Loop V7 is fully complete: V7-01 through V7-38 are DONE through PR #80. The first product TODO is now `V8-01`.

Loop V8 is a foundation-hardening retrofit. It starts from current `main` and hardens extraction correctness, crawling, statistics, verification, and desktop execution under the existing V7 modules. Design intent lives in `docs/loop-v8.md`. Code-grounded evaluation lives in `docs/project-evaluation-v8.md`.

## Operating Rules

1. Select the first TODO in `docs/progress.md`.
2. Use one branch and one PR per milestone.
3. CI is VERIFY.
4. Keep CI network-free unless the milestone explicitly uses a fake-client boundary.
5. Update progress, loop trace, and evidence notes in the milestone PR.
6. Merge only after CI is green.
7. Re-read progress before selecting the next milestone.

## Loop V8 Backlog

Each row is one branch and one PR. Complete the rows in order.

| Slice | Acceptance criteria | File targets | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V8-01 ci-and-test-harness-hardening | Add coverage, ruff lint, and mypy or equivalent to `verify.yml`; add invariant and error-path tests for scoring, extraction, and absorption. | `.github/workflows/verify.yml`, `tests/`, `src/geo_agent/visibility_scoring.py`, `src/geo_agent/engine_sampling.py`, `src/geo_agent/citation_absorption.py` | CI must remain network-free. Stop if this starts implementing V8-03 behavior. |
| V8-02 extraction-eval-harness | Add gold-set fixtures that measure precision and recall for brand mentions and citation extraction; cover multi-word names, aliases, acronyms, diacritics, and false-positive domains. | `tests/fixtures/`, extraction tests, `src/geo_agent/visibility_scoring.py`, `src/geo_agent/engine_sampling.py` | Tests must fail against obvious substring false positives on current main. |
| V8-03 entity-resolution-brand-normalization | Replace substring matching in `visibility_scoring.py` and `engine_sampling.py` with tokenized normalized brand, alias, and competitor matching; add fallback mention/citation parsing when structured fields are absent; point absorption and fidelity logic to the shared resolver where relevant. | New resolver module, `src/geo_agent/visibility_scoring.py`, `src/geo_agent/engine_sampling.py`, `src/geo_agent/citation_absorption.py`, `src/geo_agent/claim_fidelity.py` | V8-02 eval fixtures must pass. Stop if matching becomes non-deterministic. |
| V8-04 statistics-wiring | Ensure `repeated_sampling.py` and `bootstrap_stats.py` drive reported visibility, citation, and recommendation metrics as mean plus confidence interval; label single-sample output as directional-only; mark deltas under the noise floor as inconclusive. | `src/geo_agent/repeated_sampling.py`, `src/geo_agent/bootstrap_stats.py`, `src/geo_agent/visibility_scoring.py`, `src/geo_agent/report_v2.py`, retest v2 modules | Tests must assert mean, interval, sample count, noise floor, and inconclusive delta language. |
| V8-05 crawler-real-fetch | Add an opt-in live fetcher in `crawl_provider_v2.py` with robots, timeout, and error status handling; keep CI fixture-safe with a fake client; retire or supersede the dead `page_inventory.py` fetcher seam. | `src/geo_agent/crawl_provider_v2.py`, `src/geo_agent/page_inventory.py`, crawler tests | Stop if CI performs live network work. |
| V8-06 desktop-backend-wiring | Replace the hardcoded sample report path in `App.jsx`; load a generated package; wire `list_providers`; add real handlers for brand form and query generation. | `apps/desktop/src/App.jsx`, `apps/desktop/src/reportArtifacts.js`, Tauri/backend command files | Stop if sample artifacts still appear as real generated results. |
| V8-07 real-data-vertical-spike | Run one real brand through real data acquisition, extraction, diagnosis, task generation, and retest planning; record findings and regressions in `docs/project-evaluation-v8.md`. | `docs/project-evaluation-v8.md`, sanitized spike notes, regression fixtures | Stop if the spike cannot be audited or would require committing private data. |

## Review and Renewal Rules

Run Review and Renewal before adding more milestones when V8 completes, TODO backlog falls below the configured floor, CI or feedback repeats the same failure type, trace evidence is stale or missing, or product direction changes.
