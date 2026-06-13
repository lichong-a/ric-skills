#!/usr/bin/env bash

declare -A SKILLS=(
  [ric-acceptance-validation]="skills/ric-acceptance-validation/SKILL.md"
  [ric-admin-console]="skills/ric-admin-console/SKILL.md"
  [ric-agent-operating-rules]="skills/ric-agent-operating-rules/SKILL.md"
  [ric-api-design]="skills/ric-api-design/SKILL.md"
  [ric-backend-service]="skills/ric-backend-service/SKILL.md"
  [ric-brandkit]="skills/ric-brandkit/SKILL.md"
  [ric-code-review]="skills/ric-code-review/SKILL.md"
  [ric-data-pipeline]="skills/ric-data-pipeline/SKILL.md"
  [ric-delivery-loop]="skills/ric-delivery-loop/SKILL.md"
  [ric-deployment-ops]="skills/ric-deployment-ops/SKILL.md"
  [ric-design-qa]="skills/ric-design-qa/SKILL.md"
  [ric-design-taste-frontend]="skills/ric-design-taste-frontend/SKILL.md"
  [ric-design-taste-frontend-v1]="skills/ric-design-taste-frontend-v1/SKILL.md"
  [ric-docs]="skills/ric-docs/SKILL.md"
  [ric-full-output-enforcement]="skills/ric-full-output-enforcement/SKILL.md"
  [ric-gpt-taste]="skills/ric-gpt-taste/SKILL.md"
  [ric-high-end-visual-design]="skills/ric-high-end-visual-design/SKILL.md"
  [ric-image-to-code]="skills/ric-image-to-code/SKILL.md"
  [ric-imagegen-frontend-mobile]="skills/ric-imagegen-frontend-mobile/SKILL.md"
  [ric-imagegen-frontend-web]="skills/ric-imagegen-frontend-web/SKILL.md"
  [ric-imagegen-runtime]="skills/ric-imagegen-runtime/SKILL.md"
  [ric-independent-review]="skills/ric-independent-review/SKILL.md"
  [ric-industrial-brutalist-ui]="skills/ric-industrial-brutalist-ui/SKILL.md"
  [ric-infra-safety]="skills/ric-infra-safety/SKILL.md"
  [ric-minimalist-ui]="skills/ric-minimalist-ui/SKILL.md"
  [ric-node-pnpm]="skills/ric-node-pnpm/SKILL.md"
  [ric-redesign-existing-projects]="skills/ric-redesign-existing-projects/SKILL.md"
  [ric-requirements-engineering]="skills/ric-requirements-engineering/SKILL.md"
  [ric-security-review]="skills/ric-security-review/SKILL.md"
  [ric-skill-quality]="skills/ric-skill-quality/SKILL.md"
  [ric-solution-design]="skills/ric-solution-design/SKILL.md"
  [ric-stitch-design-taste]="skills/ric-stitch-design-taste/SKILL.md"
  [ric-testing-quality]="skills/ric-testing-quality/SKILL.md"
  [ric-visual-design-review]="skills/ric-visual-design-review/SKILL.md"
)

if [[ $# -eq 0 ]]; then printf "  %s\n" "${!SKILLS[@]}" | sort; exit 0; fi
if [[ -n "${SKILLS[$1]}" ]]; then echo "${SKILLS[$1]}"; exit 0; fi
echo "Unknown skill: $1" >&2
exit 1
