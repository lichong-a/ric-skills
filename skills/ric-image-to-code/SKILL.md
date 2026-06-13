---
name: ric-image-to-code
description: Use when implementing or redesigning a frontend from screenshots, mockups, generated references, design exports, or other visual sources where source-to-render fidelity is a primary acceptance criterion.
---

# RIC Image To Code

For non-trivial delivery, operate under `ric-delivery-loop` as the selected primary executor or a bounded visual-fidelity modifier. Record the active role and never approve the resulting gates.

## Overview

Translate visual evidence into maintainable frontend code while preserving hierarchy, rhythm, assets, responsive intent, and interaction behavior.

This skill is derived from the image-to-code workflow in Leonxlnx/taste-skill under the upstream MIT license. It retains image-first analysis and anti-drift discipline without forcing image generation or a fixed page recipe.

## Role

- Act as a **visual executor** for source-driven frontend implementation.
- Act as a **modifier** when a primary domain skill owns the product surface.
- Do not redirect the task or override the primary executor's information-density, permission, or workflow rules.
- Do not self-approve fidelity.

## Required Companion Skills

- **REQUIRED QUALITY GATE:** Use `ric-design-qa` for independent source-to-render comparison.
- **REQUIRED QUALITY GATE:** Use `ric-visual-design-review` when visual quality or redesign judgment is in scope.
- **REQUIRED IMAGE RUNTIME:** Use `ric-imagegen-runtime` if missing or unsuitable source assets must be generated or edited.
- Read the detected framework and component-library skills before coding.

## Source Contract

Before coding, identify:

- Authoritative source images and their viewport/state.
- Which text, logos, photos, icons, and product screenshots are real source assets.
- Which details are ambiguous, decorative, or impossible to infer.
- Which behavior must be inferred from visual state alone.
- Which primary domain skill owns product behavior.

Do not invent hidden workflows or treat generated text inside an image as authoritative copy. Resolve material ambiguity from repository evidence or the user; otherwise record the assumption.

## Workflow

1. Inspect repository structure, dependencies, current UI system, routes, assets, and target viewports.
2. Create a source inventory and an implementation map.
3. Extract the visual system before writing components.
4. Implement the structural shell and responsive layout.
5. Implement typography, assets, components, states, and interactions.
6. Render at matching viewports and compare against the source.
7. Fix the largest fidelity differences first.
8. Hand final evidence to independent quality gates.

Read [references/analysis-contract.md](references/analysis-contract.md) before extracting or implementing a source.

## Extraction Standard

Extract relationships rather than isolated pixel guesses:

- Page regions, grid, anchors, alignment, overlap, and reading order.
- Type roles, scale relationships, line length, weight, and contrast.
- Color roles, surfaces, borders, shadows, radii, and material hierarchy.
- Component variants, repeated patterns, and state differences.
- Media framing, crop behavior, aspect ratios, and focal points.
- Responsive clues, probable breakpoints, and mobile transformations.

Build reusable tokens and components where repetition is real. Do not abstract one-off visual details merely to appear systematic.

## Asset Rules

- Reuse supplied or repository assets when they are authoritative and suitable.
- Generate or edit assets only when the source is missing, unusable, or the approved redesign requires it.
- Delegate generation method, capability detection, fallback, provenance, and failure behavior to `ric-imagegen-runtime`.
- Do not crop unrelated legacy images into a fake match.
- Do not ship generic placeholder media, fake screenshots, or fabricated logos as final assets.
- Record asset provenance and any source substitutions.

## Fidelity And Adaptation

Prioritize:

1. Information hierarchy and task clarity.
2. Major geometry and section rhythm.
3. Typography and media framing.
4. Component proportions and states.
5. Fine decoration.

Match the source where it is intentional. Adapt where exact copying would break responsiveness, accessibility, product behavior, or the primary executor's constraints. Document meaningful adaptations.

Read [references/fidelity-and-validation.md](references/fidelity-and-validation.md) for comparison procedure, drift triage, and evidence requirements.

## Redesign Mode

When the user asks to improve rather than copy:

- Capture baseline screenshots first.
- Define what must be preserved.
- Identify concrete source weaknesses.
- Select a revised direction with the relevant visual executor.
- Use the original and approved direction as separate references.
- Validate both preservation and improvement.

Do not silently replace brand identity, content hierarchy, navigation, or core user flows.

## Builder Verification

- Run repository lint, typecheck, tests, and build when available.
- Render matching viewport/state pairs.
- Produce side-by-side comparisons or aligned screenshots.
- Check loading, empty, error, interaction, and responsive states when relevant.
- Confirm real assets load, text is not clipped, and no placeholder content remains.
- Record differences that are intentional, unresolved, or blocked.

## Independent Quality Gates

1. Hand source and rendered pairs to `ric-design-qa`.
2. Hand redesign or high-expression work to `ric-visual-design-review`.
3. Address findings and rerun affected repository and browser checks.
4. Request review against the updated revision.

Screenshots prove appearance, not behavior. Use browser assertions or interaction traces for navigation, focus, forms, permissions, and state transitions.

## Exit Criteria

- Source inventory and assumptions are explicit.
- Required source-to-render pairs exist.
- Functional and repository checks pass.
- No unresolved blocking fidelity or visual findings remain.
- Asset provenance and intentional adaptations are documented.
