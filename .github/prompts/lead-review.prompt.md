---
description: Senior-lead PR review with severity and verdict
agent: build
---
Use the lead-code-review skill (and api-contract if DTOs/messages changed).
PR purpose: ${input:purpose:one line or Jira key}
${input:diff:python3 scripts/ctx.py diff origin/main}
