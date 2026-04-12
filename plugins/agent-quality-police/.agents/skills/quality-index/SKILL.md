---
name: quality-index
description: Navigate this governance framework. Use when the task spans multiple concerns, when you need to choose the right policy skill, or when you need to decide which audit agent must run.
---

# Objective

Use this skill as the entry point to the framework. It maps task types to the right quality policy, examples, and police agents.

## When To Use

- The task touches more than one policy area.
- You are unsure which skill to load first.
- You need to decide which auditor or gatekeeper must run.

## When Not To Use

- The task is already clearly scoped to a single skill and the choice is obvious.

## Workflow

1. Read `docs/policy/quality-definition.md`.
2. Read `docs/policy/workflow.md`.
3. Classify the task.
4. Load only the skills required by that task.
5. Pair the work with the correct audit agent before final approval.

## Routing

- TypeScript modeling or type repair:
  read `../typescript-zero-bypass/SKILL.md`
- Vite or Vitest TDD:
  read `../vite-vitest-tdd/SKILL.md`
- React behavior tests:
  read `../react-public-api-testing/SKILL.md`
- Suspicious diff review:
  read `../anti-bypass-audit/SKILL.md`
- Refactor with legacy uncertainty:
  read `../refactoring-with-safety/SKILL.md`
- Installing or updating this framework:
  read `../governance-installation/SKILL.md`

## Quality Criteria

- The chosen skill set is the smallest set that covers the task.
- The chosen auditors match the actual risk surface.
- Canonical policy stays in `docs/policy/`, not in generated projections.

## Anti-Patterns

- Loading every skill by default.
- Starting implementation before deciding what behavior must be proven.
- Skipping the auditors because the change “looks small.”

## Examples

- Good routing: `examples/good/task-routing.md`
- Bad routing: `examples/bad/task-routing.md`

## Checklist

- See `checklists/routing-checklist.md`

## References

- `references/system-entrypoints.md`
