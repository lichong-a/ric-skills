---
name: ric-infra-safety
description: Use when work may read or modify databases, migrations, caches, queues, search indices, streams, object storage, shared services, credentials, or infrastructure provisioning.
---
# RIC Infrastructure Safety

## Role

Act as a mandatory safety policy and review gate for infrastructure and persistent data. Never approve destructive operations or fabricate credentials.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Use the relevant backend, data-pipeline, deployment, or domain skill.
- Require independent `ric-security-review` or equivalent safety review for non-trivial writes.
- Hand executable verification to `ric-testing-quality`.

## Environment Profile

Treat configured shared RIC services as the preferred profile, not as universal defaults:

- Elasticsearch `192.168.31.190:9200`
- Kafka `192.168.31.190:9092`
- TimescaleDB/PostgreSQL `192.168.31.190:15433`
- Redis `192.168.31.190:6379`
- NATS `192.168.31.190:4222`, monitoring `8222`
- MinIO `192.168.31.190:9000`, console `9001`

Verify availability, configuration, and user intent before connecting. Reuse a suitable shared service before proposing a new one.

## Operation Classes

| Class | Examples | Policy |
| --- | --- | --- |
| Read-only | schema inspection, health check, metadata query | Allowed when credentials and scope are valid |
| Additive | new prefixed table, index, topic, key, or safe migration | Allowed after preflight and evidence plan |
| Bounded mutation | scoped update required by approved behavior | Requires explicit scope, backup/rollback strategy, and independent review |
| Destructive | drop, truncate, flush, broad delete, unbounded purge | Forbidden |

Object deletion is destructive. Do not delete objects, buckets, records, topics, indices, or schemas. MinIO writes are permitted only in bucket `codex`.

## Namespace Contract

Writable resources must use:

- Elasticsearch: `ric-`
- PostgreSQL/TimescaleDB objects: `ric_` or `ric-`
- Redis keys: `ric:` or `ric-`
- Kafka/NATS topics or subjects: `ric.` or `ric-` when supported

Nonconforming resources are external and read-only.

## Secrets Contract

Use environment variables:

- `RIC_ES_PASSWORD`
- `RIC_KAFKA_USERNAME`, `RIC_KAFKA_PASSWORD`
- `RIC_PG_USER`, `RIC_PG_PASSWORD`
- `RIC_REDIS_PASSWORD`
- `RIC_MINIO_USER`, `RIC_MINIO_PASSWORD`

If a required secret is absent, stop and name the missing variable. Never log, persist, invent, or expose a secret.

## Preflight And Evidence

Before writes, record:

- target environment and resource names;
- operation class and bounded scope;
- namespace compliance;
- expected effects and failure modes;
- backup, rollback, or additive recovery strategy;
- dry-run or isolated-test method;
- monitoring and stop conditions.

After approved additive or bounded work, report exact commands, affected resources, results, and residual risk. Do not claim safety from intention alone.

## Gate Decision

- `PASS`: approved read-only, additive, or explicitly authorized bounded mutation with complete scope, recovery, independent review, and verification evidence.
- `FAIL_REWORK`: namespace, recovery, scope, or verification is incomplete.
- `BLOCKED`: missing secrets, unavailable shared service, or unsafe external resource.
- `ESCALATE`: requested operation is destructive or conflicts with safety policy.
