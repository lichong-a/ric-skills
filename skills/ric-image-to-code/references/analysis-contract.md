# Source Analysis Contract

Use this reference before implementing a visual source.

## Source Inventory

For each source, record:

- File or URL.
- Intended viewport, device, and state.
- Authority: final design, concept, generated reference, inspiration, or legacy baseline.
- Real assets and text that must be reused.
- Ambiguous or impossible-to-infer details.

Do not combine inconsistent sources silently. Resolve conflicts or record which source wins.

## Structural Analysis

Extract:

- Page regions and reading order.
- Grid, columns, anchors, overlaps, and alignment.
- Section heights and rhythm.
- Fixed, sticky, floating, and scroll-bound elements.
- Responsive transformations suggested by the source.

## Visual System

Extract relationships:

- Type roles and scale ratios.
- Color and surface roles.
- Spacing rhythm.
- Radius, border, shadow, and elevation logic.
- Component variants and state differences.
- Media aspect ratios, focal points, and crop rules.

Use tokens where repetition is meaningful. Preserve intentional exceptions.

## Behavior And State

A static source can imply but cannot prove behavior. Separate:

- Visible state that can be implemented directly.
- Probable interaction that requires repository or user evidence.
- Unknown behavior that must not be invented.

Capture loading, empty, error, selected, expanded, disabled, permission, and responsive states when provided or required by the primary executor.

## Implementation Map

Map source regions to:

- Existing reusable components.
- New reusable components.
- One-off composition.
- Real or generated assets.
- Data and interaction requirements.
- Validation evidence.

Avoid creating abstractions before the repeated pattern is clear.

