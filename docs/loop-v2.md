# Loop V2: Evidence-First GEO Agent Runner

Loop V2 turns the existing milestone runner into a stricter product-quality loop. It keeps the GitHub-only PR discipline, but adds explicit alignment, shared language, red-green verification, architecture review, and evidence gates before code can be called done.

## Source Principles

- Superpowers: brainstorm before code, write readable implementation plans, use TDD/eval-first, request review, and finish branches only after verification.
- Matt Pocock skills: align before implementation, maintain a shared project language, prefer vertical slices, use red-green-refactor, and regularly improve architecture.
- GitHub Loop Runner: use `docs/progress.md` as state, one branch and PR per selected slice, CI as the verification channel, feedback taxonomy, trace, hypotheses, repair loop, and stopper rules.

## State Files

| File | Role |
| --- | --- |
| `docs/progress.md` | Current product state and selected slice source. |
| `docs/next-steps-plan.md` | Product backlog and acceptance criteria. |
| `docs/loop-v2.md` | Operating protocol for future work. |
| `docs/context.md` | Shared domain language and naming decisions. |
| `docs/decision-log.md` | ADR-style decisions that should survive compaction or handoff. |
| `docs/feedback-log.md` | Observations, CI failures, review findings, and next-action constraints. |
| `docs/loop-trace.md` | Auditable event trace for runner actions. |
| `docs/loop-hypotheses.md` | Durable process changes with success and rollback criteria. |

## Loop Phases

1. **Reload state**
   - Read `AGENTS.md`, `docs/progress.md`, `docs/next-steps-plan.md`, `docs/context.md`, `docs/decision-log.md`, `docs/feedback-log.md`, `docs/loop-trace.md`, and `docs/loop-hypotheses.md`.
   - Select the first unfinished slice from `docs/progress.md` or the top item from the V2 plan.
   - Stop if there is no unfinished slice or a blocker in feedback, hypotheses, governance, or CI.

2. **Align and name the domain**
   - Convert vague user language into project terms in `docs/context.md`.
   - Record durable product or architecture decisions in `docs/decision-log.md`.
   - No code starts until the target slice has a concrete acceptance check.

3. **Slice vertically**
   - A slice must cross one real seam end to end: input, domain model, persistence or adapter boundary, scoring or report behavior, tests, and docs when relevant.
   - Avoid broad milestone closure unless every acceptance criterion has evidence.
   - Prefer one product capability per PR.

4. **Plan for a junior executor**
   - Write the smallest implementation plan that names exact files, public interfaces, tests, and verification commands.
   - Every task should be independently reviewable.
   - Do not introduce a framework unless the slice proves the need.

5. **Red-green verification**
   - Add or update a failing test, fixture, snapshot, or eval before product code when behavior changes.
   - Confirm the check fails for the right reason when local execution is possible.
   - In GitHub-only mode, ensure CI is capable of detecting the failure before merging.

6. **Build surgically**
   - Implement only the planned slice.
   - Keep deep modules: small public API, meaningful internal behavior, and clear seams for future adapters.
   - No dummy, noop, placeholder, or marketing-only files.

7. **Review against evidence**
   - Review for spec compliance, code quality, missing edge cases, and architecture drift.
   - Critical findings block merge.
   - Non-critical findings become issues, next-plan entries, or feedback records.

8. **Finish branch**
   - Open PR with acceptance evidence.
   - Wait for CI.
   - Merge only when current head CI is green and progress/feedback/trace are consistent.
   - Re-read `docs/progress.md` after merge before selecting the next slice.

9. **Repair or renew**
   - If the same failure class repeats, stop product work and run harness repair.
   - If a process change should persist, add a hypothesis with success criteria and rollback rule.

## Product Quality Gates

A slice is done only when all applicable gates pass:

- Acceptance criterion is testable and tested.
- CI passes on the PR head.
- The public API is named using `docs/context.md` terms.
- Data that should become product memory is persisted or has a documented storage seam.
- Mock mode exists for CI, but real adapters are not blocked by the design.
- The report or output is operational evidence, not a marketing placeholder.
- Review found no weakened assertions or scope substitution.

## Stopper Policy for V2

Stop instead of continuing when:

- CI cannot verify the current behavior.
- The next task requires secrets, paid APIs, browser rendering, or external credentials not available to the runner.
- The code would need to fake real engine sampling or real crawl evidence.
- The proposed change only marks progress as done without improving product capability.
- Safety or platform tooling blocks required repository updates repeatedly.

## Immediate V2 Backlog

| Slice | Goal | Evidence |
| --- | --- | --- |
| V2-0 | Install this loop, context, decision log, and V2 plan. | Docs PR with CI green. |
| V2-1 | Add persistent run store for raw query-answer-citation history. | SQLite-backed tests for save/load/query. |
| V2-2 | Replace parser-only page inventory with fetch-capable crawler seam. | Tests for HTTP fixture, sitemap index, canonical dedupe, and errors. |
| V2-3 | Upgrade engine sampling adapter contract. | Mock adapter plus one importable recorded-run adapter. |
| V2-4 | Rework scoring into weighted metric components. | Unit tests for weighting, competitor-only, missing citation, and rank cases. |
| V2-5 | Add evidence-backed report artifact. | Snapshot or structured JSON report test. |
