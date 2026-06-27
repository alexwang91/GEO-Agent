# Loop V9 — Thin Vertical Slice

## Intent

Loop V9 is one thin end-to-end vertical slice that delivers real user value on real data. It is not a module backlog.

## Success Criterion

One consented brand moves through this path:

Project setup -> real site crawl -> manually captured real AI answers -> existing extraction, scoring, diagnosis, and task draft path -> real generated report rendered in the desktop app -> one retest with measured delta and confidence.

## Framing

Matt Pocock vertical slicing: prefer a narrow working path across the stack over broad horizontal module work.

Superpowers eval-first: a milestone is not DONE because code exists or fixture CI is green. It is DONE only when its slice of the real case is proven and documented.

## Non-goals

- Do not add new analytics modules.
- Do not re-plan V7 or V8.
- Reuse existing measurement code.
- Do not run real network access in CI.
- Do not treat fixture CI as real user verification.

## Slice Milestones

1. V9-1 minimal real FetchClient.
2. V9-2 manual-capture import.
3. V9-3 desktop real report.
4. V9-4 eval-first trust gate.
5. V9-5 the real run.

## Done Rule

DONE requires real-case evidence recorded in docs. Fixture CI remains the regression gate only.
