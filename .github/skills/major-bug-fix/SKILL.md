---
name: major-bug-fix
description: Fix serious or complex bugs completely - production defects, data corruption, race conditions, intermittent failures, bugs spanning several services/modules - with reproduction, root cause, fix, regression tests, and a record. Use whenever a bug is high-impact, hard to reproduce, crosses modules, has already resisted a quick fix, or the user says big bug, critical bug, prod defect, or RCA.
---

# Major Bug Fix

Track it in `docs/work/bug-<slug>.md` (from the template) if it will take more than one chat.

## 1. Reproduce before fixing
- Write a failing test that reproduces the bug (unit if possible, slice/integration if needed). No repro = no fix; gather more evidence instead.
- Intermittent: look for shared mutable state, ordering assumptions, missing idempotency, retries, time zones, transaction isolation (CockroachDB 40001), caching.

## 2. Root cause
State it in 1-3 lines with evidence (log line, test, code path). Fix the cause, not the symptom. Ask: where else does this pattern exist? Search for siblings and list them.

## 3. Fix
- Minimal change that fixes the root cause, plus sibling occurrences (or log them as follow-ups).
- Data damage? Plan the data repair separately (script, dry-run first, reviewed) - never mixed into the code fix.
- Risky fix -> feature flag or staged rollout.

## 4. Prove it
The repro test now passes; the module's tests pass; add tests for the edge cases found during investigation.

## 5. Close the loop
Commit message `fix(<scope>): <root cause in plain words>`. For prod bugs: postmortem via incident-response skill; debt items into docs/tech-debt.md; release via /release-check.
