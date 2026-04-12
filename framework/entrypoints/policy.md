## Priority

- Direct system, developer, and user instructions override this file.
- [`docs/policy/quality-definition.md`]({{quality_definition_path}}) is the canonical definition of quality in this repository.
- If any skill, rule, example, or agent prompt contradicts the quality definition, the quality definition wins.
- Generated projections must not become the source of truth.

## Startup Sequence

1. Read [quality-definition]({{quality_definition_path}}).
2. Read [workflow]({{workflow_path}}).
3. Load the smallest relevant skill set from `{{primary_skill_root}}`.
4. Execute with TDD when tests are viable.
5. Run the matching audit agents before final approval.

## Mandatory Skill Routing

- Use [quality-index]({{quality_index_skill_path}}) first when the task spans multiple concerns.
- Use [typescript-zero-bypass]({{typescript_zero_bypass_skill_path}}) for any `.ts` or `.tsx` change.
- Use [vite-vitest-tdd]({{vite_vitest_tdd_skill_path}}) when working with Vite, Vitest, or unit/component TDD.
- Use [react-public-api-testing]({{react_public_api_testing_skill_path}}) for React component behavior tests.
- Use [anti-bypass-audit]({{anti_bypass_audit_skill_path}}) when reviewing diffs, suspicious helpers, or weakened configs.
- Use [refactoring-with-safety]({{refactoring_with_safety_skill_path}}) for refactors that are not pure bug fixes.
- Use [governance-installation]({{governance_installation_skill_path}}) when installing or updating this framework in another repository.

## Non-Negotiables

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

## Execution Contract

- Fix the root problem, not the symptom.
- Keep tests direct, short, and behavior-based.
- Prefer explicit domain names over generic utilities.
- Keep policy text severe and actionable; do not soften language to preserve agent comfort.
- After any change to canonical framework sources such as `.claude/skills/`, `.claude/rules/`, `docs/policy/`, or `framework/agents/specs/`, run `python3 scripts/build_framework.py` before claiming the repository is consistent.
- After the build step, run `python3 scripts/validate_framework.py`. If scripts changed, run `python3 -m unittest tests/test_framework_tools.py`.

## Audit Flow

- `implementer`: execution agent, allowed to write, never allowed to weaken rules.
- `tdd-warden`: verifies there was a real RED phase and that tests prove behavior.
- `bypass-auditor`: hunts bypasses, fake narrowing, config weakening, helper noise, and non-probative mocks.
- `pr-gatekeeper`: final verdict, does not rewrite code.

## Output Expectations

- Implementation output should state what behavior is covered, what tests were run, and what remains blocked.
- Audit output should list concrete findings with file evidence and required correction.
- Gate output should end with `APPROVED` or `REJECTED`.

## Repository Layout

- [system-layout]({{system_layout_path}})

## Tool-Specific Notes

- Claude Code should enter through `{{claude_entrypoint_label}}` and `{{claude_rules_root}}`.
- Codex should enter through this file and use `{{codex_skills_root}}` plus `{{codex_agents_root}}`.
- OpenCode should enter through this file and load extra instructions from `{{opencode_config_path}}`.
