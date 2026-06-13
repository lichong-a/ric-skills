---
name: ric-imagegen-frontend-mobile
description: Use when generating mobile app visual directions, screen concepts, flow references, or asset systems for iOS, Android, and cross-platform product experiences.
---

# RIC ImageGen Frontend Mobile

## Overview

Generate mobile product references that are platform-aware, flow-coherent, readable, and useful for later design or implementation.

This skill is derived from the mobile ImageGen workflow in Leonxlnx/taste-skill under the upstream MIT license. It preserves screen-first art direction, app design-system consistency, and flow thinking without forcing device frames, excessive screens, or decorative assets.

## Role

- Act as a **visual executor** for mobile screen and flow references.
- Act as a **modifier** when a mobile product or implementation skill owns behavior.
- Do not write production mobile code unless requested by the primary executor.
- Do not self-approve generated directions.

## Required Companion Skills

- **REQUIRED IMAGE RUNTIME:** Use `ric-imagegen-runtime` for generation, editing, fallback, provenance, and failure handling.
- **REQUIRED QUALITY GATE:** Use `ric-visual-design-review` for independent product-fit and visual critique.
- **REQUIRED QUALITY GATE:** Use `ric-design-qa` when generated screens become implementation references.
- Read relevant platform, accessibility, and implementation skills when the output targets a real codebase.

## Brief And Platform Decision

Before generation, identify:

- Product category, user, job, business goal, and critical flow.
- Target platform: iOS-native, Android-native, cross-platform, or intentionally custom.
- Existing design system, brand assets, navigation model, and accessibility constraints.
- Required states and screens needed to communicate the flow.
- Whether device frames help presentation or obstruct implementation review.

Do not infer a complete product from a single requested screen. Ask or record assumptions for material flow ambiguity.

## Screen And Flow Plan

Generate only the screens needed to understand or implement the requested flow. Include meaningful state coverage such as loading, empty, error, permission, success, and interrupted states when they affect the task.

For new or high-expression work, explore three meaningfully different visual directions before selecting one. Keep the user flow stable while varying hierarchy, navigation framing, spatial language, typography, imagery, and interaction character.

Read [references/platform-and-flow.md](references/platform-and-flow.md) for platform conventions, safe areas, navigation, flow completeness, and category-specific judgment.

## Generation Procedure

1. Retrieve `ric-imagegen-runtime` and select the available generation path.
2. Create a compact app design bible: direction, tokens, type roles, navigation, key components, imagery, icon approach, and state language.
3. Create an asset/screen manifest with purpose, viewport, state, and relationship to the flow.
4. Generate the direction board or highest-risk screen first.
5. Inspect readability, system regions, navigation, component consistency, and product specificity.
6. Generate the remaining necessary screens using the selected design bible.
7. Regenerate targeted failures with a specific correction.
8. Build a flow board or contact sheet for review.

Read [references/generation-and-review.md](references/generation-and-review.md) for prompt structure, continuity, asset quality, regeneration, and evidence.

## Mobile Product Rules

- Respect safe areas, touch targets, content hierarchy, keyboard impact, and likely system behavior.
- Keep navigation understandable and consistent with the selected platform strategy.
- Use realistic information density and readable type at device scale.
- Use imagery, texture, 3D, and decorative assets only when they support product identity or comprehension.
- Device frames are optional presentation tools, not mandatory output.
- Generated text is not authoritative copy. Keep critical labels short and validate them separately.
- Do not ship fake app-store brands, generic placeholder avatars, fabricated metrics, or incoherent screens as final references.

## Independent Review

Hand the brief, platform decision, app design bible, flow board, screen manifest, and selected assets to `ric-visual-design-review`.

If implementation will follow, hand matched screen/state references to `ric-design-qa`.

Use interaction prototypes or browser/device tests to verify behavior. Static screens cannot prove navigation, focus, keyboard, gestures, permissions, or state transitions.

## Exit Criteria

- The selected screen set explains the requested flow without unnecessary screens.
- Platform, navigation, state, and design-system decisions are coherent.
- Critical text and controls are readable at device scale.
- Independent visual review has no unresolved blocking findings.
- Implementation-bound screens have clear viewport and state metadata.
