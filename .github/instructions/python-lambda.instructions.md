---
applyTo: "**/*.py"
---
- Lambda handlers thin: parse event -> call pure function -> return. Init clients outside the handler.
- Idempotent for SQS/Kafka retries; partial batch failures via `batchItemFailures`.
- Structured JSON logs, no PII. Tests with pytest + moto/stubber; no real AWS calls.
