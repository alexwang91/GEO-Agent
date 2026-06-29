# Release Guards

A V10 release is allowed only when all guards below pass.

## Required checks

- CI verify workflow is green.
- All V10 milestones in `docs/progress.md` are marked DONE.
- Provider copy does not imply planned or manual-only providers are live.
- Manual-only engines remain explicit manual evidence paths.
- Reports keep per-engine results primary and label aggregates as directional.
- Skill packages preserve evidence IDs and return artifact references only.
- No credentials or secrets appear in docs, manifests, reports, logs, or databases.

## Release decision

If any guard fails, do not cut a release. Fix the failing guard in a separate PR and rerun CI.
