---
description: Go/no-go release checklist with rollout + rollback plan
agent: lead
---
Use the release-readiness skill.
Release: ${input:release:version/tag and target environment}
Changes: ${input:changes:git log --oneline <last-tag>..HEAD}
Migrations/config changes known: ${input:extra:or "none known"}
