# AGENTS.md

## Priority

- Direct system, developer, and user instructions override this file.
- [`docs/policy/quality-definition.md`](docs/policy/quality-definition.md) is the canonical definition of quality in this repository.
- If any skill, rule, example, or agent prompt contradicts the quality definition, the quality definition wins.
- Generated projections must not become the source of truth.
- Do not modify machine-level global configuration, home-directory state, accounts, or tools outside this repository without explicit user permission.
- Do not publish releases, tags, packages, or other external side effects without explicit user permission.

## Startup Sequence

1. Read [quality-definition](docs/policy/quality-definition.md).
2. Read [workflow](docs/policy/workflow.md).
3. Load the smallest relevant skill set from `.claude/skills/`.
4. Execute with TDD when tests are viable.
5. Run the matching audit agents before final approval.

## Skill Routing

- Use [quality-index](.claude/skills/quality-index/SKILL.md) first when the task spans multiple concerns.
- Use [typescript-zero-bypass](.claude/skills/typescript-zero-bypass/SKILL.md) for any `.ts` or `.tsx` change.
- Use [vite-vitest-tdd](.claude/skills/vite-vitest-tdd/SKILL.md) when working with Vite, Vitest, or unit/component TDD.
- Use [react-public-api-testing](.claude/skills/react-public-api-testing/SKILL.md) for React component behavior tests.
- Use [anti-bypass-audit](.claude/skills/anti-bypass-audit/SKILL.md) when reviewing diffs, suspicious helpers, or weakened configs.
- Use [refactoring-with-safety](.claude/skills/refactoring-with-safety/SKILL.md) for refactors that are not pure bug fixes.
- Use [governance-installation](.claude/skills/governance-installation/SKILL.md) when installing or updating this framework in another repository.

## Quality Rules

- TDD is mandatory when tests are technically viable.
- A passing test suite without behavior proof is not a green build.
- `any`, type assertions, non-null assertions, ts-comment bypasses, and lint/config weakening are automatic failures.
- `Map` in public or domain-facing contracts is suspicious by default and must be treated as a modeling bypass unless a stronger repository rule explicitly allows it.
- Helpers, factories, mocks, branches, or narrowing added only to silence the type system or to make tests easier are automatic failures.
- Zod is allowed only at external input boundaries.
- Joi is allowed only for environment validation when it is genuinely needed.
- Strong named types are required.
- Inline structural types are prohibited.
- Reviewers must reject suspicious diffs instead of “accepting with caveats.”

## Review Flow

- Fix the root problem, not the symptom.
- Keep tests direct, short, and behavior-based.
- Prefer explicit domain names over generic utilities.
- Keep policy text severe and actionable; do not soften language to preserve agent comfort.
- After any change to canonical framework sources such as `framework/skills/`, `framework/rules/`, `docs/policy/`, or `framework/agents/specs/`, run `python3 scripts/build_framework.py` before claiming the repository is consistent.
- After the build step, run `python3 scripts/validate_framework.py`. If scripts changed, run `python3 -m unittest tests/test_framework_tools.py` and `node --test tests/node/install.test.mjs`.
- Use `bypass-auditor` for typing, config, mocks, helpers, or suspicious diffs.
- Use `tdd-warden` when behavior or tests changed or should have changed.
- Use `pr-gatekeeper` only for final approve-or-reject review.
