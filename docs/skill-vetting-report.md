# Skill Vetting Report

Skill: github-loop-runner
Source: GitHub
Author: alexwang91
Version: not declared

## Metrics

- Stars: 0
- Forks: 0
- Last updated: 2026-06-24T13:35:47Z
- Files reviewed: 16

## Red Flags

None found in the reviewed files.

## Permissions Needed

- Files: installs `skills/github-loop-runner` into the local Codex skills directory.
- Network: GitHub repository download during installation; declared GitHub MCP endpoint in `agents/openai.yaml`.
- Commands: Python validation script and skill installation script.

## Risk Level

Medium.

Reason: the skill is a new, low-star GitHub repository and depends on a GitHub connector workflow, but reviewed contents are mainly Markdown process files and a local validation script. No credential scraping, browser cookie access, obfuscation, arbitrary eval/exec, destructive system modification, or unknown data exfiltration was found.

## Verdict

Install with caution.

The skill was installed locally at `C:\Users\w00445459\.codex\skills\github-loop-runner`. Restart Codex to pick up the new skill automatically.
