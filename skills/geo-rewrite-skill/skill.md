# GEO Rewrite Skill

This skill consumes an evidence-backed optimization execution brief from GEO-Agent.

## Contract

- Input must include `task_id`, `method`, `target_page`, `query_cluster`, `evidence_ids`, `expected_metric`, and `risk`.
- Output must include an external `artifact_ref`, preserved `evidence_ids`, and any warnings.
- The skill is an external executor. GEO-Agent core remains a measurement and planning workbench.
- The skill must not drop evidence IDs or claim unmeasured impact.
- Retesting must happen through GEO-Agent measurement paths after the external artifact exists.

## Non-goals

- Do not run live AI engines from this skill package.
- Do not store credentials.
- Do not treat generated copy as measured improvement without retest evidence.
