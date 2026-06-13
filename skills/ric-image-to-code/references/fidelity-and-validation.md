# Fidelity And Validation

Use this reference while comparing a visual source with an implementation.

## Comparison Setup

- Render source and implementation at matching viewport and state.
- Use consistent browser zoom and device scale.
- Compare a full view plus focused crops for high-risk regions.
- Keep the source, current render, and revision identifier together.

## Drift Triage

Fix in this order:

1. Missing or incorrect content and actions.
2. Major structure, geometry, and reading order.
3. Typography, media framing, and spacing rhythm.
4. Component proportions and states.
5. Color, shadow, borders, and fine decoration.

Do not polish minor effects while major hierarchy is wrong.

## Adaptation Rules

An adaptation is acceptable when it improves:

- Accessibility.
- Responsive behavior.
- Real product workflow.
- Performance.
- Framework or design-system consistency.

Record the reason. Unexplained drift is a defect.

## Browser Evidence

Screenshots verify appearance. Use browser assertions or interaction traces for:

- Navigation and return behavior.
- Form submission and validation.
- Keyboard and focus behavior.
- Permissions and hidden actions.
- Loading, empty, error, and success transitions.
- Preserved filters, pagination, tabs, and scroll state.

## Review Package

Send `ric-design-qa`:

- Authoritative source list.
- Matching source/render pairs.
- Current revision.
- Intentional adaptations.
- Unresolved ambiguity.
- Commands and browser evidence.

Send `ric-visual-design-review` when redesign quality, brand expression, or visual direction is also being judged.

