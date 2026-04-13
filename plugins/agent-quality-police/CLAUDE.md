# CLAUDE.md

## Priority

- Direct system, developer, and user instructions override this file.
- Prefer current local code and current official documentation over memory.
- Load only the smallest relevant skill set for the task.

## Startup Sequence

1. Read [quality-definition](docs/policy/quality-definition.md) when the task needs repository policy context.
2. Read [workflow](docs/policy/workflow.md) when the repository defines one.
3. Load only the relevant skill set from `.claude/skills/`.

## Skill Routing

- Use [quality-index](.claude/skills/quality-index/SKILL.md) when the task spans multiple concerns.
- Use [typescript-zero-bypass](.claude/skills/typescript-zero-bypass/SKILL.md) for `.ts` or `.tsx` changes.
- Use [vite-vitest-tdd](.claude/skills/vite-vitest-tdd/SKILL.md) for Vite or Vitest TDD.
- Use [react-public-api-testing](.claude/skills/react-public-api-testing/SKILL.md) for React behavior tests.

## Quality Rules

- Use behavior-first tests when tests are viable.
- Avoid type bypasses, comment bypasses, config weakening, and fake greens.
- Prefer named types and explicit models over inline structural shortcuts.

## Review Flow

- Before final approval, run the relevant auditors for the actual risk surface.
- Use `bypass-auditor` for typing, config, mocks, helpers, or suspicious diffs.
- Use `tdd-warden` when behavior or tests changed or should have changed.
- Use `pr-gatekeeper` only for final approve-or-reject review.

## Claude Code

- Always-on rules live under `.claude/rules/`.
- Skills live under `.claude/skills/`.
- Claude subagents live under `.claude/agents/`.
- If a skill and a rule both apply, the stricter instruction wins.
- Use the repository workflow in `docs/policy/workflow.md` before finalizing any change.
