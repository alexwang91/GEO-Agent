# Product Contract

GEO-Agent is an alpha/technical-preview AI Search Visibility Experiment Workbench. It helps teams inspect how a brand, product, website, and evidence network appear in AI-generated answers, then plan evidence-backed changes and retests.

## Promises

GEO-Agent may promise the following only when the related path is implemented and verified by CI:

- Preserve audit evidence so conclusions can point back to queries, answers, citations, pages, diagnoses, tasks, and retests.
- Distinguish owned, competitor, and third-party evidence instead of treating visibility as a generic SEO checklist.
- Surface provider support truthfully with the provider-status vocabulary in `docs/provider-status-language.md`.
- Keep planned providers labeled planned until deterministic tests and explicit configuration prove the boundary.
- Treat low-sample audit results as directional unless repeated sampling, confidence intervals, and noise-floor gates support stronger language.
- Keep raw credentials, OAuth tokens, cookies, request headers, provider secrets, and live answer payload secrets out of reports, manifests, logs, audit databases, and UI state.
- Generate optimization tasks only as drafts or handoff recommendations, with evidence, risk, confidence, owner, and retest context when those fields are available.

## Non-promises

GEO-Agent must not promise or imply:

- The product does not guarantee ranking improvement, recommendation improvement, or citation improvement in any AI engine.
- Full coverage of ChatGPT Search, Perplexity, Google AI Overviews, Gemini, Claude Search, Bing Copilot, or any other live surface unless that provider path is implemented and verified.
- OpenAI-compatible API output is not ChatGPT Search.
- That a single answer sample proves brand visibility, competitor preference, engine behavior, or optimization impact.
- That generated optimization tasks are safe to publish without human review.
- That owned-page edits alone solve GEO failures; third-party evidence, crawlability, citation source mix, and claim support may matter.
- That the desktop UI is production SaaS, hosted monitoring, or continuous automated sampling.

## Current technical-preview boundary

Current CI-verifiable behavior is fixture-backed, manual-import oriented, or routed through explicit provider-boundary code. V7 will harden this into a product workflow through the ordered milestones in `docs/progress.md` and `docs/next-steps-plan.md`.

## Completion rule

A feature claim belongs in README, UI, reports, or public docs only when one of these is true:

1. The feature is implemented and covered by deterministic CI tests.
2. The feature is explicitly labeled planned.
3. The feature is explicitly labeled directional, simulated, manual-only, or fixture-backed, with no claim of live provider coverage.
