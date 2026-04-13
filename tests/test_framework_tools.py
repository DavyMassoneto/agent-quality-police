from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from framework_tools import (
    BuildError,
    GENERATED_MARKER,
    build_all,
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
            opencode_projected_skill = root / ".opencode" / "skills" / "quality-index" / "SKILL.md"
            self.assertTrue(opencode_projected_skill.exists())
            self.assertIn("name: quality-index", opencode_projected_skill.read_text(encoding="utf-8"))


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

            self.assertTrue(claude_agent.startswith("---\n"))
            self.assertIn("name: implementer", claude_agent)
            self.assertIn("skills:", claude_agent)
            self.assertIn("mode: subagent", opencode_agent)
            self.assertIn('name = "implementer"', codex_agent)
            self.assertNotIn("[[skills.config]]", codex_agent)
            self.assertNotIn(GENERATED_MARKER, claude_agent)

    def test_build_agent_projections_fails_before_reset_when_specs_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            claude_agent = root / ".claude" / "agents" / "existing.md"
            opencode_agent = root / ".opencode" / "agents" / "existing.md"
            codex_agent = root / ".codex" / "agents" / "existing.toml"
            claude_agent.parent.mkdir(parents=True)
            opencode_agent.parent.mkdir(parents=True)
            codex_agent.parent.mkdir(parents=True)
            claude_agent.write_text("keep me\n", encoding="utf-8")
            opencode_agent.write_text("keep me\n", encoding="utf-8")
            codex_agent.write_text("keep me\n", encoding="utf-8")

            with self.assertRaises(BuildError):
                build_agent_projections(root)

            self.assertEqual("keep me\n", claude_agent.read_text(encoding="utf-8"))
            self.assertEqual("keep me\n", opencode_agent.read_text(encoding="utf-8"))
            self.assertEqual("keep me\n", codex_agent.read_text(encoding="utf-8"))


class BuildEntrypointProjectionTests(unittest.TestCase):
    def test_build_all_emits_root_agents_and_claude_from_single_entrypoint_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "docs" / "policy" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
            (root / ".claude" / "rules").mkdir(parents=True)
            (root / ".claude" / "rules" / "typescript-zero-bypass.md").write_text("# Rule\n", encoding="utf-8")
            (root / ".claude" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".claude" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints").mkdir(parents=True)
            (root / "framework" / "entrypoints" / "repo-policy.md").write_text(
                "## Priority\n\n- Shared policy.\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints" / "global-policy.md").write_text(
                "## Priority\n\n- Global policy.\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints" / "opencode.json").write_text(
                json.dumps({"$schema": "https://opencode.ai/config.json", "instructions": ["docs/policy/workflow.md"]}),
                encoding="utf-8",
            )
            (root / "framework" / "agents" / "specs").mkdir(parents=True)
            (root / "framework" / "agents" / "specs" / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet", "skills": ["quality-index"]},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )
            (root / "framework" / "distribution").mkdir(parents=True)
            (root / "framework" / "distribution" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "agent-quality-police",
                        "version": "1.2.3",
                        "description": "Strict governance package.",
                        "author": {"name": "Test Maintainer"},
                        "homepage": "https://example.com/aqp",
                        "repository": "https://example.com/aqp.git",
                        "license": "MIT",
                        "keywords": ["governance", "agents"],
                        "claudeMarketplace": {
                            "name": "agent-quality-police",
                            "owner": {"name": "Test Maintainer"},
                            "metadata": {"description": "Strict governance package.", "version": "1.2.3"},
                        },
                        "codexMarketplace": {
                            "name": "agent-quality-police",
                            "interface": {"displayName": "Agent Quality Police"},
                            "category": "Coding",
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        },
                        "codexInterface": {
                            "displayName": "Agent Quality Police",
                            "shortDescription": "Strict governance package",
                            "longDescription": "Strict governance package for coding agents.",
                            "developerName": "Test Maintainer",
                            "category": "Coding",
                            "capabilities": ["Interactive", "Read", "Write"],
                            "websiteURL": "https://example.com/aqp",
                            "defaultPrompt": ["Audit this repo", "Enforce TDD", "Block typing bypasses"],
                            "brandColor": "#111111",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "framework" / "package" / "bin").mkdir(parents=True)
            (root / "framework" / "package" / "lib").mkdir(parents=True)
            (root / "framework" / "package" / "bin" / "aqp.mjs").write_text("#!/usr/bin/env node\n", encoding="utf-8")
            (root / "framework" / "package" / "lib" / "install.mjs").write_text("export {};\n", encoding="utf-8")

            built_entrypoints, built_skills, built_agents, built_distributions = build_all(root)

            self.assertEqual(["AGENTS.md", "CLAUDE.md", "opencode.json"], built_entrypoints)
            self.assertEqual(["quality-index"], built_skills)
            self.assertEqual(["implementer"], built_agents)
            self.assertEqual(["agent-quality-police"], built_distributions)
            self.assertEqual("# AGENTS.md\n\n## Priority\n\n- Shared policy.\n", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertTrue((root / "CLAUDE.md").read_text(encoding="utf-8").startswith("@AGENTS.md\n"))
            self.assertIn("Always-on rules live under `.claude/rules/`.", (root / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertEqual(
                '{\n  "$schema": "https://opencode.ai/config.json",\n  "instructions": [\n    "docs/policy/workflow.md"\n  ]\n}\n',
                (root / "opencode.json").read_text(encoding="utf-8"),
            )


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
            (root / ".opencode" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".opencode" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / ".claude" / "agents").mkdir(parents=True)
            (root / ".claude" / "agents" / "implementer.md").write_text(
                "---\nname: implementer\ndescription: Writes\n---\nbody\n",
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

    def test_validate_repository_reports_skill_projection_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / ".claude" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".claude" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n\ncanonical\n",
                encoding="utf-8",
            )
            (root / ".agents" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".agents" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n\nstale\n",
                encoding="utf-8",
            )

            result = validate_repository(root)

            self.assertTrue(any("content drift" in error.lower() for error in result.errors))

    def test_validate_repository_reports_claude_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )

            build_agent_projections(root)
            (root / ".claude" / "agents" / "implementer.md").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any(".claude/agents/implementer.md" in error for error in result.errors))

    def test_validate_repository_reports_opencode_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )

            build_agent_projections(root)
            (root / ".opencode" / "agents" / "implementer.md").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any(".opencode/agents/implementer.md" in error for error in result.errors))

    def test_validate_repository_reports_codex_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )

            build_agent_projections(root)
            (root / ".codex" / "agents" / "implementer.toml").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any(".codex/agents/implementer.toml" in error for error in result.errors))

    def test_validate_repository_accepts_freshly_built_agent_projections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )

            build_agent_projections(root)

            result = validate_repository(root)

            self.assertEqual([], result.errors)

    def test_build_skill_projection_overwrites_stale_projection_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_skill = root / ".claude" / "skills" / "react-public-api-testing"
            source_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text(
                "---\nname: react-public-api-testing\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (source_skill / "examples").mkdir()
            (source_skill / "examples" / "sample.tsx").write_text(
                "canonical\n",
                encoding="utf-8",
            )

            projected_skill = root / ".agents" / "skills" / "react-public-api-testing"
            projected_skill.mkdir(parents=True)
            (projected_skill / "SKILL.md").write_text(
                "---\nname: react-public-api-testing\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (projected_skill / "examples").mkdir()
            (projected_skill / "examples" / "sample.tsx").write_text(
                "stale\n",
                encoding="utf-8",
            )

            build_skill_projection(root)

            self.assertEqual(
                "canonical\n",
                (projected_skill / "examples" / "sample.tsx").read_text(encoding="utf-8"),
            )

    def test_build_skill_projection_rewrites_existing_file_after_source_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_skill = root / ".claude" / "skills" / "react-public-api-testing"
            source_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text(
                "---\nname: react-public-api-testing\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (source_skill / "examples").mkdir()
            source_file = source_skill / "examples" / "primary-button.tsx"
            source_file.write_text("first-version\n", encoding="utf-8")

            build_skill_projection(root)

            source_file.write_text("second-version\n", encoding="utf-8")

            build_skill_projection(root)

            self.assertEqual(
                "second-version\n",
                (root / ".agents" / "skills" / "react-public-api-testing" / "examples" / "primary-button.tsx").read_text(
                    encoding="utf-8",
                ),
            )


class DocumentationTests(unittest.TestCase):
    def test_quality_definition_bans_inline_structural_types(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / ".claude" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")

        self.assertIn("Inline structural types are prohibited.", quality_definition)
        self.assertIn("Inline structural types are prohibited.", agents)
        self.assertIn("Prohibit inline structural types.", claude_rule)

    def test_readme_distinguishes_generated_only_reuse_from_framework_development(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Generated-only reuse", readme)
        self.assertIn("Framework development", readme)
        self.assertIn("Do not run `python3 scripts/build_framework.py`", readme)
        self.assertIn("framework/agents/specs/", readme)

    def test_readme_documents_why_codex_projection_omits_skills_config(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("`skills.config`", readme)
        self.assertIn("absolute path", readme)
        self.assertIn("`.agents/skills`", readme)


class PluginDistributionTests(unittest.TestCase):
    def test_build_all_emits_package_ready_plugin_distribution_and_marketplaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "docs" / "policy" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
            (root / ".claude" / "rules").mkdir(parents=True)
            (root / ".claude" / "rules" / "typescript-zero-bypass.md").write_text("# Rule\n", encoding="utf-8")
            (root / ".claude" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".claude" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints").mkdir(parents=True)
            (root / "framework" / "entrypoints" / "repo-policy.md").write_text(
                "## Priority\n\n- Project policy.\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints" / "global-policy.md").write_text(
                "## Priority\n\n- Global install policy.\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints" / "opencode.json").write_text(
                json.dumps({"$schema": "https://opencode.ai/config.json", "instructions": ["docs/policy/workflow.md"]}),
                encoding="utf-8",
            )
            (root / "framework" / "agents" / "specs").mkdir(parents=True)
            (root / "framework" / "agents" / "specs" / "implementer.json").write_text(
                json.dumps(
                    {
                        "name": "implementer",
                        "description": "Writes code under policy.",
                        "prompt": "Follow the governance skill stack.",
                        "claude": {"tools": ["Read"], "model": "sonnet", "skills": ["quality-index"]},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.3-codex-spark"},
                    }
                ),
                encoding="utf-8",
            )
            (root / "framework" / "distribution").mkdir(parents=True)
            (root / "framework" / "distribution" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "agent-quality-police",
                        "version": "1.2.3",
                        "description": "Strict governance package.",
                        "author": {"name": "Test Maintainer"},
                        "homepage": "https://example.com/aqp",
                        "repository": "https://example.com/aqp.git",
                        "license": "MIT",
                        "keywords": ["governance", "agents"],
                        "claudeMarketplace": {
                            "name": "agent-quality-police",
                            "owner": {"name": "Test Maintainer"},
                            "metadata": {"description": "Strict governance package.", "version": "1.2.3"},
                        },
                        "codexMarketplace": {
                            "name": "agent-quality-police",
                            "interface": {"displayName": "Agent Quality Police"},
                            "category": "Coding",
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        },
                        "codexInterface": {
                            "displayName": "Agent Quality Police",
                            "shortDescription": "Strict governance package",
                            "longDescription": "Strict governance package for coding agents.",
                            "developerName": "Test Maintainer",
                            "category": "Coding",
                            "capabilities": ["Interactive", "Read", "Write"],
                            "websiteURL": "https://example.com/aqp",
                            "defaultPrompt": ["Audit this repo", "Enforce TDD", "Block typing bypasses"],
                            "brandColor": "#111111",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "framework" / "package" / "bin").mkdir(parents=True)
            (root / "framework" / "package" / "lib").mkdir(parents=True)
            (root / "framework" / "package" / "bin" / "aqp.mjs").write_text("#!/usr/bin/env node\n", encoding="utf-8")
            (root / "framework" / "package" / "lib" / "install.mjs").write_text("export {};\n", encoding="utf-8")

            built_entrypoints, built_skills, built_agents, built_distributions = build_all(root)

            self.assertEqual(["AGENTS.md", "CLAUDE.md", "opencode.json"], built_entrypoints)
            self.assertEqual(["quality-index"], built_skills)
            self.assertEqual(["implementer"], built_agents)
            self.assertEqual(["agent-quality-police"], built_distributions)

            package_manifest = json.loads(
                (root / "plugins" / "agent-quality-police" / "package.json").read_text(encoding="utf-8")
            )
            package_readme = (root / "plugins" / "agent-quality-police" / "README.md").read_text(encoding="utf-8")
            package_license = (root / "plugins" / "agent-quality-police" / "LICENSE").read_text(encoding="utf-8")
            claude_manifest = json.loads(
                (root / "plugins" / "agent-quality-police" / ".claude-plugin" / "plugin.json").read_text(
                    encoding="utf-8"
                )
            )
            codex_manifest = json.loads(
                (root / "plugins" / "agent-quality-police" / ".codex-plugin" / "plugin.json").read_text(
                    encoding="utf-8"
                )
            )
            claude_marketplace = json.loads(
                (root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
            )
            codex_marketplace = json.loads(
                (root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
            )
            publish_workflow = (root / ".github" / "workflows" / "publish-package.yml").read_text(encoding="utf-8")

            self.assertEqual("agent-quality-police", package_manifest["name"])
            self.assertEqual({"aqp": "bin/aqp.mjs"}, package_manifest["bin"])
            self.assertEqual(["AGENTS.md", "CLAUDE.md", "opencode.json", "docs", ".claude", ".agents", ".codex", ".opencode", ".claude-plugin", ".codex-plugin", "framework", "bin", "lib", "README.md", "LICENSE"], package_manifest["files"])
            self.assertEqual({"node": ">=22.14.0"}, package_manifest["engines"])
            self.assertIn("npx agent-quality-police install", package_readme)
            self.assertIn("MIT License", package_license)
            self.assertEqual("./.claude/skills", claude_manifest["skills"])
            self.assertEqual("./.claude/agents", claude_manifest["agents"])
            self.assertIn("Global install policy.", (root / "plugins" / "agent-quality-police" / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertNotIn("python3 scripts/build_framework.py", (root / "plugins" / "agent-quality-police" / "CLAUDE.md").read_text(encoding="utf-8"))
            self.assertEqual("./.agents/skills", codex_manifest["skills"])
            self.assertEqual("Agent Quality Police", codex_manifest["interface"]["displayName"])
            self.assertEqual("./plugins/agent-quality-police", claude_marketplace["plugins"][0]["source"])
            self.assertEqual("./plugins/agent-quality-police", codex_marketplace["plugins"][0]["source"]["path"])
            self.assertEqual(
                '{\n  "$schema": "https://opencode.ai/config.json",\n  "instructions": [\n    "docs/policy/workflow.md"\n  ]\n}\n',
                (root / "plugins" / "agent-quality-police" / "opencode.json").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "## Priority\n\n- Global install policy.\n",
                (root / "plugins" / "agent-quality-police" / "framework" / "entrypoints" / "global-policy.md").read_text(encoding="utf-8"),
            )
            self.assertIn("npm publish", publish_workflow)
            self.assertIn("plugins/agent-quality-police", publish_workflow)


if __name__ == "__main__":
    unittest.main()
