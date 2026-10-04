---
name: resilience-performance
description: Make Spring Boot services fast and resilient - timeouts, retries, circuit breakers, bulkheads, connection pools, thread pools, caching, JVM/container sizing on ECS Fargate, and latency investigations. Use whenever the user reports slowness, timeouts, 502/503/504s, connection pool exhaustion, high CPU/memory, OOM, or adds an outbound call.
---

# Resilience & Performance

## Every outbound call must have
Connect + read timeout (explicit, shorter than the caller's timeout), bounded retries with backoff + jitter only for idempotent operations, a circuit breaker for critical dependencies, and a fallback or clear error.
Timeout budget: client timeout > LB idle timeout? No - LB idle timeout > service total time > downstream timeouts.

## Pools
- HikariCP: size to (DB capacity / instances), not "bigger is better"; set connection timeout; watch pending threads.
- HTTP client pools sized for expected concurrency; reuse clients (one WebClient/RestClient bean).

## Investigate slowness (evidence first)
1. Where is time spent: app vs DB vs downstream (metrics/traces/logs with timings).
2. DB: slow queries, missing index, N+1, lock contention / retries.
3. JVM: GC pauses, heap vs container memory (`-XX:MaxRAMPercentage=75`), CPU throttling on Fargate.
4. Only then change code or config, one change at a time, measure before/after.

## Output
Findings ranked by impact, exact config/code changes, and how to verify (metric to watch).
