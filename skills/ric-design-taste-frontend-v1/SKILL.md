---
name: ric-design-taste-frontend-v1
description: Use when an existing visual direction explicitly depends on the legacy taste-skill v1 language and needs a bounded compatibility modifier.
---
# RIC Design Taste Frontend V1

## Role

This is a legacy visual **modifier**, not a primary executor or orchestrator. It may influence composition, typography, spacing, asset direction, and interaction craft, but it must not redirect ownership or override requirements, accessibility, performance, the existing design system, or the primary domain skill.

## Use

- Preserve recognizable v1 taste when a user or existing project explicitly asks for it.
- Convert generic composition into a clearer focal hierarchy.
- Prefer real or generated assets when imagery materially improves the approved direction.
- Make motion purposeful, finite, reduced-motion aware, and performance-budgeted.

## Boundaries

- Do not use placeholder image services or fake assets as final output.
- Do not require every card, section, or control to animate.
- Do not impose marketing-page composition on admin utility pages.
- Return recommendations to the orchestrator; never stop and redirect the task.

## Verification

For non-trivial delivery, use `ric-delivery-loop`. Visual decisions require `ric-visual-design-review`; implemented visual fidelity requires `ric-design-qa`; behavior requires `ric-acceptance-validation`.
