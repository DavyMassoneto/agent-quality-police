# Bad Install Sequence

1. Copy only `.agents/skills/` because it “already works in Codex.”
2. Skip `.claude/skills/` and `framework/agents/specs/`.
3. Edit generated agent files directly.
4. Publish without rebuilding.

Why this is bad:

- The canonical source is gone.
- The next update cannot be regenerated safely.
- Different tools will drift apart.
