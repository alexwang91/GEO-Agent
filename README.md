# GEO-Agent

AI Search Visibility Agent for Generative Engine Optimization.

GEO-Agent is an alpha/technical-preview workbench for evidence-backed AI search visibility audits. It helps collect brand context, sample or import answer evidence, extract mentions and citations, score visibility, summarize statistical confidence, plan optimization tasks, and prepare retests.

## Current status

The repository has moved out of the external runner planning-loop format. Historical implementation notes are consolidated in `docs/v8-changelog.md`; obsolete loop, progress, handoff, and runner-state documents have been removed.

Current CI-verifiable behavior is fixture-backed, manual-import oriented, or routed through explicit provider-boundary code. Live crawling is available only through an explicit opt-in fetch seam and is tested with fake clients in CI. OpenAI-compatible API output is not ChatGPT Search.

## Product contract

See `docs/product-contract.md` for product promises and non-promises. Public-facing claims must stay inside that contract.

GEO-Agent does not guarantee ranking improvement. Low-sample visibility results are directional only; reports should preserve sample count, confidence interval, and noise-floor language where available.

## Provider status

See `docs/provider-status-language.md` for provider status vocabulary.

Implemented paths in the current technical preview:

- OpenAI-compatible: implemented API boundary; not ChatGPT Search.
- Manual Import: implemented manual/recorded evidence path.
- Static crawler: fixture-backed crawler path for deterministic tests.
- Live crawler seam: explicit opt-in fetch boundary; CI uses fake clients only.

Planned providers remain planned until deterministic tests and explicit configuration prove the implemented boundary:

- Perplexity.
- Gemini.
- Crawl4AI.
- Firecrawl.
- Google Search Console.

## Documentation

- `docs/product-brief.md` — product direction.
- `docs/product-contract.md` — claims, promises, and non-promises.
- `docs/provider-status-language.md` — provider status vocabulary.
- `docs/limitations.md` — known provider, confidence, optimization, artifact-safety, desktop, and report limitations.
- `docs/v8-changelog.md` — consolidated implementation changelog.

## Verification

The repository uses GitHub Actions `verify` for:

- product/documentation existence checks;
- Python unit tests;
- network-free Python style, type-syntax, and coverage gates.

Run locally, when needed:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python tools/check_python_style.py
python tools/check_type_annotations.py
python tools/check_coverage.py
```

## Safety boundaries

- Do not commit raw API keys, OAuth tokens, cookies, request headers, or provider secrets.
- Do not describe planned providers as live.
- Do not represent OpenAI-compatible API output as ChatGPT Search.
- Do not treat demo fixture artifacts as generated audit output.
