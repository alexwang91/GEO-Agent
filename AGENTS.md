# Agent Instructions

Read these files before development:

- `docs/autonomous-runner.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v7.md`
- `docs/project-evaluation-v7.md`
- `docs/loop-v6.md`
- `docs/project-evaluation-v6.md`
- `docs/loop-v5.md`
- `docs/project-evaluation-v5.md`
- `docs/ui-tori-brief.md`
- `docs/provider-access-architecture.md`
- `docs/development-principles.md`
- `docs/long-run-growth-loop.md`
- `docs/feedback-taxonomy.md`
- `docs/feedback-log.md`
- `docs/loop-trace.md`
- `docs/handoff-decision.md`
- `docs/review-and-renewal-loop.md`
- `docs/harness-repair-loop.md`
- `docs/loop-hypotheses.md`
- `docs/stopper-policy.md`
- `docs/loop-review.md`
- `.github/pull_request_template.md`

## State Sources

`docs/progress.md` is the single milestone state source. `docs/next-steps-plan.md` contains detailed acceptance criteria, file targets, and verification notes. When they conflict, stop and run the Review and Renewal Loop instead of guessing.

Current active product loop: V7 AI Search Visibility Experiment Workbench. V5 and V6 are complete. V7-01 through V7-04 are complete in sequence. After the V7-04 branch merges, the first TODO is `V7-05`, the audit package manifest v2 slice.

## Workflow Discipline

Use the GitHub connector for repository work. Use one branch and one PR per milestone. Use CI as VERIFY. Do not rely on local clone, package-manager install, or live provider access for completion evidence unless the milestone explicitly adds an approved CI-safe path.

Follow the Superpowers sequence: clarify intent, write a concrete plan, define verification first, implement the smallest vertical slice, request/review against evidence, and finish only after CI is green. Apply GitHub Loop Runner rules: read fresh state, select the first TODO, append loop evidence, classify feedback, update progress, and re-read state before continuing.

## Product Guardrails

- Preserve fixture-only CI unless the milestone explicitly adds fake-client provider tests.
- Do not persist raw API keys, OAuth tokens, cookies, live answers, or crawl secrets into reports, manifests, logs, audit databases, or UI state.
- Show planned providers as planned. Do not represent a provider as live until deterministic tests and explicit configuration prove the boundary.
- Keep UI work tied to an executable product path: provider registry, brand input, query preview, audit execution, evidence package, or report review.
- Do not weaken tests, evals, assertions, acceptance criteria, redaction checks, or stopper rules.
- Do not add dummy, noop, placeholder, or churn-only files.
