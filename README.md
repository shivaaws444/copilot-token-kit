# Copilot Lead Suite

One package: token optimization + daily dev skills + prompts + repo map + tech lead kit + big-change workflow,
for Spring Boot / Java projects using GitHub Copilot only. **Read RULEBOOK.md first.**

## Install (from your project root)
```bash
unzip -n ~/Downloads/copilot-lead-suite.zip -d /tmp/suite
cp -Rn /tmp/suite/copilot-lead-suite/. .
chmod +x scripts/verify.sh scripts/*.py
```
`-n` never overwrites your existing files. If you already have `.github/copilot-instructions.md`, merge it by hand.

Then:
1. Edit the `model:` line in each `.github/agents/*.agent.md` to names from your Copilot model picker
   (quick = cheapest, build = Sonnet-class, plan/lead = strongest).
2. Set your base package for trace trimming: `export CTX_PKG=com.yourcompany` (add to ~/.zshrc).
3. Gradle instead of Maven? Replace `mvn` commands in skills/prompts and scripts/verify.sh.
4. Reload VS Code (Cmd+Shift+P -> Developer: Reload Window), open the repo ROOT folder.
5. Run once: `python3 scripts/repo_map.py`, `python3 scripts/health.py`, then `/architecture-summary` and `/debt-scan`.
6. Commit everything: `git add .github scripts docs *.md && git commit -m "Add Copilot lead suite" && git push`

## Contents
| Path | What |
|---|---|
| `.github/copilot-instructions.md` | short global rules, sent with every request |
| `.github/agents/` | `quick`, `build`, `plan`, `lead` - model routing by task size |
| `.github/skills/` (22) | token-budget, repo-map, spring-feature, junit-tests, debug-failure, cockroach-sql, pr-and-commit, jira-story-to-code, safe-refactor, large-change, major-bug-fix, adr-decision, lead-code-review, incident-response, release-readiness, tech-debt, dependency-upgrade, observability, api-contract, resilience-performance, team-comms, knowledge-docs |
| `.github/prompts/` (34) | slash commands - see the table in RULEBOOK.md |
| `scripts/` | ctx.py, repo_map.py, health.py, verify.sh - zero credits |
| `docs/` | templates: decisions (ADR), incidents, runbooks, work logs, tech-debt, team-standards |
| `RULEBOOK.md` | the rules and "which prompt" table - every day |
| `LEAD-PLAYBOOK.md` | first 30 days as owner, operating rhythm, credit budget |

## Verify it works
- New chat, ask "What's a DTO?" -> References shows copilot-instructions.md; answer is terse.
- Agent dropdown shows quick / build / plan / lead. Typing `/` lists the prompts.
- `scripts/verify.sh` prints `VERIFY: PASS` on a clean main.

If skills don't trigger: enable agent skills in VS Code settings (search "skills"), or name the skill in your message.
In IntelliJ only copilot-instructions.md is reliably supported; use VS Code for agents, skills, and prompts.
