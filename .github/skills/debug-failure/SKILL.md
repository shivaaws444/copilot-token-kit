---
name: debug-failure
description: Structured debugging for Java/Spring Boot failures - exceptions, failing builds, startup errors, wrong results, issues that work locally but not in ECS/staging. Use whenever the user pastes a stack trace, error, log excerpt, or says something is broken, failing, not starting, or behaving differently between environments.
---

# Debug Failure

Work in this order and keep each step short. Do not edit code until step 3.

## 1. Read the evidence (no file reads yet)
- Find the deepest "Caused by" and the first frame in the project's own package. That is the starting point.
- Classify: compile | startup/context (bean, config, profile) | runtime exception | wrong data | timeout/connectivity | test-only.
- If the input is a raw log > 100 lines, ask the user to run `python scripts/ctx.py trace < file` and stop.

## 2. Hypotheses (max 3)
List up to 3 likely causes, most likely first, each with the ONE check that confirms or rules it out.
Common Spring causes to consider: missing/duplicate bean, wrong active profile, property not bound,
`@Transactional` on private/self-invoked method, lazy-loading outside a transaction, Jackson mapping mismatch,
NLB/ALB health check path or port mismatch, IAM/secret not available in ECS task role.

## 3. Confirm, then fix
- Open only the files the top hypothesis needs.
- Apply the minimal fix. Explain root cause in 1-2 lines.
- Add or update a test that would have caught it.

## 4. Stop rule
If two fixes fail, stop. Report: what was ruled out, what remains, what info is needed (log line, config value, env var).
Environment-only issues: list exact config/env differences to check rather than guessing at code changes.
