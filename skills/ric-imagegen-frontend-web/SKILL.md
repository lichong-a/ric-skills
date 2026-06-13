---
name: ric-imagegen-frontend-web
description: Use when generating visual directions, section references, asset concepts, or high-fidelity web comps for landing pages, public product surfaces, portfolios, campaigns, and image-led frontend work.
---

# RIC ImageGen Frontend Web

## Overview

Generate implementation-useful web visual references with clear art direction, product specificity, and controlled variation.

This skill is derived from the web ImageGen workflow in Leonxlnx/taste-skill under the upstream MIT license. It preserves image-first art direction and anti-generic standards while favoring useful, reviewed assets over image count.

## Role

- Act as a **visual executor** for web visual references and concept assets.
- Act as a **modifier** when another skill owns product design or implementation.
- Do not write production frontend code unless another primary executor requests it.
- Do not self-approve generated directions.

## Required Companion Skills

- **REQUIRED IMAGE RUNTIME:** Use `ric-imagegen-runtime` for capability detection, generation, editing, fallback, provenance, and failure handling.
- **REQUIRED QUALITY GATE:** Use `ric-visual-design-review` to select and approve directions.
- **REQUIRED QUALITY GATE:** Use `ric-design-qa` when generated references become an implementation source.

## Brief And Output Plan

Before generating, record:

- Product, audience, page purpose, desired action, and brand constraints.
- Required surfaces or sections and their implementation purpose.
- Existing assets that must be preserved.
- Target viewport, aspect ratio, and whether text must be generated separately.
- Number of directions or assets justified by the decision being made.

Generate the smallest useful set that supports direction selection or implementation. One strong direction board or a few targeted section references may be better than one image per section. Do not generate quantity merely to satisfy a page count.

## Direction Exploration

For new, high-expression, public, campaign, or redesign work, create three meaningfully different directions before selection. Vary:

- Hierarchy and composition.
- Product or subject framing.
- Typography character and density.
- Material, image, and spatial language.
- Motion-implied behavior where relevant.

Do not present palette swaps as separate directions.

Read [references/art-direction.md](references/art-direction.md) when defining visual direction, anti-template standards, typography, hierarchy, and content specificity.

## Generation Procedure

1. Retrieve `ric-imagegen-runtime` and determine the available generation path.
2. Create an asset manifest with purpose, target size, prompt intent, and destination.
3. Generate directions or assets in a deliberate sequence.
4. Inspect every result at full size.
5. Reject unreadable text, fake trademarks, distorted UI, broken anatomy, watermarks, generic filler, or unusable crop behavior.
6. Regenerate only the failed asset or direction with a specific correction.
7. Create a contact sheet or comparison set when selecting among directions.
8. Hand the evidence to independent visual review.

Read [references/generation-plan.md](references/generation-plan.md) for asset planning, prompt construction, continuity, and regeneration decisions.

## Composition Rules

- Reveal the actual product, service, subject, or experience whenever inspection matters.
- Keep the primary message and focal point readable at the target crop.
- Use believable layout hierarchy and implementation-feasible geometry.
- Avoid generated microcopy as a source of truth; overlay critical text in code or design tooling when possible.
- Avoid decorative effects that are unrelated to the brand or task.
- Vary section composition only when it improves narrative rhythm or information clarity.
- Keep related assets coherent without making every frame identical.

## Asset Quality

Generated output must be usable for its stated purpose:

- Correct aspect ratio and sufficient resolution.
- Clear focal point and safe crop region.
- No watermark, fake brand, or accidental readable nonsense.
- No generic placeholder product panels or unverifiable fake UI presented as real.
- Consistent lighting, palette, and visual language across a selected set.
- File names and manifest entries that identify purpose and version.

## Independent Review

Hand the brief, direction set, asset manifest, contact sheet, and rejected/selected rationale to `ric-visual-design-review`.

When assets become a coding reference, hand selected source files and target viewport/state information to `ric-design-qa`.

The generation agent cannot approve its own direction. Address findings and regenerate targeted assets rather than restarting the entire set without cause.

Read [references/review-checklist.md](references/review-checklist.md) before requesting final review.

## Exit Criteria

- The generated set is no larger than required for the decision or implementation task.
- Selected assets are product-specific, usable, and provenance-recorded.
- Independent visual review has no unresolved blocking findings.
- Implementation-bound assets have enough source information for `ric-design-qa`.
