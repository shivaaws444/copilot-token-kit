---
name: dependency-upgrade
description: Plan and execute safe dependency upgrades - Spring Boot / Spring Cloud version bumps, Java version, library CVE fixes, Maven dependency conflicts. Use whenever the user mentions a vulnerability/CVE, outdated dependencies, upgrading Spring Boot or Java, dependency conflicts, or security scan findings.
---

# Dependency Upgrade

## Triage
- CVE: is the vulnerable code path actually used? Severity + exploitability decide urgency (CRITICAL reachable = this sprint, others = planned).
- Prefer upgrading the BOM/parent (spring-boot-starter-parent, spring-cloud-dependencies) over pinning individual transitive versions.

## Plan
1. Read release notes / migration guide for each major/minor jump; list breaking changes that touch this codebase (search for the affected APIs).
2. One upgrade per PR. Major versions step-by-step (e.g. Boot 3.2 -> 3.3 -> 3.4), not leaps.
3. Use `mvn -q dependency:tree -Dincludes=<group>` to locate a transitive source, not the full tree.

## Execute & verify
- Fix compile errors, deprecations that become removals, and property renames (spring-boot-properties-migrator helps for Boot upgrades; remove it afterwards).
- Run full module tests + a local startup smoke test.
- Record notable upgrades as a short ADR if they change behavior or defaults.
