# Tori-Ready UI Brief: GEO Agent

## Product Type

A web application for running AI search visibility audits for a brand. The first UI should be a focused workflow app, not a broad dashboard.

## Primary User

A founder, marketer, SEO/GEO consultant, or growth operator who wants to know whether AI answer engines mention, cite, and recommend their brand compared with competitors.

## Core User Story

```text
As a user,
I open GEO Agent,
connect one or more providers,
enter my brand profile and website,
run an audit,
and receive a report with evidence, failures, tasks, and retest plan.
```

## Information Architecture

Navigation:

1. Providers
2. Brand Profile
3. Queries
4. Audit Run
5. Report
6. Evidence Package

## Screen 1: Providers

Purpose: connect services used by the audit.

Sections:

- Provider matrix
- Connected providers
- Add provider modal
- Security note

Provider cards should show:

- Provider name
- Capability badges: Answer, Search, Crawl, Model, Analytics
- Access methods: API Key, OAuth, Platform, Manual Import
- Status: Available, Planned, Connected, Missing credential
- Primary action: Connect, Configure, Disconnect, Coming soon

Required UX copy:

```text
Credentials are used only to run your audit. They are never written into reports, manifests, logs, or audit databases.
```

## Screen 2: Brand Profile

Purpose: collect brand context.

Fields:

- Brand name
- Domain
- Aliases
- Competitors
- Target regions
- Target languages
- Target customer
- Main product
- Category
- Business goal
- Website URLs or sitemap URLs

Primary action: Generate Queries

## Screen 3: Queries

Purpose: preview generated query space before running provider calls.

Table columns:

- Query
- Intent
- Funnel stage
- Region
- Language
- Engine/provider
- Priority
- Cluster

Actions:

- Edit query
- Disable query
- Add query
- Continue to Audit

## Screen 4: Audit Run

Purpose: execute and monitor audit.

Sections:

- Audit checklist
- Provider readiness
- Crawl readiness
- Run progress
- Warnings

Progress steps:

1. Build query space
2. Crawl owned pages
3. Sample answer providers
4. Store evidence
5. Score visibility
6. Diagnose failures
7. Generate tasks
8. Write audit package

## Screen 5: Report

Purpose: show the operational result.

Cards:

- Visibility score
- Mention share
- Citation share
- Recommendation share
- Competitor-only share
- Query coverage

Main sections:

- Missing queries
- Competitor map
- Cited sources
- Failure diagnoses
- Recommended tasks
- Retest plan

Actions:

- Download report.json
- Download report.md
- Download audit package
- Start follow-up audit

## Screen 6: Evidence Package

Purpose: make audit evidence inspectable.

Show files:

- manifest.json
- report.json
- report.md
- audit.sqlite

Show evidence tabs:

- Query records
- Page inventory
- Engine runs
- Diagnoses
- Tasks
- Report artifacts

## Visual Direction

- Clean technical SaaS.
- High trust, low noise.
- Strong separation between setup, execution, and evidence review.
- Prefer tables and cards over marketing visuals.
- Use warning banners for missing provider access or missing citations.

## Component List

- App shell with left navigation
- Provider card
- Access method badge
- Connection modal
- Profile form
- Query table
- Audit progress timeline
- Score metric cards
- Failure diagnosis table
- Task recommendation list
- Evidence package file list
- Download actions

## Empty States

Providers:

```text
No providers connected yet. Connect an answer provider or import recorded runs to start an audit.
```

Queries:

```text
No queries generated yet. Complete your brand profile first.
```

Report:

```text
No audit report yet. Run an audit to generate visibility evidence.
```

## Security States

- Missing credential
- Expired OAuth token
- Provider disconnected
- API key rejected
- Provider planned but unavailable
- Live calls disabled in current environment

## First Build Scope

The first implementation should include:

- Providers page with provider matrix.
- Brand profile form.
- Query preview shell.
- Audit run shell.
- Report shell.

It does not need real provider calls in the first UI slice.
