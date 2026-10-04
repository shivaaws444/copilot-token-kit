---
name: observability
description: Add or review logging, metrics, tracing, health checks, and alerts for Spring Boot services so issues are detectable and debuggable in production. Use whenever the user adds a feature that needs monitoring, asks about logs, metrics, Micrometer, Actuator, health checks, dashboards, alerts, correlation IDs, or "how would we know if this breaks".
---

# Observability

## Logging
- Structured logs (JSON) with correlation/trace ID on every line (MDC); propagate it on outbound calls and messages.
- Levels: ERROR = needs action, WARN = degraded but handled, INFO = business events (one per request max), DEBUG = details.
- Never log secrets, tokens, full card/account numbers, or PII. Mask identifiers.
- Log exceptions once, at the boundary that handles them, with context (ids, operation), not at every layer.

## Metrics (Micrometer)
For each new flow: request count, error count by type, latency (timer with percentiles), and outbound dependency latency/errors. Use low-cardinality tags (no ids in tags).

## Health
Actuator liveness vs readiness kept separate; readiness checks only dependencies needed to serve traffic. Health path and port must match the load balancer target group health check.

## Alerts
Alert on symptoms (error rate, latency SLO, consumer lag), not causes. Each alert links to a runbook in docs/runbooks/.

## Output
List of exact log lines/metrics/alerts to add, with code hunks.
