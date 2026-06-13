# Skill Quality Contract

## Structural Checks

- Folder and frontmatter names match and use lowercase letters, digits, and hyphens.
- Frontmatter contains only `name` and `description`.
- Description starts with `Use when...` and describes triggers rather than workflow.
- `SKILL.md` is concise; detailed material is in one-level references.
- Every referenced local file exists and remains inside an installable boundary.
- `agents/openai.yaml` matches the skill and quotes string values.
- No placeholder, stale path, copied redirect, circular handoff, or contradictory mandatory rule remains.

## Behavioral Checks

- Positive trigger selects the skill.
- Negative trigger excludes it.
- Composition chooses one primary executor and does not let modifiers redirect.
- Pressure scenarios do not bypass review, testing, safety, or evidence.
- When this quality gate is explicitly invoked, missing independent behavior-eval capabilities must be reported accurately. They do not retroactively block ordinary skill-repository editing or static validation.

Record scenario, context, skill version, output, pass/fail reason, and remaining risk.
