# Handoff Decision

This file records the development-mode decision for autonomous runner work.

## Current Decision

```yaml
handoff:
  status: decided
  chosen_mode: current_agent_development
  decided_at: "2026-06-26"
  decided_by: current_user_override
  external_agent_prompt_generated: true
  prompt_file: docs/runner-prompt.md
  base_branch: main
  bootstrap_pr: null
  planning_branch: claude/geo-agent-dev-plan-5dpi2i
  planning_pr: 42
  planning_pr_merged: true
  completed_milestone: V7-03
  first_todo_after_v7_03_merge: V7-04
```

First TODO: `V7-04` after the V7-03 PR merges.

## Allowed Modes

- `current_agent_development`: the current agent may enter the Loop Workflow and implement the first TODO.
- `external_agent_development`: the current agent outputs a complete prompt for another agent and stops product implementation in this session.

## Decision Rationale

The active handoff remains current-agent development for the GitHub-only runner loop.

V7-03 installs the UX contract, personas, user journey, report copy guidelines, error-state taxonomy, and copy-contract test. After this PR merges, the next implementation milestone is V7-04.

## Handoff Rules

1. The active agent must use GitHub connector repository operations.
2. The active agent must read the required runner files before editing.
3. The active agent must select the first TODO from fresh `docs/progress.md`.
4. The active agent must create one branch and one PR for the selected milestone.
5. CI is VERIFY.
6. Product work must stop under `docs/stopper-policy.md`.
7. If a future user selects external-agent development again, update this file in a planning or harness PR before changing the product code path.
