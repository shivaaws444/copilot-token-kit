# Token efficiency tactics (what this kit does and why)
1. **Path-scoped instructions** (`.github/instructions/*.instructions.md` with `applyTo`) load only for matching files, so the global `copilot-instructions.md` stays tiny.
2. **Skills load on demand**: only name + description are always visible; bodies load when relevant. Keep descriptions specific so the wrong skill isn't pulled in.
3. **Model routing via agents**: quick (cheap) -> build -> plan/lead/architect (strongest, design only).
4. **Prompt files** pin context (`${file}`, `${selection}`) instead of free-typed pastes.
5. **Trim inputs locally** with `scripts/ctx.py` and `scripts/repo_map.py` (zero credits).
6. **Hunks-only output** and no recap rules cut output tokens, which are the most expensive.
7. **New chat per task/step**; history is re-sent every turn.
8. **Handoffs** (`handoffs:` in agents) move to a cheaper/fresher agent with a short pre-filled prompt instead of carrying a long chat.
9. **Tool scoping per agent**: fewer tools = smaller tool schema in every request (quick has 2 tools).
10. **Measure**: `python3 scripts/token_audit.py [-v]` prints always-on vs on-demand tokens; CI-friendly (exit 1 if always-on > 3000; target <1500 after trimming skill descriptions).
Measure real usage too: compare premium-request counts in GitHub Copilot usage for 2 weeks before/after.
