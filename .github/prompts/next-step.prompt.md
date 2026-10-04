---
description: Execute the next unchecked step of a work log (one step per chat)
agent: build
---
Use the large-change skill, Phase 2.
Work log: ${input:log:docs/work/<slug>.md}
Do only the next unchecked step, verify it with scripts/verify.sh, update the log, and give me the commit command.
