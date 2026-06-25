# Tauri + React UI Brief: GEO Agent

## Product Type

A desktop application for running AI search visibility audits for a brand. The first UI should be a focused workflow app, not a broad dashboard.

## UI Stack Decision

Use Tauri + React:

- React renders the app shell and audit workflow UI.
- Tauri provides the desktop shell and secure command boundary.
- The existing Python audit engine remains the source of truth for domain logic during early V5.
- Provider credentials are handled through a provider access layer and must not be written into audit artifacts.

## Primary User

A founder, marketer, SEO/GEO consultant, or growth operator who wants to know whether AI answer engines mention, cite, and recommend their brand compared with competitors.

## Core User Story

```text
As a user,
I open the GEO Agent desktop app,
connect one or more providers by API key, OAuth, platform-managed access, or manual import,
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
- Status: Available, Planned, Connected, Missing credential, Configured boundary
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
- Fixture-only run path
- Run progress
- Warnings

Progress steps:

1. Build query space
2. Crawl owned pages or read fixture pages
3. Sample answer providers or read recorded answer runs
4. Store evidence
5. Score visibility
6. Diagnose failures
7. Generate tasks
8. Write audit package

### V5-5.5 Fixture Command Path

The first executable desktop boundary is fixture-only:

```text
run_fixture_audit(fixture_path, output_dir)
```

The Tauri command accepts a fixture path and output directory, delegates to the Python fixture package path, and returns package metadata plus report file locations:

- `manifest.json`
- `report.json`
- `report.md`
- `audit.sqlite`

The React app must show this as fixture-only and must state that provider-backed audit execution is still planned for V5-7. CI verifies this by Python wrapper tests and structural source checks; it does not compile or install Tauri dependencies.

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

## Tauri Command Boundary

Initial commands should be minimal and safe:

```text
list_providers()
connect_api_key_provider(provider_id, api_key)
start_oauth(provider_id)
disconnect_provider(provider_id)
validate_profile(profile)
generate_queries(profile)
run_fixture_audit(fixture_path, output_dir)
```

Commands must return redacted provider state only. No command may return raw credentials.

## Visual Direction

- Clean technical desktop app.
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

Use explicit empty states for missing providers, missing profile, no generated queries, no audit run, and no report yet. Empty states should describe the next safe user action.