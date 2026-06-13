---
name: ric-docs
description: Use when changed behavior, contracts, configuration, architecture, operations, setup, release procedures, or user workflows require accurate documentation or handoff material.
---
# RIC Documentation

## Role

Own documentation accuracy and handoff evidence. Documentation is part of the definition of done when behavior, contracts, configuration, operations, or user workflows change.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Read approved requirements, contracts, implementation, and current verification evidence.
- Use the primary domain skill for terminology and operational truth.
- Hand documentation to independent review or acceptance validation.

## Documentation Contract

Update only documents affected by the change. Depending on scope, cover:

- purpose, prerequisites, setup, and supported runtime;
- environment variables by name, source, default, sensitivity, and validation behavior;
- API or event contracts, permissions, errors, examples, and compatibility notes;
- architecture decisions and tradeoffs through ADRs when decisions are durable;
- deployment, migration, monitoring, rollback, and recovery;
- operator runbooks with symptoms, safe checks, expected results, remediation, and escalation;
- user/admin workflows, roles, permissions, states, and failure handling;
- changelog, release notes, and handoff summary.

Never include real secrets, destructive remediation commands, fabricated output, or instructions not verified against the repository.

## Verification

- Run documentation lint and link checks when available.
- Execute or safely validate documented commands and examples.
- Confirm generated API docs match the machine contract.
- Confirm configuration names and defaults match code.
- Rehearse critical runbook paths in a safe environment when feasible.
- Verify changed behavior has corresponding documentation or an explicit reason it does not need it.

## Required Evidence

Report:

- documents changed and the implementation/contract revision they describe;
- commands, links, examples, and runbooks verified;
- intentional documentation omissions with rationale;
- owners and known staleness risks;
- decision: `PASS`, `PASS_WITH_ADVISORIES`, `FAIL_REWORK`, `BLOCKED`, or `ESCALATE`.

## Exit Criteria

Pass only when documentation matches the current verified revision, contains no secrets or unsafe procedures, and gives the next engineer, operator, or user enough information to perform the documented task.
