# Query Space Builder

M2 adds a deterministic builder that converts an `EntityProfile` into records for later sampling.

## Supported intents

- `brand`
- `category`
- `comparison`
- `buying_intent`
- `problem_solving`
- `scenario`
- `negative_risk`
- `alternatives`

## Record fields

| Field | Meaning |
| --- | --- |
| `query` | Concrete prompt text. |
| `intent_type` | One supported intent type. |
| `funnel_stage` | Funnel stage derived from intent. |
| `language` | Profile language. |
| `region` | Profile region. |
| `target_engine` | Engine adapter key. |
| `competitor_entities` | Profile competitors. |
| `expected_answer_format` | Expected answer shape. |
| `priority_score` | Deterministic priority from 0.0 to 1.0. |
| `cluster` | Stable `intent:language:region:engine` key. |

The builder does not call external services. CI asserts exact output for a sample profile.
