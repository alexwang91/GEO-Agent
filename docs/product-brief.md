# GEO Agent Product Brief

## Product Goal

Build an AI Search Visibility Agent for Generative Engine Optimization. The product monitors, diagnoses, and improves how a brand, product, website, and third-party evidence network appear in AI-generated answers from engines such as ChatGPT Search, Perplexity, Google AI Overviews, Gemini, Claude Search, and Bing Copilot.

The core loop is sampling, diagnosis, optimization, experiment verification, and reusable skill learning.

## Product Boundary

The first product should not be a generic SEO title or content rewriting tool. It should focus on measurable AI-answer visibility:

- discover how users ask about a category, competitor, problem, comparison, and purchase intent;
- sample real AI engines instead of relying only on LLM simulation;
- score mention share, citation share, recommendation share, answer rank, claim accuracy, sentiment framing, source diversity, and query coverage;
- diagnose citation failure root causes;
- produce draftable optimization actions with expected impact, risk, and retest plans;
- learn which optimization skills work for each engine, query type, and vertical.

## MVP Scope

Input:

- brand;
- domain;
- competitors;
- target region;
- target language;
- target customer;
- main product;
- business goal.

Output:

- AI Visibility Score;
- top missing high-value queries;
- competitor citation map;
- citation failure diagnosis;
- website GEO audit;
- page-level optimization tasks;
- draft snippets, FAQ, schema, and comparison table recommendations;
- expected impact and confidence;
- retest plan.

## First Supported Workflow

1. User enters one brand/domain and competitors.
2. System crawls sitemap, core pages, metadata, schema, and page chunks.
3. Query Space Builder creates 100 to 300 queries across intent types.
4. Engine Sampler records answers, mentions, citations, recommendations, and source domains.
5. Scoring pipeline computes visibility and citation metrics.
6. Citation Failure Debugger classifies the likely failure type.
7. Optimization Engine generates safe draft tasks.
8. Experiment Designer creates a holdout retest plan.

## Primary Risk

The product becomes a checklist instead of a diagnosis and experiment system. Protect the long-term asset by preserving raw query-answer-citation history, failure labels, traceable optimization actions, and measured outcomes.
