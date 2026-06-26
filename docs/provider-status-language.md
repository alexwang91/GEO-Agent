# Provider Status Language

Provider status language controls how README, desktop UI copy, reports, and docs describe provider support. It prevents planned or simulated paths from reading as live engine coverage.

## Registry status vocabulary

`src/geo_agent/provider_access.py` currently defines provider implementation status with these literals:

| Status | Meaning | Allowed user-facing copy | Forbidden copy |
| :--- | :--- | :--- | :--- |
| `implemented` | The provider boundary exists in code and can be exercised by CI-safe tests or explicit user configuration. | Implemented, implemented boundary, manual import implemented, fixture-backed implementation. | Live coverage, production coverage, fully automated coverage, guaranteed connection. |
| `planned` | The provider is listed as a roadmap target but is not implemented. | Planned, planned provider, coming later. | Available, connected, live, configured, supported, automatic. |

All provider registry `implementation_status` values must be a subset of this vocabulary.

## Current provider matrix

| Provider ID | Display name | Registry status | Copy note |
| :--- | :--- | :--- | :--- |
| `openai_compatible` | OpenAI-compatible | `implemented` | Implemented answer-provider API boundary. It is not ChatGPT Search. |
| `manual_import` | Manual Import | `implemented` | Implemented manual/recorded evidence path. |
| `perplexity` | Perplexity | `planned` | Planned; do not describe as live or available. |
| `gemini` | Gemini | `planned` | Planned; do not describe as live or available. |
| `crawl4ai` | Crawl4AI | `planned` | Planned crawler provider. |
| `firecrawl` | Firecrawl | `planned` | Planned crawler provider. |
| `google_search_console` | Google Search Console | `planned` | Planned analytics/search provider. |

## Copy rules

- Use the lowercase literal (`implemented` or `planned`) in structural data, tests, and machine-readable docs.
- Use simple title-case copy (`Implemented`, `Planned`) in user-facing UI labels.
- Never call OpenAI-compatible output ChatGPT Search.
- Never imply that a planned provider can run a live audit.
- Manual import can be called implemented only as a manual/recorded evidence path, not a live automated provider.
- Fixture-backed or fake/test execution can be described in explanatory copy, but it must not become a provider `implementation_status` unless the registry adds that literal in a later milestone.

## Future vocabulary

V7-10 may add richer user-facing status labels such as manual-only, simulated, unavailable, or provider-failure states. Until then, docs and UI copy must remain anchored to the registry literals above.
