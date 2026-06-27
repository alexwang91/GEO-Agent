# Loop V9 — Real-World Readiness

## Intent

Loop V9 turns the fixture-proven GEO-Agent engine into a real, usable, validated technical-preview product. It does not add new analytics. It makes the existing measurement system acquire real evidence, load real reports, support a usable desktop flow, and validate behavior on realistic data.

## Rationale

Loop V8 hardened the measurement foundation. The next step is not another scoring model or abstract planning loop. The product must answer a narrower operational question:

> Can a user collect real evidence, run the existing pipeline, inspect a real report, and trust the limitations?

## Non-goals

- Do not re-plan V7 or V8.
- Do not redo entity resolution, extraction fallback, bootstrap statistics, or CI harness work completed in V8.
- Do not add new analytics unless required to make existing paths usable.
- Do not add live network access to CI.
- Do not overclaim provider support.

## Design Principles

1. Real acquisition before new analysis: the current gap is data acquisition and usability, not another metric.
2. Manual capture is a first-class bridge while live APIs remain planned.
3. Live network is explicit and opt-in: crawler HTTP access must require `allow_live_fetch=True` and stay covered by fake-client CI tests.
4. Desktop must load real artifacts: demo fixtures are acceptable only when explicitly labeled demo.
5. Validation must be honest: at least one sanitized real-brand run is needed before stronger readiness claims.
6. Provider truth labels are product safety: planned providers remain planned until implemented and verified.

## Backlog Order

1. V9-01 concrete-live-crawler-client
2. V9-02 manual-capture-import-ux
3. V9-03 desktop-real-report-loading
4. V9-04 desktop-run-flow-wiring
5. V9-05 extraction-regression-on-realistic-data
6. V9-06 real-brand-validation-run
7. V9-07 limitations-and-provider-matrix-refresh

## Verification Philosophy

GitHub Actions `verify` remains the gate. CI must stay deterministic and network-free. Real network behavior belongs behind explicit opt-in seams and should be tested with fake clients, recorded fixtures, or sanitized offline artifacts.
