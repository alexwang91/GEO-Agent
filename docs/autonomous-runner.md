# Autonomous Runner Protocol

Goal: move each `docs/progress.md` row to DONE through one CI-verified PR into `main`.

## Soft Check

Quietly probe GitHub connector, CI, and optional local access. In GitHub-only mode, verification is CI.

## Autonomous Loop

1. Fetch progress, feedback log, loop trace, loop hypotheses, and stopper policy.
2. Decide whether review, harness repair, or hypothesis validation is due.
3. Select the first TODO row. Skip DONE, BLOCKED, DEFERRED, and CANCELLED.
4. Append trace events for selected_milestone, branch_created, pr_opened, ci_observed, feedback_classified, merge_attempted, progress_updated, review_run, harness_repair_run, hypothesis_updated, and stop.
5. Plan and implement the smallest vertical slice.
6. Use CI as VERIFY. Do not weaken tests or assertions.
7. Merge only after CI, progress, feedback, trace, and hypothesis evidence are complete.
8. Re-fetch progress before choosing the next milestone.

## Repository Mode

This repository is bootstrapped for GitHub-only milestone execution. Use GitHub branches, PRs, and CI as the verification channel.
