---
name: ric-infra-safety
description: "RIC shared infrastructure and data-safety skill. Use whenever work touches Elasticsearch, Kafka, TimescaleDB/PostgreSQL, Redis, NATS, MinIO, migrations, schemas, indices, topics, streams, keys, buckets, secrets, or provisioning decisions. Enforces reuse-before-create, ric namespace isolation, non-destructive operations, and environment-variable secrets."
---
# RIC Infrastructure Safety

Use this skill for any infrastructure, data, cache, message, search, storage, or migration work.

## Shared Services

Reuse these services when they satisfy requirements:

- Elasticsearch: `192.168.31.190:9200`, version 9.3.1, username `elastic`, password from `RIC_ES_PASSWORD`.
- Kafka: `192.168.31.190:9092`, version 4.2.0, SASL_PLAINTEXT, credentials from `RIC_KAFKA_USERNAME` and `RIC_KAFKA_PASSWORD`.
- TimescaleDB/PostgreSQL: `192.168.31.190:15433`, PostgreSQL 18 + TimescaleDB, credentials from `RIC_PG_USER` and `RIC_PG_PASSWORD`.
- Redis: `192.168.31.190:6379`, version 8.x, password from `RIC_REDIS_PASSWORD`.
- NATS: `192.168.31.190`, client `4222`, monitoring `8222`, version 2.12.
- MinIO: `192.168.31.190:9000`, console `9001`, version `RELEASE.2025-09-07`, credentials from `RIC_MINIO_USER` and `RIC_MINIO_PASSWORD`.

## Absolute Safety Rules

Never execute destructive operations against databases, caches, message systems, or object storage.

Forbidden examples:

- SQL: `DROP DATABASE`, `DROP TABLE`, `TRUNCATE TABLE`, broad `DELETE FROM`.
- Redis: `FLUSHALL`, `FLUSHDB`.
- Elasticsearch: `DELETE INDEX`, `DROP INDEX`.
- Object storage deletion outside explicit safe user-approved scope.

Migrations must not remove existing user data.

## Namespace Rules

Writable resources must use ric namespace:

- Elasticsearch indices start with `ric-`.
- PostgreSQL/TimescaleDB databases, schemas, tables, sequences, views, and related resources start with `ric_` or `ric-` depending on naming constraints.
- Redis keys start with `ric:` or `ric-`.
- Kafka/NATS subjects/topics created for ric work should use a clear `ric.` or `ric-` prefix when the platform allows it.
- MinIO manipulation is allowed only for bucket `codex`.

Resources without required ric prefixes are external assets. Read-only inspection is allowed when necessary; writes are prohibited.

## Secrets

Never hardcode secrets.

Use:

- `RIC_ES_PASSWORD`
- `RIC_KAFKA_USERNAME`
- `RIC_KAFKA_PASSWORD`
- `RIC_PG_USER`
- `RIC_PG_PASSWORD`
- `RIC_REDIS_PASSWORD`
- `RIC_MINIO_USER`
- `RIC_MINIO_PASSWORD`

If a required secret is missing:

1. Stop.
2. State which secret is missing.
3. Ask the user to provide it through the environment.
4. Do not fabricate credentials.

## Provisioning Policy

Before creating a new service, verify whether shared infrastructure satisfies the requirement.

If a capability is missing, ask:

`A shared infrastructure for this capability does not currently exist. Would you like to add a reusable shared environment instead of creating a project-specific instance?`

Do not create duplicate infrastructure automatically.

## Implementation Pattern

For infrastructure-related code:

- Put host, port, username, password, database/index/topic/key prefix, TLS, and auth settings in configuration.
- Use environment variables for secrets.
- Add connection health checks.
- Add timeouts and retries with bounded backoff.
- Add clear logging without secret leakage.
- Add tests using mocks or local isolated resources when possible.
- Document required environment variables.

