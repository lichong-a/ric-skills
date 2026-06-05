# Page Patterns

Use this reference when selecting content page structures.

## Workbench

The workbench is the default entry page for most admin systems.

Treat the first screen as a productized admin surface. It can use a dashboard hero, command header, or branded overview when the system opens here by default.

Recommended modules:

- Personal summary: avatar, name, role, department, tenant, current status.
- Calendar: projects, tasks, deadlines, meetings, approvals.
- Todo list: pending approvals, tasks, incidents, unread messages.
- Activity feed: team dynamics, operations, workflow updates.
- Quick start: shortcuts to common actions and modules.
- Personalized metrics: role-relevant counts, SLA, anomalies, service health.
- System notices: announcements, maintenance, policy updates.

Rules:

- Show role-specific content. An operator, manager, auditor, and admin should not see identical workbench cards.
- The top region should clarify identity, today's priorities, key risks, and next actions.
- Use brand expression, visual assets, or background texture only when it improves orientation and hierarchy.
- Primary CTAs must be permission-aware and operational, such as create, approve, invite, import, configure, or handle.
- Empty states should suggest next actions.
- Do not create fake vanity metrics without business meaning.
- Avoid repeated generic metric cards with meaningless growth rates.

## Login Page

Use a full-screen or focused shell exception for login.

Required:

- Brand mark/name in the first viewport.
- Clear login form and one primary login CTA.
- Secondary actions such as forgot password, SSO, tenant join/register, help, or security notice when relevant.
- Trust cues such as data security, tenant isolation, audit log, service status, or support channel.
- Existing brand asset or generated visual asset when available.

Rules:

- Login copy should be short, business-specific, and trustworthy.
- Form fields must remain high contrast over visual backgrounds.
- Loading, disabled, validation, expired-session, and authentication-failure states must be designed.
- Avoid generic slogans, random blue-purple gradients, fake logos, and critical text embedded in images.

## Module Homepage

Use when a major module needs an entry page before list/detail workflows.

Required:

- Concise module purpose.
- Primary action and secondary shortcuts.
- Current status summary.
- Recent activity, alerts, or setup progress when useful.

Rules:

- Use `product` visual impact mode: stronger hierarchy and brand rhythm than a table page, less narrative than a public landing page.
- Keep actions immediately reachable.
- Do not hide workflow entry points behind decorative graphics.

## List Page

Use for CRUD and searchable datasets.

Page structure:

1. Breadcrumb/page title.
2. Query card.
3. Table card.
4. Modal/drawer for create/edit/detail when appropriate.

Query card rules:

- Use business query dimensions.
- Keep common filters visible.
- Collapse advanced filters.
- Enter triggers search.
- Reset clears filters and returns page 1.

Table rules:

- Primary create action top-left.
- Batch actions appear only with row selection.
- Refresh, column settings, density, export/import top-right when allowed.
- Sort state is visible.
- Name/title column opens detail.
- Last column contains row actions.
- Pagination by default.

## Detail Page

Use a full page when:

- The object has multiple sections.
- There are child tables, audit logs, timeline, attachments, or related entities.
- Users need to perform follow-up actions.

Use modal/drawer when:

- Detail is short.
- Users need to inspect without losing list context.
- The content is mostly read-only.

Common sections:

- Basic information.
- Current status.
- Key metrics.
- Associated records.
- Operation history.
- Workflow timeline.
- Attachments.
- Permission-aware actions.

Return behavior:

- Preserve list filters, sorting, pagination, and selected tab.

## Personal Center

Entry: avatar dropdown -> personal information.

Sections:

- Basic profile.
- Password change.
- Account security.
- Login records.
- Notification preferences.
- Theme/language preferences when supported.

Rules:

- Separate editable personal fields from read-only organization fields.
- Password change needs old password, new password, confirm password, strength hint, validation, and feedback.
- Security-sensitive changes may require re-authentication.

## Permission Management

Common modules:

- User management.
- Role management.
- Department/organization tree.
- Menu permissions.
- Button/action permissions.
- Data permissions.

Patterns:

- Organization tree + user table.
- Role table + permission drawer.
- Permission tree with checked/indeterminate states.
- Data scope selector: all, department, department and children, self, custom.

Rules:

- Make inherited permissions clear.
- Do not silently grant destructive permissions.
- Separate route/menu/action/data permissions when the system supports them.

## Approval Workflow

Common tabs:

- Pending.
- Processed.
- Initiated.
- CC'd to me.

Detail structure:

- Form data.
- Current node.
- Timeline.
- Comments.
- Attachments.
- Approve/reject/transfer/cancel buttons based on permissions.

Rules:

- Show operation consequences before submission.
- Require reason for reject/return actions.
- Preserve audit trail.

## Dashboard

Use dashboards for operational monitoring, not decorative charts.

Dashboard first screens and big-screen command centers may use `product` or `immersive` visual impact mode when stronger visual hierarchy helps monitoring.

Required qualities:

- Metric definitions are explicit.
- Time range is visible.
- Units are visible.
- Empty/no-data states exist.
- Chart colors match semantic meaning.
- Alerts are actionable.
- Refresh state and abnormal thresholds are visible.
- Drill-down or next action exists for important anomalies when allowed.

Avoid:

- Too many unrelated charts.
- Fake precision.
- Unlabeled trends.
- Decorative charts with no decision value.
- Motion that makes data freshness or abnormal state unclear.

## Settings

Use for system, notification, integration, and parameter configuration.

Rules:

- Group settings by domain.
- Use save/reset per group when possible.
- Include dirty-state behavior.
- Dangerous zone is visually separated and requires confirmation.

## Audit Logs

Filters:

- Time range.
- Operator.
- Module.
- Action.
- Result.
- IP/device when relevant.

Table fields:

- Time.
- Operator.
- Module.
- Action.
- Target.
- Result.
- Details.

Rules:

- Logs should be read-only.
- Export requires permission.
- Detail drawer should show request/response only if safe and sanitized.

## Message Center

Views:

- Unread.
- All.
- Announcements.
- Task reminders.
- System notifications.

Rules:

- Support mark as read.
- Support batch read.
- Link messages to target pages when possible.
- Keep unread badges consistent with global header.

## Import And Export

Import flow:

1. Download template.
2. Upload file.
3. Parse preview.
4. Show validation errors.
5. Confirm import.
6. Show progress/result.
7. Download error rows if needed.

Export flow:

- Use current filters by default.
- Confirm large exports.
- Prefer async task center for large jobs.

## Task Center

Fields:

- Task name.
- Type.
- Status.
- Progress.
- Created by.
- Created time.
- Finished time.
- Result/action.

Rules:

- Provide retry when supported.
- Provide result download for export/import/report tasks.
- Show failure reason.

## Error And Empty Pages

Required states:

- 403 no permission.
- 404 not found.
- 500 server error.
- Network error.
- Login expired.
- Empty data.

Rules:

- Give clear action: back, retry, login again, request permission, create first record.
- Empty states must explain why the state exists and what the user can do next.
- Use existing or generated visual assets for important empty states when they improve comprehension.
- CTA visibility must respect permissions.
- Do not show technical stack traces to normal users.
