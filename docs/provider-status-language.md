# Provider Status Language

Provider status language controls how README, desktop UI copy, reports, and docs describe provider support. It prevents planned, manual, simulated, or unavailable paths from reading as live engine coverage.

## User-facing status vocabulary

| Status | Meaning | Allowed user-facing copy | Forbidden copy |
| :--- | :--- | :--- | :--- |
| `implemented` | The provider boundary exists and can run when explicitly configured. | Implemented, configured provider boundary. | ChatGPT Search, guaranteed live coverage. |
| `manual` | The manual or recorded evidence path is implemented. | Manual import, recorded evidence, imported run. | Automated live provider, crawler-backed live coverage. |
| `manual_only` | Evidence may enter only through explicit manual capture/import. | Manual-only evidence source. | Automated capture, live provider, connected provider. |
| `simulated` | Fixture or fake-provider path used for deterministic tests. | Simulated, fixture-backed, test evidence. | Live evidence, production provider result. |
| `planned` | Roadmap provider not implemented for audit execution. | Planned, coming later. | Available, connected, live, supported. |
| `unavailable` | Provider cannot run due to missing setup or access failure. | Unavailable, resolve issue, not collected. | Successful, configured, collected. |

## Registry status vocabulary

`src/geo_agent/provider_access.py` uses `implemented`, `planned`, and `manual_only` for structural registry status. The richer statuses above are user-facing runtime and report copy labels from `src/geo_agent/provider_status_copy.py`.

## Current provider matrix

| Provider ID | Display name | Registry status | User-facing copy note |
| :--- | :--- | :--- | :--- |
| `openai_compatible` | OpenAI-compatible | `implemented` | Implemented answer-provider API boundary. It is not ChatGPT Search. |
| `manual_import` | Manual Import | `implemented` | Manual import / recorded evidence path. |
| `perplexity` | Perplexity | `planned` | Planned; do not describe as live or available. |
| `gemini` | Gemini | `planned` | Planned; do not describe as live or available. |
| `google_aio` | Google AIO | `manual_only` | Manual-only evidence source. AIO share links are gated and not auto-capturable. |
| `deepseek` | DeepSeek | `manual_only` | Manual-only evidence source through explicit pasted or recorded capture. |
| `kimi` | Kimi | `manual_only` | Manual-only evidence source through explicit pasted or recorded capture. |
| `qianwen` | Qianwen | `manual_only` | Manual-only evidence source through explicit pasted or recorded capture. |
| `crawl4ai` | Crawl4AI | `planned` | Planned crawler provider. |
| `firecrawl` | Firecrawl | `planned` | Planned crawler provider. |
| `google_search_console` | Google Search Console | `planned` | Planned analytics/search provider. |

## Google AIO evidence boundary

- `google_aio` is a manual-only evidence source because AIO share links are gated and not auto-capturable.
- Google AIO evidence enters through explicit manual capture and the implemented manual-import path.
- Do not describe Google AIO as an automated live provider, connected provider, or share-link capture flow.

## Chinese AI search evidence boundary

- `deepseek`, `kimi`, and `qianwen` are manual-only evidence sources until sanctioned provider paths exist.
- Their evidence enters through explicit manual capture or recorded imports only.
- Do not describe them as automated live providers or CI-capturable engines.

## Copy rules

- Use registry literals only for machine-readable registry status.
- Use the richer status labels for UI cards, run paths, report notes, and recovery states.
- Never call OpenAI-compatible output ChatGPT Search.
- Never imply that a planned provider can run a live audit.
- Manual import is implemented only as a manual or recorded evidence path.
- Manual capture is the multi-engine evidence path for ChatGPT Search, Perplexity, Gemini, Google AIO, Chinese AI engines, and comparable pasted answers until provider-specific connectors are implemented and verified.
- Simulated or fixture-backed paths support validation and tests, not live market conclusions.
