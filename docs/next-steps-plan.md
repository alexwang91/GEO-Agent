# Next Steps Plan

## Product Goal

Build an AI Search Visibility Agent for GEO that helps a brand understand where it appears or fails to appear in AI answers, why it is missing or uncited, what actions should be taken, and whether those actions improve measurable visibility after retesting.

## Methodology Map

- Matt Pocock skills: alignment, shared language, ADRs, and vertical-slice issues.
- Superpowers: brainstorm -> plan -> TDD/eval-first -> review -> finish.
- Karpathy guidelines: think before coding, simplicity first, surgical changes.

## Optional Skill Invocation Map

| Phase | Optional invocation | Fallback |
| --- | --- | --- |
| Align | `$grill-with-docs` or `/grill-with-docs` | Clarify goal and terms. |
| Slice | `$to-issues` or `/to-issues` | Create vertical milestones. |
| Brainstorm | `$brainstorming` or `/brainstorming` | Explore options. |
| Plan | `$writing-plans` or `/writing-plans` | Write concrete steps. |
| Behavior changes | `$test-driven-development` or `/test-driven-development` | Define the failing check first. |
| Review | `$requesting-code-review` or `/requesting-code-review` | Review diff and evidence. |
| Finish | `$finishing-a-development-branch` or `/finishing-a-development-branch` | Merge after CI and state updates. |

## M0 Acceptance Criteria

- Required runner files exist.
- Product brief captures the GEO Agent boundary and MVP scope.
- Progress table contains vertical, verifiable milestones.
- CI verifies required docs and rejects placeholder files.
- PR template requires acceptance evidence, CI, trace, and feedback links.

## M1 Acceptance Criteria

- A structured entity profile type or schema exists.
- Required fields include brand, aliases, domain, competitors, target regions, target languages, target customer, main product, category, and business goal.
- Invalid or missing required fields produce actionable validation errors.
- Tests or CI checks cover valid and invalid profiles.

## M2 Acceptance Criteria

- Query generation supports brand, category, comparison, buying intent, problem solving, scenario, negative/risk, and alternatives.
- Queries include intent type, funnel stage, language, region, target engine, competitor entities, expected answer format, and priority score.
- Unit tests or eval fixtures verify deterministic query records for a sample entity.

## M3 Acceptance Criteria

- Page inventory records URL, title, H1, schema types, last modified when available, canonical URL, and content chunks.
- Sitemap and manual URL input are both supported.
- Tests cover missing sitemap, duplicate URLs, and malformed pages.

## M4 Acceptance Criteria

- Engine runs are persisted with engine, query, timestamp, region, language, raw answer, parsed citations, mentions, and source domains.
- The sampler interface can run in mock mode for CI.
- Real engine integrations are isolated behind adapters.

## M5 Acceptance Criteria

- Score functions are deterministic and documented.
- Metrics include mention share, citation share, recommendation share, answer rank, source diversity, and query coverage.
- Tests cover zero-result, mixed-result, and competitor-only cases.

## M6 Acceptance Criteria

- Citation failures are classified into one or more known failure types with evidence.
- The classifier produces an explanation and recommended next diagnostic step.
- Tests cover each failure type.

## M7 Acceptance Criteria

- Recommendations include target page, query cluster, failure type, action type, expected impact, confidence, risk, and draft content.
- Drafts avoid auto-publish behavior.
- Tests verify safe output shape and required evidence fields.

## M8 Acceptance Criteria

- Experiments define train, validation, and holdout query sets.
- Retest plans compare pre/post metrics under the same engine, query, language, and region.
- Tests cover holdout leakage prevention.

## M9 Acceptance Criteria

- The report shows score, missing queries, competitor map, cited sources, failure diagnosis, and recommended tasks.
- The first screen is operational, not a marketing landing page.
- Visual checks or snapshots verify the report renders without overlapping text.
