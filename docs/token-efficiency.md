# Token efficiency tactics (what this kit does and why)
1. **Path-scoped instructions** (`.github/instructions/*.instructions.md` with `applyTo`) load only for matching files, so the global `copilot-instructions.md` stays tiny.
2. **Skills load on demand**: only name + description are always visible; bodies load when relevant. Keep descriptions specific so the wrong skill isn't pulled in.
3. **Model routing via agents**: quick (cheap) -> build -> plan/lead/architect (strongest, design only).
4. **Prompt files** pin context (`${file}`, `${selection}`) instead of free-typed pastes.
5. **Trim inputs locally** with `scripts/ctx.py` and `scripts/repo_map.py` (zero credits).
6. **Hunks-only output** and no recap rules cut output tokens, which are the most expensive.
7. **New chat per task/step**; history is re-sent every turn.
