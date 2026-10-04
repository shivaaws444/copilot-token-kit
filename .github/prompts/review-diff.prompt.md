---
description: Review only the current diff, not the whole repo
agent: build
---
Review ONLY this diff. Do not open other files unless a change clearly depends on them.
Report up to 7 findings, highest severity first, each as: file:line - issue - fix (one line).
Focus: correctness, null handling, transactions, security, missing tests. Skip style nits.

${input:diff:Paste output of: python3 scripts/ctx.py diff}
