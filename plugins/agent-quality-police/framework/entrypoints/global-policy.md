## Priority

- Direct system, developer, and user instructions override this file.
- Prefer current local code and current official documentation over memory.
- Load only the smallest relevant skill set for the task.

## Quality Rules

- Use behavior-first tests when tests are viable.
- Avoid type bypasses, comment bypasses, config weakening, and fake greens.
- Prefer named types and explicit models over inline structural shortcuts.

## Review Flow

- Before final approval, run the relevant auditors for the actual risk surface.
- Use `bypass-auditor` for typing, config, mocks, helpers, or suspicious diffs.
- Use `tdd-warden` when behavior or tests changed or should have changed.
- Use `pr-gatekeeper` only for final approve-or-reject review.

## Tool-Specific Notes

- Claude Code should enter through `{{claude_entrypoint_label}}` and `{{claude_rules_root}}`.
- Codex should enter through this file and use `{{codex_skills_root}}` plus `{{codex_agents_root}}`.
- OpenCode should enter through this file and load extra instructions from `{{opencode_config_path}}`.
