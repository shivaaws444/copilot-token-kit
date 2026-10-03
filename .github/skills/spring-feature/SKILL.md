---
name: spring-feature
description: Implement a Spring Boot feature end to end (REST endpoint, service, repository, DTOs, validation, error handling) following the project's existing layering. Use whenever the user asks to add or change an API, endpoint, controller, service method, or business logic in a Spring Boot module, even if they only say "add X to the service".
---

# Spring Boot Feature

## Before coding
1. Find ONE existing, similar endpoint in the same module and copy its patterns (package layout, naming, exception style, response wrapper). Do not invent a new style.
2. Confirm the module with `-pl` scope. Do not touch other modules unless the plan says so.

## Layering rules
- Controller: mapping, `@Valid` input, call one service method, return DTO. No business logic, no repository calls.
- Service: business logic, `@Transactional` at this layer only, and only on public methods that write.
- Repository: data access only.
- DTOs are Java records unless the module already uses Lombok classes. Never expose JPA entities in the API.
- Map entity <-> DTO in one place (mapper class or static `from()`), matching the module's existing choice.

## Must-haves
- Bean Validation on request DTOs (`@NotNull`, `@NotBlank`, `@Size`...).
- Errors go through the existing `@ControllerAdvice`; add a new exception type only if none fits.
- Log with the existing logger pattern; never log tokens, card numbers, account numbers, or PII.
- Constructor injection only. No field `@Autowired`.
- Config values via `@ConfigurationProperties` or existing property classes, not hard-coded.

## Done when
- Code compiles, a unit test for the service and a `@WebMvcTest` slice for the controller pass:
  `mvn -q -pl <module> -Dtest='<Service>Test,<Controller>Test' test`
- Output only the changed/new files as hunks, plus a 3-line summary.
