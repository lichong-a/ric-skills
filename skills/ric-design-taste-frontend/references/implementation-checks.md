# Implementation Checks

Use this reference before handing a public frontend implementation to independent quality gates.

## Repository Checks

- Existing stack and conventions were preserved or approved changes are documented.
- Lint, typecheck, tests, and production build pass when available.
- New dependencies are justified, version-compatible, and actually used.
- No console errors, broken routes, missing assets, or failed network requests remain.

## Visual Checks

- First viewport clearly identifies the subject and primary action.
- Typography, spacing, alignment, and media framing are coherent.
- Product-specific content replaces generic filler.
- Repeated layouts are intentional.
- Generated assets are visible, correctly cropped, and provenance-recorded.
- Text and controls do not overlap, clip, or wrap incoherently.

## State And Interaction Checks

- Hover, focus, active, disabled, loading, empty, error, and success states exist when relevant.
- Keyboard navigation and visible focus work.
- Forms have labels, validation, and understandable feedback.
- Motion is purposeful, cleaned up, and reduced-motion compatible.
- Navigation and CTAs perform the intended action.

## Responsive Checks

- Verify required desktop, tablet, and mobile viewports.
- Confirm no horizontal overflow or hidden primary actions.
- Confirm reading order and interaction order remain logical.
- Confirm media crops and typography remain usable.

## Evidence Package

Provide:

- Brief and Design Read.
- Selected direction and rejected alternatives when applicable.
- Current revision or immutable snapshot.
- Commands and results.
- Screenshot matrix and interaction evidence.
- Asset manifest.
- Known deviations, risks, and blockers.

The builder checklist is not final approval. Send the package to `ric-visual-design-review` and, when a source of truth exists, `ric-design-qa`.

