---
description: Plan a dependency / Spring Boot / CVE upgrade
agent: build
---
Use the dependency-upgrade skill.
Target: ${input:target:e.g. Spring Boot 3.3 -> 3.4, or CVE-XXXX in library Y}
Plan first (breaking changes that touch our code, PR sequence), wait for my OK, then implement step 1 only.
