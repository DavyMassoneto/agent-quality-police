from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from framework_tools import (  # type: ignore
    GENERATED_MARKER,
    build_agent_projections,
    build_skill_projection,
    validate_repository,
)


class BuildSkillProjectionTests(unittest.TestCase):
    def test_build_skill_projection_copies_claude_skills_to_agents_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill_root = root / ".claude" / "skills" / "quality-index"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: entry point\n---\n\nUse this skill.\n",
                encoding="utf-8",
            )
            (skill_root / "references").mkdir()
            (skill_root / "references" / "map.md").write_text(
                "# Reference\n",
                encoding="utf-8",
            )

            build_skill_projection(root)

            projected_skill = root / ".agents" / "skills" / "quality-index" / "SKILL.md"
            self.assertTrue(projected_skill.exists())
            self.assertIn("name: quality-index", projected_skill.read_text(encoding="utf-8"))
            projected_reference = root / ".agents" / "skills" / "quality-index" / "references" / "map.md"
            self.assertTrue(projected_reference.exists())


class BuildAgentProjectionTests(unittest.TestCase):
    def test_build_agent_projections_emits_tool_specific_agent_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {
                            "tools": ["Read", "Write", "Edit"],
                            "permissionMode": "acceptEdits",
                            "model": "sonnet",
                            "skills": ["quality-index", "typescript-zero-bypass"],
                        },
                        "opencode": {
                            "mode": "subagent",
                            "model": "anthropic/claude-sonnet-4-20250514",
                            "temperature": 0.1,
                            "permission": {"edit": "allow", "bash": "allow", "webfetch": "deny"},
                        },
                        "codex": {
                            "model": "gpt-5.3-codex-spark",
                            "model_reasoning_effort": "medium",
                            "sandbox_mode": "workspace-write",
                        },
                    }
                ),
                encoding="utf-8",
            )

            build_agent_projections(root)

            claude_agent = (root / ".claude" / "agents" / "implementer.md").read_text(encoding="utf-8")
            opencode_agent = (root / ".opencode" / "agents" / "implementer.md").read_text(encoding="utf-8")
            codex_agent = (root / ".codex" / "agents" / "implementer.toml").read_text(encoding="utf-8")

            self.assertIn("name: implementer", claude_agent)
            self.assertIn("skills:", claude_agent)
            self.assertIn("mode: subagent", opencode_agent)
            self.assertIn('name = "implementer"', codex_agent)
            self.assertIn(GENERATED_MARKER, claude_agent)


class ValidateRepositoryTests(unittest.TestCase):
    def test_validate_repository_passes_for_minimal_consistent_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / ".claude" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".claude" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / ".agents" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".agents" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / ".claude" / "agents").mkdir(parents=True)
            (root / ".claude" / "agents" / "implementer.md").write_text(
                f"{GENERATED_MARKER}\n---\nname: implementer\ndescription: Writes\n---\nbody\n",
                encoding="utf-8",
            )
            (root / ".opencode" / "agents").mkdir(parents=True)
            (root / ".opencode" / "agents" / "implementer.md").write_text(
                f"{GENERATED_MARKER}\n---\ndescription: Writes\nmode: subagent\n---\nbody\n",
                encoding="utf-8",
            )
            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "implementer.toml").write_text(
                'name = "implementer"\ndescription = "Writes"\ndeveloper_instructions = """body"""\n',
                encoding="utf-8",
            )

            result = validate_repository(root)

            self.assertEqual([], result.errors)

    def test_validate_repository_reports_placeholder_and_missing_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text("TODO\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any("placeholder" in error.lower() for error in result.errors))


if __name__ == "__main__":
    unittest.main()
