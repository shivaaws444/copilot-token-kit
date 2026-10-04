---
name: incident-response
description: Lead a production incident - triage severity, mitigate first, coordinate, write status updates, then a blameless postmortem in docs/incidents/. Use whenever the user reports production is down, errors spiking, latency, a failed deploy, data issue, alert firing, customer impact, or asks for a postmortem / RCA.
---

# Incident Response

## Phase 1 - Triage (first reply, <= 10 lines)
- Severity: SEV1 customer-facing outage/data risk | SEV2 degraded / partial | SEV3 internal or workaround exists.
- Blast radius: which endpoints, consumers, regions.
- **Mitigate before root-causing**: rollback the last deploy, scale ECS tasks, disable a feature flag, fail over, or shed load. Pick the fastest safe option and say it first.
- What changed? last deploy, config/secret rotation, dependency, traffic, upstream.

## Phase 2 - Investigate
Use the debug-failure skill. Ask for specific evidence (log query, metric, ECS task events, health check status) rather than guessing.

## Phase 3 - Communicate
Status update template every 30 min (SEV1) / 60 min (SEV2):
`[SEV#] <service> - Impact: ... | Status: investigating/mitigated/resolved | Next update: HH:MM | Actions: ...`

## Phase 4 - Postmortem (blameless)
Write `docs/incidents/YYYY-MM-DD-title.md` from `docs/incidents/TEMPLATE.md`:
timeline, impact, root cause (5 whys), what went well, what went poorly, action items with owner + due date.
Every action item must be one of: prevent, detect faster, mitigate faster. Add debt items to docs/tech-debt.md.
