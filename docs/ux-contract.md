# UX Contract

GEO-Agent's technical-preview UX must make the evidence boundary visible at every step. Users should know what was measured, how it was collected, what is directional, and what should be retested.

## Contract surfaces

- Personas: `docs/personas.md`.
- Ten-step journey: `docs/user-journeys.md`.
- Report and UI copy rules: `docs/report-copy-guidelines.md`.
- Error states: `docs/error-state-taxonomy.md`.
- Product promises and limits: `docs/product-contract.md` and `docs/limitations.md`.
- Provider status vocabulary: `docs/provider-status-language.md`.

## Required product language

- Manual evidence is user-supplied or recorded.
- Simulated evidence is fixture-backed or fake-provider test data.
- Live configured execution requires an implemented provider boundary and explicit user configuration.
- Planned providers are roadmap entries and are not audit execution paths.
- Low-sample visibility metrics are directional.
- Report claims must be traceable to samples, citations, pages, or imported evidence when those IDs exist.

## UI and report obligations

1. Show provider status before the user runs or imports evidence.
2. Disable planned-provider execution controls.
3. Show empty states that describe the next safe action.
4. Show partial-failure states without discarding usable evidence.
5. Keep metric cards tied to sample and package context.
6. Show diagnosis and task copy as evidence-backed recommendations, not automatic fixes.
7. Separate retest planning from observed baseline results.

## Copy contract test scope

`tests/test_ux_copy_contract.py` scans the UX docs, README, and desktop app copy for required provider distinctions and for overclaim phrases that would make low-sample or planned-provider states read as live coverage.
