# Autonomous Progress

> Base branch: `main`.
>
> State source rule: this file is the single milestone state source for the runner loop.
>
> Planning branch for this review-and-renewal: `v9-readiness-plan`.

## Status Legend

- TODO
- DONE

## Current Completion Summary

| Loop | State | Evidence |
| :--- | :--- | :--- |
| V1 bootstrap / MVP foundation | DONE | Historical foundation completed before retained V8 changelog. |
| V2 evidence/report hardening | DONE | Historical loop completed before retained V8 changelog. |
| V3 fixture audit productization | DONE | Historical loop completed before retained V8 changelog. |
| V4 reproducible audit package | DONE | Historical loop completed before retained V8 changelog. |
| V5 UI and provider access | DONE | Historical loop completed before retained V8 changelog. |
| V6 provider-backed GEO agent | DONE | Historical loop completed before retained V8 changelog. |
| V7 AI visibility workbench | DONE | Completed before V8; do not re-plan or redo. |
| V8 measurement foundation hardening | DONE | See `docs/v8-changelog.md`. |
| Loop V9 real-world readiness | TODO | V9-01 through V9-03 are DONE; V9-04 through V9-07 remain TODO. |

## Milestone State

| Milestone | Status | Title |
| :--- | :--- | :--- |
| V1 | DONE | Bootstrap MVP / initial audit foundation history |
| V2 | DONE | Evidence and report hardening history |
| V3 | DONE | Fixture audit productization history |
| V4 | DONE | Reproducible audit package history |
| V5 | DONE | UI and provider access history |
| V6 | DONE | Provider-backed GEO agent history |
| V7 | DONE | AI visibility workbench history |
| V8 | DONE | Measurement foundation hardening; see `docs/v8-changelog.md` |
| V9-01 | DONE | concrete-live-crawler-client |
| V9-02 | DONE | manual-capture-import-ux |
| V9-03 | DONE | desktop-real-report-loading |
| V9-04 | TODO | desktop-run-flow-wiring |
| V9-05 | TODO | extraction-regression-on-realistic-data |
| V9-06 | TODO | real-brand-validation-run |
| V9-07 | TODO | limitations-and-provider-matrix-refresh |

## Invariants

- First TODO is V9-04.
- V1 through V8 are DONE history and must not be re-planned.
- V9 adds no new analytics; it makes the existing engine real, usable, and validated.
- CI remains deterministic.
- Real web access remains opt-in.
