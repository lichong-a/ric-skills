---
name: ric-api-design
description: "RIC API design skill for REST, OpenAPI, RPC, service contracts, request/response schemas, pagination, filtering, sorting, errors, auth, permissions, idempotency, compatibility, and frontend-backend integration in ric projects."
---
# RIC API Design

Use this skill when designing or changing API contracts.

## Contract First

Define:

- Resource or operation.
- HTTP method or RPC name.
- Path/name.
- Auth requirement.
- Permission requirement.
- Request schema.
- Response schema.
- Error schema.
- Pagination/filter/sort behavior.
- Compatibility impact.

## REST Conventions

Use consistent patterns:

- `GET` for read.
- `POST` for create/actions.
- `PUT` or `PATCH` for update based on local convention.
- `DELETE` only for safe user-approved logical delete patterns; never destructive data removal without explicit approved domain design.

For admin list APIs:

- Pagination: page/pageSize or cursor, matching existing convention.
- Filtering: explicit query params or structured body for complex search.
- Sorting: field + direction.
- Response includes data and total when paginated.

## Error Shape

Use the existing project error format. If absent, define:

- code.
- message.
- details.
- trace/request ID.
- field errors for validation.

Do not expose sensitive internals.

## Auth And Permissions

- Distinguish unauthenticated from unauthorized.
- Enforce permission server-side.
- Return stable codes for frontend handling.
- Do not rely on menu/button hiding.

## Compatibility

- Avoid breaking response fields.
- Add fields instead of renaming when possible.
- Version APIs when breaking changes are required.
- Preserve route semantics unless the user asks for redesign.

## Idempotency

Use idempotency keys for:

- Payment-like operations.
- Imports.
- Long-running jobs.
- Retried creates.
- External integrations.

## Documentation

Update OpenAPI/docs/examples when present.
Include realistic Chinese enterprise admin examples when relevant.

