# Workflow

## Standard Sequence

1. Read `AGENTS.md` and `docs/policy/quality-definition.md`.
2. Load the relevant skill or skill set.
3. Define the behavior to prove.
4. Write or adjust the failing test first when tests are viable.
5. Implement the minimum code needed to pass.
6. Refactor without changing the proven behavior.
7. Run the appropriate audit agents.
8. Validate the repository before commit or publication.

## Required Audit Pairing

- TypeScript or config-heavy change: run `bypass-auditor`.
- New behavior or bug fix with tests: run `tdd-warden` and `bypass-auditor`.
- Final merge or publication decision: run `pr-gatekeeper`.

## Repository Maintenance

- Edit canonical policy and skill sources first.
- Rebuild generated projections with `python3 scripts/build_framework.py` every time canonical framework sources change.
- Validate with `python3 scripts/validate_framework.py`.
- Run `python3 -m unittest tests/test_framework_tools.py` after changing scripts.

## Failure Handling

- If research support is unclear, mark it as unsupported instead of inventing it.
- If a fix is blocked, record the blocker explicitly and stop calling it complete.
- If a generated projection diverges from the canonical source, rebuild before review.
