---
name: token-budget
description: Spend the fewest AI credits for the best result. Use this skill at the start of ANY non-trivial coding task (features, bug fixes, refactors, test failures, reviews, explanations of large code) to pick the right model tier, scope context tightly, and avoid wasted agent loops. Use it even if the user does not mention cost or tokens.
---

# Token Budget

Copilot bills by tokens (input + output + cached). Cost = model price x tokens.
The two levers are: **which model** and **how much context**. Context is usually the bigger one.

## Step 1 - Classify the task (do this silently, first)

| Tier | Task looks like | Use |
|---|---|---|
| S - small | rename, add a field, write a DTO, explain one method, regex, one unit test, fix a compile error | cheapest available model (`quick` agent) |
| M - medium | implement a well-defined feature in 1-3 files, fix a failing test with a clear trace, add tests for one class | mid-tier model (`build` agent) |
| L - large | design across modules, unclear root cause, concurrency/transaction bugs, security-sensitive auth (ADFS/OAuth), performance | top model, PLAN ONLY (`plan` agent), then hand off to `build` |

If the user is on a top-tier model for an S task, say so in one line and continue.

## Step 2 - Scope context before reading anything
1. Name the specific files/classes needed. Search by symbol name; do not list or open whole folders.
2. Read the method or class, not the file, when the file is > 300 lines.
3. For failures, use trimmed output from `scripts/ctx.py` instead of raw Maven logs.
4. Never pull in: `target/`, generated code, `*.log`, every module's `pom.xml`, lock files.

## Step 3 - Execute cheaply
- Plan in <= 8 bullets before editing anything in tier M/L.
- Make the smallest edit that solves the problem. Output diffs/hunks only.
- Run the narrowest verification: `mvn -q -pl <module> -Dtest=<TestClass> test`, not the full build.
- If the same fix fails twice: STOP. Summarize findings in <= 5 lines and suggest escalating tier. Do not loop.

## Step 4 - Hand-off (L tier)
`plan` outputs a numbered plan with exact file paths and method signatures.
The user then runs `build` with that plan, so the expensive model never writes bulk code.

## Anti-patterns that burn credits
- Long chat threads: history is re-sent each turn. Start a new chat per task.
- Pasting entire stack traces or logs. Trim to project frames + "Caused by" lines.
- Asking the agent to "look around the codebase".
- Regenerating whole files to change 3 lines.
- Using agent mode for questions ask mode can answer.
