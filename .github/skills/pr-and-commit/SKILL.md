---
name: pr-and-commit
description: Write commit messages and pull request descriptions from a diff, cheaply. Use whenever the user asks for a commit message, PR title, PR description, changelog entry, or release notes, or says "summarize my changes".
---

# PR and Commit

Input should be a compact diff (`python scripts/ctx.py diff origin/main`). Do not open other files.

## Commit message
Conventional Commits: `type(scope): imperative summary` (<= 72 chars).
Types: feat, fix, refactor, test, docs, chore, perf, build, ci. Scope = module name.
Body only if the "why" is not obvious: 1-3 lines. Add the Jira key if the branch name contains one.

## PR description
```
## What
<2-4 bullets of behavior change, not file lists>

## Why
<1-2 lines; link Jira key>

## How to test
<exact commands or curl / steps>

## Risk
<low|medium|high> - <what could break, migrations, config/env changes needed>
```
Flag in Risk: DB migrations, new env vars/secrets, changed API contracts, removed endpoints, dependency bumps.
No marketing language. No restating the diff line by line.
