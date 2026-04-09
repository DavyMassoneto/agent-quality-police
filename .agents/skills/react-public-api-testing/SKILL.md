---
name: react-public-api-testing
description: Behavior-focused React component testing through the public API. Use when testing components, hooks through components, or rendered output in a way that must survive refactoring.
---

# Objective

Test React through what the user can perceive: roles, names, text, states, and callbacks exposed by the component contract.

## When To Use

- Component tests in React or Vite projects
- Review of suspicious Testing Library queries
- Replacing brittle DOM-detail assertions

## When Not To Use

- Pure domain functions without UI behavior
- Low-level rendering details that are not part of the contract

## Workflow

1. Identify the component’s public contract.
2. Render through the same props a caller would use.
3. Query by role, accessible name, label text, visible text, or user-visible state.
4. Assert the observable result.
5. Reject container selectors and implementation-specific details unless the contract truly exposes them.

## Quality Criteria

- Queries follow the Testing Library priority order.
- Assertions describe visible outcomes.
- The test would stay meaningful after a structural refactor that preserves the UI contract.

## Anti-Patterns

- `container.querySelector` for elements that already have an accessible role
- asserting hook state directly
- asserting CSS class names when a semantic state is available
- clicking internal nodes instead of the public control

## Examples

- Good component and test: `examples/good/primary-button.tsx`, `examples/good/primary-button.test.tsx`
- Bad implementation-detail test: `examples/bad/primary-button.internal.test.tsx`

## Checklist

- See `checklists/query-checklist.md`

## References

- `references/query-order.md`
