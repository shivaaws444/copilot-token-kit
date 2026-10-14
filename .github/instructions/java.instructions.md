---
applyTo: "**/*.java"
---
- Constructor injection; records for DTOs; `@Transactional` only on service write methods.
- Never log PII, card/account numbers, tokens. Use existing `@ControllerAdvice` for errors.
- Tests: JUnit 5 + Mockito; smallest slice (`@WebMvcTest`, `@DataJpaTest`) before `@SpringBootTest`.
