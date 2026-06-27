# Next Steps Plan — V9 Vertical Slice

## Scope

Planning/docs only. V9 is one thin vertical slice, not a module backlog.

## Loop Done

One consented brand must complete: project setup -> real site crawl -> manual AI answer capture -> existing scoring/report path -> desktop report render -> retest delta with confidence.

Fixture CI is the regression gate. It is not the definition of DONE.

## Milestones

| Milestone | Acceptance |
| :--- | :--- |
| V9-1 minimal real FetchClient | Concrete `crawl_provider_v2.FetchClient`; robots, timeout, retry, errors; behind `allow_live_fetch`; one brand crawl documented. |
| V9-2 manual-capture import | Validated pasted answer and citation import; redaction checked; one or two real engines summarized in docs. |
| V9-3 desktop real report | Desktop loads real `manifest.json` and `report.json`; demo labeled demo; minimal brand -> run/prep -> view path documented. |
| V9-4 eval-first trust gate | Realistic answer/citation eval samples; precision/recall recorded; below-bar extraction must be fixed before trusting report. |
| V9-5 the real run | One consented brand full path; retest delta with confidence; findings and limits recorded in sanitized docs. |

## Guardrails

- No new analytics modules.
- Reuse V7/V8 measurement code.
- Real network access is opt-in and never in CI.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
- Planned providers stay planned.
