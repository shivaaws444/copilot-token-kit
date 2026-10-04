---
description: PR description from diff
agent: quick
---
Use the pr-and-commit skill. Write the PR description (What / Why / How to test / Risk).
Jira: ${input:jira:ticket key or none}
${input:diff:python3 scripts/ctx.py diff origin/main}
