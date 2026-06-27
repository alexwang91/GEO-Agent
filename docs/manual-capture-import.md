# Manual Capture Import

Manual capture is the current multi-engine evidence path for ChatGPT Search, Perplexity, Gemini, and Google AIO while direct live provider integrations remain planned.

## Purpose

Use manual capture when a human collects answer evidence from a live AI/search surface and imports it into GEO-Agent as recorded evidence.

## Required fields

| Field | Required | Notes |
| --- | --- | --- |
| `engine` | yes | One of `chatgpt_search`, `perplexity`, `gemini`, `google_aio`, or `manual_import`. |
| `query` | yes | The exact query/prompt used for the capture. |
| `answer_text` | yes | Pasted answer text. |
| `captured_at` | yes | ISO-8601 timestamp. |
| `citations` | no | List of cited URLs. If omitted, URLs can still be extracted from `answer_text`. |
| `region` | no | Capture market or region. Defaults to `unknown`. |
| `language` | no | Capture language. Defaults to `unknown`. |
| `brand` | no | Brand to extract from the answer. |
| `brand_aliases` | no | List of brand aliases. |

## Example

```json
{
  "engine": "chatgpt_search",
  "query": "best acme alternative",
  "answer_text": "Acme is mentioned and cited by https://example.com/acme.",
  "citations": ["https://example.com/acme"],
  "captured_at": "2026-06-27T12:00:00+00:00",
  "region": "US",
  "language": "en",
  "brand": "Acme",
  "brand_aliases": ["ACME Inc"]
}
```

## Safety

Manual captures are checked with artifact safety before and after normalization. Do not include API keys, OAuth tokens, cookies, request headers, passwords, or raw provider secrets in captured payloads.

## Provider truth

Manual capture does not make a planned provider live. It records human-collected evidence from that provider surface. Planned provider integrations must remain planned until implemented and verified.
