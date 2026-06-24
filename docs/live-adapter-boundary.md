# Live Adapter Boundary

GEO Agent is currently fixture-based. Live AI search adapters are intentionally out of scope for the current implementation. This document defines the boundary a future live adapter must satisfy before implementation.

## Non-goals for current CI

- No live AI search calls.
- No browser automation.
- No paid API calls.
- No secrets in tests.
- No network dependency for unit tests.

## Required live adapter contract

A future live adapter must implement the existing `EngineAdapter` shape:

```python
sample(query: str, *, region: str, language: str, timestamp: str | None = None) -> EngineRun
```

The adapter must produce an `EngineRun` with:

- `engine`: stable engine identifier.
- `query`: exact submitted query.
- `timestamp`: ISO timestamp of sampling.
- `region`: requested region.
- `language`: requested language.
- `raw_answer`: raw answer text.
- `citations`: citation URLs or source strings.
- `mentions`: parsed entity mentions.
- `recommendations`: parsed recommendations.
- `source_domains`: normalized source domains.

## Required provenance metadata

Before adding live calls, the design must define how to persist:

- request ID or provider response ID when available.
- model or engine name/version.
- sampling location or region parameter.
- request timestamp and response timestamp.
- latency and retry count.
- redacted request metadata.
- adapter version.
- error type for failed calls.

## Secrets and configuration

A future live adapter must not read credentials implicitly from code. It must use explicit configuration such as environment variables or injected config objects. Tests must use recorded fixtures unless an explicit integration-test flag is set.

## Rate limits and retries

A future live adapter must document:

- request limits.
- retry policy.
- timeout behavior.
- backoff policy.
- quota failure behavior.
- cost tracking assumptions.

## Stopper rules

Stop implementation rather than merge when:

- API credentials are unavailable.
- provider terms or rate limits are unclear.
- CI would require external network calls.
- raw response evidence cannot be preserved or redacted safely.
- the adapter cannot distinguish engine failure from empty answer.
- tests would need to mock behavior so heavily that they no longer verify the adapter contract.

## Future implementation path

1. Add recorded fixture examples from real manual runs.
2. Add an adapter-specific raw response envelope type.
3. Add integration tests behind an opt-in environment flag.
4. Add live adapter implementation.
5. Convert successful live responses into recorded dataset fixtures for deterministic CI.
