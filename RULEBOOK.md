# Rule Book - every task, every day

## The 10 rules
1. **New chat per task (per step for big work).** History is re-billed every turn.
2. **Pick the agent by size:** `quick` = small, `build` = normal, `plan`/`lead` = hard or decisions. Top models plan; they don't type bulk code.
3. **Use a slash prompt before free-typing.** If none fits, use: Goal / Scope / Constraints / Done when / Output.
4. **Trim before you paste:** traces -> `ctx.py trace`, diffs -> `ctx.py diff`, one method -> `ctx.py file`. Never paste raw logs.
5. **Map before you explore:** questions about flows go through `docs/repo-map.md`, never "scan the repo".
6. **Big work = work log + one step per chat + commit when green.** Never leave the build red.
7. **Bugs: failing test first,** then root cause, then fix.
8. **Two strikes:** same fix fails twice -> stop, `/replan` or escalate to `plan`/`lead`.
9. **If it's not in docs/, it doesn't exist:** decisions -> ADR, incidents -> postmortem, risks -> tech-debt, repeat questions -> doc.
10. **You own git and production.** Copilot proposes; you review the diff, run verify, commit, and deploy.

## Every task - 60-second checklist
- [ ] New chat? Right agent selected?
- [ ] Size: S (quick) / M (build) / L (big change or plan/lead)?
- [ ] Scope named (module, class, method)?
- [ ] Context trimmed with ctx.py?
- [ ] Output asked as hunks / plan / message only?
- [ ] Verify: `scripts/verify.sh <module> [TestClass]` = PASS?
- [ ] Commit, and docs updated if behavior or decisions changed?

## Which prompt?
| Situation | Prompt | Agent |
|---|---|---|
| Understand an endpoint/flow | `/explain-flow` | build |
| What will this change break? | `/impact-analysis` | build |
| Explain selected code | `/explain` | quick |
| Jira story -> plan | `/plan-story` | plan |
| New endpoint | `/new-endpoint` | build |
| Write tests | `/write-tests` | build |
| Failing test | `/fix-test` | build |
| Error / stack trace | `/debug` | build |
| Serious / complex bug | `/big-fix` | build |
| Big feature / refactor / migration | `/big-change` -> `/next-step` x N -> `/finish-change` | lead / build |
| Came back to a big change | `/resume` | quick |
| Step failing twice | `/replan` | lead |
| Refactor | `/refactor` | build |
| SQL / entity / migration | `/sql-review` | build |
| Slow / timeouts / outbound call | `/perf-check` | build |
| Dependency / CVE / Boot upgrade | `/upgrade-deps` | build |
| Technical decision | `/decide` | lead |
| Review a design | `/design-review` | lead |
| Review a PR | `/lead-review` (+ `/mentor`) | build |
| Quick review of my diff | `/review-diff` | build |
| Commit message / PR text | `/commit-msg`, `/pr-desc` | quick |
| Ready to deploy? | `/release-check` | lead |
| Production incident | `/incident` -> `/postmortem` | lead |
| Tech debt | `health.py` -> `/debt-scan` | lead |
| Sprint planning | `/sprint-plan` | lead |
| Weekly update | `/status-update` | quick |
| Runbook / onboarding | `/runbook`, `/onboard` | build |
| Refresh architecture doc | `repo_map.py` -> `/architecture-summary` | plan |

## Rhythm
- **Daily:** review PRs within a day; build with cheapest-fit agent; one step per chat.
- **Weekly:** `health.py` + `/debt-scan`; Friday `/status-update`.
- **Per release:** `/release-check`. **Per decision:** `/decide`. **Per incident:** `/postmortem`.
- **Monthly:** `/upgrade-deps`; check credit usage in GitHub billing.
- **After structural changes:** `python3 scripts/repo_map.py`.

## Zero-credit scripts (use them first)
| Script | Does |
|---|---|
| `python3 scripts/ctx.py trace < err.txt` | trims stack traces / Maven output |
| `python3 scripts/ctx.py diff origin/main` | compact diff |
| `python3 scripts/ctx.py file Path.java method` | extracts one method |
| `python3 scripts/repo_map.py` | docs/repo-map.md: endpoints, flows, DB, integrations |
| `python3 scripts/health.py` | code health and debt signals |
| `scripts/verify.sh <module> [TestClass]` | build + test, trimmed PASS/FAIL |

## Never
- Paste secrets, tokens, customer data, or production data into chat.
- Ask the agent to "look around the codebase".
- Let an agent loop on the same error.
- Merge without a green verify and a reviewed diff.
- Use the top model for DTOs, commit messages, or status updates.
