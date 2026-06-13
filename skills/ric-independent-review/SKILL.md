---
name: ric-independent-review
description: Use when requirements, designs, code, tests, evidence, or release decisions need a read-only fresh-context reviewer who is independent from the artifact author or fixer.
---
# RIC Independent Review

Provide an independent gate decision, not implementation help.

## Reviewer Contract

- Use a fresh-context subagent or isolated reviewer context.
- Review a pinned source revision or artifact version.
- Remain read-only. Do not edit, fix, or approve work you authored.
- Receive raw artifacts, requirements, rubric, and evidence without the author's intended conclusion.
- Reproduce or independently verify high-risk claims when possible.
- Distinguish missing evidence from passing evidence.

Read [references/review-contract.md](references/review-contract.md) before issuing a decision.

## Required Output

Return:

1. Reviewed artifact and exact version.
2. Gate decision: `PASS`, `PASS_WITH_ADVISORIES`, `FAIL_REWORK`, `BLOCKED`, or `ESCALATE`.
3. Findings ordered by `S0`, `S1`, `S2`, then `S3`.
4. Evidence, affected requirement or acceptance IDs, and concrete remediation for each finding.
5. Verification performed, evidence gaps, and residual risks.

## Independence Failure

If a fresh reviewer cannot be obtained, try an isolated thread or external agent. Otherwise report `BLOCKED`. A user may accept a diagnostic or degraded handoff, but it remains `BLOCKED` and cannot be recorded as `PASS` or `PASS_WITH_ADVISORIES`. Never self-approve or claim independence that did not occur.
