# Autonomous Progress

## Loop Success Criterion

Loop V9 is one thin vertical slice, not a module backlog. Success means one consented brand goes from project setup to real evidence, existing extraction/scoring/diagnosis/tasks, a real generated report rendered in the desktop app, and one retest with a measured delta and confidence.

## Branch State

- Base branch: `main`
- Requested planning branch: `v9-vertical-slice-plan`
- Actual planning branch: `v9-slice-plan`
- State source: this file
- First TODO: V9-1

## Milestone State

| Milestone | Status | Title |
| :--- | :--- | :--- |
| V1 | DONE | Historical foundation |
| V2 | DONE | Historical evidence/report hardening |
| V3 | DONE | Historical fixture audit productization |
| V4 | DONE | Historical reproducible audit package |
| V5 | DONE | Historical UI/provider access |
| V6 | DONE | Historical provider-backed agent |
| V7 | DONE | AI visibility workbench history |
| V8 | DONE | Measurement foundation hardening; see `docs/v8-changelog.md` |
| V9-1 | TODO | Minimal real FetchClient for the one brand site |
| V9-2 | TODO | Manual capture import for real AI answers |
| V9-3 | TODO | Desktop real report path |
| V9-4 | TODO | Eval-first trust gate |
| V9-5 | TODO | Real vertical-slice run and retest |

## Done Rule

A V9 milestone is DONE only when its part of the real case is proven and recorded in docs. Fixture CI is a regression gate, not the definition of DONE.

## Guardrails

- No new analytics modules.
- Reuse V7/V8 measurement code.
- Real network access is opt-in and never runs in CI.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
