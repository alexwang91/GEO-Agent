# Provider Status Language

Provider status language controls how README, desktop UI copy, reports, and docs describe provider support. It prevents planned, manual, manual-only, simulated, or unavailable paths from reading as live engine coverage.

## User-facing status vocabulary

| Status | Meaning | Allowed user-facing copy | Forbidden copy |
| :--- | :--- | :--- | :--- |
| `implemented` | The provider boundary exists and can run when explicitly configured. | Implemented, configured provider boundary. | ChatGPT Search, guaranteed live coverage. |
| `manual` | The manual or recorded evidence path is implemented. | Manual import, recorded evidence, imported run. | Automated live provider, crawler-backed live coverage. |
| `manual_only` | Docs/UI label for evidence that can be included only through explicit manual capture. Automated collection is unavailable. | Manual only, explicit manual capture, not auto-capturable. | Automated, live connector, share-link capture, available provider. |
| `simulated` | Fixture or fake-provider path used for deterministic tests. | Simulated, fixture-backed, test evidence. | Live evidence, production provider result. |
| `planned` | Roadmap provider not implemented for audit execution. | Planned, coming later. | Available, connected, live, supported. |
| `unavailable` | Provider cannot run due to missing setup or access failure. | Unavailable, resolve issue, not collected. | Successful, configured, collected. |

## Registry status vocabulary

`src/geo_agent/provider_access.py` still uses `implemented` and `planned` for structural registry status. `src/geo_agent/provider_status_copy.py` exposes the runtime status copy used by provider-boundary flows. The `manual_only` label is intentionally documented for README and desktop UI evidence boundaries without changing the runtime provider enum in this docs-only milestone. A provider can be user-facing `manual_only` while its evidence enters through the implemented manual-import path.

## Current provider matrix

| Provider ID | Display name | Registry status | User-facing status | User-facing copy note |
| :--- | :--- | :--- | :--- | :--- |
| `openai_compatible` | OpenAI-compatible | `implemented` | `implemented` | Implemented answer-provider API boundary. It is not ChatGPT Search. |
| `manual_import` | Manual Import | `implemented` | `manual` | Manual import / recorded evidence path. |
| `google_aio` | Google AIO | manual capture path | `manual_only` | AIO share links are gated and not auto-capturable; use explicit manual capture only. |
| `perplexity` | Perplexity | `planned` | `planned` | Planned; do not describe as live or available. |
| `gemini` | Gemini | `planned` | `planned` | Planned; do not describe as live or available. |
| `crawl4ai` | Crawl4AI | `planned` | `planned` | Planned crawler provider. |
| `firecrawl` | Firecrawl | `planned` | `planned` | Planned crawler provider. |
| `google_search_console` | Google Search Console | `planned` | `planned` | Planned analytics/search provider. |

## Copy rules

- Use registry literals only for machine-readable registry status.
- Use the richer status labels for UI cards, run paths, report notes, and recovery states.
- Never call OpenAI-compatible output ChatGPT Search.
- Never imply that a planned provider can run a live audit.
- Never imply that `google_aio` has automated or share-link capture; it is `manual_only`.
- Manual import is implemented only as a manual or recorded evidence path.
- Manual capture is the multi-engine evidence path for ChatGPT Search, Perplexity, Gemini, Google AIO, and comparable pasted answers until provider-specific connectors are implemented and verified.
- Simulated or fixture-backed paths support validation and tests, not live market conclusions.
