# Development Principles

## Skill Pack Map

| Source skill family | What to do in this repo |
| --- | --- |
| Superpowers | Clarify intent, brainstorm tradeoffs, write concrete plans, use TDD/eval-first, request review, finish only after CI evidence. |
| GitHub Loop Runner | Use GitHub-only branch/PR loops, `docs/progress.md` as state, CI as VERIFY, Loop Trace, Feedback Taxonomy, Handoff Decision, Long-Run Growth, Harness Repair, and Stopper Policy. |
| GEO product brief | Measure AI-answer visibility, diagnose citation failures, create evidence-backed optimization tasks, preserve audit history, and retest. |
| Simplicity and surgical-change discipline | State assumptions, choose the smallest vertical slice, touch only required files, avoid broad rewrites. |

## Optional Runtime Invocations

Use these only when installed:

| Phase | Optional invocation | Fallback in this repo |
| --- | --- | --- |
| Align | `$grill-with-docs` or `/grill-with-docs` | Clarify goal, vocabulary, acceptance criteria, and open decisions. |
| Slice | `$to-issues` or `/to-issues` | Split work into vertical milestones with file targets and verification. |
| Brainstorm | `$brainstorming` or `/brainstorming` | Compare implementation options before editing. |
| Plan | `$writing-plans` or `/writing-plans` | Write concrete steps with tests/evals and exact files. |
| Behavior changes | `$test-driven-development` or `/test-driven-development` | Define the failing test, eval, or CI assertion first. |
| Review | `$requesting-code-review` or `/requesting-code-review` | Review diff against acceptance criteria and loop evidence. |
| Finish | `$finishing-a-development-branch` or `/finishing-a-development-branch` | Merge only after CI, progress, feedback, and trace are current. |

## Workflow Discipline

1. Re-read state.
2. Select the first TODO from `docs/progress.md`.
3. Confirm acceptance criteria from `docs/next-steps-plan.md`.
4. Add deterministic verification first when behavior changes.
5. Implement the smallest vertical slice.
6. Update progress, feedback, and loop trace.
7. Open one PR.
8. Use CI as VERIFY.
9. Review against plan and PR template.
10. Merge only after green CI and complete evidence.

## Product Principles

- Measure real AI engine outputs when possible, but keep CI deterministic with fixtures and fake clients.
- Keep LLM simulation separate from real sampling.
- Diagnose why the brand is missing before generating content.
- Draft changes with evidence, impact, confidence, risk, and retest plan.
- Do not auto-publish in the MVP.
- Preserve query, answer, citation, diagnosis, recommendation, optimization, and retest history.
- Keep provider status truthful: implemented, fake/test, planned, unavailable.
- Treat the desktop UI as a product entry point, not decorative shell work.

## Credential and Provider Safety

- Raw API keys, OAuth tokens, cookies, request headers, and provider secrets must stay inside explicit session/provider boundaries.
- Return redacted labels or opaque session IDs to UI, reports, manifests, logs, and audit artifacts.
- Never require live provider credentials in CI.
- Use fake HTTP clients, recorded fixtures, manual imports, and structural checks for verification.
- Stop before implementing live-provider behavior that lacks redaction, artifact safety, or explicit user configuration.

## Anti-Patterns

- UI-only changes that do not connect to audit execution, provider access, evidence package, or report review.
- Provider code that makes default live calls.
- Broad refactors mixed into a feature milestone.
- Tests weakened or deleted to get CI green.
- Placeholder, dummy, noop, temporary, or churn-only files.
- Progress rows marked DONE without CI or explicit review evidence.
- Reports that claim improvement without measured baseline/follow-up evidence.