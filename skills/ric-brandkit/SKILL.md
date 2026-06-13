---
name: ric-brandkit
description: Use when generating or refining a visual identity system, logo direction, brand board, palette, typography direction, image language, or branded application concepts.
---

# RIC Brandkit

## Overview

Create a coherent identity direction that can guide real product, marketing, and asset work rather than a collection of unrelated logo and mockup images.

This skill is derived from the brandkit workflow in Leonxlnx/taste-skill under the upstream MIT license. It preserves strategy-first identity generation, logo concept methods, system boards, and premium presentation standards while making selection and approval independent.

## Role

- Act as a **visual executor** for identity directions and brand-system assets.
- Act as a **modifier** when another primary executor needs brand guidance.
- Do not replace product design, frontend implementation, or legal trademark review.
- Do not self-approve a brand direction.

## Required Companion Skills

- **REQUIRED IMAGE RUNTIME:** Use `ric-imagegen-runtime` for image generation, editing, fallback, provenance, and failure handling.
- **REQUIRED QUALITY GATE:** Use `ric-visual-design-review` for independent direction selection and brand-system critique.
- **REQUIRED QUALITY GATE:** Use `ric-design-qa` when approved brand assets are applied to a product or frontend.

## Brand Brief

Before generation, record:

- Brand name, category, audience, promise, personality, and desired perception.
- Existing identity assets and elements that must be preserved.
- Competitors, category conventions, differentiation targets, and cultural constraints.
- Required applications, languages, light/dark needs, and accessibility constraints.
- Whether the output is exploratory, presentation-ready, or implementation-ready.

Do not fabricate a brand story from visual fashion alone. Resolve material naming, legal, cultural, or positioning ambiguity before treating a direction as final.

## Direction Exploration

Create three meaningfully different identity directions for new brands or substantial rebrands. Each direction must differ in concept, symbol logic, typography character, composition, image language, and application behavior, not only palette.

Each direction should state:

- Strategic idea and intended perception.
- Logo or mark concept.
- Type and color logic.
- Image and motion language.
- Best-fit product and communication applications.
- Risks, limitations, and similarity concerns.

Read [references/strategy-and-system.md](references/strategy-and-system.md) for concept methods, identity-system decisions, and anti-generic review criteria.

## Generation Procedure

1. Retrieve `ric-imagegen-runtime`.
2. Define the minimum boards and assets needed for direction selection.
3. Generate concept boards before expanding applications.
4. Inspect marks at small size, single color, light/dark, and without presentation effects.
5. Reject unreadable, derivative, accidental, watermark-bearing, or inconsistent output.
6. Select a direction through independent visual review.
7. Generate only the applications needed to prove the selected system.
8. Record prompts, provenance, selected files, rejected directions, and limitations.

Read [references/board-and-review.md](references/board-and-review.md) for board composition, application proof, asset checks, and review evidence.

## Identity Rules

- A logo must work independently of mockup effects.
- Color, typography, imagery, iconography, layout, and motion must express one coherent idea.
- Generated lettering and wordmarks require manual verification and often reconstruction before production use.
- Do not present generated trademarks as legally cleared.
- Do not fill boards with random merchandise or mockups unrelated to the actual brand.
- Avoid generic symbols, arbitrary monograms, fashionable effects, and category-default palettes unless strategically justified.
- Prefer a compact, proven system over a large collection of weak assets.

## Independent Review

Hand the brand brief, direction boards, asset manifest, application proofs, and risk notes to `ric-visual-design-review`.

When the identity is applied to a real product or frontend, hand approved source assets and rendered applications to `ric-design-qa`.

The generation agent cannot issue the final selection. Address findings and regenerate only the affected direction or asset.

## Exit Criteria

- The selected direction is strategically specific and visually coherent.
- Core marks have been inspected without presentation effects.
- Required light/dark, small-size, and application proofs exist.
- Asset provenance and legal/trademark limitations are explicit.
- Independent visual review has no unresolved blocking findings.
