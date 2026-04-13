---
name: typescript-zero-bypass
description: Strong TypeScript modeling without any assertions or fake narrowing. Use for any .ts or .tsx change, especially when the compiler is resisting the intended design.
---

# Objective

Define what acceptable TypeScript looks like in this framework. The compiler is evidence, not an opponent to be silenced.

## When To Use

- Any `.ts` or `.tsx` change.
- Fixing types after a bug or refactor.
- Designing new domain shapes, DTOs, or result states.

## When Not To Use

- The task does not touch TypeScript at all.

## Workflow

1. Name the domain concepts first.
2. Model the allowed states explicitly with interfaces and named unions.
3. Keep absence explicit with `null` when the domain has “no value.”
4. If external input is involved, validate it at the boundary instead of coercing it internally.
5. If the compiler resists, redesign the model or the control flow. Do not cast, fabricate instances, or hide meaning behind abbreviations.

## Quality Criteria

- No `any`
- No `as`, `as const`, chained assertions, angle-bracket assertions, or non-null assertions
- No ts-comment bypasses
- No inline structural types, including private methods, local helpers, and return types
- No inline structural object return types such as `(): { completed: number; total: number }`
- No `Record` or index signatures as generic escape hatches
- No `Map` used to avoid modeling a named input contract
- No `Object.create(SomeClass.prototype)` or equivalent prototype fabrication to fake typed instances
- No `Object.assign(...)` or direct internal field hydration to bypass constructors, factories, or invariants
- No meaningless abbreviations in identifiers, including single-letter callback parameters such as `c`, `x`, or `i` when they do not carry real meaning
- Named types instead of anonymous structural sprawl

## Anti-Patterns

- Adding `if (!value) return fallback` only to narrow a type you modeled poorly
- Smuggling domain uncertainty through `Record<string, string>`
- Smuggling domain uncertainty through `Map<string, string>` in a public or domain-facing signature
- Fabricating a typed instance with `Object.create(SomeClass.prototype)` and then hydrating internal fields
- Returning inline structural objects from private methods or helpers instead of naming the concept
- Writing `this.allChecklists.find((c) => c.id === checklistId)` instead of using a meaningful callback name
- Using a test helper to hide an imprecise type instead of fixing the model

## Hard Cases

- For external input, validate at the edge and convert into explicit internal types.
- For collection lookups, model the input structure explicitly and translate `undefined` to a named result shape before it reaches the domain.
- For literals, prefer explicit unions declared once instead of assertion-based narrowing.
- For framework or class instances, use the real constructor or a real public factory. If the current API makes honest construction impossible, refactor the API instead of fabricating instances.

## Examples

- Good: `examples/good/no-assertion-model.ts`
- Bad: `examples/bad/assertion-shortcuts.ts`

## Checklist

- See `checklists/review-checklist.md`

## References

- `references/modeling-patterns.md`
