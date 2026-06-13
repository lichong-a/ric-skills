# Motion And Assets

Use this reference when the selected direction includes generated assets, photography, video, canvas, WebGL, Three.js, GSAP, Motion, or advanced CSS animation.

## Asset Plan

For each asset, record:

- Purpose and placement.
- Required dimensions, aspect ratio, crop behavior, and theme variants.
- Source: provided, repository, licensed, generated, or edited.
- Alt text or decorative status.
- Loading and performance strategy.
- Owner and destination path.

Use `ric-imagegen-runtime` for image generation and editing. Do not duplicate runtime detection or fallback instructions here.

## Asset Selection

- Prefer assets that reveal the real product, subject, place, or experience.
- Generate custom assets when stock or existing assets cannot express the approved direction.
- Keep generated assets inspectable and implementation-feasible.
- Reject watermarks, accidental text, fake trademarks, distorted UI, and unusable crops.
- Do not ship generic placeholders or fabricated product screenshots as final assets.

## Motion Decision

Add motion only when it communicates at least one of:

- Hierarchy or attention.
- Feedback or state change.
- Orientation or spatial relationship.
- Narrative progression.
- Brand character that remains usable.

If motion exists only because a library is available, remove it.

## Technology Choice

- Prefer CSS transitions and animations for simple state and entry motion.
- Prefer a framework-native motion library for component transitions and gestures.
- Use GSAP for justified timeline, pinning, scrub, or complex sequencing.
- Use Three.js/WebGL for a genuine spatial or interactive requirement.
- Isolate advanced animation and rendering in leaf components with cleanup.
- Avoid multiple animation engines controlling the same property or component.

## Performance And Accessibility

- Respect `prefers-reduced-motion`.
- Provide a usable static state when advanced rendering fails or is disabled.
- Avoid blocking content on nonessential media.
- Reserve layout space to prevent shifts.
- Optimize media formats, resolution, and lazy-loading based on placement.
- Check CPU/GPU cost on representative hardware and mobile viewports.
- Keep controls operable without animation.

## Evidence

Capture:

- Asset manifest and provenance.
- Static screenshots of key states.
- Short interaction evidence for motion behavior.
- Reduced-motion state.
- Performance or build evidence relevant to the chosen technology.
- Known browser or device limitations.

