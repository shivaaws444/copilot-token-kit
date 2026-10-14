# AGENTS.md
Cross-tool entry point (Copilot coding agent, Claude Code, Cursor, Codex). Keep under 40 lines.
- Rules: `.github/copilot-instructions.md` (global) + `.github/instructions/*.instructions.md` (path-scoped).
- Domain + lessons: `docs/knowledge/` — read only the file relevant to the task.
- Build/verify: `scripts/verify.sh <module> [TestClass]` (Maven). Frontend: `npm test -- <file>`. Python: `pytest -q`.
- Map before exploring: `docs/repo-map.md` (`python3 scripts/repo_map.py`).
- Never commit secrets/PII; never run terraform apply / kubectl delete; never push to main.
- Output: hunks only, no recap.
