---
description: Update the tech debt register from health.py output
agent: lead
---
Use the tech-debt skill. Update docs/tech-debt.md (create it if missing) and recommend this sprint's picks.
Sprint capacity for debt: ${input:capacity:e.g. 6 story points or 2 dev-days}
${input:health:python3 scripts/health.py}
