---
description: Sprint plan with capacity, debt, and risks
agent: lead
---
Use the team-comms (sprint plan) and tech-debt skills.
Team and capacity: ${input:capacity:people, days, leave, on-call}
Candidate stories: ${input:stories:keys + titles + rough size}
Top debt items: read docs/tech-debt.md.
Output: sprint goal, committed vs stretch, owners, risks, what we are explicitly NOT doing.
