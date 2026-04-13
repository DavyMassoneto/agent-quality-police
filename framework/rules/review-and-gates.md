# Review And Gates

- Run `tdd-warden` for behavior and TDD verification when tests changed or should have changed.
- Run `bypass-auditor` for any TypeScript, lint, config, mock, helper, or suspicious review surface.
- Run `pr-gatekeeper` before publishing or claiming approval.
- Inline self-review does not replace invoking the named audit agents.
- If a required audit agent cannot run, report `BLOCKED` instead of claiming completion.
- Auditor outputs must be concrete, short, evidence-based, and severe.
- A reviewer who cannot prove safety must reject the change.
