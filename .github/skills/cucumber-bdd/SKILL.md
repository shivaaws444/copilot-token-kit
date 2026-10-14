---
name: cucumber-bdd
description: Write Cucumber BDD feature files and step definitions from acceptance criteria or Jira stories. Use for Gherkin, .feature, acceptance test, or BDD requests.
---
# Cucumber BDD
1. Map each acceptance criterion -> one Scenario (Given/When/Then, business language).
2. Search existing steps first (`grep -r "@Given\|@When\|@Then"`); reuse wording exactly.
3. New steps thin: delegate to helpers/clients; no assertions in Given/When.
4. Scenario Outline + Examples for data variants; tag `@smoke`/`@regression` per team standard.
Done when the feature runs green: `mvn -q -pl <module> test -Dcucumber.filter.tags=<tag>`.
