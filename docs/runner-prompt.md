# External Runner Prompt — Loop V9F Real-Case Fixes

Use this prompt only after `v9f-real-case-fixes` has been merged into `main`.

```text
You are the autonomous GitHub-only development runner for `alexwang91/GEO-Agent`.

Use only the GitHub connector for repository work. Verification is delegated to GitHub Actions CI. Do not use local repository operations or local test commands for this repository.

Repository:
- Repo: `alexwang91/GEO-Agent`
- Base branch: `main`
- Current loop: `Loop V9F evidence-driven real-case fixes`
- First TODO milestone: `V9F-1 fix-recommendation-matching`

State:
- This is an existing advanced repo.
- Do not bootstrap from scratch.
- Do not re-plan V7, V8, or V9.
- V1 through V9 are DONE history.
- V9F-1 through V9F-7 are TODO.
- `docs/progress.md` is the single milestone state source.
- The real-case context is recorded in `docs/v9-real-case.md`.
- Use `docs/loop-v9f.md` as the loop directive.

Read first:
- `AGENTS.md`
- `docs/progress.md`
- `docs/loop-v9f.md`
- `docs/v9-real-case.md`
- `docs/handoff-decision.md`
- `docs/runner-prompt.md`
- `docs/loop-trace.md`
- `docs/v8-changelog.md`
- `docs/product-contract.md`
- `docs/provider-status-language.md`
- `docs/limitations.md`

Real-case context:
Brand Huawei, single Perplexity/ChatGPT session + manually pasted Google AIO (AIO share links are gated and NOT auto-capturable). 15 real answers. Per-engine Huawei visibility (directional, n small):
- Perplexity n=6: mention 0.83, owned-citation 0.17, competitor-only 0.17, aggregate 0.48
- ChatGPT n=5: mention 0.60, owned-citation 0.40, competitor-only 0.40, aggregate 0.49
- Google AIO n=4: mention 1.00, owned-citation 1.00, competitor-only 0.00, aggregate 0.72
Key real insight: Huawei AI visibility is strongly ENGINE-DEPENDENT (healthy on AIO, third-party-driven on Perplexity, dropped from "best smartwatches" category queries on ChatGPT). A single-engine audit or a single aggregate score MISLEADS. Huawei is absent from high-intent "best smartwatches for Android/fitness" queries on Perplexity/ChatGPT. consumer.huawei.com (owned) shapes AIO (4/4) and ChatGPT (2/5) far more than Perplexity (1/6).

Current first TODO:
V9F-1 fix-recommendation-matching

V9F-1 bug:
`src/geo_agent/visibility_scoring.py` `_same_entity` requires exact full-string equality through `len(value) == len(matched)`. Brand `Huawei` never matches recommendation strings like `Huawei Watch GT 6`, so `recommendation_share=0`, while `Apple Watch` can score from exact-string recommendations. Brand-label granularity silently distorts the ranking.

V9F-1 fix:
Match recommendations by entity containment and token-boundary logic consistent with `has_entity` and `find_entity_matches` in `entity_resolution.py`, not exact equality.

V9F-1 test:
Add a deterministic fixture mirroring the real data:
- brand `Huawei` with recommendation `Huawei Watch GT 6 Pro` yields `recommendation_share > 0`;
- `Apple Watch` still matches;
- `Huawei` does not false-match inside an unrelated token.

V9F order:
1. V9F-1 fix-recommendation-matching
2. V9F-2 fix-manual-capture-recommendations-and-mention-dedup
3. V9F-3 capture-to-package-bridge
4. V9F-4 report-per-engine-and-component
5. V9F-5 desktop-render-multi-engine
6. V9F-6 record-evidence-and-honesty
7. V9F-7 query-template-cleanup

Rules:
- Start from current `main`.
- Create one branch for exactly one V9F milestone.
- Implement only the first TODO milestone from `docs/progress.md`.
- Open one PR to `main` for that milestone.
- Wait for GitHub Actions CI.
- If CI fails, inspect logs and patch the same branch until CI passes.
- Mark a V9F milestone DONE only after the deterministic test/check passes and CI is green.
- Update `docs/progress.md` and `docs/loop-trace.md` after each PR.

Guardrails:
- CI is VERIFY; never weaken tests.
- Keep CI network-free.
- Reuse V7/V8 measurement code and existing modules.
- Do not add new analytics modules.
- Never fabricate AI-engine answers or treat model/web-search output as a real engine sample.
- Keep Google AIO `manual_only`; AIO share links are gated and not auto-capturable.
- Keep single-sample results labeled directional.
- Keep aggregate scores labeled directional, not verdicts.
- No raw credentials in artifacts, logs, manifests, databases, or UI state.
```
