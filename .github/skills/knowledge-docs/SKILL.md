---
name: knowledge-docs
description: Build and maintain the team's knowledge base in the repo - README, onboarding guide, runbooks, team standards, how-to guides - so the lead isn't a single point of failure. Use whenever the user asks to document something, write a runbook, onboard a new developer, explain the system to someone, or answer a question that will come up again.
---

# Knowledge Docs

## Where things live
- `README.md` - what the service does, how to run/test locally (copy-paste commands), links to docs.
- `docs/ARCHITECTURE.md` + `docs/repo-map.md` - system overview (see repo-map skill).
- `docs/runbooks/<alert-or-task>.md` - from `docs/runbooks/TEMPLATE.md`: symptom, impact, diagnosis steps, fix, escalation.
- `docs/team-standards.md` - definition of done, review rules, branching, conventions.
- `docs/decisions/` ADRs, `docs/incidents/` postmortems, `docs/tech-debt.md`.

## Rules
- Write for a new joiner on day 3: concrete commands, real class names, no assumed knowledge.
- Prefer updating an existing doc over creating a new one. Keep each doc < 200 lines.
- If a question was asked twice in chat, it becomes a doc.
- Docs change in the same PR as the code they describe.
