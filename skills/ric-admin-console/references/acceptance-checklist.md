# Acceptance Checklist

Run this before declaring an admin-console task complete.

## Shell

- [ ] The selected layout mode matches the brief or existing system.
- [ ] Sidebar/topbar fixed behavior works without covering content.
- [ ] Logo placement follows the selected layout.
- [ ] Avatar, nickname, settings, and secondary icons are present where required.
- [ ] Avatar dropdown contains personal information, system settings, and logout.
- [ ] Menus support grouping, collapse/expand, active state, disabled/no-permission state, and external-link state when relevant.
- [ ] Breadcrumbs show the current hierarchy and support upward navigation.

## Auth And Permissions

- [ ] Unauthenticated state hides protected menus and actions.
- [ ] Missing-permission state is handled with disabled action, hidden action, or 403 page.
- [ ] Button visibility matches route/menu permissions.
- [ ] Sensitive operations are not only protected by front-end hiding.
- [ ] Token/session expiration has a clear flow.

## Workbench

- [ ] Default workbench exists when the system needs a default page.
- [ ] Workbench first screen uses a dashboard hero, command header, or branded overview when it is the primary entry surface.
- [ ] Workbench cards are role/business-specific.
- [ ] Calendar/todo/activity/quick-start/metrics/notices are meaningful for the domain.
- [ ] Priority metrics, today's work, urgent risks, notices, and quick starts are visually prioritized.
- [ ] Primary CTAs are operational, permission-aware, and not duplicated.
- [ ] Empty states provide useful next actions.

## Login And Branded Entry

- [ ] Login page has a visible brand signal in the first viewport.
- [ ] Login form has clear primary CTA, secondary actions, loading, validation, disabled, expired-session, and authentication-failure states.
- [ ] Login visual asset/background is existing, generated, or deliberately omitted with a reason.
- [ ] Module homepages or onboarding pages use product-level brand expression when they are entry surfaces.
- [ ] Strong visual treatment does not hide core navigation, form, or action paths.

## List Pages

- [ ] Query card exists with business-relevant filters.
- [ ] Search and reset actions work.
- [ ] Enter triggers search where appropriate.
- [ ] Search resets to page 1 unless infinite scroll is used.
- [ ] Table loading, empty, and error states exist.
- [ ] Sortable columns show sort state.
- [ ] Selection appears only when multi-select is supported.
- [ ] Cross-page selection semantics are explicit when supported.
- [ ] Create/batch/delete/export/import actions respect permissions.
- [ ] Refresh and column settings exist when expected.
- [ ] Name/title column opens detail.
- [ ] Row actions are in the final column and do not overcrowd the row.
- [ ] Pagination or infinite-scroll states are complete.

## Modal, Drawer, Form

- [ ] Modal has title, content area, and action area.
- [ ] Modal content scrolls internally after height/width thresholds.
- [ ] Scrollbars do not show when unnecessary.
- [ ] Long forms use drawer or grouped layout.
- [ ] Form validation, loading, submit success, and submit failure states exist.
- [ ] Dangerous actions require confirmation and clear wording.

## Detail And Profile

- [ ] Detail complexity chooses page vs modal/drawer correctly.
- [ ] Detail contains status, basic info, related data, history/activity, and allowed actions.
- [ ] Returning to list preserves filters, sorting, pagination, and tab state when applicable.
- [ ] Personal center includes profile, password change, security/login records, and notification preferences when relevant.

## Visual Quality

- [ ] The UI reads as refined Chinese enterprise admin with productized brand expression where the page type needs it.
- [ ] `utility`, `product`, or `immersive` visual impact mode is appropriate for each major page.
- [ ] Information density is useful but not cramped.
- [ ] Chinese labels are concise and consistent.
- [ ] Primary/semantic colors are consistent.
- [ ] Icons come from one family and icon-only actions have tooltips.
- [ ] No meaningless fake data, `John Doe`, `Acme`, or generic placeholder business values.
- [ ] Empty/error/loading states are visually aligned with the app.
- [ ] Important empty states explain why the state exists and provide permission-aware next actions.
- [ ] High-impact surfaces have clear brand signal, visual hierarchy, and CTA hierarchy without generic slogans.
- [ ] Ordinary CRUD, permission, audit, settings, and detail pages remain utility-first and are not polluted by marketing-page hero patterns.
- [ ] Needed login, empty-state, announcement, onboarding, report, profile, or background assets use existing brand assets or generated bitmap assets instead of generic placeholders.
- [ ] If built-in image generation was unavailable for needed assets, the RIC CLI fallback path was used or the missing `OPENAI_API_KEY` was reported.

## Engineering

- [ ] Existing framework and UI library conventions are respected.
- [ ] Routes, menus, permissions, columns, forms, and status dictionaries use structured data where practical.
- [ ] No duplicated hardcoded menus scattered across pages.
- [ ] Request, loading, and error handling follow local conventions.
- [ ] pnpm is used for Node work unless the repo clearly uses another package manager.
- [ ] Available lint/test/build/static checks pass.
- [ ] Key layouts were visually checked at common desktop sizes such as 1366x768, 1440x900, and 1920x1080 when a runnable app exists.
