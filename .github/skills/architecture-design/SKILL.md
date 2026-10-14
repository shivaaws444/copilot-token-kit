---
name: architecture-design
description: Produce or review a system/solution design (new service, integration, migration, event flow) with options, trade-offs, NFRs and ADR. Use for "design", "architecture", "how should we build", or HLD/LLD requests.
---
# Architecture Design
Output in this order, terse:
1. Problem + constraints (3-5 bullets) and NFRs: availability, latency, throughput, cost, compliance (PCI/PII).
2. Options table (2-3): pros, cons, cost, risk, reversibility.
3. Recommendation + why. Mermaid sequence or component diagram.
4. Failure modes: retries, idempotency, DLQ, timeouts, circuit breakers, data consistency.
5. Security: authN/Z (OAuth2/JWT), secrets, encryption, audit logging.
6. Observability: metrics, logs (Splunk), traces (Dynatrace), alerts.
7. Rollout + rollback; ADR draft in docs/decisions/.
