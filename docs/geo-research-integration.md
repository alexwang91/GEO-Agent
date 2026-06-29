# GEO Research Integration Map

## Identity boundary statement

GEO-Agent is an AI search visibility measurement, diagnosis, experiment-planning, and retest workbench. Measurement research belongs in the core. Content rewriting, content-production skills, and distribution systems belong only behind an optimization plugin or downstream executor interface. GEO-Agent may emit an evidence-backed task brief, but it must not generate final marketing copy.

## Source access notes

This file maps the resources named for Loop V10. Public arXiv and GitHub resources are directly inspectable. The short-link research/manual/prompt resources are recorded as specified sources and should be manually reviewed again during their target milestones before code is changed.

## Resource-to-module map

| Source | Key usable idea | GEO-Agent module / artifact | V10 milestone | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| `GEO: Generative Engine Optimization` — https://doc.laoyao.cn/0elhy1 and https://arxiv.org/abs/2311.09735 | Position-Adjusted Word Count; Subjective Impression; nine GEO methods: Authoritative, Statistics Addition, Keyword Stuffing, Cite Sources, Quotation Addition, Easy-to-Understand, Fluency Optimization, Unique Words, Technical Terms | `visibility_scoring`, `report_v2`, `optimization_tasks` | V10-05, V10-10 | Core measurement for metrics; task taxonomy only for optimization |
| `A Measurement Framework for GEO Across AI Search Platforms` — https://doc.laoyao.cn/ykiktr | Citation selection -> absorption -> attribution decomposition; citation-level feature records; multi-platform measurement | `report_v2`, `evidence_graph`, citation feature schema | V10-06, V10-07 | Core measurement |
| `GEO in digital repositories` — https://doc.laoyao.cn/fnf30e | Repository-domain GEO evidence; lower-priority domain transfer | Research notes and future vertical fixtures | Deferred after V10-08 unless needed | Core only if used as a domain fixture |
| GEO content-engineering manuals and feature-annotation demo — https://doc.laoyao.cn/9fl0bc, https://doc.laoyao.cn/t754wa, https://doc.laoyao.cn/54yx5b, https://doc.laoyao.cn/00j3ps | Content feature taxonomy: statistics, quotations, authoritative sources, schema, entity clarity, FAQ, freshness | diagnosis feature gaps; scoring features | V10-08 | Core diagnosis; no copy generation |
| GEO rewrite prompt and skill — https://ai.laoyao.cn/ylOfC, https://ai.laoyao.cn/cqWRs | Rewrite execution patterns | `optimization_plugins` interface and task brief export | V10-11 | Plugin only; no final content in core |
| `yao-geo-skills` — https://github.com/yaojingang/yao-geo-skills | Skill catalog spanning measurement, content production, knowledge assets, research, and GEOFlow operations | provider sampling guidance; plugin interface; YAO packaging precedent | V10-09, V10-11, V10-16 | Measurement skills may inform core; content-production skills stay external |
| GEOFlow — https://github.com/yaojingang/GEOFlow | Content engineering, multi-site distribution, AI tasks, analytics, WordPress target publishing | GEOFlow export/import interface | V10-12 | Downstream executor only |
| YAO / `yao-meta-skill` — https://github.com/yaojingang/yao-meta-skill | `SKILL.md`, `agents/interface.yaml`, Skill IR, evals, blind-review, release governance | packaged research-query, audit, diagnose, task, retest skills | V10-16, V10-17 | Packaging discipline |
| `Thinking in Systems` | Feedback loops, leverage points, Goodhart risks | diagnosis -> task -> retest -> learning loop; CI-as-proxy warning | All phases | Conceptual only |
| `engineering-literacy` | Tradeoff framing | milestone acceptance, risk, owner, retest fields | All phases | Conceptual only |

## Measurement-core integration

### V10-05 Position-Adjusted Word Count

Implement a source/citation visibility metric that weights cited sentences by word count and response position. This replaces the current naive rank approximation. The same milestone adds a Subjective-Impression-style component as a deterministic fixture-backed approximation or schema slot, not as live LLM judging in CI.

### V10-06 Selection, absorption, attribution decomposition

Report v2 should separate:

1. Selection: whether the engine selected or cited a source.
2. Absorption: whether source claims entered the answer body.
3. Attribution: whether absorbed claims were attributed to the correct source or brand.

The report must keep these sections per engine.

### V10-07 Citation-level feature records

Each citation evidence node should carry feature fields sufficient for downstream diagnosis. Required field families should include source identity, rank/position, citation context, claim span, absorption status, attribution status, claim fidelity, and content-feature signals where available.

### V10-08 Content-feature diagnosis

Diagnosis should translate `why not cited` into feature gaps. Examples: missing statistics, missing quotation, weak authority signal, unclear entity, absent schema, absent FAQ, stale source, or weak claim support.

## Optimization plugin integration

### V10-10 Task taxonomy

Optimization tasks should map to the nine GEO paper methods and include:

- evidence IDs;
- owner;
- expected metric movement;
- risk;
- retest plan;
- target engine;
- target query or query cluster.

Do not hardcode confidence. Confidence must derive from evidence maturity, sample size, and repeated-sampling status.

### V10-11 Rewrite plugin boundary

GEO-Agent exports a task brief to a plugin interface. A fake plugin in tests can prove the contract. The core does not produce final copy.

Required contract families:

- input: brand, page/source, evidence IDs, task method, target feature gaps, constraints, risk, retest metric;
- output: plugin status, draft artifact pointer or external reference, claimed method, evidence used, warnings;
- validation: no silent final-copy injection into core reports.

### V10-12 GEOFlow interface

GEO-Agent may export a task plan to GEOFlow-compatible input and import GEOFlow analytics as evidence. The milestone is interface-and-fixture only. CI must not call live GEOFlow.

## Provider and sampling integration

V10-09 should add provider statuses for manual-only engines and repeated-sampling probability/confidence summaries. Provider matrix rules:

- Google AIO: `manual_only`.
- DeepSeek: `manual_only`.
- Kimi: `manual_only`.
- Qianwen: `manual_only`.
- CI: fixture-only.

Repeated sampling must expose n, engine, query cluster, sample collection method, probability estimate, and directional confidence label.

## UI and packaging integration

UI milestones come after capture and report foundations. UI must display per-engine results before aggregates and must label previews not connected to live providers.

YAO packaging comes after core behavior stabilizes. Package research-query, audit, diagnose, task, and retest as skills with compact entrypoints, neutral interfaces, Skill IR, evals, and governance checks.
