# Loop V5: UI-First Provider Access Loop

Loop V5 starts after GEO Agent can produce reproducible audit packages from fixtures. Its purpose is to move the product back toward the original agent vision: a user-facing app that connects providers, collects brand context, executes audits, and presents evidence.

## Source Principles

- Superpowers: evaluate the real product gap before coding, write a plan, add verification first, and merge only after CI.
- Matt Pocock skills: keep shared language, build vertical slices, preserve architecture boundaries, and avoid UI-only theater.
- GitHub Loop Runner: use repository state, one branch and PR per slice, CI verification, and explicit stoppers.

## V5 Product Thesis

The core missing capability is not another CLI feature. The core missing capability is product entry:

```text
Tauri + React UI
  -> Provider Access Layer
  -> Brand Profile
  -> Query Preview
  -> Provider-backed audit execution
  -> Evidence Package
  -> Report Review
```

## Provider Access Model

The UI must support four access modes:

- `api_key`: user supplies a provider key.
- `oauth`: user authorizes an account through an external provider.
- `platform_managed`: the deployment uses its own configured provider access.
- `manual_import`: user imports recorded evidence.

The product must not assume all providers support OAuth. The UI should show access methods per provider.

## UI Stack

The first UI stack is Tauri + React:

- Tauri desktop app shell.
- React workflow UI.
- Tauri command boundary for provider access and audit commands.
- Existing Python audit package remains the domain engine until a later packaging decision.

## V5 Quality Gates

A V5 slice is complete only if:

- It moves the product toward real provider-connected audit execution.
- It does not leak API keys or OAuth tokens into reports, manifests, logs, or audit databases.
- CI remains fixture-based and does not require external network calls.
- Planned providers are visible but not executable.
- UI work has tests or structural verification.

## V5 Backlog

| Slice | Goal | Evidence |
| --- | --- | --- |
| V5-0 | Install V5 evaluation, Tauri + React UI brief, provider access architecture, and loop plan. | Docs PR with CI green. |
| V5-1 | Add provider access domain model and registry. | Tests cover provider definitions, access methods, status, and redaction. |
| V5-2 | Add Tauri + React app shell. | App files, provider/profile/query/report shell, and non-network checks. |
| V5-3 | Add BYOK API key session flow. | Key accepted by backend/session boundary, redacted everywhere, no artifact leakage. |
| V5-4 | Add OAuth framework with fake provider. | Start/callback/disconnect flow, state validation, token redaction, no live calls. |
| V5-5 | Add first OpenAI-compatible answer provider behind explicit config. | Fake HTTP client in CI; opt-in live path documented. |
| V5-6 | Add crawler provider abstraction and first crawler adapter. | Static/fake crawler in CI; Crawl4AI or Firecrawl boundary documented. |
| V5-7 | Wire UI Run Audit to provider registry and audit package output. | UI can run fixture/fake-provider audit and display report shell. |

## Stopper Rules

Stop rather than merge when:

- Credentials or tokens would be persisted without a redaction/encryption policy.
- CI needs live network calls.
- A provider is shown as available when it is only planned.
- Tauri commands expose raw credentials to React.
- UI claims live search support before provider evidence exists.
