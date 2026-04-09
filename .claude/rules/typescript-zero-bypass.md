---
paths:
  - "**/*.{ts,tsx}"
---

# TypeScript Zero Bypass

- Prohibit `any`, `as`, `as const`, chained assertions, angle-bracket assertions, and non-null assertions.
- Prohibit `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, and `@ts-check` as escape hatches.
- Prefer named interfaces and named unions over inline structural types.
- Reject `Record` and index signatures when they are used as generic escape hatches.
- Do not add branches or fallback values solely to satisfy the compiler.
- If the type system is resisting, remodel the data instead of coercing it.
