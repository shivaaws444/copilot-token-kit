---
description: Diagnose an error from a trimmed trace
agent: build
---
Use the debug-failure skill.
Where it fails: ${input:where:local / test / ECS dev / staging}
What changed recently: ${input:changed:last commit, config, dependency, or "unknown"}
Trimmed trace (python3 scripts/ctx.py trace < err.txt):
${input:trace}
Give hypotheses first. Do not edit until the top hypothesis is confirmed.
