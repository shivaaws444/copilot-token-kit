---
description: Finish a big change - review, docs, PR, release check
agent: lead
---
Use the large-change skill, Phase 3.
Work log: ${input:log:docs/work/<slug>.md}
Branch diff: ${input:diff:python3 scripts/ctx.py diff origin/main}
Give: review verdict with blockers, docs to update, PR description (from the log), release-readiness verdict.
