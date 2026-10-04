---
description: Fix a failing test using trimmed context
agent: build
---
Fix the failing test below. Use the token-budget skill.
Only open the test class and the class under test unless the trace points elsewhere.
Verify with: mvn -q -pl ${input:module} -Dtest=${input:testClass} test

Trimmed failure output:
${input:failure:Paste output of: python3 scripts/ctx.py trace < failure.txt}
