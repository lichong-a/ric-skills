---
name: ric-solution-design
description: Use when approved requirements need an implementation-ready product, architecture, data, API, visual, operational, or migration design before coding begins.
---
# RIC Solution Design

Create an inspectable design that traces to approved requirements and can be independently reviewed.

## Procedure

1. Pin the approved requirements artifact version.
2. Inspect existing architecture and conventions before selecting technologies or patterns.
3. Define components, boundaries, data flow, interfaces, state transitions, permissions, failure modes, observability, rollout, rollback, and test strategy as relevant.
4. Record alternatives and decisions. Do not disguise defaults as user requirements.
5. Split implementation into work packages with owners, dependencies, allowed scope, and integration order.
6. For high-visual work, produce three materially different directions and use relevant visual, ImageGen, Creative Production, or Product Design capabilities when available.
7. Dispatch two fresh-context design reviewers that load `ric-independent-review`, `ric-solution-design`, and the primary domain skill. Every non-trivial task also requires a design-security reviewer loading `ric-independent-review`, `ric-solution-design`, `ric-security-review`, the primary domain skill, and relevant safety skills; it may count as one of the two design reviewers when its dispatch covers both roles. Add visual, data, or operations specialists as relevant.
8. Use a separate fixer, then re-review. Never self-approve.

Read [references/design-contract.md](references/design-contract.md) before finalizing the design.

## Capability Routes

- Creative Production: brand direction, logo exploration, moodboards, scene/shot exploration, and ImageGen direction boards. Record outputs as design inputs, not final approval.
- Product Design: user flows, product experience critique, prototypes, and design-source review. Feed approved outputs into design QA.
- Build Web Data Visualization: dashboards, charts, maps, command centers, architecture diagrams, and data narratives. Record metric semantics and interaction contracts.
- Codex Security or equivalent: threat modeling, diff scanning, finding validation, and security evidence.
- OpenAI Developers / Agents SDK or equivalent: optional live-eval adapters and agentic application architecture.

Detect capabilities before use. If unavailable, record a concrete fallback or `BLOCKED`; never claim a plugin or tool ran when it did not.

## Exit

Exit only when requirements are traced, risks and tradeoffs are explicit, reviewers pass the pinned design version, and no unresolved `S0` or `S1` remains. After three failed loops, return `ESCALATE`.
