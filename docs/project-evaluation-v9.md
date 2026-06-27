# Project Evaluation V9 — Current Main Assessment

## Scope

This evaluation starts from the current `main` after V7 and V8 completion and after repository cleanup removed the prior runner planning/state files. `docs/v8-changelog.md` is the retained prior-history document.

## What V8 Already Solved

V8 hardened the measurement foundation and should not be redone.

- `entity_resolution.py` backs `visibility_scoring.py` with entity-aware matching through `has_entity` and `find_entity_matches`.
- Brand matching is alias, boundary, and diacritics aware; naive substring matching has been removed from visibility scoring.
- The extraction eval harness covers brand boundaries, aliases, diacritics, URL extraction, fallback mentions, and false positives.
- Bootstrap statistics are wired into `report_v2` with mean, interval, sample count, noise floor, and inconclusive-delta language.
- GitHub Actions `verify` includes unit tests plus network-free style, type-syntax, and coverage gates.

## Real-World Readiness Gaps

### 1. No complete real data acquisition path

`crawl_provider_v2.py` exposes a `FetchClient` protocol and a live crawler seam behind `allow_live_fetch`, but there is no concrete HTTP client implementation committed for out-of-the-box real crawling. The live seam is verified with fake clients only. This is correct for CI safety, but not enough for user-ready acquisition.

All answer engines except `openai_compatible` remain planned in `provider_access.py`: Perplexity, Gemini, Crawl4AI, Firecrawl, and Google Search Console are not live audit providers. Multi-engine evidence is therefore manual or recorded today.

### 2. Desktop remains a demo-oriented shell

The desktop app still depends on sample/demo report artifacts. V8 recorded the decision that demo artifacts must be labeled and separated from generated audit output, but it did not complete real report loading, provider listing, brand form wiring, query preview, or run flow.

A non-engineer cannot yet move from project setup to real audit to real report inside the app.

### 3. No real-world validation run

V8-07 was a sanitized dry-run record, not a consented real-brand run. Extraction precision, diagnosis quality, and task usefulness on live or manually captured answers remain unproven.

### 4. Manual capture is not polished enough

Manual import is the realistic bridge for multi-engine evidence while live provider APIs remain planned. The schema and UX need to accept pasted answer text, citations, engine label, capture time, query, region, and language, then validate and redaction-check the data before it enters the evidence graph.

## Principle For V9

V9 adds no new analytics. It makes the existing engine real and usable, then validates it.

The correct sequence is:

1. concrete live crawler client;
2. polished manual-capture import;
3. desktop real report loading;
4. desktop run flow wiring;
5. realistic extraction regression data;
6. one consented real-brand validation run;
7. README, provider matrix, and limitations refresh.

## Guardrails

- Keep CI network-free.
- Use fake clients for live network seams in CI.
- Keep real network access opt-in.
- Never persist raw credentials into artifacts, logs, manifests, databases, or UI state.
- Do not represent `openai_compatible` as ChatGPT Search.
- Do not describe planned providers as live or available.
- Keep single-sample evidence directional.
