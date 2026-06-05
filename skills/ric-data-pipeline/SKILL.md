---
name: ric-data-pipeline
description: "RIC data pipeline skill for Kafka, NATS, Redis streams, TimescaleDB/PostgreSQL, Elasticsearch indexing, event schemas, ingestion, projection, retries, idempotency, backfills, observability, and non-destructive migration design under ric namespace rules."
---
# RIC Data Pipeline

Use this skill for event-driven, streaming, indexing, ingestion, projection, and analytical data flows.

## Safety

Always apply `ric-infra-safety`.

- Reuse shared services.
- Use ric-prefixed writable resources.
- Never perform destructive data operations.
- Do not delete, truncate, flush, or drop existing data.
- Backfills and migrations must be additive and reversible when possible.

## Pipeline Design

Define:

- Source system.
- Event or record schema.
- Transport: Kafka, NATS, Redis stream, database polling, file/object import.
- Consumer group / durable name.
- Idempotency key.
- Retry policy.
- Dead-letter handling.
- Target projection/index/table.
- Monitoring and replay plan.

## Event Schema

Events should include:

- Event name/type.
- Version.
- Event ID.
- Occurred time.
- Producer.
- Tenant/account/project context when relevant.
- Entity ID.
- Payload.
- Trace/correlation ID.

Rules:

- Version schemas.
- Keep backward compatibility.
- Avoid unbounded payloads.
- Do not include secrets.

## Idempotency

Every consumer should be safe to retry.

Patterns:

- Idempotency key table.
- Upsert by natural key.
- Last-write version check.
- Deduplicate by event ID.
- Store processed offset/checkpoint.

## Storage Targets

TimescaleDB/PostgreSQL:

- Use `ric_` names.
- Prefer additive migrations.
- Use indexes intentionally.
- Keep hypertable/time-series design explicit.

Elasticsearch:

- Index names start with `ric-`.
- Define mappings before indexing when field types matter.
- Use aliases for versioned index rollout when needed.

Redis:

- Keys start with `ric:` or `ric-`.
- Set TTLs for cache keys when appropriate.
- Do not use `FLUSH*`.

Kafka/NATS:

- Use ric-prefixed subjects/topics when creating.
- Define retention and consumer behavior.
- Add dead-letter or retry strategy for poison messages.

## Backfills

Backfills must be:

- Non-destructive.
- Bounded.
- Resumable.
- Observable.
- Idempotent.

Report progress and failures clearly.

## Verification

Test:

- Happy path.
- Duplicate event.
- Out-of-order event when possible.
- Retryable failure.
- Permanent failure/dead-letter.
- Schema version compatibility.

