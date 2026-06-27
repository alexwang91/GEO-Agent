# V9 Real Case Evidence

## Case

- Brand: GEO-Agent
- Consent basis: project-owned public repository
- Target site for V9-1 crawl: `https://github.com/alexwang91/GEO-Agent`
- Private data: none
- Credentials: none

## V9-1 Evidence

The minimal real FetchClient part of the vertical slice is satisfied by the current code path:

- `UrlLibFetchClient` implements concrete HTTP fetch behavior using stdlib urllib.
- It validates http/https URLs, supports timeout, retry, HTTP error handling, and robots.txt checks.
- `LiveCrawlerProviderV2` uses that client only behind `allow_live_fetch=True`.
- CI coverage uses fake clients and does not perform network access.

Real-case verification record:

- The selected brand and site are public and consented.
- The crawler boundary is ready for an opt-in crawl of the selected site.
- No raw credentials or private data are required for this crawl.
- This milestone does not add analytics; it only enables the vertical-slice evidence acquisition path.

## Remaining V9 Evidence To Collect

- V9-2: manually captured real AI answers and citations.
- V9-3: real generated package rendered in desktop.
- V9-4: extraction precision/recall gate on realistic samples.
- V9-5: full run, task usefulness review, retest delta, and confidence record.
