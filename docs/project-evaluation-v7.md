# Project Evaluation V7

## Method

This evaluation applies the Superpowers sequence before implementation: identify the real product gap,
pressure-test assumptions, define the smallest useful vertical slices, and require verification before
merge. It applies GitHub Loop Runner constraints: one milestone, one branch, one PR, CI as VERIFY, state
in `docs/progress.md`, feedback classification, Loop Trace, long-run review, and hard stoppers. It also
folds in a four-block competitive and UX analysis (industry tools, OSS references, self-critique, and
end-to-end UX).

## What V6 Shipped

V6 delivered a provider-backed GEO agent core: provider-backed audit orchestration, manual/recorded
import, a provider output eval harness, an evidence-backed report UI, access/artifact safety hardening,
retest planning, release-readiness checks, and skill-learning records. The repository can produce a
reproducible audit package and review it through the desktop shell.

## Four-Block Competitive Analysis

- **Industry tools:** Semrush/Ahrefs (SEO base + AI visibility), Profound (engine coverage + crawler
  behavior), Evertune (repeated sampling + statistics), Ahrefs Brand Radar (source/citation graph).
- **OSS references:** onvoyage-ai/gtm-engineer-skills (skill packaging + deliverable files),
  cxcscmu/AutoGEO (engine-preference rules + GEO/GEU separation as an optimization plugin),
  stanford-oval/storm (multi-perspective query generation, unknown-unknowns, outline-before-audit).
- **Self-critique:** the evidence/provider/report/scoring architecture is solid, but real sampling,
  statistical credibility, UX, and case validation are weak.
- **UX:** the full journey - first open, project creation, query review, source selection, dashboard,
  evidence drilldown, task handoff, retest report, and export - is not yet a coherent product flow.

## Main Product Gap

V6 can run provider-backed audits, but the result is not yet trustworthy or usable end to end: scores
come from single samples without confidence, conclusions are not consistently traceable to raw evidence,
query discovery is template-bound, citation analysis stops at "was it cited" rather than "did it shape
the answer," and a non-engineer cannot run the full loop in the desktop product.

The highest-value V7 direction:

```text
Reposition as an AI Search Visibility Experiment Workbench
  -> traceable evidence graph
  -> STORM-style multi-perspective query discovery
  -> real-answer ingestion via manual import + truthful provider status
  -> citation absorption + claim fidelity
  -> repeated sampling + confidence + retest judgment
  -> owner-mapped executable tasks
  -> end-to-end desktop UX + role-based reports
  -> skill learning of what worked
```

## Completion Assessment

| Area | Rating | Assessment |
| :--- | ---: | :--- |
| Deterministic domain core | 8.5/10 | Strong schemas, scoring, diagnosis, task, package artifacts. |
| Provider-backed audit | 7/10 | Works for fixtures and fake providers; real-answer ingestion still leans on import. |
| Evidence traceability | 5/10 | Evidence store exists; metric/diagnosis/task to sample-ID traceability needs hardening (V7-04/05). |
| Query discovery | 4.5/10 | Template intents only; needs STORM multi-perspective generation (V7-06/07). |
| Statistical credibility | 3/10 | Single-sample scoring; needs repeated sampling, CI, noise floor (V7-17/18). |
| Citation depth | 3/10 | Selection only; needs absorption and claim fidelity (V7-15/16). |
| Desktop end-to-end UX | 4/10 | Shell exists; full journey pages and dashboard not yet built (V7-24..30). |
| Role-based reporting | 4/10 | Report artifacts exist; owner-specific reports needed (V7-31). |
| Runner state consistency | 8/10 | V7-01 adds a state audit, current-agent handoff reconciliation, workflow checks, and a docs-state consistency test. |

## Strategic Direction

Differentiate on explainability, local reproducibility, raw-evidence traceability, diagnosis depth,
executable owner-mapped tasks, repeated-sampling credibility, retest loops, and skill learning - not on
SEO data volume, enterprise coverage, or algorithm papers. Keep AutoGEO-style optimization as a plugin.

## Risks

| Risk | Why it matters | Control |
| :--- | :--- | :--- |
| Overclaiming provider support | Equating API output with ChatGPT Search misleads users. | Truthful provider-status vocabulary (V7-02/10); manual import as first real path. |
| False confidence | Single-sample scores read as definitive. | Repeated sampling, CI, noise-floor gating (V7-17/18); directional-only labels. |
| Evidence drift | UI/reports can diverge from raw evidence. | Traceable evidence graph and metric-to-sample IDs (V7-04/05); reports read artifacts. |
| UI theater | Pages without executable audit paths add no value. | Every desktop slice connects to evidence, audit, or report artifacts. |
| Over-broad milestones | Provider, stats, UI, and report work can exceed one PR. | One PR-sized slice per branch; Review and Renewal when scope grows. |
| Stale runner state | A stale first-TODO pointer can make the runner skip or repeat the wrong milestone. | V7-01 state audit and CI consistency test. |

## Decision

Proceed with Loop V7 as encoded in `docs/progress.md`, `docs/next-steps-plan.md`, and `docs/loop-v7.md`.
V7-01 reconciles runner state and marks the technical-preview boundary. After the V7-01 PR merges, the
first TODO is `V7-02`: product contract, provider-status language, and limitations docs.

## Stopper Assessment

No hard stopper blocks the V7 backlog. Product work must stop if any next slice requires live credentials in
CI, weakens redaction, represents planned providers as live, equates API output with a search UI, states
low-sample conclusions as definite, or cannot map acceptance criteria to CI/review evidence.
