---
name: adr-decision
description: Make and record technical decisions as a tech lead - choosing libraries, patterns, architecture, data models, build vs buy, trade-offs, "should we do X or Y". Produces an Architecture Decision Record in docs/decisions/. Use whenever the user faces a technical choice, asks for a recommendation between options, or a design debate needs closing.
---

# Decision (ADR)

A lead's job is to make reversible decisions fast and irreversible ones carefully.

## 1. Frame (3 lines max)
- Decision needed, by when, and who is affected.
- Classify: **two-way door** (easy to reverse -> decide now, note it) or **one-way door** (data model, public API, security, vendor lock-in -> full ADR).

## 2. Options (2-4, always include "do nothing")
For each: how it works (1 line), effort (S/M/L), risk, operational cost (on-call, infra, licensing), team skill fit, reversibility.

## 3. Decide
- Criteria, ranked (e.g. correctness > security > operability > delivery speed > elegance).
- **Recommend one option and say why.** No fence-sitting. State what evidence would change the decision.
- Check against existing ADRs in docs/decisions/ - do not silently contradict one; supersede it explicitly.

## 4. Record
Write `docs/decisions/NNNN-kebab-title.md` (next number) using `docs/decisions/0000-template.md`.
Status: Proposed until the user confirms, then Accepted.

## Output
The ADR file + a 3-line summary the user can paste into Slack/Teams.
