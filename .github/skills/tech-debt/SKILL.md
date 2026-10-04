---
name: tech-debt
description: Find, score, and maintain the tech debt register in docs/tech-debt.md, and decide what to pay down each sprint. Use whenever the user mentions tech debt, code health, refactoring priorities, legacy code, "what should we fix", sprint capacity for maintenance, or after an incident action item.
---

# Tech Debt

## Find (cheap first)
Run `python3 scripts/health.py` and use its output; do not scan the repo manually.
Add items from incidents, reviews, and recurring bugs.

## Score each item
- Impact 1-5 (incident risk, dev slowdown, security/compliance exposure)
- Effort 1-5
- Priority = Impact x 2 - Effort. Security/compliance items with impact >= 4 jump the queue.

## Register format (docs/tech-debt.md table)
`| ID | Item | Area | Impact | Effort | Priority | Owner | Status | Link |`
Keep it < 30 open items; merge duplicates, close stale ones.

## Decide
Recommend a fixed ~15-20% of sprint capacity for debt. Each sprint pick the top items that fit, favoring ones that unblock upcoming features. Output: chosen items + one-line justification each.
