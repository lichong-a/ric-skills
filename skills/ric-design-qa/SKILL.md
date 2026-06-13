---
name: ric-design-qa
description: Use when a rendered UI or generated asset implementation must be compared with an approved design, screenshot, reference image, direction board, or source-of-truth visual target.
---
# RIC Design QA

Compare the approved visual source with the rendered implementation at matching states and viewports.

## Procedure

1. The dispatched Design QA reviewer loads `ric-independent-review`, `ric-design-qa`, the primary UI skill, and active source-fidelity skills; then pins the source-of-truth visual target and implementation revision.
2. Capture matching screenshots for the required viewport and state matrix.
3. Build side-by-side comparisons and focused crops.
4. Check structure, hierarchy, spacing, typography, color, assets, responsive behavior, states, and motion timing.
5. Use [references/comparison-contract.md](references/comparison-contract.md) to classify drift.
6. Remain read-only and issue a gate decision.

## Boundaries

- Do not replace product judgment with pixel matching when the approved target is conceptual.
- Do not excuse missing states or assets as implementation details.
- Screenshots do not prove interactions; report behavioral gaps to `ric-delivery-loop`.
- Report overall visual-quality review needs to `ric-delivery-loop`; do not dispatch or approve another quality gate.

## Exit

Return the result only to `ric-delivery-loop`. Pass only when no actionable `S0`, `S1`, or required-to-fix fidelity finding remains for the pinned revision.
