# Copilot Token Kit

Get the best answer for the fewest GitHub AI Credits.
Copilot now bills by tokens, so cost = model price x (input + output tokens).
This kit attacks both: right model per task, and minimal context per request.

## Install (per repo)
Copy `.github/` and `scripts/` into your repo root and commit. VS Code + Copilot picks them up automatically.

| File | What it does |
|---|---|
| `.github/copilot-instructions.md` | Short global rules: terse output, diffs only, no repo crawling. Sent on every request, so it is kept tiny. |
| `.github/skills/token-budget/SKILL.md` | Agent skill: classify task S/M/L, scope context, stop loops after 2 failures. |
| `.github/agents/quick.agent.md` | Cheapest model for small edits. |
| `.github/agents/build.agent.md` | Mid-tier model for implementation. |
| `.github/agents/plan.agent.md` | Top model, plans only (never writes bulk code). |
| `.github/prompts/*.prompt.md` | `/fix-test` and `/review-diff` slash commands wired to trimmed input. |
| `scripts/ctx.py` | Trims stack traces, diffs, and files before you paste them. |

## Set the models to what YOUR org allows
Open the model picker in Copilot Chat and copy the exact names into the `model:` line of each agent file.
Rule of thumb: `quick` = cheapest "mini/Haiku/Flash" model, `build` = a Sonnet-class model,
`plan` = the strongest model you have (Opus-class or top GPT). If unsure, use **Auto** for `build`.

## Daily workflow
1. **New chat per task.** Old history is re-sent and billed every turn.
2. Small thing -> pick `quick`. Normal feature -> `build`. Hard bug/design -> `plan`, then paste its plan into `build`.
3. Test failing? `mvn ... > failure.txt; python scripts/ctx.py trace < failure.txt` then `/fix-test`.
4. Before PR: `python scripts/ctx.py diff origin/main` then `/review-diff`.
5. Need one method explained? `python scripts/ctx.py file src/.../CardService.java activate` instead of attaching the file.
6. Inline code completions don't use credits; use them for boilerplate instead of chat.

Set `CTX_PKG=com.yourcompany` so `ctx.py trace` keeps only your own stack frames.

## Track it
Check usage in GitHub Settings -> Billing / Copilot usage weekly. If one week is high, look for long agent runs on the top model.
