# GEO-Agent

AI Search Visibility Agent for Generative Engine Optimization.

This repository is managed through the GitHub Loop Runner. See `docs/progress.md` for milestone state and `docs/product-brief.md` for product direction.

## Technical preview status

GEO-Agent is in alpha/technical preview. It is an AI Search Visibility Experiment Workbench for evidence-backed audit, diagnosis, task planning, and retest workflows, not a production SaaS and not a general SEO copywriting tool.

Current CI-verifiable behavior is fixture-backed, manual-import oriented, or routed through explicit provider-boundary code. Planned providers must stay labeled planned until deterministic tests and explicit configuration prove the implemented boundary. OpenAI-compatible API output is not ChatGPT Search.

The product does not guarantee ranking improvement. Low-sample visibility results are directional only until repeated sampling, confidence intervals, and noise-floor checks are available in later V7 milestones.

## Product contract

See `docs/product-contract.md` for product promises and non-promises. Current public-facing claims must stay inside that contract.

## Provider status

See `docs/provider-status-language.md` for the provider status vocabulary. Current registry statuses are `implemented` and `planned`.

Implemented providers in the current technical preview:

- OpenAI-compatible: implemented API boundary; not ChatGPT Search.
- Manual Import: implemented manual/recorded evidence path.

Planned providers:

- Perplexity.
- Gemini.
- Crawl4AI.
- Firecrawl.
- Google Search Console.

See `docs/limitations.md` for known provider, confidence, optimization, artifact-safety, desktop, and report limitations.
