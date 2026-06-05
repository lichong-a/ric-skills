# Component Contracts

Use these contracts to keep admin UI behavior complete.

## Page Header

Required behavior:

- Current page title appears once.
- Breadcrumb can include the current page label, but it must not create a second large title.
- A module hero or command header can own the page title; if so, the table card title should be compact or omitted.
- Card titles describe the contained dataset or section only when they add information.
- In shadcn projects, use shadcn `Breadcrumb` for hierarchy and one page header or command header for the primary title.
- In shadcn projects, use `CardTitle` only for a distinct section or dataset label; do not repeat the page title in `CardTitle`.

Avoid:

- Breadcrumb current label + H1 + hero/card title all repeating the same text.
- A blue tag or pill repeating the same page title above the same page title.
- Large page title duplicated inside the table card.

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

shadcn mapping:

- Use shadcn `Card` for the query panel, `FieldGroup`/`Field` for form layout, `Input`, `Select`, installed date controls, and `Button` for search/reset.
- Use `InputGroup` when an input contains an icon or inline action.
- Do not build query forms from raw styled divs when the project has shadcn field/form primitives.

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
- Deduplicated create action and selection actions.

Column conventions:

- Selection column first only when multi-select exists.
- Name/title second by default.
- Status uses tags/badges.
- Time fields use consistent format.
- Actions last and fixed right when table is wide.

shadcn mapping:

- Use TanStack Table for table state when selection, sorting, pagination, column visibility, remote loading, or row actions are non-trivial.
- Render with shadcn `Table`, `Checkbox`, `Badge`, `Button`, `DropdownMenu`, `Pagination`, `Skeleton`, `Empty`, and `Alert`/retry controls as appropriate.
- Use shadcn `ScrollArea` or the shared `ric-scroll-region` wrapper for wide or long table regions.
- Keep column definitions structured so column settings, export, detail labels, and table renderers share one model where practical.

Selection:

- Show selected count.
- Support one clear selection action.
- Cross-page selection must be explicit.
- Batch actions must be disabled without selection.
- If delete permission exists, show batch delete when selection exists.

Selection toolbar rules:

- Use one clear action label, default `清空选择`.
- Do not show both `取消选择` and `清空选择`.
- Put batch actions near selected count, not far away from the selection context.
- `批量删除` uses danger styling and requires confirmation.
- Confirmation copy includes selected count and whether selection crosses pages.
- If selection is cross-page, clarify whether the operation applies to selected rows only or all matching records.
- If user lacks delete permission, hide or disable `批量删除` with an explanation.
- Clearing selection must clear all selected row keys, including preserved cross-page keys.

shadcn selection mapping:

- Use `Checkbox` for row and header selection.
- Use a compact selection bar composed from `Card`, `Alert`, or a toolbar region plus `Button` variants.
- Use `Button variant="destructive"` for `批量删除`.
- Use `AlertDialog` for batch delete confirmation and include selected count plus cross-page scope.
- Use one clear button labelled `清空选择`; do not add a second cancel/clear control.

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

shadcn mapping:

- Use `Dialog` for short create/edit/detail flows and `AlertDialog` for destructive confirmation.
- Always include `DialogTitle`/`AlertDialogTitle`; use a visually hidden title only when the visual design truly has an equivalent title.
- Use shadcn `Button` variants and `Spinner` composition for pending states; do not invent `isLoading` props.

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

shadcn mapping:

- Use `Sheet` or `Drawer` based on the project shadcn setup and viewport convention.
- Always include `SheetTitle` or `DrawerTitle`.
- Keep long-form actions in a sticky footer region inside the sheet/drawer content.

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

shadcn mapping:

- Use `FieldGroup`, `Field`, `FieldLabel`, `FieldDescription`, and validation states from the shadcn skill.
- Put validation on `data-invalid` plus `aria-invalid`.
- Use `ToggleGroup` for 2-7 option mode switches; do not loop buttons with manual active styling.

## Action Buttons

Placement:

- Page-level primary actions in page/table header.
- Row-level actions in final table column.
- Dangerous actions separated or confirmed.
- Secondary actions can be icons with tooltips.

