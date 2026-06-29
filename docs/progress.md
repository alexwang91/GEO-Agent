# Autonomous Progress

## Loop V9F Real-Case Fix Loop

Brand Huawei, single Perplexity/ChatGPT session + manually pasted Google AIO (AIO share links are gated and NOT auto-capturable). 15 real answers. Per-engine Huawei visibility (directional, n small):
- Perplexity n=6: mention 0.83, owned-citation 0.17, competitor-only 0.17, aggregate 0.48
- ChatGPT n=5: mention 0.60, owned-citation 0.40, competitor-only 0.40, aggregate 0.49
- Google AIO n=4: mention 1.00, owned-citation 1.00, competitor-only 0.00, aggregate 0.72
Key real insight: Huawei AI visibility is strongly ENGINE-DEPENDENT (healthy on AIO, third-party-driven on Perplexity, dropped from "best smartwatches" category queries on ChatGPT). A single-engine audit or a single aggregate score MISLEADS. Huawei is absent from high-intent "best smartwatches for Android/fitness" queries on Perplexity/ChatGPT. consumer.huawei.com (owned) shapes AIO (4/4) and ChatGPT (2/5) far more than Perplexity (1/6).

## Branch State

- Base branch: `main`
- Planning branch: `v9f-real-case-fixes`
- Loop: `Loop V9F evidence-driven real-case fixes`
- State source: this file
- First TODO: `V9F-1 fix-recommendation-matching`
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
| V9 | DONE | Historical real vertical-slice loop |
| V9F-1 | TODO | fix-recommendation-matching |
| V9F-2 | TODO | fix-manual-capture-recommendations-and-mention-dedup |
| V9F-3 | TODO | capture-to-package-bridge |
| V9F-4 | TODO | report-per-engine-and-component |
| V9F-5 | TODO | desktop-render-multi-engine |
| V9F-6 | TODO | record-evidence-and-honesty |
| V9F-7 | TODO | query-template-cleanup |

## Done Rule

A V9F milestone is DONE only when its deterministic regression test fails before the fix, passes after the fix, CI is green, and the milestone state plus evidence trail are updated. One milestone equals one branch, one PR, and CI verification before merge.

## Guardrails

- Fix backlog priority order is mandatory.
- Do not add new analytics modules.
- Reuse existing V7/V8 code and `entity_resolution` paths.
- Keep CI network-free.
- Never fabricate AI-engine answers or treat model/web-search output as a real engine sample.
- Keep Google AIO `manual_only`; AIO share links are gated and not auto-capturable.
- Keep single-sample and aggregate results labeled directional.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
