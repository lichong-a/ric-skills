# Requirements Contract

## Baseline Contents

- Problem, desired outcome, audience, and success measures.
- Current behavior and evidence.
- In-scope and explicitly out-of-scope behavior.
- Functional requirements with stable IDs.
- Non-functional requirements: security, privacy, performance, reliability, accessibility, compatibility, localization, and operations as relevant.
- Roles, permissions, tenant/data boundaries, and sensitive actions.
- Failure, empty, loading, offline, retry, and recovery behavior.
- Assumptions, dependencies, unresolved questions, and risks.

## Acceptance Criteria

Each criterion must:

- Have a stable ID.
- Describe observable behavior, not implementation preference.
- Define setup, action, expected result, and required evidence.
- Map to one or more requirement IDs.
- Be feasible for an independent validator to execute.

Requirements review fails when acceptance criteria are subjective, missing negative cases, impossible to verify, or silently depend on an unstated assumption.
