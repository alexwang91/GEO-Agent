# Provider Status Language

Provider status language controls how README, desktop UI copy, reports, and docs describe provider support. It prevents planned, manual, simulated, or unavailable paths from reading as live engine coverage.

## User-facing status vocabulary

| Status | Meaning | Allowed user-facing copy | Forbidden copy |
| :--- | :--- | :--- | :--- |
| `implemented` | The provider boundary exists and can run when explicitly configured. | Implemented, configured provider boundary. | ChatGPT Search, guaranteed live coverage. |
| `manual` | The manual or recorded evidence path is implemented. | Manual import, recorded evidence, imported run. | Automated live provider, crawler-backed live coverage. |
| `simulated` | Fixture or fake-provider path used for deterministic tests. | Simulated, fixture-backed, test evidence. | Live evidence, production provider result. |
| `planned` | Roadmap provider not implemented for audit execution. | Planned, coming later. | Available, connected, live, supported. |
| `unavailable` | Provider cannot run due to missing setup or access failure. | Unavailable, resolve issue, not collected. | Successful, configured, collected. |

## Registry status vocabulary

`src/geo_agent/provider_access.py` still uses `implemented` and `planned` for structural registry status. The richer statuses above are user-facing runtime and report copy labels from `src/geo_agent/provider_status_copy.py`.

## Current provider matrix

| Provider ID | Display name | Registry status | User-facing copy note |
| :--- | :--- | :--- | :--- |
| `openai_compatible` | OpenAI-compatible | `implemented` | Implemented answer-provider API boundary. It is not ChatGPT Search. |
| `manual_import` | Manual Import | `implemented` | Manual import / recorded evidence path. |
| `perplexity` | Perplexity | `planned` | Planned; do not describe as live or available. |
| `gemini` | Gemini | `planned` | Planned; do not describe as live or available. |
| `crawl4ai` | Crawl4AI | `planned` | Planned crawler provider. |
| `firecrawl` | Firecrawl | `planned` | Planned crawler provider. |
| `google_search_console` | Google Search Console | `planned` | Planned analytics/search provider. |

## Copy rules

- Use registry literals only for machine-readable registry status.
- Use the richer status labels for UI cards, run paths, report notes, and recovery states.
- Never call OpenAI-compatible output ChatGPT Search.
- Never imply that a planned provider can run a live audit.
- Manual import is implemented only as a manual or recorded evidence path.
- Simulated or fixture-backed paths support validation and tests, not live market conclusions.
