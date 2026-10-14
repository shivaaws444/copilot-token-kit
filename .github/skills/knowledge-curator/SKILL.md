---
name: knowledge-curator
description: Promote mature lessons from docs/knowledge/lessons-learned.md into instruction files or skills and prune the inbox. Use for "curate knowledge", "merge lessons", or monthly knowledge review.
---
# Knowledge Curator
1. Group lessons by area. A lesson is mature if seen 2+ times or caused an incident.
2. Promote: path-specific rule -> matching `.github/instructions/*.instructions.md`; workflow -> relevant skill "Must-haves"; global (rare) -> copilot-instructions.md.
3. Write the rule as one imperative line; drop the lesson from the inbox.
4. Never grow copilot-instructions.md beyond ~25 lines; run `python3 scripts/token_audit.py` and report before/after.
Output: table (lesson -> destination) + the diff.
