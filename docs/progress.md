# Autonomous Progress

## Branch State

- Base branch: `main`
- Current loop: `V12 seo-geo-subject-classifier`
- First TODO: `V12-00 state-source`
- V10 completion report: `docs/v10-completion-report.md`
- V11 plan: `docs/v11-reliability-loop-plan.md`
- V11 human-only pending TODO: `V11-02 collect-sanitized-manual-capture`
- V12 plan: `docs/loop-v12.md`

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
| V8 | DONE | Measurement foundation hardening |
| V9 | DONE | Historical history |
| V10-01 | DONE | evidence-and-integration-map |
| V10-02 | DONE | fix-recommendation-matching |
| V10-03 | DONE | fix-manual-capture-recommendations-and-mention-dedup |
| V10-04 | DONE | capture-to-package-bridge |
| V10-05 | DONE | position-adjusted-visibility |
| V10-06 | DONE | report-v2-selection-absorption-attribution |
| V10-07 | DONE | citation-level-feature-schema |
| V10-08 | DONE | content-feature-taxonomy-diagnosis |
| V10-09 | DONE | repeated-sampling-and-manual-only-provider-matrix |
| V10-10 | DONE | optimization-task-action-taxonomy |
| V10-11 | DONE | optimization-execution-plugin-boundary |
| V10-12 | DONE | geoflow-interface |
| V10-13 | DONE | ui-brand-form-query-preview |
| V10-14 | DONE | ui-reproducible-preview-artifact |
| V10-15 | DONE | ui-capture-package-import-wizard |
| V10-16 | DONE | yao-skill-packaging |
| V10-17 | DONE | yao-governance-evals-release-guards |
| V11-01 | DONE | real-case-smoke-harness |
| V11-02 | TODO | collect-sanitized-manual-capture |
| V12-00 | TODO | state-source |
| V12-01 | TODO | skill-scaffold |
| V12-02 | TODO | generalize-packaging-validator |
| V12-03 | TODO | classifier-function |
| V12-04 | TODO | diagnosis-pre-check |
| V12-05 | TODO | seo-action-taxonomy-out-of-core |
| V12-06 | TODO | docs |

## V11 Notes

- V11-01 adds the validation harness and report template only.
- Template data is not product evidence.
- V11-02 must replace the template with actual sanitized manual capture data before any reliability claim.
- V11-02 remains a human-only real-data task. Loop V12 work only touches V10-shipped planning, skill, classifier, and diagnosis boundaries and does not depend on V11-02 data collection.

## Loop V12 Notes

- V12 formalizes the SEO/GEO subject boundary for incoming asks.
- GEO-Agent routes only the GEO half into existing measurement, diagnosis, task-planning, and retest paths.
- Plain Google/Bing organic ranking providers remain absent from the provider matrix by design.
- SEO actions are named as out-of-core references only; GEO-Agent must not execute or measure them.
