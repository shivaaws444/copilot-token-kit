---
name: lead-code-review
description: Review pull requests the way a senior tech lead does - prioritizing correctness, security, data integrity, operability, and team standards, with clear severity and teaching-quality comments. Use whenever the user asks to review a PR, diff, branch, or a teammate's code, or asks "is this good to merge".
---

# Lead Code Review

Input: compact diff (`python3 scripts/ctx.py diff origin/main`) + PR description. Open other files only to confirm a suspected issue.

## Review order (stop at first BLOCKER category and report)
1. **Correctness**: logic, null/empty, edge cases, concurrency, idempotency of retries/listeners.
2. **Security & data**: secrets in code/logs, PII/card/account data in logs, authz checks on every endpoint, input validation, SQL injection, unsafe deserialization.
3. **Data integrity**: transactions, migrations backward compatible, no remote calls inside transactions.
4. **Operability**: timeouts on outbound calls, error handling, useful logs/metrics, config not hard-coded.
5. **Tests**: new behavior tested; bug fixes have a regression test.
6. **Design & standards**: per docs/team-standards.md. Style nits last, and only if not auto-formatted.

## Comment format
`[BLOCKER|MAJOR|MINOR|NIT] file:line - problem - why it matters - suggested fix`
For juniors on MAJOR+, add one line of "why" that teaches the principle.

## Verdict
End with: **Approve** / **Approve with comments** / **Request changes**, plus the top 3 items to fix. Max 10 comments; group repeats.
Also call out one thing done well (keeps reviews constructive).
