"""Shared deterministic routing rules used by evals and delivery validation."""

from __future__ import annotations


ADMIN_UTILITY_TERMS = (
    "utility-first",
    "utility-only",
    "audit-log list",
    "audit log list",
    "dense list",
    "crud list",
    "permissions page",
    "settings page",
)

ADMIN_VISUAL_OVERRIDE_TERMS = (
    "branded",
    "brand",
    "login",
    "workbench",
    "portal",
    "public",
    "immersive",
    "generated asset",
    "visual",
    "redesign",
    "source fidelity",
    "source-to-render",
)

VISUAL_SURFACE_TERMS = (
    "ui",
    "frontend",
    "front-end",
    "react",
    "vue",
    "shadcn",
    "antd",
    "ant design",
    "element plus",
    "naive ui",
    "arco",
    "portal",
    "login",
    "workbench",
    "landing",
    "branded",
    "brand",
    "redesign",
    "dashboard",
    "console",
    "admin",
    "screen",
    "page",
    "component",
    "asset",
    "screenshot",
    "mockup",
)

VISUAL_UTILITY_EXEMPT_TERMS = (
    "utility-first",
    "utility-only",
    "audit-log list",
    "audit log list",
    "dense list",
    "crud list",
    "permissions page",
    "settings page",
    "api-only",
    "backend-only",
    "no ui",
    "no frontend",
)


def admin_requires_visual_work(request: str) -> bool:
    """Visual surfaces override utility terms; only a fully utility scope is exempt."""
    lowered = request.lower()
    if any(term in lowered for term in ADMIN_VISUAL_OVERRIDE_TERMS):
        return True
    return not any(term in lowered for term in ADMIN_UTILITY_TERMS)


def request_indicates_visual_work(request: str) -> bool:
    """Detect visual work across all primary executors, not just ric-admin-console.

    A request with visual surface terms requires visual-review and design-qa gates
    unless it is explicitly scoped to a pure utility or API-only/backend-only task.
    """
    lowered = request.lower()
    if any(term in lowered for term in VISUAL_UTILITY_EXEMPT_TERMS):
        return False
    return any(term in lowered for term in VISUAL_SURFACE_TERMS)
