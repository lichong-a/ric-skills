---
name: ric-redesign-existing-projects
description: Use when an existing website, product, admin console, or application needs a visual or interaction redesign while preserving verified behavior.
---
# RIC Redesign Existing Projects

## Role

This skill may be a primary executor for a focused redesign or a modifier under another primary. The active role must be recorded in the delivery run; it never redirects ownership by itself.

## Preservation Contract

Before editing, inventory routes, workflows, permissions, states, framework conventions, responsive behavior, analytics, tests, and existing assets. Convert preserved behavior into acceptance criteria.

## Redesign Contract

- Distinguish public/marketing surfaces, product UI, and admin utility surfaces.
- Explore different directions when the visual gate requires them.
- Preserve or intentionally migrate the existing component system; do not silently mix UI libraries.
- Use real or generated assets instead of placeholder services.
- Validate the same final revision with code review, tests, design QA, visual review, and behavioral acceptance as applicable.

## Failure Loop

Any regression or acceptance failure returns through implementation repair, code/security re-review, affected tests, required full tests, and acceptance validation.
