# V11 Reliability Loop Plan

## Goal

V11 should prove the V10 measurement system on one sanitized real-case flow before more feature breadth is added.

## Scope

1. Prepare a sanitized manual capture fixture with real answer metadata and no private data.
2. Run `capture-package` to generate manifest, report, and SQLite artifacts.
3. Load the package through the desktop import path.
4. Record extraction trust metrics before trusting the report.
5. Retest one query cluster and interpret the delta against the noise floor.

## Non-goals

- Do not add live provider automation.
- Do not generate final marketing content in core.
- Do not publish or distribute external artifacts from core.

## Done criteria

- A `docs/v11-real-case-smoke-report.md` exists.
- The smoke report links the sanitized input, package manifest summary, report summary, trust check, retest result, and limitations.
- CI remains green.
