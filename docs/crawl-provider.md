# Crawler Provider Boundary

V5-6 adds the first crawler-provider boundary for GEO Agent.

## Scope

The implemented provider is `StaticCrawlerProvider`, a fixture-backed crawler used for CI and recorded crawls. It does not call Crawl4AI, Firecrawl, or any external crawler service.

## Request

`CrawlProviderRequest` contains:

- `provider_id`
- `manual_urls`
- `sitemap_urls`
- `chunk_size`
- optional `metadata`

A request must include at least one manual URL or sitemap URL, and every URL must be HTTP or HTTPS.

## Result

`CrawlProviderResult` contains:

- `provider_id`
- `pages`: existing `PageInventoryRecord` objects
- `errors`: typed `CrawlProviderError` objects
- `metadata`

`pages_from_crawl_result()` returns the page inventory records so callers can use the existing `EvidenceStore.save_page_records()` path.

## CI Contract

CI must use static fixtures only. Live crawler integrations remain planned until they have explicit configuration, credential boundaries, network-isolated tests, and artifact redaction checks.