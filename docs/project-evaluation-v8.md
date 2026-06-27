# Project Evaluation V8

Evaluation date: 2026-06-27

## Summary

V7 completed the AI visibility workbench through V7-38. V8 hardens the foundation below that workbench.

## Current gaps

- Brand and mention extraction still relies on naive substring behavior in `visibility_scoring.py`.
- `crawl_provider_v2.py` is fixture/static oriented and does not perform real opt-in fetching.
- `verify.yml` previously ran only docs checks and unittest discovery.
- The desktop report path still needs real generated-package loading.
- Sampling and bootstrap helpers need report wiring.
- No real-data vertical spike has been recorded.

## V8-01 finding

The first hardening slice adds network-free verification gates and invariant/error-path tests before changing product behavior.
