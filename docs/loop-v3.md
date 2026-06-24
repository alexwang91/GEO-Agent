# Loop V3: Demo-Ready Evidence Loop

Loop V3 starts after the scaffold is complete. Its purpose is to turn GEO Agent from a set of tested seams into a demo-ready audit workflow that produces a traceable report from a concrete entity profile, page evidence, recorded or mock engine evidence, scoring, diagnosis, tasks, and retest plan.

## Source Principles

- Superpowers: brainstorm before implementation, write an executable plan, use TDD or eval-first verification, review the branch, and finish only after CI proves the slice.
- Matt Pocock skills: align on intent, maintain shared language, create vertical slices, preserve architecture quality, and avoid agent-built balls of mud.
- GitHub Loop Runner: operate through GitHub branches and PRs, keep state in planning docs, use CI as verification, record durable process decisions, repair the harness when the loop itself fails, and stop rather than fake unavailable evidence.

## Loop V3 Goal

Produce a runnable, evidence-backed audit path:

```text
EntityProfile
  -> QueryRecord list
  -> PageInventoryRecord list
  -> EngineRun evidence
  -> EvidenceStore records
  -> WeightedVisibilityScore
  -> FailureDiagnosis list
  -> OptimizationTaskBrief list
  -> ReportView
  -> JSON or Markdown report artifact
```

A slice is not complete unless it moves this path closer to a user-observable audit output.

## Operating Rules

1. **Reload state**
   - Read `AGENTS.md`, `docs/loop-v3.md`, `docs/next-steps-plan.md`, `docs/context.md`, `docs/decision-log.md`, `docs/feedback-log.md`, and current tests before coding.
   - Select the first TODO in the Loop V3 backlog.

2. **State the evidence contract**
   - Each slice must name the exact input evidence, output evidence, and persisted or rendered artifact.
   - Mock and recorded modes are allowed. Claims of live engine support require real adapter evidence and must not be faked.

3. **Slice through the audit path**
   - Prefer vertical slices that touch orchestration, fixture data, tests, and report output.
   - Avoid isolated helper modules unless they are immediately consumed by the audit workflow.

4. **Verify before implementation**
   - Add or update tests first for the user-visible behavior.
   - CI must be able to detect a broken audit path.

5. **Preserve seams**
   - Keep adapters separate from domain logic.
   - Keep persistence separate from scoring and rendering.
   - Keep report rendering deterministic.

6. **Review for product truth**
   - Reject changes that only mark state as done.
   - Reject report output that is marketing copy rather than evidence.
   - Reject scoring or diagnosis that hides missing evidence.

7. **Finish branch**
   - One slice per branch and PR.
   - CI green on the current head before merge.
   - Update next-step status only when the acceptance criteria are met.
   - Re-read the plan after merge.

## V3 Quality Gates

A V3 slice is done only if:

- It has a concrete fixture or recorded dataset.
- It produces a deterministic artifact or persisted records.
- It preserves existing public APIs unless a migration is documented.
- It has tests that fail if the end-to-end evidence path breaks.
- It avoids unsupported claims of live external integration.

## Stop Conditions

Stop and report instead of continuing when:

- A required external API key, browser, paid engine, or network credential is unavailable.
- CI cannot verify the behavior.
- The slice would require fabricating real engine evidence.
- The repository state source and code disagree after a merge.
- Repeated platform or tool failures prevent safe PR updates.

## Immediate V3 Backlog

| Slice | Goal | Evidence |
| --- | --- | --- |
| V3-0 | Install Loop V3 and productization plan. | Docs PR with CI green. |
| V3-1 | Add `AuditRunner` orchestrating the existing modules over fixtures. | End-to-end test creates report from profile, pages, and recorded runs. |
| V3-2 | Add recorded dataset schema and fixture loader. | Tests validate good fixtures and reject malformed fixtures. |
| V3-3 | Expand EvidenceStore beyond engine runs. | Tests persist query records, page inventory, diagnoses, tasks, and reports. |
| V3-4 | Add Diagnosis V2 using run, page, and competitor evidence. | Tests cover attribution, retrieval, competitor-source, entity, and intent mismatch cases. |
| V3-5 | Add CLI entry point for fixture-based audits. | CLI test writes JSON and Markdown report artifacts. |
