<!-- Sent with EVERY chat request. Keep it short: every line costs input tokens on every turn. -->
# Response rules
- Answer first. No preamble, no recap, no closing summary.
- Code changes: changed hunks or the edited method only, never whole files unless asked.
- Don't restate pasted code; reference file:line.
- One line of "why" max for non-obvious changes. Ask ONE question if the request is ambiguous.

# Context rules
- Read only what you need. Search by symbol; don't open whole directories.
- Never read: target/, build/, node_modules/, *.log, generated sources, lock files.
- For endpoints, flows, or impact: read docs/repo-map.md (and docs/ARCHITECTURE.md) first.
- For multi-step work: the work log in docs/work/ is the source of truth; do one step at a time.
- Stop after 2 failed attempts at the same fix and report what you learned.

# Stack & standards
Java 17+, Spring Boot multi-module (Maven), JUnit 5 + Mockito, AWS ECS Fargate, CockroachDB.
Follow existing patterns in the module and docs/team-standards.md. Verify with scripts/verify.sh <module> [TestClass].
Never put secrets, tokens, or PII in code or logs.
