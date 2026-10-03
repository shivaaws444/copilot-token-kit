---
name: junit-tests
description: Write or fix JUnit 5 + Mockito tests for Spring Boot code with high signal and low noise. Use whenever the user asks for unit tests, test coverage, a test for a bug, to fix a failing or flaky test, or mentions JUnit, Mockito, @WebMvcTest, @DataJpaTest, or @SpringBootTest.
---

# JUnit Tests

## Pick the smallest test type that proves the behavior
| Testing | Use | Avoid |
|---|---|---|
| Service/business logic | plain JUnit + `@ExtendWith(MockitoExtension.class)` | `@SpringBootTest` |
| Controller mapping/validation/status codes | `@WebMvcTest(XController.class)` + `@MockitoBean` | full context |
| Repository queries | `@DataJpaTest` (or the module's existing DB test setup) | mocking the repository |
| Cross-module wiring | `@SpringBootTest` only if explicitly needed | |

## Style
- Name: `methodName_condition_expectedResult` (or follow the class's existing convention).
- Structure each test as given / when / then with blank lines between.
- One behavior per test. Use `@ParameterizedTest` for input variations instead of copy-pasted tests.
- AssertJ (`assertThat`) if the project has it; otherwise JUnit assertions. Match what exists.
- Verify interactions only when the interaction IS the behavior (e.g. "publishes event", "does not call repo").
- No `Thread.sleep`; use Awaitility if the project has it.

## Cover, in order
1. Happy path. 2. Each validation/guard branch. 3. Exceptions from dependencies. 4. Boundary values (null, empty, max).

## Fixing a failing test
Decide first: is the test wrong or the code wrong? Say which in one line, with the evidence, before editing.
Run only that class: `mvn -q -pl <module> -Dtest=<TestClass> test`.
