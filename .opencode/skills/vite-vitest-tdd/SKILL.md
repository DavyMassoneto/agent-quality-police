---
name: vite-vitest-tdd
description: TDD workflow for Vite and Vitest. Use when adding or fixing behavior in projects that rely on Vitest, especially when you need to distinguish a real green from a fake one.
---

# Objective

Enforce Red -> Green -> Refactor in Vite and Vitest projects without mock fraud, helper noise, or implementation-detail assertions.

## When To Use

- Bug fixes in Vitest projects
- New behavior in Vite applications
- Unit or component tests that should prove public behavior

## When Not To Use

- The repository has no viable automated tests for the surface being changed
- The task is purely documentation with no executable surface

## Workflow

1. Name the behavior to prove.
2. Write the failing test first.
3. Implement the minimum change.
4. Refactor only after the test is green.
5. Reject any helper or mock that weakens the claim.

## Quality Criteria

- Tests read like contract statements.
- Each assertion proves public behavior.
- Mocks exist only to control collaborators, never to replace the core behavior under test.
- Factories stay local and obvious.

## Anti-Patterns

- Writing implementation first and backfilling a confirming test
- Snapshotting everything because the assertion was unclear
- Hiding data setup behind a generic helper with a dozen defaults
- Mocking the exact function whose behavior you claim to prove

## Examples

- Good pure function test: `examples/good/discount.test.ts`
- Good probative mock: `examples/good/checkout-service.test.ts`
- Good direct factory: `examples/good/direct-factory.test.ts`
- Bad implementation-detail test: `examples/bad/implementation-detail.test.ts`
- Bad fraudulent mock: `examples/bad/fraudulent-mock.test.ts`
- Bad helper noise: `examples/bad/helper-noise.test.ts`

## Checklist

- See `checklists/tdd-checklist.md`

## References

- `references/mock-policy.md`
