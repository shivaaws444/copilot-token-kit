<!-- Sent with EVERY chat request. Keep it short: every line here costs input tokens on every turn. -->
# Response rules
- Answer first. No preamble, no recap of the question, no closing summary.
- Code changes: show only changed hunks or the edited method, never whole files unless asked.
- Do not restate code I pasted. Reference it by file:line.
- No explanations unless asked; one line of "why" max for non-obvious changes.
- If a request is ambiguous, ask ONE question before doing heavy work.

# Context rules
- Read only files you need. Prefer search over opening whole directories.
- Never read: target/, build/, node_modules/, *.log, generated sources, lock files.
- Stop after 2 failed attempts at the same fix and report what you learned.

# Stack
Java 17+, Spring Boot multi-module (Maven), JUnit 5 + Mockito, AWS ECS Fargate, CockroachDB.
Follow existing patterns in the module you are editing.
