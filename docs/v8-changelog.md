# Loop V8 Change Log

## Summary

Loop V8 hardens the completed V7 workbench foundation.

## Completed slices

- V8-01: CI/test harness hardening with network-free style, type, coverage, docs, and unit-test gates.
- V8-02: Extraction eval harness covering brand boundaries, aliases, diacritics, URL extraction, fallback mentions, and false positives.
- V8-03: Entity normalization for visibility scoring and engine-run extraction fallback.
- V8-04: Statistics wiring for mean, confidence interval, sample count, noise floor, and inconclusive deltas.
- V8-05: Opt-in crawler fetch seam verified with fake clients in CI.
- V8-06: Desktop wiring decision recorded: demo/sample artifacts must be labeled as demo and generated artifacts must be separated from fixture output.
- V8-07: Real-data vertical spike recorded as sanitized dry-run evidence without private data.

## Cleanup

Old V7 planning language is superseded by this file, `docs/progress.md`, and the V8 test/code changes. Do not merge stale V8 planning branches.

## Verification

Final VERIFY is GitHub Actions `verify` on the merged V8 completion branch.