Rules:

- Only one create/new button per page-level workflow. For normal CRUD, place it in the table toolbar. For a branded hero/command header, do not repeat the same create action in the table toolbar.
- Primary action label must be specific, such as `新增会员`, `新建角色`, `创建任务`, not generic `新增` when the object type is known.
- Disable actions without permission or missing prerequisites.
- Do not show impossible actions.
- Icon-only buttons need accessible labels/tooltips.
- Bulk action availability follows selection state.

shadcn mapping:

- Use `Button` variants and shadcn icon rules; icons inside buttons use `data-icon`.
- Use `Tooltip` for icon-only actions and `DropdownMenu` for overflow row actions.
- Use semantic variants before custom color classes.

## Toolbar

Top-left:

- Primary create action, unless already owned by a hero/command header.
- Batch actions only after selection exists or as disabled controls with clear reason.
- One selected-count/selection-toolbar region.

Top-right:

- Refresh.
- Column settings.
- Density when supported.
- Export/import when authorized.
- Do not duplicate icon actions with both text and icon-only variants unless they serve different scope.

Rules:

- Refresh appears once per table.
- Column settings appears once per table.
- Do not place create actions on both left and right toolbars.
- Keep destructive batch actions visually separate from neutral tools.

shadcn mapping:

- Compose toolbar actions with `Button`, `DropdownMenu`, `Tooltip`, `Separator`, and `ToggleGroup` when density or view mode is selectable.
- Keep neutral table tools on the right and selection/batch actions near the selected-count region.

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

shadcn mapping:

- Use shadcn `Empty` when installed; otherwise add it through the shadcn CLI or use the existing local empty-state component.
- Pair empty-state CTA with permission checks and avoid raw placeholder markup.

## Loading State

Rules:

- Use skeletons for page/card/table initial loading where possible.
- Use button loading for submissions.
- Use table loading for data refresh.
- Avoid full-screen loading after the shell has rendered unless route data is genuinely blocking.

shadcn mapping:

- Use `Skeleton` for card/table placeholders and `Spinner` composed inside `Button` for submissions.
- Do not build custom `animate-pulse` blocks when shadcn `Skeleton` exists.

## Error State

Rules:

- Give retry for recoverable errors.
- Give re-login for auth expiration.
- Give request-permission or back action for 403.
- Do not expose unsafe technical details.

## Scrollbar And Overflow

Use a consistent admin scrollbar style for scrollable regions.

Targets:

- Sidebar menu.
- Main content container.
- Table horizontal/vertical scroll wrappers.
- Modal body.
- Drawer body.
- Long dropdown/popup lists when locally styled by the project.

Rules:

- Avoid double scrollbars. Usually exactly one vertical scroll owner should exist for the shell content area.
- Do not show scrollbars when content does not overflow.
- Normal cards should not scroll internally unless the card is a bounded widget.
- Track should be transparent.
- Thumb should be semi-transparent, rounded, and thin.
- Show stronger thumb only on hover, focus-within, or active scrolling when CSS/JS supports it.
- Remove scrollbar arrows/buttons.
- Do not use thick, opaque system scrollbars in polished admin surfaces.

Recommended CSS contract:

```css
.ric-scroll-region {
  scrollbar-width: thin;
  scrollbar-color: rgba(15, 23, 42, 0.28) transparent;
}

.ric-scroll-region::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.ric-scroll-region::-webkit-scrollbar-track {
  background: transparent;
}

.ric-scroll-region::-webkit-scrollbar-thumb {
  background: rgba(15, 23, 42, 0.24);
  border-radius: 999px;
  border: 2px solid transparent;
  background-clip: content-box;
}

.ric-scroll-region:hover::-webkit-scrollbar-thumb,
.ric-scroll-region:focus-within::-webkit-scrollbar-thumb {
  background: rgba(15, 23, 42, 0.36);
  border: 2px solid transparent;
  background-clip: content-box;
}

.ric-scroll-region::-webkit-scrollbar-button {
  display: none;
  width: 0;
  height: 0;
}
```

If the app already has a design-system scrollbar token or utility, adapt this contract into that system instead of adding a competing style.
