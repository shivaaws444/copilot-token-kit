---
name: release-readiness
description: Decide if a change or release is safe to deploy and produce the go/no-go checklist, rollout and rollback plan for Spring Boot services on AWS ECS. Use whenever the user is about to deploy, cut a release, merge to main, promote to production, or asks "is this ready to ship".
---

# Release Readiness

Input: diff or list of PRs since last release (`git log --oneline <last-tag>..HEAD`).

## Checklist (mark each PASS / FAIL / N/A with one-line evidence)
1. Build green, tests pass, no new skipped/@Disabled tests.
2. DB migrations: backward compatible with the currently running version (old code + new schema must work).
3. Config: new properties/env vars/secrets exist in every target environment.
4. API: no breaking change for consumers (see api-contract skill) or consumers are ready.
5. Dependencies: no new HIGH/CRITICAL vulnerabilities.
6. ECS: task definition (CPU/memory), health check path and grace period, desired count, target group still valid.
7. Observability: logs/metrics/alerts exist for the new behavior.
8. Feature flag or kill switch for risky changes.
9. Rollback plan: exact steps, and whether rollback is safe after migrations run.

## Verdict
**GO / GO with conditions / NO-GO**, with blockers listed. Then a rollout plan: order of services, canary or one-task-first, what to watch for 30 minutes, rollback trigger.
