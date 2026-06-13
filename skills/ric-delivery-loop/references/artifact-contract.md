# Delivery Artifact Contract

Store transient run artifacts under `.ric-work/<run-id>/`. Projects must ignore this directory by default. Commit only deliberately selected, redacted delivery artifacts.

## Canonical Files

```text
.ric-work/<run-id>/
  run.json
  requirements.md
  acceptance.json
  traceability.json
  risk-register.json
  design.md
  dispatch/*.json
  review-results/*.json
  adjudication-results/*.json
  test-plan.json
  test-results/*.json
  evidence-manifest.json
  handoff.md
  live-eval-result.json        # optional final behavior evaluation
  live-eval-evidence/*         # optional retained live-eval evidence
```

Machine contracts use JSON and the schemas under `schemas/`. Markdown is for human-readable requirements, design, and handoff only.

`run.json` records lifecycle state, capabilities, selected skills with `active_role`, actor identities, final source revision, artifact versions, gate iteration counts, run epoch, degraded-mode state, and an ordered event history. Reworked gates must preserve failure, fix, invalidation, and re-pass events instead of rewriting history into a clean snapshot.

`evidence-manifest.json` maps acceptance criteria and evidence paths plus SHA-256 hashes to the final verified revision. Environment-variable names may be recorded; values and secrets must never be persisted.

Every canonical JSON artifact is bound to `run_id`. Source-bound gates and
evidence bind to the final source revision; requirements and design reviews bind
to the current artifact version. Evidence paths remain inside the run directory
and match retained SHA-256 hashes. Optional live-eval results must bind to the
same run and revision when present, but they are not required for ordinary
repository validation, commits, or releases.

## Dispatch Packet

Every independent agent or isolated reviewer receives a self-contained JSON packet:

```json
{
  "run_id": "run-identifier",
  "dispatch_id": "stable dispatch packet identifier",
  "invocation_id": "unique per-actor invocation identifier",
  "capability_route": "gate capability route this dispatch targets",
  "role": "reviewer-role",
  "actor_id": "independent-actor-id",
  "fresh_context": true,
  "read_only": true,
  "objective": "bounded objective",
  "scope": ["owned paths or artifacts"],
  "non_goals": ["explicit exclusions"],
  "source_revision": "immutable revision",
  "artifact_version": "immutable artifact version",
  "constraints": ["safety and independence constraints"],
  "required_skills": ["required skills"],
  "capabilities": ["available capabilities"],
  "expected_output": "schema or report contract"
}
```

Packets must not leak the intended conclusion. Before handoff, run secret scanning and `scripts/validate-delivery-run.py`.

Every dispatch packet carries `dispatch_id` (the stable packet identifier),
`invocation_id` (a unique per-actor invocation identifier), and
`capability_route` (the gate capability route the dispatch targets). Each
dispatched actor records `dispatch_id`, `invocation_id`, and
`capability_route` on the result it produces so every review, test, and
adjudication result traces back to the exact packet and route that produced it.
The Required Dispatch Skill Mapping table names the required skills by
`capability_route`.

Gate actors must use the role assigned to their gate. A packet cannot relabel a
code reviewer as a test executor or use one role's smaller skill set to bypass
the gate's required skills. The validator combines gate and role requirements,
and rejects a role that does not match the actor's assigned gate.

## Required Dispatch Skill Mapping

| Gate | Required skills in the dispatched context |
| --- | --- |
| Requirements review | `ric-independent-review`, `ric-requirements-engineering`, primary domain skill |
| Requirements security review | `ric-independent-review`, `ric-security-review`, primary domain skill, and `ric-infra-safety` or other safety skills when relevant |
| Design review | `ric-independent-review`, `ric-solution-design`, primary domain skill |
| Design security review | `ric-independent-review`, `ric-solution-design`, `ric-security-review`, primary domain skill, and relevant safety skills; may count as one of the two design reviewers only with this dual-role loadout |
| Visual review | `ric-independent-review`, `ric-visual-design-review`, relevant visual/UI skills |
| Design QA | `ric-independent-review`, `ric-design-qa`, primary UI skill |
| Code review | `ric-independent-review`, `ric-code-review`, primary domain skill |
| Security review | `ric-independent-review`, `ric-security-review`, primary domain skill, and relevant security/infrastructure skills |
| Test execution | `ric-testing-quality`, primary domain skill, relevant framework testing skills |
| Acceptance validation | `ric-independent-review`, `ric-acceptance-validation`, primary domain and browser/runtime skills |

Passing test results retain at least one evidence reference. Every acceptance
coverage entry must include the evidence IDs declared by its matching
acceptance criterion; unrelated evidence cannot substitute for the declared
proof. Gate-scoped lifecycle events, including invalidation events, always name
a known gate.

Recognized review, test, dispatch, live-eval, and adjudication JSON files must
pass their schemas before they can contribute to a gate. Non-object or malformed
auxiliary artifacts are findings, never ignored witnesses. A `fix-applied`
event is bound to a declared fixer and the final revision, and invalidates all
source-bound gates until current passes are recorded. Required adjudication
targets the exact exhausted or conflicted gate and cannot pass the run with a
blocked, failed, or undeclared adjudicator result.

Every review, test, and adjudication result records the dispatch context that
produced it: `loaded_skills` (the skills actually loaded into the actor's
context), `actor_role` (the gate role the actor performed), `dispatch_id`,
`invocation_id`, `capability_route`, `fresh_context`, and `read_only`.
These fields bind each result to the packet and route that created it, so a
gate decision is never attributed to a context that did not perform it.

## Typed Evidence Binding

Each evidence item binds to its gate, the producer actor (`actor_role` and
`actor_id`), the invocation (`dispatch_id`/`invocation_id`), the suite or
acceptance ID it satisfies, the artifact version or source revision it covers,
the evidence type, the evidence path inside the run directory, and the SHA-256
of the retained file. A single generic document cannot satisfy every review,
test, and acceptance gate; evidence is typed and scoped to the gate that
produced it.

Test evidence records the command or test entry that ran, the process exit code,
and the transcript or report hash. Screenshots prove visual state only and
cannot stand in for functional test or interaction acceptance evidence.
Interaction acceptance requires browser action, assertion, and trace evidence.
Requirements and design `artifact_versions` are SHA-256 content hashes of the
artifact, not free-form labels.