---
name: ric-api-design
description: Use when creating or changing REST, RPC, event, webhook, OpenAPI, request-response, pagination, error, authorization, or compatibility contracts between systems.
---
# RIC API Design

For non-trivial delivery, operate under `ric-delivery-loop` as the selected primary executor or a bounded contract modifier. Record the active role and never approve the resulting gates.

## Role

Own the machine-verifiable interface contract. Do not implement unrelated business logic or approve your own contract review.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Use `ric-backend-service` for implementation.
- Use `ric-infra-safety` when persistence, queues, or shared services are involved.
- Require independent contract review and `ric-testing-quality` before handoff.

## Inputs

Inspect existing routes, schemas, generated clients, auth model, permission model, error format, versioning policy, and consumers. Record the current contract version and compatibility constraints.

## Contract Artifact

Produce or update a machine-verifiable contract such as OpenAPI, AsyncAPI, protobuf, GraphQL schema, JSON Schema, or the repository's equivalent. The contract must define:

- operation, method, path, media types, and version;
- authentication, authorization, tenant/data scope, and audit expectations;
- request, response, field validation, and stable errors;
- status codes and retry semantics;
- pagination, filtering, sorting, and limits;
- idempotency, concurrency control, and duplicate handling;
- rate limits, caching, asynchronous-job behavior, and webhook/event delivery when relevant;
- realistic examples without secrets.

## Compatibility Contract

- Generate a compatibility diff against the prior contract.
- Prefer additive changes.
- Identify breaking changes, affected consumers, migration path, deprecation window, and rollback strategy.
- Do not silently change field meaning, nullability, ordering, error codes, or authorization scope.

## Security And Reliability

- Enforce authorization and tenant/data scope server-side.
- Distinguish unauthenticated, unauthorized, validation, conflict, not-found, throttled, and dependency failures.
- Prevent sensitive internals, secrets, and cross-tenant identifiers from leaking.
- Require idempotency for retried creates, imports, payment-like actions, long-running jobs, and external callbacks.
- Define optimistic concurrency or conflict behavior for contested mutations.

## Required Evidence

Provide:

- contract artifact and compatibility diff;
- acceptance examples and negative examples;
- generated-client or schema-validation result when applicable;
- contract tests for success, validation, authorization, compatibility, concurrency, and idempotency;
- unresolved consumer, migration, or security risks.

## Gate And Handoff

An independent reviewer evaluates the pinned contract artifact. Pass only with no unresolved blocking contract, authorization, compatibility, or test findings. Return the decision to `ric-delivery-loop`; implementation discoveries that alter semantics invalidate affected downstream gates and return to contract review.
