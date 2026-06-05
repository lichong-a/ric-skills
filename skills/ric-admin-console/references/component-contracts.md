# Component Contracts

Use these contracts to keep admin UI behavior complete.

## Query Card

Required behavior:

- Visible primary filters.
- Optional advanced filters.
- Search button.
- Reset button.
- Enter key triggers search.
- Loading state during request.
- Search resets pagination to page 1 unless infinite scroll.
- Filters sync to URL or stable store when return-state matters.

Recommended fields:

- Keyword/name/code.
- Status.
- Type/category.
- Owner/department.
- Time range.
- Created/updated by.

## Table

Required behavior:

- Loading state.
- Empty state.
- Error state with retry.
- Sort state.
- Pagination or infinite scroll.
- Column settings.
- Row actions.
- Permission-aware actions.

Column conventions:

- Selection column first only when multi-select exists.
- Name/title second by default.
- Status uses tags/badges.
- Time fields use consistent format.
- Actions last and fixed right when table is wide.

Selection:

- Show selected count.
- Support clear selection.
- Cross-page selection must be explicit.
- Batch actions must be disabled without selection.

Column settings:

- Toggle column visibility.
- Preserve required columns.
- Reset to default.
- Persist preference when the project has user settings storage.

## Pagination

Default behavior:

- Current page.
- Page size.
- Total count.
- Page size changer when total can justify it.

Rules:

- Reset to page 1 after new search.
- Preserve page state when returning from detail.
- Show compact mode when width is limited.

## Modal

Required structure:

- Title.
- Content area.
- Footer/action area.
- Confirm/cancel actions when editable.
- Close behavior.

Overflow:

- Content scrolls internally after 90% viewport height.
- Content scrolls horizontally only when unavoidable and within the content area.
- Do not show scrollbars if not needed.

Rules:

- Keep short forms in modal.
- Do not put full-page workflows in modal.
- Destructive actions require confirmation.

## Drawer

Use for:

- Long forms.
- Detail inspection.
- Side-by-side list/detail workflows.
- Multi-section data.

Rules:

- Use sticky footer for long editable drawers.
- Keep title and primary status visible.
- Preserve page context behind it.

## Form

Required states:

- Initial values.
- Dirty state when relevant.
- Validation errors.
- Disabled fields.
- Loading submit.
- Submit success.
- Submit failure.

Rules:

- Group long forms.
- Align labels consistently.
- Use concise Chinese labels.
- Do not hide required field semantics.
- Provide field-level validation for common errors.
- Provide form-level error for server failures.

## Action Buttons

Placement:

- Page-level primary actions in page/table header.
- Row-level actions in final table column.
- Dangerous actions separated or confirmed.
- Secondary actions can be icons with tooltips.

Rules:

- Disable actions without permission or missing prerequisites.
- Do not show impossible actions.
- Icon-only buttons need accessible labels/tooltips.
- Bulk action availability follows selection state.

## Status Tags

Rules:

- Use semantic colors consistently.
- Same status has same label and color everywhere.
- Avoid too many arbitrary colors.
- Include neutral/default state.

Example semantics:

- Success: enabled, completed, online, approved.
- Warning: pending, waiting, partial.
- Error: failed, rejected, offline, abnormal.
- Neutral: draft, disabled, archived.

## Notifications

Use:

- Toast/message for transient success/failure.
- Inline errors for forms.
- Notification panel for persistent messages.
- Confirm dialog for destructive operations.

Rules:

- Do not use toast as the only validation feedback.
- Keep messages concise and business-specific.
- Long-running operations should show progress or task-center entry.

## Empty State

Required qualities:

- Explain what is empty.
- Offer a next action when allowed.
- Respect permissions. If the user cannot create data, do not show create CTA.
- Avoid decorative emptiness with no instruction.

## Loading State

Rules:

- Use skeletons for page/card/table initial loading where possible.
- Use button loading for submissions.
- Use table loading for data refresh.
- Avoid full-screen loading after the shell has rendered unless route data is genuinely blocking.

## Error State

Rules:

- Give retry for recoverable errors.
- Give re-login for auth expiration.
- Give request-permission or back action for 403.
- Do not expose unsafe technical details.
