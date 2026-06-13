# Mobile Platform And Flow

Use this reference when defining mobile platform strategy and required screen coverage.

## Platform Strategy

Choose one:

- iOS-native: align with iOS navigation, system regions, gestures, and interaction expectations.
- Android-native: align with Android navigation, back behavior, system regions, and Material conventions when appropriate.
- Cross-platform neutral: preserve platform usability while using a shared branded system.
- Intentional custom: document why divergence improves the product and how usability remains clear.

## Flow Definition

For each flow, record:

- Entry condition.
- Primary task.
- Required decisions and data.
- Success state.
- Loading, empty, error, permission, interrupted, and recovery states.
- Exit or return behavior.

Generate only the screens needed to communicate these states.

## Navigation

- Keep top-level destinations stable and understandable.
- Make back, close, cancel, and completion behavior explicit.
- Avoid mixing multiple navigation models without a product reason.
- Reserve system and safe-area regions.
- Account for keyboard, sheets, dialogs, and gesture regions.

## Category Judgment

Category conventions are evidence, not recipes:

- Finance and health require high trust, clear status, and careful risk communication.
- Commerce requires product inspection, pricing clarity, and purchase-state feedback.
- Productivity requires scanability, prioritization, and efficient repeated action.
- Social and communication require identity, context, and state clarity.
- Lifestyle products may use stronger imagery, but controls must remain readable.

## Accessibility

- Use readable type and adequate touch targets.
- Preserve contrast and visible focus where applicable.
- Avoid relying on color alone.
- Keep critical content reachable with text scaling and assistive technology.

