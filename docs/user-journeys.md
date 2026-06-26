# User Journeys

This document defines the technical-preview end-to-end UX contract. The journey is intentionally evidence-first: the workbench must show how each conclusion connects to samples, citations, pages, and retest plans.

## Ten-step journey

1. **Create project**: enter brand name, domain, category, market, language, competitors, and business goal.
2. **Choose evidence source**: pick manual import, simulated fixture/fake-provider data, live configured implemented provider, or planned provider information.
3. **Review provider status**: see whether each source is implemented, planned, manual, simulated, or live configured.
4. **Generate query space**: create candidate queries with personas, funnel stages, clusters, and business priority.
5. **Review query budget**: edit, delete, add, or reprioritize queries before running or importing evidence.
6. **Collect evidence**: use fixture data, manual recorded answers, configured provider output, crawler snapshots, or imported audit package artifacts.
7. **Read dashboard**: inspect directional visibility, mention, citation, recommendation, confidence, and missing-query metrics.
8. **Drill into evidence**: trace every metric to prompt, sample, answer, citation, page, and source classification IDs when available.
9. **Plan actions**: create owner-mapped optimization tasks with evidence, target asset, expected metric, risk, and retest plan.
10. **Retest and learn**: rerun the same prompt/engine/region/language where supported, compare against the noise floor, and store outcomes.

## Required UX behavior

- Provider labels must distinguish manual, simulated, live configured, and planned evidence paths.
- Low-sample metrics must read as directional.
- Empty states must explain the next safe action.
- Errors must identify the failed stage and preserve provider boundaries.
- Reports must not convert evidence gaps into certain causal claims.
