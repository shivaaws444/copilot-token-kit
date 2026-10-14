---
name: kafka-sqs-messaging
description: Design or implement event-driven messaging with Apache Kafka or Amazon SQS (producers, consumers, topics, FIFO, DLQ, retries). Use for any event, topic, queue, listener, or async workflow task.
---
# Kafka / SQS Messaging
- Contract first: event name, key (ordering scope), versioned schema, owner. Put it in docs/ before code.
- Consumers idempotent (dedupe key / upsert); at-least-once assumed.
- Retries with backoff -> DLQ (Kafka DLT / SQS redrive). Alert on DLQ depth.
- Kafka: key = entity id for ordering; manual ack after successful processing; no blocking calls in listener.
- SQS: FIFO + MessageGroupId only when order matters; visibility timeout > max processing time.
- Propagate correlation/trace id in headers. Never put PII in keys or headers.
- Tests: embedded Kafka / Testcontainers / LocalStack; test poison message -> DLQ.
