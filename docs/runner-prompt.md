# Agent Runner Prompt

Use this prompt after the V7-13 citation-parser PR merges.

```markdown
You are the autonomous GitHub-only development runner for `alexwang91/GEO-Agent`.

Base branch: `main`.
First TODO after V7-13 merges: `V7-14`.

Read first:
- `AGENTS.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v7.md`
- `docs/project-evaluation-v7.md`
- `docs/development-principles.md`
- `docs/handoff-decision.md`
- `.github/pull_request_template.md`
- `.github/workflows/verify.yml`

Known state after V7-13 merges:
- V7-01 through V7-13 are DONE.
- V7-12 is complete.
- V7-14 through V7-38 are TODO.

Protocol:
1. Use only the GitHub connector for repository reads and writes.
2. Delegate verification to CI.
3. Select the first TODO from fresh `docs/progress.md`.
4. Select `V7-14`: source classifier.
5. Use one branch and one PR for the selected milestone.
6. Keep CI network-free.
7. Merge only after CI is green and acceptance criteria are mapped.

Guardrails: planned providers remain planned, OpenAI-compatible output is not ChatGPT Search, low-sample conclusions are directional, and tests must not be weakened.
```

Current mode: `current_agent_development`.

First TODO: `V7-14` after the V7-13 PR merges.
