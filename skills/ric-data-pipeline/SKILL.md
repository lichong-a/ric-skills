---
name: ric-data-pipeline
description: Use when designing or changing event streams, ingestion, projections, indexing, analytics flows, consumers, retries, dead-letter handling, replay, reconciliation, or backfills.
---
# RIC Data Pipeline

For non-trivial delivery, operate as the single primary executor under `ric-delivery-loop`; do not approve requirements, design, code review, security review, tests, or acceptance.

## Role

Own data-flow semantics and implementation. Never waive infrastructure safety, reconciliation, independent review, or test evidence.

## Required Companions

- Apply `ric-agent-operating-rules` and `ric-infra-safety`.
- Use `ric-api-design` for externally consumed event or data contracts.
- Hand changes to independent `ric-code-review` and `ric-testing-quality`.

## Required Design Record

Define before implementation:

- source, target, owner, schema, version, and volume expectations;
- delivery semantic: at-most-once, at-least-once, or effectively-once;
- partition key, ordering boundary, and concurrency model;
- consumer group or durable identity;
- offset/checkpoint commit point and recovery behavior;
- idempotency and deduplication strategy;
- retry policy, poison-message handling, DLQ, and replay procedure;
- backpressure, rate limits, lag thresholds, and stop conditions;
- source-to-target reconciliation and retention policy.

## Data Contract

Events or records must have stable identity, schema version, timestamps, producer, tenant/data scope, entity identity, payload bounds, and correlation context when relevant. Do not include secrets. Preserve backward compatibility or provide an approved migration.

## Processing Contract

- Commit checkpoints only after the defined durable success point.
- Make retries safe and observable.
- Handle duplicates and out-of-order input according to declared semantics.
- Bound queues, batches, payloads, retries, and concurrency.
- Route permanent failures to an inspectable DLQ without losing source context.
- Define replay idempotency and prevent replay from bypassing authorization or safety rules.

## Backfill Contract

Every backfill must be additive, bounded, resumable, throttled, observable, and idempotent. Define:

- checkpoint format and resume behavior;
- source range and exclusion rules;
- throttle and resource budget;
- abort and rollback/recovery conditions;
- validation queries and reconciliation thresholds;
- failure report and safe rerun procedure.

## Required Evidence

Provide:

- approved pipeline design record and schema compatibility result;
- tests for happy path, duplicate, out-of-order, retryable failure, permanent failure/DLQ, replay, checkpoint recovery, backpressure, and schema versions;
- reconciliation report showing source and target counts or domain invariants;
- lag, throughput, failure, and DLQ monitoring plan;
- remaining data-correctness and operational risks.

## Gate And Handoff

Independent review must confirm semantics, safety, and reconciliation against the pinned artifact. The test gate must use isolated or approved RIC-prefixed resources. A failed reconciliation, unbounded backfill, unsafe resource, or missing recovery procedure blocks handoff.
