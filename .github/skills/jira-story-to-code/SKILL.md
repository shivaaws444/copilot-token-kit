---
name: jira-story-to-code
description: Turn a Jira story or ticket (pasted text or fetched via Jira MCP) into a concrete implementation plan, acceptance tests, and task breakdown before coding. Use whenever the user shares a Jira story, ticket, acceptance criteria, or requirements and wants to start implementing, estimate, or break it down.
---

# Jira Story to Code

## 1. Extract (output this first, short)
- Goal in one sentence.
- Acceptance criteria as numbered, testable statements (Given/When/Then).
- Open questions / ambiguities - max 5. If any block implementation, ask before planning.

## 2. Map to the codebase
- Search for the existing classes/endpoints this touches. List them with paths.
- Identify: API changes, DB/schema changes, config/env changes, external calls.

## 3. Plan
Numbered steps, each a small, independently testable change, with file paths.
Mark each step S/M/L (see token-budget skill) so cheap models handle the small ones.

## 4. Tests first
For each acceptance criterion, name the test class and test method that will prove it.

Do not write implementation code in this skill. Hand off: "Implement step 1 with build agent."
