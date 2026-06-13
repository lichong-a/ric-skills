---
name: ric-requirements-engineering
description: Use when a non-trivial request has ambiguous scope, unstated constraints, missing acceptance criteria, competing stakeholder needs, or requires a reviewable requirements baseline.
---
# RIC Requirements Engineering

Turn intent into a testable, reviewable requirements baseline before design or implementation.

## Procedure

1. Inspect the repository and existing behavior before asking discoverable questions.
2. Record goal, audience, current state, scope, non-goals, constraints, assumptions, dependencies, and risks.
3. Define stable requirement IDs and acceptance criterion IDs.
4. Cover functional behavior, non-functional requirements, permissions, data safety, failure states, compatibility, operations, accessibility, and observability as relevant.
5. Mark unresolved ambiguity explicitly; do not hide guesses as requirements.
6. Dispatch two fresh-context reviewers. The completeness reviewer loads `ric-independent-review`, `ric-requirements-engineering`, and the primary domain skill. The requirements-security reviewer loads `ric-independent-review`, `ric-security-review`, the primary domain skill, and `ric-infra-safety` or other safety skills when relevant.
7. Use a separate fixer for failed reviews, then re-review. Never self-approve.

Read [references/requirements-contract.md](references/requirements-contract.md) when creating or reviewing the baseline.

## Outputs

Produce `.ric-work/<run-id>/requirements.md`, `acceptance.json`, `traceability.json`, and initial `risk-register.json`, each tied to an artifact version.

## Exit

Exit with `PASS` only when every requirement is testable, all blocking ambiguity is resolved, and no unresolved `S0` or `S1` finding remains. After three failed loops, return `ESCALATE`.
