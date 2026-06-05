# Page Patterns

Use this reference when selecting content page structures.

## Workbench

The workbench is the default entry page for most admin systems.

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
- Empty states should suggest next actions.
- Do not create fake vanity metrics without business meaning.

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

Required qualities:

- Metric definitions are explicit.
- Time range is visible.
- Units are visible.
- Empty/no-data states exist.
- Chart colors match semantic meaning.
- Alerts are actionable.

Avoid:

- Too many unrelated charts.
- Fake precision.
- Unlabeled trends.
- Decorative charts with no decision value.

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
- Do not show technical stack traces to normal users.
