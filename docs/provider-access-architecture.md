# Provider Access Architecture

Provider Access is the layer between the UI and external capabilities. It must support API keys, OAuth, platform-managed credentials, and manual import without leaking secrets into audit evidence.

## Provider Types

| Type | Purpose |
| --- | --- |
| `answer` | Ask an AI answer engine and receive answer evidence. |
| `search` | Retrieve web search results or search snippets. |
| `crawl` | Fetch and transform owned-page or competitor-page evidence. |
| `model` | Perform extraction, normalization, or diagnosis assistance. |
| `analytics` | Read first-party performance data such as Search Console. |

## Access Methods

| Method | Description |
| --- | --- |
| `api_key` | User supplies a provider API key for the session or encrypted storage. |
| `oauth` | User authorizes the app through an external provider authorization flow. |
| `platform_managed` | The GEO Agent deployment uses its own managed provider key. |
| `manual_import` | User imports recorded evidence without live provider access. |

## Core Objects

```text
ProviderDefinition
  provider_id
  display_name
  provider_type
  capabilities
  access_methods
  implementation_status

ProviderConnection
  provider_id
  access_method
  auth_status
  redacted_label
  scopes
  expires_at

ProviderSession
  connection_id
  credential_ref
  runtime_config
```

## Security Rules

- API keys and OAuth tokens must never be written to `manifest.json`, `report.json`, `report.md`, or `audit.sqlite`.
- API keys and OAuth tokens must not be returned by API responses.
- Logs must use redacted labels only.
- OAuth state must be validated.
- OAuth tokens require a storage abstraction before persistence.
- Missing credentials must fail clearly.
- Planned providers must be visible but not executable.

## Initial Provider Matrix

| Provider | Type | Access | Status |
| --- | --- | --- | --- |
| OpenAI-compatible | answer/model | api_key, platform_managed | planned |
| Perplexity | answer/search | api_key | planned |
| Gemini | answer/model | api_key | planned |
| Crawl4AI | crawl | local/platform_managed | planned |
| Firecrawl | crawl | api_key | planned |
| Google Search Console | analytics | oauth | planned |
| Manual Import | answer | manual_import | implemented |

## First Implementation Principle

The first UI/provider slices should implement the registry and UI shell before making live calls. CI must remain fixture-based.
