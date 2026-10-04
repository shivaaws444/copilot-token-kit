---
name: api-contract
description: Protect API and event contracts - detect breaking changes, version endpoints, evolve DTOs and Kafka/SQS message schemas safely, and keep OpenAPI docs accurate. Use whenever the user changes a request/response DTO, endpoint path, status codes, error format, message payload, or asks if a change will break consumers.
---

# API Contract

## Breaking changes (any of these = breaking)
Removing/renaming a field or endpoint, changing a type, making an optional field required, changing status codes or error shape, changing enum values consumers rely on, changing message topic/queue or key.

## Safe evolution
- Add, don't change: new optional fields, new endpoints. Consumers must ignore unknown fields (`FAIL_ON_UNKNOWN_PROPERTIES=false`).
- Breaking needed -> new version (`/v2/...`) or new field, run both, deprecate the old with a date, remove after consumers move.
- Messages: producers add fields only; include a schema/version field.

## Check
Compare old vs new DTOs in the diff. Output: BREAKING / NON-BREAKING per change, affected consumers (from docs/repo-map.md and integration notes), and the migration plan if breaking. Update OpenAPI annotations/spec in the same PR.
