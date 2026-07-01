# Loop V12 — SEO/GEO Subject Classifier

## Intent

Loop V12 adds a reasoning skill and classifier boundary that separates SEO asks from GEO asks before GEO-Agent routes work into measurement, diagnosis, task planning, or retest paths.

The loop formalizes the existing product promise to distinguish owned, competitor, and third-party evidence instead of treating visibility work as a generic SEO checklist.

## Scope boundary

GEO-Agent core handles AI search visibility measurement, evidence preservation, diagnosis, optimization task planning, and retest preparation.

GEO-Agent core does not execute SEO ranking actions.

SEO ranking work includes crawlability, indexability, sitemap, canonical, internal links, Core Web Vitals, and backlinks. V12 may name those actions as out-of-core references, but it must not run, score, or claim impact from them.

Plain Google and Bing organic ranking providers are deliberately absent from the provider matrix. That absence is the SEO/GEO scope boundary.

## Existing schemas to reuse

### Subject

Brand and product subjects must use `src/geo_agent/entity_profile.py` `EntityProfile` fields: `brand`, `aliases`, `domain`, `competitors`, `target_regions`, `target_languages`, `target_customer`, `main_product`, `category`, and `business_goal`.

Page, claim, and third-party-source subjects must map to the existing page snapshot, claim fidelity, and source classifier records. V12 must not invent a parallel subject schema.

### Demand context

Demand context must map to `src/geo_agent/query_discovery/cluster_schema.py` `QueryCluster` and the five `DEFAULT_CLUSTERS`: `problem`, `solution`, `brand`, `source`, and `decision`.

V12 must not add a second demand-context taxonomy.

### Platform

Platform status must come from `src/geo_agent/provider_access.py`, `src/geo_agent/manual_only_providers.py`, and `docs/provider-status-language.md`.

Current provider classes are:

- `openai_compatible`: implemented provider boundary, not ChatGPT Search.
- `manual_import`: implemented manual evidence path.
- `perplexity`, `gemini`, `crawl4ai`, `firecrawl`, `google_search_console`: planned.
- `google_aio`, `deepseek`, `kimi`, `qianwen`: manual-only.

### Diagnosis

Constraint diagnosis must reuse `src/geo_agent/diagnosis_taxonomy_v3.py` `DiagnosisV3` and `DiagnosisType` values:

- `missing_owned_content`
- `weak_citation_absorption`
- `claim_fidelity_gap`
- `competitor_displacement`
- `low_query_coverage`
- `unstable_sampling`
- `provider_unavailable`

The six-step pre-audit checklist annotates diagnosis output only. It must not add diagnosis types.

Checklist dimensions:

1. discoverability
2. accessibility
3. understandability
4. trust
5. usefulness
6. actionability

### GEO actions

GEO actions must continue to use the existing `optimization_tasks` taxonomy from Loop V10-10. V12 must not duplicate it.

## Milestones

| Milestone | Scope | Acceptance |
| :--- | :--- | :--- |
| V12-00 | Add state source and loop plan. | `docs/progress.md` tracks V12, and this file states the design boundaries. |
| V12-01 | Add skill scaffold. | Skill manifest and entrypoint exist, and structural tests verify the package shape without invoking the generic packaging validator. |
| V12-02 | Generalize skill packaging validation. | Validator reads required inputs, outputs, and boundary substrings from each skill manifest while retaining strict manifest and entrypoint failures. |
| V12-03 | Add classifier function. | The classifier returns subject type, cluster mapping, platform status, classification, reason, and confidence using existing enums and provider data. |
| V12-04 | Add diagnosis pre-check annotation. | Diagnosis records can carry six-step checklist annotations without new diagnosis types. |
| V12-05 | Add out-of-core SEO action reference list. | SEO classifications expose named SEO actions flagged as not executed by GEO-Agent; GEO routing remains unchanged. |
| V12-06 | Update product docs. | Product contract, provider language, report copy, and skill inventory describe the boundary honestly. |

## CI rule

GitHub Actions `verify` remains the only verification source. CI must remain network-free.
