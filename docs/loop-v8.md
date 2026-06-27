# Loop V8: Foundation Hardening

Status: active
First TODO: `V8-01`

Loop V8 hardens the foundation under the completed V7 workbench. It does not re-plan V7 and does not bootstrap from scratch.

## Backlog

1. `V8-01` ci-and-test-harness-hardening.
2. `V8-02` extraction-eval-harness.
3. `V8-03` entity-resolution-brand-normalization.
4. `V8-04` statistics-wiring.
5. `V8-05` crawler-real-fetch.
6. `V8-06` desktop-backend-wiring.
7. `V8-07` real-data-vertical-spike.

## V8-01 acceptance

`verify.yml` must run network-free unit tests, coverage, lint, and type/annotation checks. V8-01 must add invariant and error-path tests for scoring, extraction inputs, citation absorption, and provider-data edge cases without changing V8-03 entity-resolution behavior.
