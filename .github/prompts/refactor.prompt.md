---
description: Refactor selected code without changing behavior
agent: build
---
Use the safe-refactor skill.
Goal: ${input:goal:e.g. split this method, remove duplication, convert to records}
Code: ${selection} in ${file}
Check tests exist first; add characterization tests if missing. Small steps, hunks only.
