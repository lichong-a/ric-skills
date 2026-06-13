---
name: ric-design-taste-frontend
description: Use when creating or substantially redesigning public-facing websites, landing pages, portfolios, product marketing surfaces, or branded frontend experiences where visual direction, interaction craft, and anti-template quality materially affect the outcome.
---

# RIC Design Taste Frontend

For non-trivial delivery, operate as the single primary executor under `ric-delivery-loop`, or as an explicitly selected modifier under another primary. Record the active role and never approve the resulting gates.

## Overview

Create distinctive, product-specific public frontend experiences without turning taste into a fixed visual recipe.

This skill is derived from Leonxlnx/taste-skill under the upstream MIT license. It preserves the upstream focus on anti-slop design, brief inference, visual hierarchy, responsive craft, and purposeful motion while making those capabilities composable and independently reviewable.

## Role

- Act as a **visual executor** when the task owns a public-facing frontend experience.
- Act as a **visual modifier** when another primary executor owns implementation.
- Never redirect or replace the primary domain skill.
- Never approve the final visual result.

## Required Companion Skills

- **REQUIRED QUALITY GATE:** Use `ric-visual-design-review` for independent visual critique.
- **REQUIRED QUALITY GATE:** Use `ric-design-qa` when a design source, screenshot, generated reference, or approved direction exists.
- **REQUIRED IMAGE RUNTIME:** Use `ric-imagegen-runtime` whenever generating or editing visual assets.
- Read the detected framework, animation, accessibility, and component-library skills before implementation.

## Trigger Boundary

Use for:

- Landing pages, marketing sites, portfolios, editorial brand pages, and public product surfaces.
- High-expression login, onboarding, invitation, report-cover, or portal surfaces owned by another primary skill.
- Existing frontend redesigns where visual quality is a primary success criterion.

Do not use as the primary executor for:

- Dense CRUD, permissions, audit, settings, or operational screens.
- Backend-only, infrastructure-only, or documentation-only work.
- Pure image generation without frontend implementation.

When the task includes both expressive and utility surfaces, apply this skill only to the expressive surfaces and preserve the primary executor's utility rules elsewhere.

## Operating Contract

1. Inspect the brief, repository, current visual system, available assets, and existing dependencies.
2. Identify the primary executor and record this skill as either visual executor or modifier.
3. Produce a concise Design Read:

   `Reading this as: <surface> for <audience>, with <brand/product intent>, using <visual direction> at <expression level>.`

4. Define observable acceptance criteria before implementation.
5. Implement the selected direction using the existing stack unless a change is justified and approved.
6. Run builder checks, then hand evidence to the independent visual and fidelity gates.
7. Fix findings and repeat the relevant checks. Do not self-approve.

## Direction Selection

Choose direction from the brief, not from a default palette or fashionable pattern.

Assess:

- Audience, task, trust requirements, and conversion intent.
- Existing brand assets, typography, imagery, and product UI.
- Desired expression: restrained, product-led, editorial, kinetic, immersive, or experimental.
- Content density, accessibility constraints, performance budget, and target viewports.

For new, immersive, image-led, or major redesign work, explore three meaningfully different directions before committing. Differences must affect hierarchy, composition, product framing, material language, or interaction model, not only color.

Read [references/visual-direction.md](references/visual-direction.md) when selecting hierarchy, layout rhythm, typography, materiality, copy, and anti-template patterns.

## Implementation Rules

- Preserve existing framework, router, state, styling, and component conventions unless the task explicitly changes them.
- Use semantic HTML, accessible controls, visible focus, meaningful alt text, and reduced-motion handling.
- Treat responsive layouts as designed states, not scaled desktop screenshots.
- Use a coherent token system for color, type, spacing, radius, shadow, and motion.
- Use real product content and real or generated assets. Do not fabricate fake product screenshots or ship generic placeholder media as final work.
- Use motion only when it communicates hierarchy, feedback, state, orientation, or narrative.
- Use GSAP, Three.js, WebGL, Motion, or CSS animation only when the selected direction and performance budget justify them.
- Avoid introducing a second UI system for isolated components.
- Make loading, empty, error, disabled, hover, focus, and active states intentional when relevant.

Read [references/motion-and-assets.md](references/motion-and-assets.md) when the direction uses ImageGen assets, advanced motion, canvas, WebGL, or 3D.

## Anti-Template Standard

Reject output that could be relabeled for an unrelated product without meaningful changes.

Common warning signs:

- Generic value propositions, fake metrics, generic testimonials, or invented logos.
- Repeated equal cards, repeated split sections, or one composition copied across the page.
- Decorative gradients, glass, glows, marquees, or motion without product meaning.
- A hero with no inspectable product, service, subject, or brand signal.
- Visual novelty that weakens navigation, comprehension, accessibility, or conversion.

Treat these as review evidence, not universal bans. A pattern is acceptable when it has a clear task-specific reason and passes independent review.

## Builder Verification

Before handoff:

- Run the repository's lint, typecheck, tests, and production build when available.
- Open the actual page in a browser and inspect the required viewport/state matrix.
- Verify no overflow, clipped text, broken assets, unreadable controls, or incoherent responsive transitions.
- Verify advanced motion cleans up correctly and respects reduced motion.
- Record the selected direction, generated assets, viewports, states, commands, and known risks.

Read [references/implementation-checks.md](references/implementation-checks.md) for the builder checklist and evidence package.

## Independent Quality Gates

Hand the brief, selected direction, current revision, screenshots, interaction evidence, and builder checklist to:

1. `ric-visual-design-review` for independent product-fit, hierarchy, distinctiveness, and craft scoring.
2. `ric-design-qa` for source-to-render comparison when a source of truth exists.

The implementation agent cannot issue the final visual pass. Address findings, rerun affected checks, and request a fresh review of the updated revision.

## Exit Criteria

- The implementation matches the approved direction and primary executor constraints.
- Required repository checks pass.
- Required viewport and state evidence exists.
- No unresolved blocking findings remain from `ric-visual-design-review` or `ric-design-qa`.
- Any residual risks are explicit and owned.
