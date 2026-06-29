<div align="center">

<pre>
+------------------------------------------------------------+
| GEO-AGENT                                                  |
| AI visibility audits | evidence graphs | retests           |
+------------------------------------------------------------+
</pre>

# GEO-Agent

_AI Search Visibility Agent for evidence-backed Generative Engine Optimization audits._

<p align="center">
  <a href="https://github.com/alexwang91/GEO-Agent/actions/workflows/verify.yml"><img src="https://github.com/alexwang91/GEO-Agent/actions/workflows/verify.yml/badge.svg" alt="Verify"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-%3E%3D3.11-3776ab?logo=python&logoColor=white" alt="Python 3.11+"></a>
  <a href="docs/product-contract.md"><img src="https://img.shields.io/badge/status-alpha_technical_preview-f59e0b" alt="Alpha technical preview"></a>
  <a href="docs/provider-status-language.md"><img src="https://img.shields.io/badge/providers-truthful_status_labels-111827" alt="Truthful provider status labels"></a>
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> |
  <a href="#what-it-does">What it does</a> |
  <a href="#how-it-works">How it works</a> |
  <a href="#proof">Proof</a> |
  <a href="#documentation">Docs</a>
</p>

</div>

GEO-Agent is an alpha workbench for auditing how a brand, product, website, and evidence network appear in AI-generated answers. It preserves query, answer, citation, page, diagnosis, task, and retest evidence so GEO work stays measurable instead of becoming a generic SEO checklist.

> **Technical-preview boundary:** current CI-verifiable behavior is fixture-backed, manual-import oriented, or routed through explicit provider-boundary code. Live crawling requires explicit opt-in and is tested with fake clients in CI. OpenAI-compatible API output is not ChatGPT Search. Google AIO is manual-only because AIO share links are gated and not auto-capturable.

## What It Does

- **Builds audit packages** - runs fixture or recorded datasets into `manifest.json`, `report.json`, `report.md`, and `audit.sqlite` artifacts.
- **Preserves evidence traceability** - links metrics back to samples, prompts, citations, pages, and audit graph records.
- **Extracts mentions and citations** - detects brand/entity mentions, URL citations, source domains, and obvious substring false positives.
- **Scores AI visibility** - computes mention share, citation share, recommendation share, answer-rank score, source diversity, query coverage, and competitor-only share.
- **Adds statistical guardrails** - carries mean, confidence interval, sample count, noise floor, and inconclusive-delta language where repeated samples exist.
- **Separates provider truth from provider plans** - implemented, manual, simulated, planned, unavailable, and manual-only evidence labels use explicit status language.
- **Protects credentials and artifacts** - raw API keys, OAuth tokens, cookies, request headers, and provider secrets are forbidden in reports, manifests, logs, audit databases, UI state, and exported artifacts.

## How It Works

```text
Brand profile + competitors + target market
        |
        v
Query set / recorded answer evidence / page evidence
        |
        v
Extraction: mentions, citations, recommendations, source domains
        |
        v
Scoring + confidence summaries + citation failure diagnosis
        |
        v
Report artifacts + optimization task drafts + retest plan
```

The intended product loop is: sample answers, diagnose visibility and citation gaps, draft evidence-backed optimization tasks, run a holdout retest, and keep the result traceable.

## Quickstart

Run the deterministic fixture-audit path from source:

```bash
# 1. Run tests
PYTHONPATH=src python -m unittest discover -s tests -v

# 2. Run quality gates
python tools/check_python_style.py
python tools/check_type_annotations.py
python tools/check_coverage.py

# 3. Run the CLI against a recorded dataset
PYTHONPATH=src python -m geo_agent.cli audit path/to/recorded-dataset.json --out out/audit-package

# 4. Run the CLI against explicit manual captures
PYTHONPATH=src python -m geo_agent.cli capture-package path/to/captures.json --out out/manual-package
```

The CLI writes:

| Artifact | Purpose |
|----------|---------|
| `manifest.json` | Package provenance, counts, profile, artifact list, and traceability map |
| `report.json` | Machine-readable report output |
| `report.md` | Human-readable report output |
| `audit.sqlite` | Local evidence database |

## Proof

| Check | What It Verifies | Command / Source |
|-------|------------------|------------------|
| Unit tests | Product contracts, extraction, statistics, crawler seam, artifact safety | `PYTHONPATH=src python -m unittest discover -s tests -v` |
| Style gate | Python files parse cleanly in the network-free style check | `python tools/check_python_style.py` |
| Type-syntax gate | Python source annotations parse in the network-free type gate | `python tools/check_type_annotations.py` |
| Coverage gate | Test coverage stays above the configured baseline | `python tools/check_coverage.py` |
| CI workflow | Runs docs, unit tests, style, type-syntax, and coverage gates | `.github/workflows/verify.yml` |

## Provider Status

