# Core Non-Negotiables

- Treat `docs/policy/quality-definition.md` as the canonical quality contract.
- TDD is mandatory when tests are technically viable.
- Never accept passing tests as proof if they do not demonstrate observable behavior.
- Never weaken TypeScript, ESLint, Vitest, Vite, or equivalent configuration to make a change appear green.
- Never introduce bypasses, fake narrowing, or helper noise to hide uncertainty.
- Before finalizing, run the matching audit agents and validate the repository.
