---
description: Write unit tests for the selected class or method
agent: build
---
Use the junit-tests skill.
Write tests for: ${selection}
File: ${file}
Cover: happy path, each guard/validation branch, dependency exceptions, null/empty boundaries.
Use the smallest test type. Run only the new test class and report the result.
