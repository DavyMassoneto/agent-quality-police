# Quality Definition

## What Counts as Quality

Quality in this framework is not “the build passed.” Quality means the change is behaviorally proven, type-safe without lies, narrow in scope, and reviewable without detective work.

## Valid Test

A valid test:

- proves behavior that a user, caller, or public contract can observe
- fails for the right reason before implementation
- passes after the smallest responsible change
- stays readable without helper indirection that hides the claim
- does not assert internal implementation details unless the public contract is exactly that detail

A test is invalid if it:

- only mirrors the implementation
- mocks away the behavior that should have been proven
- asserts internal state, hook calls, private methods, or class internals when the public API was available
- passes because the fixture, helper, or environment swallowed the real condition

## Proof of Behavior

Proof of behavior means the evidence survives refactoring that preserves the public contract.

Acceptable proof:

- returned values from a pure function
- rendered output, accessibility tree, and callback effects visible through a component API
- thrown domain errors or documented failure states
- persisted or emitted output that the contract explicitly promises

Weak proof:

- spy counts with no user-visible consequence
- asserting which helper was called
- asserting transient local state when the rendered output already proves the same fact
- broad snapshots that hide the real claim

## Fraud

Fraud is any change that makes tooling quieter without making the system more correct.

Fraud includes:

- `any`
- `as`, `as const`, angle-bracket assertions, chained assertions, and non-null assertions
- `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, `@ts-check`
- disabling ESLint to suppress a local violation
- weakening `tsconfig`, `eslint`, `vite`, `vitest`, or equivalent config to silence a problem
- adding impossible fallback branches, fake narrowing, or defensive code only to satisfy TypeScript
- constructor bypass through `Object.create(SomeClass.prototype)` or equivalent prototype fabrication
- internal field hydration through `Object.assign(...)` or direct assignment to simulate a valid instance without using the real constructor or public factory
- meaningless abbreviations in identifiers that hide domain meaning
- plumbing or persistence names in APIs and helpers when the behavior can be named in domain terms
- heterogeneous unions of unrelated models in a single parameter or return contract when a named domain concept should exist
- unreadable inline comparator callbacks that compress fallback logic, ordering logic, and weak names into one expression
- using `Map` in public or domain-facing contracts to avoid explicit named input modeling
- helper layers that hide what the test is proving
- mocks that replace the exact behavior under test
- “green” tests that would still pass after breaking the actual contract

## Automatic Rejection

Reject immediately when a diff introduces any of the following without an explicit, documented framework-level exception:

- type bypasses
- comment bypasses
- config weakening
- unproven tests
- suspicious helper noise
- meaningless abbreviations in newly introduced identifiers, including single-letter callback parameters such as `c`, `x`, or `i` when they do not carry real meaning
- plumbing or persistence names such as `Join`, `Model`, `Type`, or `listOfAll...` when they leak storage or implementation structure instead of behavior
- heterogeneous unions of unrelated models used as a convenience parameter type instead of a named domain contract
- unreadable inline comparator callbacks such as `sort((sortA, sortB) => (sortA.description || '').localeCompare(sortB.description || ''))`
- narrowing that exists only to appease the compiler
- constructor bypasses, prototype fabrication, or internal field hydration that fabricate class instances without their real invariants
- branching that changes runtime semantics without product or domain justification

## Safe Refactor

A refactor is safe when:

- current behavior is characterized before structural change
- the change preserves public behavior
- any new abstractions remove duplication or clarify boundaries instead of hiding uncertainty
- tests remain behavior-first and minimal

A refactor is unsafe when:

- characterization is skipped
- structural cleanup is mixed with behavior change without clear isolation
- the change introduces generic helpers that centralize confusion instead of meaning

## Acceptable Modeling

Acceptable modeling favors:

- named interfaces for object shapes
- named union types for state and result variants
- explicit nullability instead of implicit missing cases
- domain vocabulary over generic containers
- behavior-oriented names over plumbing or persistence terminology
- Zod only for external input boundaries
- Joi only for environment validation when that boundary exists and matters

Inline structural types are prohibited, including private methods, local helpers, and return types.

Unacceptable modeling includes:

- anonymous structural types in signatures
- inline structural types in local declarations when a named concept exists
- inline structural object return types such as `(): { completed: number; total: number }`
- `Record` or index signatures as generic escape hatches
- `Map` used as a lookup-bag escape hatch in a public or domain-facing contract
- generic “utils” that absorb domain meaning
- function names that leak plumbing or persistence details such as `listOfAllChecklistJoinCategory`
- heterogeneous unions of unrelated models such as `CategoryJoinChecklists | CategoryTypeModel | EconnectInformationModel['category']` when a named domain input should exist

## Acceptable Typing

Acceptable typing:

- makes invalid states hard or impossible to express
- keeps narrowing honest and evidence-based
- keeps imported types and values coherent
- lets the compiler confirm the model instead of being tricked into silence
- uses names that preserve domain meaning instead of meaningless abbreviations
- keeps callbacks and comparators readable instead of compressing fallback-heavy logic into one opaque expression

Unacceptable typing:

- trusts runtime luck over explicit modeling
- forces the compiler with assertions
- broadens types to avoid thinking

## Reviewer Contract

Reviewers in this framework must:

- assume suspicious diffs are wrong until they are proven safe
- cite concrete evidence, not vibes
- demand the smallest correction that removes the risk
- reject softened justifications like “it works locally” or “tests pass now”
- separate factual findings from optional refinements

The required reviewer stance is severe, precise, and unemotional.
