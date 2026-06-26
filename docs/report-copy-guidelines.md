# Report Copy Guidelines

Report and UI copy must preserve the product contract: GEO-Agent is an alpha/technical-preview workbench for evidence-backed AI search visibility experiments.

## Provider and evidence language

| Evidence path | Required copy | Notes |
| :--- | :--- | :--- |
| Manual import | manual, recorded, user-supplied evidence | Use when answers or citations were pasted or imported by the user. |
| Simulated fixture | simulated, fixture-backed, fake-provider test data | Use for deterministic CI and demo packages. |
| Live configured | live configured, implemented provider boundary | Use only when the provider path is implemented and explicitly configured. |
| Planned provider | planned, not available for audit execution | Use for roadmap providers and disabled UI cards. |

## Metric language

Use cautious metric language until repeated sampling, confidence intervals, and noise-floor gates are implemented:

- Directional visibility score.
- Observed in this sample.
- Cited in this imported answer.
- Likely evidence gap.
- Retest recommended.
- Inconclusive until more samples are collected.

## Recommendation language

Optimization tasks should name the observed issue, evidence ID when available, recommended owner, target asset, expected metric movement, risk, and retest plan.

## Error language

Error copy should say what failed, what evidence is still usable, and what the next safe action is. A failed provider call remains a failed provider call, not audit completion.

## Guardrails for user-facing surfaces

- One sample is not enough to establish broad engine behavior.
- The product does not ensure ranking or citation improvement.
- OpenAI-compatible output is not ChatGPT Search.
- A planned provider remains planned until implemented and verified.
- Imported evidence is a bounded sample, not whole-market coverage.
