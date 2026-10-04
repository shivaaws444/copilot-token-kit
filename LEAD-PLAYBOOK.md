# Lead Playbook - owning the service with GitHub Copilot only

The lead (Copilot `lead` agent) decides and directs; you execute and verify.
The repo is the lead's memory: if it isn't in `docs/`, it doesn't exist next chat.

## Agents
| Agent | Role | Typical use |
|---|---|---|
| `lead` | owner / tech lead (top model) | decisions, design review, release go/no-go, incidents, sprint plan |
| `build` | senior dev (mid model) | features, reviews, upgrades, perf, runbooks |
| `quick` | fast helper (cheap model) | status updates, commit/PR text, small edits, mentoring notes |

## First 30 days as owner
**Week 1 - know the system**
1. `python3 scripts/repo_map.py` then `/architecture-summary` -> review and commit docs/ARCHITECTURE.md
2. `/onboard` -> docs/ONBOARDING.md (proves you can explain the system end to end)
3. Adapt docs/team-standards.md with the team; commit it

**Week 2 - know the risks**
4. `python3 scripts/health.py` then `/debt-scan` -> docs/tech-debt.md
5. `/explain-flow` on the 3-5 most critical endpoints; `/perf-check` on any outbound call missing timeouts
6. List alerts that exist; `/runbook` for each top alert

**Week 3 - make it safe to change**
7. `/release-check` on the next release; adopt it as the release gate
8. Fix the top 2 security/compliance debt items; add tests to the top hot-spot classes

**Week 4 - make it move faster**
9. Record the 3 biggest standing decisions as ADRs with `/decide` (even past ones - "Accepted, retroactive")
10. `/sprint-plan` with 15-20% debt capacity; start weekly `/status-update`

## Operating rhythm
| When | Do | Prompt |
|---|---|---|
| Daily | review teammates' PRs within a day | `/lead-review` (+ `/mentor` for juniors) |
| Daily | implement with cheap-first routing | `/plan-story` -> `/new-endpoint`, `/write-tests` |
| Weekly (Fri) | status to manager | `/status-update` |
| Weekly | health scan, debt review | `health.py` + `/debt-scan` |
| Every release | go/no-go | `/release-check` |
| Every decision | record it | `/decide` |
| Incident | command it, then learn | `/incident` -> `/postmortem` |
| Sprint start | plan with capacity + debt | `/sprint-plan` |
| Monthly | dependencies and CVEs | `/upgrade-deps` |
| After structural change | refresh map | `repo_map.py` |

## Credit budget (example for 4000/month)
Rough split to protect: ~50% build work, ~20% reviews, ~15% lead decisions/design/incidents, ~15% reserve for incidents.
Lead agent is the most expensive: give it plans and docs, never bulk coding. Scripts (repo_map, health, ctx) cost zero.

## What makes you the go-to person
- Fast, high-quality reviews that teach (people come back to you)
- Decisions written down (ADRs) - nobody re-argues settled questions
- Calm incident command + blameless postmortems with real follow-through
- Up-to-date docs and runbooks - others can self-serve, which multiplies you
- Debt and risks raised early with options, not just problems
- Predictable releases: every prod deploy passes /release-check
