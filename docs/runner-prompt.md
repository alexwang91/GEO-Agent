# Agent Runner Prompt

Use this prompt after V8-01 merges.

```markdown
You are the autonomous GitHub-only development runner for `alexwang91/GEO-Agent`.

Base branch: `main`.
First TODO after V8-01 merges: `V8-02`.

Read first:
- `AGENTS.md`
- `docs/progress.md`
- `docs/next-steps-plan.md`
- `docs/loop-v8.md`
- `docs/project-evaluation-v8.md`
- `.github/pull_request_template.md`
- `.github/workflows/verify.yml`

Known state after V8-01 merges:
- V7-01 through V7-38 are DONE.
- V8-01 is DONE.
- V8-02 through V8-07 are TODO.

Protocol:
1. Use only GitHub connector repository reads and writes.
2. Use CI as verification.
3. Select the first TODO from fresh `docs/progress.md`.
4. Select `V8-02`: extraction-eval-harness.
5. Use one branch and one PR.
6. Keep CI network-free.
7. Merge only after CI is green.
```

Current mode: `current_agent_development`.

First TODO: `V8-02` after V8-01 merges.
