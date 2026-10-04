---
description: Incident command - triage and mitigate now
agent: lead
---
Use the incident-response skill. Phase 1 now.
What we see: ${input:symptoms:errors, latency, alerts, which endpoints/consumers}
Started at / last change: ${input:changes:time, last deploy, config change, or unknown}
Evidence: ${input:evidence:trimmed logs or metrics (ctx.py trace)}
