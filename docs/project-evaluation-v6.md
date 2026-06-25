# Project Evaluation V6

## Method

This evaluation applies the Superpowers sequence before implementation: identify the real product gap, pressure-test assumptions, define the smallest useful vertical slices, and require verification before merge. It also applies GitHub Loop Runner constraints: one milestone, one branch, one PR, CI as VERIFY, state in `docs/progress.md`, feedback classification, Loop Trace, long-run review, and hard stoppers.

## Current Repository State

GEO Agent has a substantial deterministic core:

- entity profile and query records;
- page inventory and crawler seam;
- engine sampling records and adapter-neutral import path;
- evidence store for raw query-answer-citation history;
- weighted visibility/citation scoring;
- citation failure diagnosis;
- optimization task briefs;
- experiment planning;
- `AuditRunner` over fixtures;
- recorded dataset schema and loader;
- reproducible audit package output with manifest, report artifacts, and audit database;
- Tauri + React desktop shell;
- provider access registry;
- BYOK API key session boundary;
- fake OAuth/state/callback boundary.

## Main Product Gap

The project is still not a provider-connected GEO agent. It can produce deterministic audit packages and now has UI/provider access scaffolding, but the user cannot yet run a provider-backed audit from the desktop product and review a live or recorded evidence-backed report through the UI.

The highest-value next gap is:

```text
Provider connection
  -> answer/crawl/search evidence acquisition
  -> existing AuditRunner evidence graph
  -> reproducible audit package
  -> desktop report review
  -> retest comparison
  -> learned optimization outcomes
```

## Completion Assessment

| Area | Rating | Assessment |
| :--- | ---: | :--- |
| Deterministic domain core | 8.5/10 | Existing schemas, scoring, diagnosis, task, experiment, and package artifacts create a strong core. |
| Reproducible fixture audit | 8.5/10 | The CLI and package path are useful and testable. |
| Provider access architecture | 6.5/10 | Registry, BYOK, and fake OAuth exist; provider-backed answer/crawl execution remains missing. |
| Desktop product entry | 5/10 | Tauri + React shell exists; Run Audit and report display are not yet wired end to end. |
| Credential safety | 6.5/10 | Redaction boundaries exist; artifact-wide leakage tests should be strengthened before real provider use. |
| Evidence-backed report UI | 3.5/10 | Report artifacts exist; UI consumption and warning states remain. |
| Retest and learning loop | 3/10 | Experiment planning exists; measured before/after packages and action learning remain future work. |

## Strategic Direction

Continue V5 through `V5-7` before starting broad V6 product expansion. The next PR should be `V5-5`, not a UI-only polish slice, because the product needs a real answer-provider boundary behind explicit configuration and fake-client CI verification.

After V5 completes, V6 should focus on provider-backed orchestration, manual import, parser/eval safety, evidence-backed report UI, credential hardening, retest comparison, release-readiness, and skill-learning records.

## Risks

| Risk | Why it matters | Control |
| :--- | :--- | :--- |
| UI theater | A desktop shell without executable audit paths does not advance the product. | Every UI milestone must connect to provider registry, audit execution, package artifacts, or report review. |
| Credential leakage | Provider work introduces API keys, tokens, headers, and response payload risk. | Add artifact-wide redaction tests before broader live-provider paths. |
| Live-service CI dependency | External services make CI flaky and unsafe. | Use fake clients, recorded fixtures, and explicit opt-in live configuration only. |
| Evidence drift | Report UI can drift from raw evidence and package artifacts. | Report UI must read generated artifacts rather than duplicate logic. |
| Over-broad milestones | Provider orchestration, crawler, UI, and report work can expand too far for one PR. | Keep one vertical slice per PR and run Review and Renewal when scope grows. |

## Decision

Proceed with the V5/V6 plan in `docs/next-steps-plan.md` and `docs/loop-v6.md`.

The first TODO remains `V5-5`: add the OpenAI-compatible answer provider behind explicit config with fake HTTP client tests, missing-credential failures, evidence conversion, no default live calls, and redaction checks.

## Stopper Assessment

No hard stopper blocks planning. Product work must stop if any next milestone requires live credentials in CI, weakens redaction, represents planned providers as live, or cannot map acceptance criteria to CI/review evidence.