| Path | Status | What it means |
|------|:------:|---------------|
| OpenAI-compatible | Implemented | API boundary exists when explicitly configured; not ChatGPT Search. |
| Manual Import | Implemented | Recorded/manual evidence path for imported answer runs. |
| Google AIO | Manual only | AIO share links are gated and not auto-capturable; use explicit manual capture. |
| Static crawler | Simulated | Fixture-backed crawler path for deterministic tests. |
| Live crawler seam | Implemented seam | Requires explicit opt-in and a fetch client; CI uses fake clients only. |
| Perplexity | Planned | Do not describe as live or available. |
| Gemini | Planned | Do not describe as live or available. |
| Crawl4AI | Planned | Planned crawler provider. |
| Firecrawl | Planned | Planned crawler provider. |
| Google Search Console | Planned | Planned analytics/search provider. |

Planned providers must remain planned until deterministic tests and explicit configuration prove the boundary. Manual-only evidence must remain manual-only until automated capture is implemented and verified.

## Compatibility

| Surface | Status | Notes |
|---------|:------:|-------|
| Python | Ready | `pyproject.toml` requires Python `>=3.11`. |
| CLI | Preview | `geo-agent audit` runs fixture/recorded datasets into an audit package; `geo-agent capture-package` packages explicit manual captures. |
| Desktop shell | Preview | Tauri/React shell exists, but is not a complete end-to-end non-engineer workflow. |
| Live provider coverage | Limited | Provider claims are restricted by `docs/provider-status-language.md` and `docs/limitations.md`. |
| CI | Ready | GitHub Actions `verify` is network-free except for Actions setup itself. |

## When To Use / When To Skip

**Great fit if you...**

- need an evidence-first GEO audit workbench instead of a copywriting prompt;
- want to preserve raw query-answer-citation history for later diagnosis and retesting;
- need provider status labels that avoid overstating live engine coverage;
- are comfortable with alpha technical-preview workflows and fixture/manual evidence paths.

**Skip it if you...**

- need a production SaaS, hosted monitoring service, or continuous automated sampler today;
- require verified automated coverage for ChatGPT Search, Perplexity, Gemini, Google AI Overviews, Claude Search, or Bing Copilot;
- want guaranteed ranking, citation, recommendation, or traffic improvement;
- want generated tasks to be published without human review.

<details>
<summary><b>Repository map</b></summary>

| Path | Purpose |
|------|---------|
| `src/geo_agent/cli.py` | Fixture-audit and manual-capture package CLI entry points |
| `src/geo_agent/provider_access.py` | Provider registry, BYOK session boundary, and credential redaction model |
| `src/geo_agent/crawl_provider_v2.py` | Static crawler and explicit opt-in live crawler seam |
| `src/geo_agent/report_v2.py` | Report sections, metric summaries, per-engine breakdowns, and noise-floor delta comparison |
| `tests/` | Product contract, extraction, statistics, crawler, and artifact-safety tests |
| `tools/` | Network-free style, type-syntax, and coverage gates |
| `docs/` | Product contract, limitations, provider copy rules, and consolidated changelog |

</details>

## Documentation

| Start here | Go deeper |
|------------|-----------|
| [Product brief](docs/product-brief.md) | [Product contract](docs/product-contract.md) |
| [Provider status language](docs/provider-status-language.md) | [Limitations](docs/limitations.md) |
| [V9 real-case evidence](docs/v9-real-case.md) | [Verification workflow](.github/workflows/verify.yml) |

## Compared To

| | Scope | Evidence-aware | Provider truth labels | Live-provider claim |
|-|-------|:--------------:|:---------------------:|--------------------|
| **GEO-Agent** | AI visibility audit, diagnosis, task drafts, retest planning | Yes | Yes | Limited to implemented/configured/manual-capture boundaries |
| Generic SEO checklist | Page/task checklist | Usually no | No | Often unspecified |
| LLM copywriting prompt | Draft content generation | No durable evidence graph | No | Not applicable |
| Hosted rank tracker | Monitoring/reporting | Depends on vendor | Depends on vendor | Vendor-defined |

## Safety Boundaries

- The product does not guarantee ranking improvement, recommendation improvement, citation improvement, or traffic improvement.
- OpenAI-compatible API output is not ChatGPT Search.
- Google AIO is manual-only; AIO share links are gated and not auto-capturable.
- Planned providers are not live, available, or supported until implemented and verified.
- Demo, fixture-backed, simulated, manual-only, and manual-import artifacts must not be represented as generated automated live-market audit output.
- Raw API keys, OAuth tokens, cookies, request headers, provider secrets, and raw credential labels must not appear in reports, manifests, logs, audit databases, UI state, or exported artifacts.

## Star History

<a href="https://www.star-history.com/?repos=alexwang91%2FGEO-Agent&type=date&legend=top-left">
  <picture>
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=alexwang91/GEO-Agent&type=date&legend=top-left" />
  </picture>
</a>
