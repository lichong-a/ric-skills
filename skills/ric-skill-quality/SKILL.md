---
name: ric-skill-quality
description: Use when creating, editing, reviewing, packaging, or releasing skills and the repository needs structural checks, trigger evaluation, conflict detection, behavioral scenarios, or independent quality evidence.
---
# RIC Skill Quality

Act as the explicit final quality gate for a skill change. Do not force every
skill-repository edit through `ric-delivery-loop`; authors may edit and run
static checks directly before invoking this gate.

## Required Procedure

1. Load the relevant skill-authoring guidance and pin the baseline skill version.
2. Define realistic trigger, negative-trigger, conflict, pressure, and behavioral scenarios.
3. Run baseline scenarios before editing when fresh-context subagents are available; record failures and rationalizations.
4. Make the smallest skill change that addresses observed failures.
5. Run the same scenarios with fresh-context subagents, then add new scenarios for discovered loopholes.
6. Dispatch an independent fresh-context skill reviewer that loads `ric-skill-quality`, `ric-independent-review`, the changed skill, and applicable domain skills. The author cannot approve the skill.
7. Validate structure, references, metadata, portability, and repository boundaries.

Read [references/quality-contract.md](references/quality-contract.md) for required checks.

## Boundaries

- Do not assume metadata proves behavior.
- Do not allow descriptions to summarize the workflow; descriptions must state trigger conditions.
- Do not claim subagent evaluation when the same context authored and approved the skill.
- If this gate is explicitly requested and fresh-context subagents, isolated threads, or external reviewers are unavailable, report that behavior evaluation was not independently completed. This does not prevent ordinary repository edits, static validation, commits, or releases from proceeding with an accurate limitation statement.

## Exit

Pass this quality gate only when structural checks and behavioral scenarios pass for the pinned skill version with no unresolved `S0` or `S1` finding.
