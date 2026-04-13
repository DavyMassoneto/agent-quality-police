---
paths:
  - "**/*.{ts,tsx}"
---

# TypeScript Zero Bypass

- Prohibit `any`, `as`, `as const`, chained assertions, angle-bracket assertions, and non-null assertions.
- Prohibit `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, and `@ts-check` as escape hatches.
- Prohibit inline structural types, including in private methods, local helpers, and return types.
- Require named interfaces and named unions instead of inline structural types.
- Prohibit `Object.create(SomeClass.prototype)` and equivalent prototype fabrication to fake typed instances.
- Prohibit `Object.assign(...)` or direct internal field hydration when used to bypass constructors, factories, or invariants.
- Reject `Record` and index signatures when they are used as generic escape hatches.
- Do not add branches or fallback values solely to satisfy the compiler.
- If the type system is resisting, remodel the data instead of coercing it.
