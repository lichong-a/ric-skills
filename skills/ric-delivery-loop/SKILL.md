---
name: ric-delivery-loop
description: Use when delivering a non-trivial feature, fix, redesign, migration, or system change that requires coordinated requirements, design, implementation, review, testing, validation, and evidence.
---
# RIC Delivery Loop

Own the delivery lifecycle without approving artifacts you authored.

Use this orchestrator for non-trivial product or engineering delivery. Maintaining
the `ric-skills` repository, editing a skill, or making a mechanical documentation
change does not automatically require this complete lifecycle; use
`ric-skill-quality` explicitly for final skill behavior evaluation.

## Required Skills

- Load `ric-agent-operating-rules`.
- Load one primary domain skill and any relevant policy or modifier skills.
- Load `ric-independent-review`, `ric-security-review`, `ric-code-review`, `ric-testing-quality`, and `ric-acceptance-validation` for code, configuration, migration, or deployment changes.
- Add `ric-visual-design-review` and `ric-design-qa` for visual work.

## Run Contract

Create `.ric-work/<run-id>/` and record the request, scope, non-goals, assumptions, acceptance criteria, risks, selected skills with `active_role`, capabilities, actor identities, source revision, artifact versions, gate iteration counts, and run epoch.

Read [references/gate-contract.md](references/gate-contract.md) before dispatching any gate. Read [references/artifact-contract.md](references/artifact-contract.md) before creating run artifacts.

## Lifecycle

1. Use `ric-requirements-engineering`; dispatch a completeness reviewer loading `ric-independent-review`, `ric-requirements-engineering`, and the primary domain skill, plus a requirements-security reviewer loading `ric-independent-review`, `ric-security-review`, the primary domain skill, and relevant safety skills. A separate fixer changes the artifact, then reviewers assess the new artifact version.
2. Use `ric-solution-design`; dispatch two fresh-context design reviewers loading `ric-independent-review`, `ric-solution-design`, and the primary domain skill. For every non-trivial task, also dispatch a design-security reviewer loading `ric-independent-review`, `ric-solution-design`, `ric-security-review`, the primary domain skill, and relevant safety skills; this specialist may be one of the two design reviewers if its dispatch contract satisfies both roles. Add other relevant specialists. A separate fixer changes the artifact, then reviewers assess the new artifact version.
3. Dispatch isolated implementation work only when scopes do not share mutable state. Integrate into one pinned revision.
4. Dispatch independent code and security reviewers with their gate skill, `ric-independent-review`, and the primary domain skill. Visual work also requires independent visual review and design QA with the relevant visual/UI skills. Quality gates return results only to this orchestrator; gates never hand off to each other.
5. Dispatch independent test executors by suite. Each loads `ric-testing-quality`, the primary domain skill, and relevant framework testing skills. Test executors collect evidence and never fix production code.
6. Dispatch independent acceptance validators against the tested revision. Each loads `ric-independent-review`, `ric-acceptance-validation`, the primary domain skill, and required browser/runtime skills.
7. On validation failure, fix, create a new revision, invalidate every source-bound code/security/test/visual/design-QA/acceptance result, rerun code and security review, rerun impacted tests and required full suites, rerun affected visual/design-QA gates, then validate again.
8. Publish an evidence-backed handoff only after all mandatory gates pass.

## Independence Rules

- Authors and fixers cannot approve their own artifacts.
- Reviewers and validators are read-only.
- Use fresh-context subagents. If unavailable, try an isolated thread or external agent.
- If independence cannot be achieved, report `BLOCKED`. User-accepted degraded handoff may continue diagnostics, but the run remains `BLOCKED` and cannot produce a passing gate.
- All non-trivial tasks require security review.

## Loop Budget

- Each gate permits at most three review/fix iterations.
- The same finding with no progress across two fixes requires an independent adjudicator.
- Returning to requirements or design increments the run epoch; at most three epochs are allowed.
- Reviewer conflict, exhausted iteration/epoch budget, major scope change, or unresolved risk returns `ESCALATE` or `BLOCKED`.
- Every source or artifact revision change invalidates affected downstream gates. Never reuse stale approval.

## Exit

Finish only with the exact verified revision, gate decisions, evidence index and hashes, unresolved advisories, residual risks, explicit blockers, and machine validation from `scripts/validate-delivery-run.py`. Optional live behavior evals may strengthen evidence, but they are not required for ordinary repository development or delivery validation.
