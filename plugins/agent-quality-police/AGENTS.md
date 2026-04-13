# AGENTS.md

## Priority

- Direct system, developer, and user instructions override this file.
- Prefer current local code and current official documentation over memory.
- Treat the required skills and auditors in this file as mandatory workflow requirements.

## Startup Sequence

1. Read [quality-definition](docs/policy/quality-definition.md) when the task needs repository policy context.
2. Read [workflow](docs/policy/workflow.md) when the repository defines one.
3. Load the smallest required skill set from `skills/` before proposing edits or writing code.

## Skill Routing

- Use [quality-index](skills/quality-index/SKILL.md) when the task spans multiple concerns or when you are unsure which validators apply.
- Use [typescript-zero-bypass](skills/typescript-zero-bypass/SKILL.md) for `.ts` or `.tsx` changes.
- Use [vite-vitest-tdd](skills/vite-vitest-tdd/SKILL.md) for Vite or Vitest TDD.
- Use [react-public-api-testing](skills/react-public-api-testing/SKILL.md) for React behavior tests.
- Use [anti-bypass-audit](skills/anti-bypass-audit/SKILL.md) when reviewing diffs, suspicious helpers, weakened configs, or type/config-heavy changes.
- Use [refactoring-with-safety](skills/refactoring-with-safety/SKILL.md) for refactors that are not pure bug fixes.
- Use [governance-installation](skills/governance-installation/SKILL.md) when installing or updating this governance package.

## Quality Rules

- Load the required skills before proposing edits or writing code.
- If a required skill is unavailable in the current runtime, stop and report `BLOCKED`.
- Use behavior-first tests when tests are viable.
- Avoid type bypasses, comment bypasses, config weakening, and fake greens.
- Prefer named types and explicit models over inline structural shortcuts.

## Review Flow

- For code changes, explicitly invoke the required auditors before final approval.
- For code changes, do not finalize until the required auditors have run and their results were reviewed.
- Do not substitute inline self-review for a required audit agent invocation.
- For typing, config, mocks, helpers, or suspicious diffs, run `bypass-auditor`.
- For behavior changes or bug fixes, run `tdd-warden` and `bypass-auditor`.
- For final approval, release, or merge decisions, run `pr-gatekeeper` after the other required auditors.
- If a required skill or auditor cannot run in the current runtime, stop and report `BLOCKED`.
