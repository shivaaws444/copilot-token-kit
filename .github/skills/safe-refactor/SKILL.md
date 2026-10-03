---
name: safe-refactor
description: Refactor Java/Spring Boot code without changing behavior - extract methods/classes, remove duplication, split large services, rename, upgrade deprecated APIs, modernize to Java 17+ features. Use whenever the user asks to refactor, clean up, simplify, reduce duplication, break up a large class, or fix code smells.
---

# Safe Refactor

## Rules
- Behavior must not change. If a behavior change is needed, stop and call it out separately.
- Tests first: confirm tests exist for the code being changed. If not, write characterization tests that pin current behavior, run them, then refactor.
- Small steps: one refactoring type per step (rename OR extract OR move), compile + test after each.
- Keep public API signatures unless the user approved changing them; check usages before any rename.

## Good targets
- Methods > 40 lines or > 3 levels of nesting -> extract methods with intention-revealing names.
- Services with > 7 dependencies -> split by responsibility.
- Duplicate mapping/validation -> one shared mapper/validator.
- Java 17+: records for DTOs, switch expressions, `Optional` returns instead of null, text blocks, pattern matching `instanceof`.
- Replace field injection with constructor injection.

## Output
For each step: what changed (1 line) + hunk. End with the test command and result.
Never output whole unchanged files.
