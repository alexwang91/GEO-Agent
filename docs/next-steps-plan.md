# Next Steps Plan

## Current State

V7-01 through V7-38 are DONE. The first product TODO is `V8-01`.

## Loop V8 Backlog

| Slice | Acceptance criteria | File targets | Verification / stop-if |
| :--- | :--- | :--- | :--- |
| V8-01 ci-and-test-harness-hardening | Harden `verify.yml`; add coverage, lint, and type gates; add invariant and error-path tests for scoring, extraction, and absorption. | `.github/workflows/verify.yml`, `tests/`, `tools/`, `src/geo_agent/visibility_scoring.py`, `src/geo_agent/engine_sampling.py`, `src/geo_agent/citation_absorption.py` | CI remains network-free. Stop if this changes V8-03 product behavior. |
| V8-02 extraction-eval-harness | Add gold fixtures for brand mentions and citation extraction. | `tests/fixtures/`, extraction tests. | Eval fixtures must expose current substring weaknesses. |
| V8-03 entity-resolution-brand-normalization | Replace substring matching with normalized brand, alias, and competitor matching. | Resolver, scoring, sampling, absorption, fidelity. | V8-02 fixtures pass. |
| V8-04 statistics-wiring | Wire repeated sampling and bootstrap summaries into report metrics. | Sampling, bootstrap, scoring, report, retest. | Reports show mean, interval, sample count, noise floor. |
| V8-05 crawler-real-fetch | Add opt-in live fetch with fake-client CI verification. | Crawler files and tests. | CI performs no live network work. |
| V8-06 desktop-backend-wiring | Replace hardcoded sample report path with generated package loading. | Desktop and backend files. | Sample artifacts are labeled as demo only. |
| V8-07 real-data-vertical-spike | Run one real brand spike and record findings. | Evaluation doc and sanitized notes. | No private data is committed. |
