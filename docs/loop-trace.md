# Trace

## Current Loop

- Loop: V11 real-case reliability
- Base branch: `main`
- First TODO: `V11-02 collect-sanitized-manual-capture`
- Final V10 merge commit: `90b57fca7c423ad2f209ee009c6ac2f34c39778a`
- Post-merge audit commit: `0372b61a9487de67f054d93b0a87020503749309`

## V10 merged milestone ledger

| Milestone | PR | Branch | Verification | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| V10-01 | #115 | `v10-geo-research-integration-plan` | verify 332 | merged |
| V10-02 | #116 | `v10-02-recommendation-matching` | verify 334 | merged |
| V10-03 | #117 | `v10-03-manual-capture-dedup` | verify 336 | merged |
| V10-04 | #118 | `v10-04-capture-package-bridge` | verify 338 | merged |
| V10-05 | #119 | `v10-05-visibility-metrics` | verify 340 | merged |
| V10-06 | #120 | `v10-06-report-decomposition` | verify 347 | merged |
| V10-07 | #121 | `v10-07-citation-feature-schema` | verify 349 | merged |
| V10-08 | #122 | `v10-08-feature-gap-diagnosis` | verify 351 | merged |
| V10-09 | #123 | `v10-09-sampling-provider-matrix` | verify 365 | merged |
| V10-10 | #124 | `v10-10-optimization-taxonomy` | verify 373 | merged |
| V10-11 | #125 | `v10-11-plugin-boundary` | verify 375 | merged |
| V10-12 | #126 | `v10-12-interface` | verify 377 | merged |
| V10-13 | #127 | `v10-13-ui-brand-preview` | verify 379 | merged |
| V10-14 | #128 | `v10-14-ui-preview-artifact` | verify 382 | merged |
| V10-15 | #129 | `v10-15-ui-import` | verify 384 | merged |
| V10-16 | #130 | `v10-16-skill-packaging` | verify 386 | merged |
| V10-17 | #131 | `v10-17-release-guards` | verify 389 | merged |

## V11-01

- Branch: `v11-01-smoke-harness`
- Added `src/geo_agent/real_case_smoke.py`.
- Added `fixtures/smoke/template.json`.
- Added `docs/v11-real-case-smoke-report.md`.
- Added `tests/test_v11_real_case_smoke.py`.
- Boundary: template data is not product evidence.

## Guardrails retained

- CI remains network-free.
- Real AI-engine evidence must come from explicit manual capture or sanctioned provider paths.
- Manual-only providers must not be described as live providers.
- Per-engine results stay primary; aggregate results stay directional.
- External rewrite and distribution systems stay behind plugin or downstream interfaces.
- Skill packages preserve evidence IDs and return artifact references only.
- No secrets in docs, manifests, reports, logs, databases, or UI state.

## Next

V11-02 must collect or import actual sanitized manual capture data before any reliability claim.
