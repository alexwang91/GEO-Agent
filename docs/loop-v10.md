# Loop V10 — GEO-Research Integration

## Design intent

Loop V10 converts GEO research into product-grade measurement, diagnosis, experiment planning, and retesting inside GEO-Agent. The loop starts with documentation-only evidence mapping, then fixes real-data correctness bugs, then deepens measurement, then adds an optimization plugin boundary, then gates UI and skill packaging.

## Product boundary

GEO-Agent is an AI search visibility measurement, diagnosis, and experiment workbench.

Core responsibilities:

- collect and validate explicit engine evidence;
- score brand, competitor, citation, recommendation, and attribution visibility;
- diagnose feature gaps and evidence gaps;
- create evidence-backed optimization tasks;
- export task briefs to external executors;
- retest and learn from post-change measurements.

Out-of-core responsibilities:

- final marketing copy generation;
- rewrite execution;
- multi-site publishing;
- external crawler analytics ingestion beyond an explicit interface.

Rewrite skills, GEO rewrite prompts, and GEOFlow may be integrated only as optimization plugins or downstream executor interfaces. GEO-Agent emits draftable task briefs and evidence contracts. It must not generate final content.

## Research principles

- Per-engine measurement is primary. A single aggregate score is directional context only.
- Single samples are directional. Repeated sampling may estimate probability and confidence, but must expose n and uncertainty.
- Google AIO is manual-only because share links are gated and not auto-capturable.
- Chinese AI search engines are manual-only until sanctioned provider paths exist.
- CI stays network-free. Live providers do not run in CI.
- Engine answers must come from explicit manual capture or sanctioned provider paths. Do not fabricate answers.
- Existing V7/V8 measurement modules and entity-resolution helpers are preferred over churn.

## Source-to-module integration map

Detailed mapping lives in `docs/geo-research-integration.md`. Summary:

- `GEO: Generative Engine Optimization`: visibility metrics, Position-Adjusted Word Count, Subjective Impression, and the nine optimization methods.
- `A Measurement Framework for GEO Across AI Search Platforms`: citation selection, absorption, and attribution decomposition plus citation-level feature records.
- `GEO in digital repositories`: lower-priority repository-domain evidence source.
- GEO content-engineering manuals and annotation demo: content feature taxonomy for diagnosis.
- GEO rewrite prompt, GEO rewrite skill, and `yao-geo-skills`: external execution/plugin inputs, not core writing behavior.
- GEOFlow: downstream executor/export-import interface.
- YAO / `yao-meta-skill`: packaging discipline for V10-16 and V10-17.
- Systems thinking and engineering literacy: diagnosis-task-retest-learning feedback loop and Goodhart guardrails.

## Phase 0 — Evidence and integration map

### V10-01 evidence-and-integration-map

Docs only.

Required outputs:

- `docs/v10-real-case.md` with the Huawei three-engine directional evidence matrix.
- `docs/geo-research-integration.md` with resource-to-module mapping and the identity boundary statement.
- No code changes.

Acceptance:

- The identity boundary is explicit.
- The Huawei real-case evidence is preserved per engine.
- Each named source resource maps to a module, milestone, or plugin boundary.
- The first implementation TODO remains V10-02 after V10-01 is complete.

## Phase A — Correctness and measurement core

### V10-02 fix-recommendation-matching

Fix `visibility_scoring._same_entity` from exact equality to entity containment using `entity_resolution.has_entity` and `find_entity_matches`.

Regression test:

- Brand `Huawei` matches recommendation `Huawei Watch GT 6 Pro`.
- `Apple Watch` still matches.
- Unrelated token substrings do not match.

### V10-03 fix-manual-capture-recommendations-and-mention-dedup

Carry recommendations into `EngineRun` during manual capture import and deduplicate mention extraction.

Regression test:

- Imported capture yields non-empty matched recommendations.
- Mentions are de-duplicated.

### V10-04 capture-to-package-bridge

Add a function and CLI subcommand to turn multi-engine manual captures into a real package with `manifest`, `report.json`, and `audit.sqlite`, without query generation.

Regression test:

- N captures across two engines produce a package with all runs per engine.
- Test remains network-free.

### V10-05 position-adjusted-visibility

Replace the naive `answer_rank` char/20 weighting with Position-Adjusted Word Count and add a Subjective-Impression-style component.

Regression test:

- Position weighting matches the paper definition on fixtures.
- The magic `/20` approximation is removed.

### V10-06 report-v2-selection-absorption-attribution

Add report v2 per-engine sections for citation selection, absorption, and attribution decomposition. Flag single aggregate as directional.

Regression test:

- Report JSON has per-engine and three-layer sections.

## Phase B — Measurement deepening

### V10-07 citation-level-feature-schema

Add citation-level feature records to the evidence graph, including citation absorption and claim fidelity.

Regression test:

- Each citation carries the required feature fields.

### V10-08 content-feature-taxonomy-diagnosis

Wire GEO content-feature taxonomy into diagnosis so `why not cited` can identify concrete feature gaps.

Regression test:

- Diagnosis references concrete taxonomy feature gaps.

### V10-09 repeated-sampling-and-manual-only-provider-matrix

Add repeated-sampling probability/confidence strengthening. Add DeepSeek, Kimi, Qianwen, and AIO as manual-only providers in the provider matrix.

Regression test:

- Provider statuses are correct.
- CI remains network-free.

## Phase C — Optimization plugin

### V10-10 optimization-task-action-taxonomy

Map optimization task actions to the nine GEO paper methods with evidence IDs, expected metric, owner, risk, and retest plan.

Regression test:

- Tasks map to the nine methods with evidence IDs.
- Confidence is not hardcoded.

### V10-11 optimization-execution-plugin-boundary

Define the plugin interface from `optimization_tasks` to external rewrite skills. GEO-Agent emits a draftable brief and hands off. It does not generate final content.

Regression test:

- Plugin interface contract passes with a fake plugin.

### V10-12 geoflow-interface

Export a task plan to a GEOFlow-compatible input and import GEOFlow AI-crawler analytics as an evidence source. Interface and fixtures only; no live GEOFlow in CI.

Regression test:

- Export/import fixtures pass.

## Phase D — UI gated correctly

### V10-13 ui-brand-form-query-preview

Frontend-only brand form and query preview. Preview is labeled `not yet connected`. Results render per engine.

Regression test:

- Structural JSX test verifies nine fields, preview, and honesty label.

### V10-14 ui-reproducible-preview-artifact

Add a reproducible CI UI preview/screenshot artifact.

Regression test:

- CI publishes PNG preview artifact.

### V10-15 ui-capture-package-import-wizard

Import wizard gated behind V10-03 and V10-04. Shows validation, manual-only/AIO boundary, and real multi-engine package per engine.

Regression test:

- Wizard states and per-engine render pass.

## Phase E — YAO packaging

### V10-16 yao-skill-packaging

Adopt YAO-style packaging for research-query, audit, diagnose, task, and retest skills with `SKILL.md`, `interface.yaml`, Skill IR, and `evals/`.

Regression test:

- Packaging evals pass.

### V10-17 yao-governance-evals-release-guards

Add governance eval packs, blind-review discipline, release guards, and claim guards for packaged skills.

Regression test:

- Governance and release guard checks pass.

## Stop condition

Stop after the first TODO milestone unless the runner is explicitly instructed to continue. One milestone equals one branch, one PR, and CI verification.
