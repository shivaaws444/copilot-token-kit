---
name: large-change
description: Deliver big code changes end to end - multi-file features, cross-module refactors, migrations, framework upgrades, rewrites - safely and without losing track across chats. Uses a work log in docs/work/ as persistent state and executes in small verified steps with a git commit after each. Use whenever a task touches more than ~3 files or 1 module, will take more than one chat, or the user says big change, epic, rewrite, migration, or "do the whole thing".
---

# Large Change

Copilot forgets between chats. The work log is the memory. Small green steps are the safety net.

## Phase 1 - Plan (lead agent, once)
1. Read docs/repo-map.md (+ ARCHITECTURE.md). Use impact analysis: entry points, classes, tables, contracts, tests.
2. Create `docs/work/<task-slug>.md` from `docs/work/TEMPLATE.md`:
   goal, acceptance criteria, out of scope, risks, and a numbered step list.
3. Step rules: each step compiles and passes tests on its own, touches <= ~5 files, is S or M size, has its verify command.
   Order: tests/characterization first -> new code behind existing behavior (or feature flag) -> switch over -> remove old code.
4. Ask the user to create the branch: `git checkout -b feature/<task-slug>`.

## Phase 2 - Execute (build agent, ONE step per chat)
1. Read the work log. Do only the next unchecked step. Do not re-plan or re-investigate settled items.
2. Edit, then run that step's verify command (`scripts/verify.sh <module> [TestClass]`).
3. Green -> tick the step, add 1-2 lines to the log (what changed, any surprise), tell the user to commit:
   `git add -A && git commit -m "<type>(<scope>): step N - <summary>"`
4. Red twice -> stop, record the blocker in the log, recommend the lead agent re-plan that step.
5. If reality differs from the plan, update the plan in the log before continuing.

## Phase 3 - Finish
Full module tests, `/lead-review` on the whole branch diff, `/release-check`, update docs (ARCHITECTURE, repo-map, ADR if a decision was made), PR description from the log.

## Never
- Do several steps in one chat "to save time" (context grows, quality drops, credits climb).
- Leave the build red between steps.
- Mix refactoring and behavior change in one step.
