# Loop V9F — Evidence-Driven Real-Case Fixes

## Directive

Loop V9F fixes concrete, real-data-proven bugs surfaced by a three-engine validation run for brand `Huawei`. This loop is an evidence-driven fix loop, not a new analytics buildout.

Use Matt Pocock vertical slicing and Superpowers eval-first discipline:

- One milestone equals one branch, one PR, one CI-verified merge.
- Each milestone starts with a deterministic failing test or structural check.
- The fix must reuse existing V7/V8 code where possible.
- The runner must not add new analytics modules.

## Real-Case Context

Brand Huawei, single Perplexity/ChatGPT session + manually pasted Google AIO (AIO share links are gated and NOT auto-capturable). 15 real answers. Per-engine Huawei visibility (directional, n small):
- Perplexity n=6: mention 0.83, owned-citation 0.17, competitor-only 0.17, aggregate 0.48
- ChatGPT n=5: mention 0.60, owned-citation 0.40, competitor-only 0.40, aggregate 0.49
- Google AIO n=4: mention 1.00, owned-citation 1.00, competitor-only 0.00, aggregate 0.72
Key real insight: Huawei AI visibility is strongly ENGINE-DEPENDENT (healthy on AIO, third-party-driven on Perplexity, dropped from "best smartwatches" category queries on ChatGPT). A single-engine audit or a single aggregate score MISLEADS. Huawei is absent from high-intent "best smartwatches for Android/fitness" queries on Perplexity/ChatGPT. consumer.huawei.com (owned) shapes AIO (4/4) and ChatGPT (2/5) far more than Perplexity (1/6).

## Priority Backlog

### V9F-1 fix-recommendation-matching

Highest priority. This corrupts core cross-brand comparison.

Bug: `src/geo_agent/visibility_scoring.py` `_same_entity` requires exact full-string equality through `len(value) == len(matched)`. Brand `Huawei` never matches recommendation strings like `Huawei Watch GT 6`, so `recommendation_share=0`, while `Apple Watch` can score from exact-string recommendations. Brand-label granularity silently distorts the ranking.

Fix: match recommendations by entity containment and token-boundary logic consistent with `has_entity` and `find_entity_matches` in `entity_resolution.py`.

Test: fixture mirroring the real data. Brand `Huawei` with recommendation `Huawei Watch GT 6 Pro` yields `recommendation_share > 0`; `Apple Watch` still matches; `Huawei` must not match inside an unrelated token.

### V9F-2 fix-manual-capture-recommendations-and-mention-dedup

Bug A: `src/geo_agent/manual_capture.py` drops recommendations. `to_engine_run()` and `run_from_payload()` produce empty `run.recommendations` even when the capture supplies them.

Bug B: mention extraction over-emits with no dedup. One answer yielded repeated `Huawei`, `Watch Fit 5`, and `Huawei Watch Fit 5` matches.

Fix: carry recommendations through manual capture into `EngineRun`; dedup normalized entity matches in the mention/extraction path through `engine_sampling.py` / `entity_resolution.py`.

Test: import a capture with recommendations; resulting `run.recommendations` is non-empty and matched. Mentions are de-duplicated.

### V9F-3 capture-to-package-bridge

Gap: manual captures produce `EngineRun` objects, but there is no path from captures to `EvidenceStore` / `AuditRunner` / reproducible package. Fixture `AuditRunner` audits only its own generated queries and cannot ingest arbitrary captured queries, causing `KeyError: No recorded run for query: <generated query>`.

Fix: add an ingestion entrypoint, function plus CLI subcommand, that takes a list of multi-engine manual captures and writes a real package: `manifest.json`, `report.json`, and `audit.sqlite`, without query generation.

Test: fixture of N captures across two engines produces a package whose evidence and report contain all runs per engine. CI stays network-free.

### V9F-4 report-per-engine-and-component

Fix: `src/geo_agent/report_v2.py` must output a per-engine breakdown: mention, owned-citation, recommendation, and competitor-only per engine. It must explicitly flag any single aggregate score as directional, not a verdict. Lead with per-engine, per-component output, not one number.

Test: report JSON has per-engine sections, asserts engine breakdown present, and aggregate is labeled directional.

### V9F-5 desktop-render-multi-engine

Fix: build on V9-3's real-load path in `apps/desktop/src/reportArtifacts.js` and `apps/desktop/src/App.jsx` so the desktop renders the real package's per-engine breakdown instead of a single score. Demo data remains explicitly labeled demo.

Test/structural check: loading a real multi-engine package shows per-engine sections.

### V9F-6 record-evidence-and-honesty

Fix: write `docs/v9-real-case.md` with the three-engine matrix and findings. Update provider matrix/docs so `google_aio` is `manual_only`, because AIO share links are gated and not auto-capturable. Add limitations: single aggregate is misleading, single-sample is directional, and manual capture is the multi-engine evidence path.

Test/check: doc present; provider status vocabulary consistent across README/UI/docs.

### V9F-7 query-template-cleanup

Fix clunky generated query grammar in `src/geo_agent/query_space.py`, such as `Compare Huawei Watch Fit 5 vs Apple Watch, and Apple for Huawei Watch Fit 5`.

Test: generated comparison and alternatives queries read naturally.

## Guardrails

- Start every milestone branch from current `main`, after the V9F planning PR has been merged.
- Implement only the first TODO milestone from `docs/progress.md`.
- Do not weaken tests to make CI pass.
- Keep CI network-free.
- Reuse existing V7/V8 measurement and entity-resolution modules.
- Do not add new analytics modules.
- Never fabricate AI-engine answers or treat model/web-search output as a real engine sample.
- Keep Google AIO `manual_only`.
- Keep single-sample results labeled directional.
- Keep single aggregate scores labeled directional, not verdicts.
- No raw credentials in artifacts.

## Status

- Planning branch: `v9f-real-case-fixes`
- First TODO: `V9F-1 fix-recommendation-matching`
- State source: `docs/progress.md`
