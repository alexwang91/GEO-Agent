# Limitations

GEO-Agent is an alpha/technical-preview workbench. These limitations are product constraints, not incidental bugs.

## Provider coverage

- OpenAI-compatible API output is an implemented answer-provider boundary, but it is not ChatGPT Search.
- Perplexity, Gemini, Crawl4AI, Firecrawl, and Google Search Console are planned providers unless the registry and CI tests prove otherwise.
- Manual Import is implemented as a manual/recorded evidence path. It is not live automated engine sampling.
- CI must stay network-free unless a future milestone explicitly adds a fake-client or fixture-backed verification path.

## Statistical confidence

- single-sample outputs are directional only.
- Repeated sampling, confidence intervals, volatility, and noise-floor gates are planned V7 milestones.
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

## Desktop and report maturity

- The desktop shell is not yet a complete end-to-end non-engineer workflow.
- Role-specific report packs, dashboard confidence cues, source maps, and evidence drilldowns are planned later in V7.
- Public technical-preview docs and examples are planned for V7-38.
