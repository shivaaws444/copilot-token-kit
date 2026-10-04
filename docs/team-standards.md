# Team Standards

## Definition of Done
- Code reviewed and approved by 1 engineer (2 for security/DB/API-contract changes)
- Unit tests for new behavior; regression test for every bug fix
- No new HIGH/CRITICAL vulnerabilities; no secrets or PII in code or logs
- Logs/metrics for new flows; runbook for new alerts
- Docs updated in the same PR (README, ARCHITECTURE, ADR if a decision was made)
- Backward-compatible DB migrations and API changes, or a documented migration plan

## Pull requests
- Small (< 400 changed lines ideally), one purpose, Jira key in title
- Description: What / Why / How to test / Risk
- Review within 1 working day; author resolves or replies to every comment

## Code
- Constructor injection; DTOs as records; no entities in APIs
- `@Transactional` in services only; no remote calls inside transactions
- Every outbound call has timeouts; retries only for idempotent operations
- Conventional Commits

## Branching & release
- Short-lived feature branches off main; rebase before merge
- Release via tag; release checklist (/release-check) for production
