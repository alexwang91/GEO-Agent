# Loop V4: Reproducible Audit Package Loop

Loop V4 starts after the fixture-based audit CLI exists. Its purpose is to turn a report-producing CLI into a reproducible audit package that can be inspected, rerun, archived, and used as evidence.

## Source Principles

- Superpowers: evaluate before coding, write plans for verifiable behavior, use test-first implementation, and finish branches only after review and CI.
- Matt Pocock skills: preserve shared language, avoid architecture drift, prefer vertical slices, and keep feedback loops fast.
- GitHub Loop Runner: keep state in repository docs, run one branch and PR per slice, require CI verification, and stop rather than fabricate live evidence.

## Loop V4 Goal

A fixture audit should produce a complete output directory:

```text
out/
  manifest.json
  report.json
  report.md
  audit.sqlite
```

The package must be sufficient to answer:

- Which fixture produced this audit?
- Which profile, queries, pages, runs, diagnoses, tasks, and reports were used?
- Which artifacts were written?
- Can a reviewer inspect the raw evidence without rerunning the audit?

## Operating Rules

1. Reload `AGENTS.md`, `docs/next-steps-plan.md`, `docs/loop-v4.md`, `docs/project-evaluation-v4.md`, and current tests.
2. Select the first TODO in the Loop V4 backlog.
3. State the audit package artifact being improved.
4. Add verification that fails if package reproducibility regresses.
5. Preserve recorded/fixture-only CI behavior.
6. Avoid unsupported live engine claims.
7. Merge only after CI is green, update state, then re-read the plan.

## Quality Gates

A V4 slice is complete only if:

- It creates or improves a durable audit artifact.
- It has deterministic tests.
- It preserves the existing `geo-agent audit` fixture workflow.
- It writes or validates evidence needed for review.
- It does not require network, browser, API keys, or paid engines in CI.

## V4 Backlog

| Slice | Goal | Evidence |
| --- | --- | --- |
| V4-0 | Install V4 evaluation, loop, and package plan. | Docs PR with CI green. |
| V4-1 | Persist the full audit evidence graph during `AuditRunner.run`. | Store contains queries, pages, runs, diagnoses, tasks, and report artifacts after a run. |
| V4-2 | Write reproducible audit package artifacts from CLI. | CLI writes `manifest.json`, `audit.sqlite`, `report.json`, and `report.md`. |
| V4-3 | Add canonical example fixture and usage docs. | `examples/acme-fixture.json` works with the CLI in CI. |
| V4-4 | Publish recorded dataset schema documentation. | Schema and docs validate required dataset sections. |
| V4-5 | Document live adapter boundary without implementing live calls. | Docs define safe future adapter contract and stopper rules. |
