# Query Space V2

V7 query discovery uses a deterministic no-LLM fixture mode before any live generation path. The goal is to broaden query coverage without making unverified provider claims.

## Clusters

- `problem`: awareness questions about the user problem and category need.
- `solution`: consideration questions comparing approaches and vendors.
- `brand`: brand-validation questions for the target brand and alternatives.
- `source`: third-party source discovery questions about reviews, benchmarks, directories, and cited sources.
- `decision`: decision-support questions about shortlists, risks, and next actions.

## Perspectives

- `buyer`: economic buyer and budget owner.
- `operator`: daily user and workflow evaluator.
- `technical`: engineering, data, and security evaluator.
- `pr`: communications and brand owner.

## Fixture mode

`discover_queries_no_llm()` emits one query for every cluster and perspective pair. It attaches:

- a `QueryRecord` compatible with the existing audit runner;
- `cluster_id`;
- `perspective_id`;
- seed source IDs;
- deterministic priority.

This is not a live LLM generation path. Later V7 slices may add ranking, dedupe, and provider-backed generation, but CI remains network-free.
