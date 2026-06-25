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

AnswerProviderConfig
  provider_id
  model
  endpoint_url
  temperature

AnswerCredentialRef
  access_method
  session_id or platform-managed transient key

AnswerProviderRequest
  query
  region
  language
  config
  credential_ref
```

## Security Rules

- API keys and OAuth tokens must never be written to `manifest.json`, `report.json`, `report.md`, or `audit.sqlite`.
- API keys and OAuth tokens must not be returned by API responses.
- Logs must use redacted labels only.
- OAuth state must be validated.
- OAuth tokens require a storage abstraction before persistence.
- Missing credentials must fail clearly.
- Planned providers must be visible but not executable.
- OpenAI-compatible answer-provider tests must use an injected fake HTTP client in CI.
- OpenAI-compatible provider response objects must convert to `EngineRun` evidence without returning raw request headers or provider keys.

## Initial Provider Matrix

| Provider | Type | Access | Status |
| --- | --- | --- | --- |
| OpenAI-compatible | answer/model | api_key, platform_managed | implemented behind explicit config and fake-client CI |
| Perplexity | answer/search | api_key | planned |
| Gemini | answer/model | api_key | planned |
| Crawl4AI | crawl | local/platform_managed | planned |
| Firecrawl | crawl | api_key | planned |
| Google Search Console | analytics | oauth | planned |
| Manual Import | answer | manual_import | implemented |

## OpenAI-Compatible Boundary

The first implemented answer provider is `openai_compatible`. It is not a default live integration. Callers must pass:

- an explicit `AnswerProviderConfig` with model and endpoint;
- an explicit `AnswerCredentialRef` backed by a BYOK session id or a transient platform-managed key;
- an injected HTTP client.

CI uses fake HTTP clients only. The adapter converts successful responses to existing `EngineRun` evidence. Missing credentials, malformed provider payloads, and provider error responses raise `ProviderAccessError`.

## First Implementation Principle

Provider implementation must advance in narrow, testable boundaries. New live-provider behavior must stay behind explicit configuration, fake-client verification, clear missing-credential errors, and artifact redaction checks.