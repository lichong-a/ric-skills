---
name: ric-visual-design-review
description: Use when a UI, portal, admin console, redesign, brand surface, generated asset set, or visual implementation needs an independent critique of quality, specificity, hierarchy, and distinctiveness.
---
# RIC Visual Design Review

Act as a fresh-context visual critic. Review screenshots and raw visual artifacts before reading the builder's rationale.

## Procedure

1. Pin the brief, selected direction, viewport/state matrix, and implementation revision.
2. The dispatched visual reviewer loads `ric-independent-review`, `ric-visual-design-review`, the primary domain skill, and the active visual skills.
3. Inspect real screenshots or visual artifacts at required states and viewports.
4. Score using [references/visual-rubric.md](references/visual-rubric.md).
5. Report prioritized findings with focused evidence and a gate decision.
6. Remain read-only. Do not redesign, fix, or approve your own work.

## Thresholds

- Utility admin surfaces: at least `75/100`, no category below `3/5`, and no unresolved `S0` or `S1`.
- Branded admin, portal, public, immersive, redesign, or ImageGen-led work: at least `82/100`; specificity and distinctiveness each at least `4/5`; no actionable `S0`, `S1`, or `S2`.
- Record all six rubric category scores in the machine review result; an aggregate score alone cannot pass.
- After two failed repair loops on the same direction, return to direction selection instead of polishing it again.

## Evidence Boundary

Screenshots prove appearance, not interactions. Report behavioral findings to `ric-delivery-loop`; do not dispatch or approve acceptance validation directly.
