# Limitations

GEO-Agent is an alpha/technical-preview workbench. These limitations are product constraints, not incidental bugs.

## Provider coverage after V9

- OpenAI-compatible API output is an implemented answer-provider boundary, but it is not ChatGPT Search.
- Manual Import is implemented as the realistic multi-engine evidence bridge for pasted or recorded ChatGPT Search, Perplexity, Gemini, Google AIO, and manual evidence.
- Perplexity, Gemini, Crawl4AI, Firecrawl, and Google Search Console remain planned providers unless the registry and CI tests prove otherwise.
- The concrete live crawler client exists behind explicit opt-in and is tested with fake clients in CI.
- CI must stay network-free.

## Statistical confidence

- single-sample outputs are directional only.
- Repeated sampling, confidence intervals, volatility, and noise-floor language exist where repeated samples are available.
- The product must not state low-sample conclusions as definite.
- Retest comparison must not attribute improvement to a task unless the retest layer has enough evidence and the task was actually executed.

## Optimization scope

- GEO-Agent produces evidence-backed task drafts and handoff recommendations. It does not auto-publish website, PR, SEO, schema, or content changes.
- The system does not guarantee ranking, citation, recommendation, or traffic improvement.
- Owned-site fixes may not be sufficient when the failure comes from source selection, third-party evidence gaps, claim support, crawl constraints, or category authority.

## Artifact and credential safety

- Raw API keys, OAuth tokens, cookies, request headers, provider secrets, and raw credential labels must not appear in reports, manifests, logs, audit databases, UI state, or exported artifacts.
- Provider failures must surface as failures or unavailable states, not successful audit execution.
- Planned providers must remain labeled planned until implementation and deterministic verification exist.

## Desktop and report maturity after V9

- The desktop shell can load a real generated audit package from `manifest.json` and `report.json`.
- Demo data must be explicitly labeled demo.
- Run-flow helper logic exists for brand defaults, query preview, path selection, and run-preparation state.
- The desktop shell is still not a complete backend-wired end-to-end workflow for non-engineers.

## Validation maturity after V9

- A sanitized project-owned validation record exists in `docs/v9-validation.md`.
- This is not an independent customer validation.
- Realistic extraction regression fixtures exist, but the fixture set is still small.
