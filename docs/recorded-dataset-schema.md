# Recorded Dataset Schema

A recorded dataset is the CI-safe input format for fixture-based GEO audits. It contains brand profile data, owned-page HTML fixtures, audit controls, and recorded AI answer evidence.

The JSON Schema lives at:

```text
schemas/recorded-dataset.schema.json
```

## Required top-level sections

| Section | Type | Purpose |
| --- | --- | --- |
| `profile` | object | Brand and market context used to build query space. |
| `pages` | object | Mapping of URL to HTML fixture. |
| `audit` | object | Audit controls such as manual URLs, sitemap URLs, and max query count. |
| `recorded_runs` | object | Recorded answer evidence keyed by query string. |

## `profile`

Required fields:

- `brand`: non-empty string.
- `aliases`: array of strings.
- `domain`: non-empty string, normalized by the entity profile validator.
- `competitors`: non-empty array of strings.
- `target_regions`: non-empty array of strings.
- `target_languages`: non-empty array of strings.
- `target_customer`: non-empty string.
- `main_product`: non-empty string.
- `category`: non-empty string.
- `business_goal`: non-empty string.

## `pages`

`pages` is an object whose keys are HTTP or HTTPS URLs and whose values are HTML strings. These fixtures are read by the static page fetcher and never require network access.

## `audit`

Supported fields:

- `manual_urls`: array of URLs to inventory directly.
- `sitemap_urls`: array of sitemap fixture URLs.
- `max_queries`: positive integer limiting generated query records.

## `recorded_runs`

Required fields:

- `engine`: non-empty string such as `recorded`.
- `runs`: object mapping exact generated query text to recorded answer payloads.

Each recorded run must contain:

- `raw_answer`: answer text string.

Each recorded run may also contain:

- `timestamp`: string or null.
- `citations`: array of citation strings.
- `mentions`: array of entity mention strings.
- `recommendations`: array of recommended entity strings.

## Example

See `examples/acme-fixture.json` for the canonical fixture used by CI.
