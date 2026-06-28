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

## V9-2 Evidence Gate

Manual-capture import code exists and supports pasted answer text, citations, engine, captured_at, region, language, brand, and aliases.

V9-2 is not marked DONE in this branch because the real manual capture evidence is not present in this repository state. To complete V9-2, record sanitized capture metadata here:

| Field | Value |
| :--- | :--- |
| Engine | TODO |
| Query | TODO |
| Captured at | TODO |
| Citation URLs | TODO |
| Redaction checked | TODO |
| Converted to EngineRun | TODO |

Do not paste private data, API keys, cookies, tokens, or credential labels.

## V9-3 Desktop Readiness

The desktop report-loading path is implementation-ready:

- `apps/desktop/src/reportArtifacts.js` loads a real generated package from `manifest.json` and `report.json`.
- It keeps demo data behind an explicit demo path and labels demo output as demo.
- `apps/desktop/src/App.jsx` exposes empty, loading, error, demo, and loaded report states.
- V9-3 remains real-case pending until a generated package from the real V9 evidence path is loaded and recorded.

## V9-4 Eval Gate

Realistic extraction regression coverage exists in `tests/test_v9_05_extraction_regression.py` and `tests/fixtures/realistic_answer_samples.json`.

Minimum bar:

| Metric | Bar |
| :--- | :--- |
| Entity precision | 0.75 |
| Entity recall | 0.80 |
| URL recall | 0.95 |

If this gate fails, extraction must be fixed before generated reports are used as trusted evidence. This gate reuses existing extraction code and does not add analytics modules.

## V9-5 Run Checklist

V9-5 remains blocked until the real capture and retest inputs exist. Do not mark V9-5 DONE until every item below is filled with sanitized evidence:

| Required item | Status |
| :--- | :--- |
| Real manual capture imported | TODO |
| Real generated package created | TODO |
| Desktop real package render recorded | TODO |
| Eval gate result recorded | TODO |
| Task usefulness reviewed | TODO |
| Retest delta recorded | TODO |
| Confidence statement recorded | TODO |
| Limitations updated | TODO |

Recovery path: once the real captures are provided, resume at V9-2, generate the package, load it in desktop, run the eval gate, then record the retest result here.

## Remaining V9 Evidence To Collect

- V9-2: manually captured real AI answers and citations.
- V9-3: real generated package rendered in desktop.
- V9-4: extraction precision/recall gate on realistic samples.
- V9-5: full run, task usefulness review, retest delta, and confidence record.
