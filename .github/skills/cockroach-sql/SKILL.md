---
name: cockroach-sql
description: Write, review, or migrate SQL and JPA data access for CockroachDB safely - queries, indexes, schema migrations (Flyway/Liquibase), transactions and retries. Use whenever the user works on SQL, repositories, @Query, entities, schema changes, slow queries, or transaction errors such as "restart transaction" / 40001 / RETRY_SERIALIZABLE.
---

# CockroachDB SQL

## Transactions
- CockroachDB defaults to SERIALIZABLE; contention returns SQLSTATE 40001. Writes must be retry-safe.
- Retry at the service boundary (existing retry utility, Spring Retry, or Resilience4j - whichever the project uses), never inside a single SQL statement.
- Keep transactions short: no remote calls (HTTP, AWS, Kafka) inside `@Transactional`.

## Keys & schema
- Prefer UUID primary keys (`gen_random_uuid()`) over sequential IDs to avoid write hotspots.
- Every foreign key and every frequent WHERE/ORDER BY column needs an index; use `STORING` for covering reads.
- Migrations: one change per migration, backward compatible (add column nullable -> backfill -> add constraint). Never edit an applied migration.

## Queries
- Check plans with `EXPLAIN` for any new query on a large table; flag full scans.
- Paginate with keyset (WHERE id > :last ORDER BY id LIMIT n) for large tables, not big OFFSETs.
- Batch inserts/updates (`hibernate.jdbc.batch_size`, `saveAll`) instead of per-row loops.
- Avoid N+1: use fetch joins or entity graphs; say explicitly if a change introduces extra queries.

## Output
Show the SQL or repository change, the index/migration needed, and one line on transaction/retry impact.
