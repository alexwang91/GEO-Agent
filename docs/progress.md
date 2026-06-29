# Autonomous Progress

## Loop V10 GEO-Research Integration

Loop V10 integrates GEO measurement research into GEO-Agent's core while preserving the product boundary: GEO-Agent measures, diagnoses, plans experiments, and retests AI search visibility. It does not become a content writer.

## Branch State

- Base branch: `main`
- Planning branch: `v10-geo-research-integration-plan`
- Loop: `Loop V10 GEO-research integration`
- State source: this file plus `docs/loop-v10.md`
- First TODO: `V10-05 position-adjusted-visibility`
- Runner mode: GitHub-only development; CI verifies; no local repository operations required.

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
| V9 | DONE | Historical real vertical-slice loop and V9F/UI follow-up history |
| V10-01 | DONE | evidence-and-integration-map |
| V10-02 | DONE | fix-recommendation-matching |
| V10-03 | DONE | fix-manual-capture-recommendations-and-mention-dedup |
| V10-04 | DONE | capture-to-package-bridge |
| V10-05 | TODO | position-adjusted-visibility |
| V10-06 | TODO | report-v2-selection-absorption-attribution |
| V10-07 | TODO | citation-level-feature-schema |
| V10-08 | TODO | content-feature-taxonomy-diagnosis |
| V10-09 | TODO | repeated-sampling-and-manual-only-provider-matrix |
| V10-10 | TODO | optimization-task-action-taxonomy |
| V10-11 | TODO | optimization-execution-plugin-boundary |
| V10-12 | TODO | geoflow-interface |
| V10-13 | TODO | ui-brand-form-query-preview |
| V10-14 | TODO | ui-reproducible-preview-artifact |
| V10-15 | TODO | ui-capture-package-import-wizard |
| V10-16 | TODO | yao-skill-packaging |
| V10-17 | TODO | yao-governance-evals-release-guards |

## Done Rule

A milestone is DONE only when its deterministic regression test/check passes, CI is green, and the milestone state plus evidence trail are updated. One milestone equals one branch, one PR, and CI verification before merge.

## Guardrails

- Implement V10 milestones in priority order.
- Keep GEO-Agent as a measurement, diagnosis, experiment, task-planning, and retest workbench.
- Put content rewriting and distribution behind plugin/downstream executor interfaces only.
- Reuse existing V7/V8 code and entity-resolution paths before adding new paths.
- Keep CI network-free.
- Use only explicit manual captures or sanctioned provider paths as real engine evidence.
- Keep Google AIO manual-only; AIO share links are gated and not auto-capturable.
- Keep DeepSeek, Kimi, Qianwen, and other Chinese AI engines manual-only unless a sanctioned provider path is explicitly added later.
- Keep per-engine results primary and label single-sample or aggregate results as directional.
- Do not store secrets in artifacts, logs, manifests, databases, or UI state.
