---
name: ric-full-output-enforcement
description: Use when a requested implementation or artifact must be complete and partial snippets, placeholders, omitted files, or user-side assembly would make delivery unusable.
---
# RIC Full Output Enforcement

## Role

This is an output-completeness **modifier**. It cannot become the primary executor, redirect the task, approve its own output, or replace review and testing.

## Rules

- Produce every required file and integration change within the assigned scope.
- Do not leave `TODO`, placeholder logic, fake data paths, omitted sections, or instructions that make the user assemble critical pieces.
- Preserve existing project conventions and user changes.
- Explicitly report genuine external blockers instead of inventing output.
- Large output is acceptable when completeness requires it, but avoid unrelated expansion.

## Exit

Completion still requires the primary skill's tests, independent review, and acceptance evidence. This modifier only prevents incomplete delivery.
