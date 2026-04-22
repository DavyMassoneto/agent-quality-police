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
    def test_build_skill_projection_discovers_framework_skills_without_root_projections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill_root = root / "framework" / "skills" / "quality-index"
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

            built_skills = build_skill_projection(root)

            self.assertEqual(["quality-index"], built_skills)
            self.assertFalse((root / ".agents").exists())
            self.assertFalse((root / ".opencode").exists())


class BuildAgentProjectionTests(unittest.TestCase):
    def test_build_agent_projections_discovers_framework_specs_without_root_projections(self) -> None:
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

            built_agents = build_agent_projections(root)

            self.assertEqual(["implementer"], built_agents)
            self.assertFalse((root / ".claude").exists())
            self.assertFalse((root / ".opencode").exists())
            self.assertFalse((root / ".codex").exists())

    def test_build_agent_projections_preserves_proactive_validator_descriptions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "docs" / "policy" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
            (root / "framework" / "rules").mkdir(parents=True)
            (root / "framework" / "rules" / "typescript-zero-bypass.md").write_text("# Rule\n", encoding="utf-8")
            (root / "framework" / "skills" / "quality-index").mkdir(parents=True)
            (root / "framework" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints").mkdir(parents=True)
            (root / "framework" / "entrypoints" / "policy.md").write_text(
                "## Prioridade\n\n{{priority_body}}\n\n## Sequência de Inicialização\n\n{{startup_sequence_body}}\n\n## Roteamento de Skills\n\n{{skill_routing_body}}\n\n## Regras de Qualidade\n\n{{quality_rules_body}}\n\n## Fluxo de Revisão\n\n{{review_flow_body}}\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints" / "opencode.json").write_text(
                json.dumps({"$schema": "https://opencode.ai/config.json", "instructions": ["docs/policy/workflow.md"]}),
                encoding="utf-8",
            )
            spec_dir = root / "framework" / "agents" / "specs"
            spec_dir.mkdir(parents=True)
            (spec_dir / "bypass-auditor.json").write_text(
                json.dumps(
                    {
                        "name": "bypass-auditor",
                        "description": "Use proativamente antes da aprovação final para qualquer revisão de tipagem, config, mock, helper ou diff suspeito.",
                        "prompt": "Audit the diff.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.4-mini"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (spec_dir / "tdd-warden.json").write_text(
                json.dumps(
                    {
                        "name": "tdd-warden",
                        "description": "Use proativamente antes da aprovação final sempre que comportamento mudou, testes mudaram ou testes deveriam ter mudado.",
                        "prompt": "Audit the TDD flow.",
                        "claude": {"tools": ["Read"], "model": "sonnet"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-sonnet-4-20250514"},
                        "codex": {"model": "gpt-5.4-mini"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (spec_dir / "pr-gatekeeper.json").write_text(
                json.dumps(
                    {
                        "name": "pr-gatekeeper",
                        "description": "Use proativamente como porta final de aprovação ou rejeição após os demais auditores exigidos concluírem.",
                        "prompt": "Gate the change.",
                        "claude": {"tools": ["Read"], "model": "opus"},
                        "opencode": {"mode": "subagent", "model": "anthropic/claude-opus-4-1-20250805"},
                        "codex": {"model": "gpt-5.4"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (root / "framework" / "distribution").mkdir(parents=True)
            (root / "framework" / "distribution" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "agent-quality-police",
                        "version": "1.2.3",
                        "description": "Pacote de governança estrito.",
                        "author": {"name": "Test Maintainer"},
                        "homepage": "https://example.com/aqp",
                        "repository": "https://example.com/aqp.git",
                        "license": "MIT",
                        "keywords": ["governance", "agents"],
                        "claudeMarketplace": {
                            "name": "agent-quality-police",
                            "owner": {"name": "Test Maintainer"},
                            "metadata": {"description": "Pacote de governança estrito.", "version": "1.2.3"},
                        },
                        "codexMarketplace": {
                            "name": "agent-quality-police",
                            "interface": {"displayName": "Agent Quality Police"},
                            "category": "Coding",
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        },
                        "codexInterface": {
                            "displayName": "Agent Quality Police",
                            "shortDescription": "Pacote de governança estrito",
                            "longDescription": "Pacote de governança estrito para agents de codificação.",
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

            build_all(root)

            claude_bypass = (root / "plugins" / "agent-quality-police" / "agents" / "bypass-auditor.md").read_text(encoding="utf-8")
            opencode_tdd = (root / "plugins" / "agent-quality-police" / "framework" / "agents" / "specs" / "tdd-warden.json").read_text(encoding="utf-8")
            codex_gatekeeper = (root / "plugins" / "agent-quality-police" / "framework" / "agents" / "specs" / "pr-gatekeeper.json").read_text(encoding="utf-8")

            self.assertIn("Use proativamente antes da aprovação final para qualquer revisão de tipagem, config, mock, helper ou diff suspeito.", claude_bypass)
            self.assertIn("Use proativamente antes da aprovação final sempre que comportamento mudou, testes mudaram ou testes deveriam ter mudado.", opencode_tdd)
            self.assertIn("Use proativamente como porta final de aprovação ou rejeição após os demais auditores exigidos concluírem.", codex_gatekeeper)

    def test_audit_agent_prompts_scope_reviews_to_current_branch_diff(self) -> None:
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        tdd_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "tdd-warden.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("apenas os arquivos alterados no branch corrente", bypass_prompt)
        self.assertIn("branch alvo de merge", bypass_prompt)
        self.assertIn("não vagueie pelos arquivos não tocados", bypass_prompt)
        self.assertIn("apenas os testes alterados e os arquivos de implementação alterados", tdd_prompt)
        self.assertIn("diff do branch corrente", tdd_prompt)
        self.assertIn("avalie apenas o diff contra o branch alvo de merge", gate_prompt)
        self.assertIn("não bloqueie por problemas pré-existentes não relacionados", gate_prompt)

    def test_audit_agent_prompts_explicitly_block_inline_structural_modeling(self) -> None:
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("tipos estruturais inline", bypass_prompt)
        self.assertIn("tipos estruturais anônimos", bypass_prompt)
        self.assertIn("tipos estruturais inline", gate_prompt)
        self.assertIn("tipos estruturais anônimos", gate_prompt)

    def test_audit_agent_prompts_forbid_inventing_local_exceptions(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("a menos que o usuário autorize explicitamente a exceção na tarefa corrente", quality_definition)
        self.assertIn("não invente exceções locais", bypass_prompt)
        self.assertIn("apenas autorização explícita do usuário", bypass_prompt)
        self.assertIn("não invente exceções locais", gate_prompt)
        self.assertIn("apenas autorização explícita do usuário", gate_prompt)
        self.assertIn("Não invente exceções locais à política", implementer_prompt)
        self.assertIn("apenas autorização explícita do usuário", implementer_prompt)

    def test_audit_agent_prompts_hunt_inference_fraud(self) -> None:
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )
        tdd_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "tdd-warden.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("fraude de inferência", bypass_prompt)
        self.assertIn("imports, APIs, métodos, funções ou tipos referenciados que não existem no repositório alterado", bypass_prompt)
        self.assertIn("inferência não verificada", gate_prompt)
        self.assertIn("não empilhe inferências", implementer_prompt)
        self.assertIn("valores esperados foram inferidos", tdd_prompt)

    def test_build_agent_projections_fails_before_reset_when_specs_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            with self.assertRaises(BuildError):
                build_agent_projections(root)


class BuildEntrypointProjectionTests(unittest.TestCase):
    def test_build_all_emits_root_agents_only_from_single_entrypoint_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "docs" / "policy" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
            (root / "framework" / "rules").mkdir(parents=True)
            (root / "framework" / "rules" / "typescript-zero-bypass.md").write_text("# Rule\n", encoding="utf-8")
            (root / "framework" / "skills" / "quality-index").mkdir(parents=True)
            (root / "framework" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints").mkdir(parents=True)
            (root / "framework" / "entrypoints" / "policy.md").write_text(
                "## Prioridade\n\n{{priority_body}}\n\n## Sequência de Inicialização\n\n{{startup_sequence_body}}\n\n## Roteamento de Skills\n\n{{skill_routing_body}}\n\n## Regras de Qualidade\n\n{{quality_rules_body}}\n\n## Fluxo de Revisão\n\n{{review_flow_body}}\n",
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
                        "description": "Pacote de governança estrito.",
                        "author": {"name": "Test Maintainer"},
                        "homepage": "https://example.com/aqp",
                        "repository": "https://example.com/aqp.git",
                        "license": "MIT",
                        "keywords": ["governance", "agents"],
                        "claudeMarketplace": {
                            "name": "agent-quality-police",
                            "owner": {"name": "Test Maintainer"},
                            "metadata": {"description": "Pacote de governança estrito.", "version": "1.2.3"},
                        },
                        "codexMarketplace": {
                            "name": "agent-quality-police",
                            "interface": {"displayName": "Agent Quality Police"},
                            "category": "Coding",
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        },
                        "codexInterface": {
                            "displayName": "Agent Quality Police",
                            "shortDescription": "Pacote de governança estrito",
                            "longDescription": "Pacote de governança estrito para agents de codificação.",
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

            self.assertEqual(["AGENTS.md"], built_entrypoints)
            self.assertEqual(["quality-index"], built_skills)
            self.assertEqual(["implementer"], built_agents)
            self.assertEqual(["agent-quality-police"], built_distributions)
            self.assertIn(
                "Não modifique configuração global, estado de diretório home, contas ou ferramentas fora deste repositório sem permissão explícita do usuário.",
                (root / "AGENTS.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Não publique releases, tags, pacotes ou outros efeitos externos sem permissão explícita do usuário.",
                (root / "AGENTS.md").read_text(encoding="utf-8"),
            )
            self.assertNotIn("Tool-Specific Notes", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("framework/skills/quality-index/SKILL.md", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("framework/skills/grounding-first/SKILL.md", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertFalse((root / "CLAUDE.md").exists())
            self.assertFalse((root / "opencode.json").exists())


class ValidateRepositoryTests(unittest.TestCase):
    def test_validate_repository_passes_for_minimal_consistent_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "framework" / "skills" / "quality-index").mkdir(parents=True)
            (root / "framework" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
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

    def test_validate_repository_reports_tool_specific_runtime_dirs_at_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / ".claude" / "skills" / "quality-index").mkdir(parents=True)
            (root / ".claude" / "skills" / "quality-index" / "SKILL.md").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any("must not exist at repository root" in error.lower() for error in result.errors))

    def test_validate_repository_reports_claude_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
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

            (root / ".claude" / "agents").mkdir(parents=True)
            (root / ".claude" / "agents" / "implementer.md").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any("must not exist at repository root" in error.lower() for error in result.errors))

    def test_validate_repository_reports_opencode_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
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

            (root / ".opencode" / "agents").mkdir(parents=True)
            (root / ".opencode" / "agents" / "implementer.md").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any("must not exist at repository root" in error.lower() for error in result.errors))

    def test_validate_repository_reports_codex_agent_content_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
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

            (root / ".codex" / "agents").mkdir(parents=True)
            (root / ".codex" / "agents" / "implementer.toml").write_text("drift\n", encoding="utf-8")

            result = validate_repository(root)

            self.assertTrue(any("must not exist at repository root" in error.lower() for error in result.errors))

    def test_validate_repository_accepts_freshly_built_agent_projections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Load [quality](docs/policy/quality-definition.md).\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "framework" / "skills" / "quality-index").mkdir(parents=True)
            (root / "framework" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
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
            source_skill = root / "framework" / "skills" / "react-public-api-testing"
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

            built_skills = build_skill_projection(root)

            self.assertEqual(["react-public-api-testing"], built_skills)

    def test_build_skill_projection_rewrites_existing_file_after_source_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_skill = root / "framework" / "skills" / "react-public-api-testing"
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

            built_skills = build_skill_projection(root)

            self.assertEqual(["react-public-api-testing"], built_skills)


class DocumentationTests(unittest.TestCase):
    def test_quality_definition_bans_inline_structural_types(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")

        self.assertIn("Tipos estruturais inline são proibidos", quality_definition)
        self.assertIn("incluindo em métodos privados, helpers locais e tipos de retorno", quality_definition)
        self.assertIn("Tipos estruturais inline são proibidos", agents)
        self.assertIn("Proibido tipos estruturais inline", claude_rule)
        self.assertIn("incluindo em métodos privados, helpers locais e tipos de retorno", claude_rule)

    def test_policy_enforces_single_responsibility_files(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("uma única razão para mudar", quality_definition)
        self.assertIn("uma classe", quality_definition)
        self.assertIn("funções de topo", quality_definition)
        self.assertIn("`helpers.ts`", quality_definition)
        self.assertIn("Arquivos de responsabilidade única são exigidos", agents)
        self.assertIn("`helpers.ts`", agents)
        self.assertIn("uma classe por arquivo", claude_rule)
        self.assertIn("sem funções de topo irmãs", claude_rule)
        self.assertIn("responsabilidade compartilhada", claude_rule)
        self.assertIn("nomes de arquivo genéricos como `helpers.ts`", claude_rule)
        self.assertIn("Uma classe por arquivo sem funções de topo irmãs", zero_bypass_skill)
        self.assertIn("responsabilidade compartilhada", zero_bypass_skill)
        self.assertIn("`helpers.ts`", anti_bypass_skill)
        self.assertIn("múltiplas classes em um arquivo", bypass_prompt)
        self.assertIn("mistura de classe com funções de topo em um arquivo", bypass_prompt)
        self.assertIn("`helpers.ts`", bypass_prompt)
        self.assertIn("violações de responsabilidade de arquivo", gate_prompt)
        self.assertIn("funções de topo", implementer_prompt)
        self.assertIn("`helpers.ts`", implementer_prompt)

    def test_policy_bans_redundant_union_undefined_for_omittable_signatures(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("`result: User | undefined`", quality_definition)
        self.assertIn("`result?: User`", quality_definition)
        self.assertIn("parâmetros e propriedades omitíveis", agents)
        self.assertIn("`T | undefined` em assinaturas de parâmetro e propriedade omitíveis", claude_rule)
        self.assertIn("Use `?` para parâmetros e propriedades omitíveis", zero_bypass_skill)
        self.assertIn("`result: User | undefined`", zero_bypass_skill)
        self.assertIn("`T | undefined` em assinaturas de parâmetro ou propriedade omitíveis", anti_bypass_skill)
        self.assertIn("assinaturas de parâmetro ou propriedade omitíveis", bypass_prompt)
        self.assertIn("`T | undefined`", gate_prompt)
        self.assertIn("`T | undefined`", implementer_prompt)

    def test_policy_bans_overloaded_return_contracts(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        gate_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "pr-gatekeeper.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("uma única forma estável no topo", quality_definition)
        self.assertIn("`IProductionAssetDashboard[] | { data: IProductionAssetDashboard[]; total: number }`", quality_definition)
        self.assertIn("uma forma estável de topo", agents)
        self.assertIn("Proibido contratos de retorno que mudam a forma de topo", claude_rule)
        self.assertIn("Uma forma estável de topo por contrato público", zero_bypass_skill)
        self.assertIn("`T[] | { data: T[]; total: number }`", zero_bypass_skill)
        self.assertIn("uniões de contrato de retorno que mudam a forma de topo", anti_bypass_skill)
        self.assertIn("uniões de contrato de retorno que mudam a forma de topo", bypass_prompt)
        self.assertIn("contratos de retorno que mudam a forma de topo", gate_prompt)
        self.assertIn("formas de topo diferentes do mesmo contrato", implementer_prompt)

    def test_policy_bans_constructor_bypass_and_prototype_fabrication(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )
        implementer_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "implementer.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("constructor bypass", quality_definition)
        self.assertIn("Object.create(SomeClass.prototype)", quality_definition)
        self.assertIn("hidratação de campos internos", quality_definition)
        self.assertIn("Object.create(SomeClass.prototype)", claude_rule)
        self.assertIn("constructor bypass", anti_bypass_skill)
        self.assertIn("fabricação de protótipo", bypass_prompt)
        self.assertIn("Object.create(SomeClass.prototype)", implementer_prompt)
        self.assertIn("bypassar constructors ou factories públicos", implementer_prompt)

    def test_policy_bans_meaningless_abbreviations_in_identifiers(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("abreviações sem significado", quality_definition)
        self.assertIn("parâmetros de callback de letra única como `c`", quality_definition)
        self.assertIn("abreviações sem significado", claude_rule)
        self.assertIn("abreviações sem significado", zero_bypass_skill)
        self.assertIn("Object.create(SomeClass.prototype)", zero_bypass_skill)
        self.assertIn("tipos de retorno estruturais inline", zero_bypass_skill)
        self.assertIn("parâmetros de callback de letra única", anti_bypass_skill)
        self.assertIn("abreviações sem significado", bypass_prompt)

    def test_policy_bans_plumbing_names_and_heterogeneous_model_unions(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("nomes de plumbing ou persistência", quality_definition)
        self.assertIn("listOfAllChecklistJoinCategory", quality_definition)
        self.assertIn("uniões heterogêneas de modelos não relacionados", quality_definition)
        self.assertIn("Join", claude_rule)
        self.assertIn("uniões heterogêneas de modelos não relacionados", zero_bypass_skill)
        self.assertIn("nomes de plumbing", anti_bypass_skill)
        self.assertIn("uniões heterogêneas de modelos", bypass_prompt)

    def test_policy_bans_unreadable_inline_comparator_callbacks(self) -> None:
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "typescript-zero-bypass.md").read_text(encoding="utf-8")
        zero_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "typescript-zero-bypass" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        anti_bypass_skill = (PROJECT_ROOT / "framework" / "skills" / "anti-bypass-audit" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        bypass_prompt = (PROJECT_ROOT / "framework" / "agents" / "prompts" / "bypass-auditor.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("callbacks comparadores inline ilegíveis", quality_definition)
        self.assertIn("sort((sortA, sortB) => (sortA.description || '').localeCompare(sortB.description || ''))", quality_definition)
        self.assertIn("callbacks comparadores inline ilegíveis", claude_rule)
        self.assertIn("sort e filtro", zero_bypass_skill)
        self.assertIn("callbacks comparadores inline", anti_bypass_skill)
        self.assertIn("callbacks comparadores inline", bypass_prompt)

    def test_grounding_rules_and_skill_exist(self) -> None:
        grounding_rule = (PROJECT_ROOT / "framework" / "rules" / "grounding-and-verification.md").read_text(encoding="utf-8")
        grounding_skill = (PROJECT_ROOT / "framework" / "skills" / "grounding-first" / "SKILL.md").read_text(encoding="utf-8")
        quality_definition = (PROJECT_ROOT / "docs" / "policy" / "quality-definition.md").read_text(encoding="utf-8")
        core_non_negotiables = (PROJECT_ROOT / "framework" / "rules" / "core-non-negotiables.md").read_text(encoding="utf-8")

        self.assertIn("Dados de treinamento não são fonte de verdade", grounding_rule)
        self.assertIn("Sem fonte, não há afirmação", grounding_rule)
        self.assertIn("Três perguntas obrigatórias", grounding_rule)
        self.assertIn("Enforce verificação antes de afirmar ou agir", grounding_skill)
        self.assertIn("Hierarquia de Fontes", grounding_skill)
        self.assertIn("Fraude de Inferência", quality_definition)
        self.assertIn("Nunca use dados de treinamento como fonte de verdade", core_non_negotiables)

    def test_runtime_specific_rules_exist_for_claude_and_codex(self) -> None:
        claude_rule = (PROJECT_ROOT / "framework" / "rules" / "claude-code-specific.md").read_text(encoding="utf-8")
        codex_rule = (PROJECT_ROOT / "framework" / "rules" / "codex-specific.md").read_text(encoding="utf-8")
        runtime_notes = (PROJECT_ROOT / "docs" / "policy" / "runtime-notes.md").read_text(encoding="utf-8")

        self.assertIn("Regras Específicas Claude Code", claude_rule)
        self.assertIn("Claude Code lê `CLAUDE.md`, não `AGENTS.md`", claude_rule)
        self.assertIn("code.claude.com/docs", claude_rule)
        self.assertIn("Regras Específicas Codex", codex_rule)
        self.assertIn("`AGENTS.override.md`", codex_rule)
        self.assertIn("32 KiB", codex_rule)
        self.assertIn("developers.openai.com/codex", codex_rule)
        self.assertIn("Claude Code", runtime_notes)
        self.assertIn("Codex", runtime_notes)

    def test_readme_distinguishes_generated_only_reuse_from_framework_development(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Reuso só com arquivos gerados", readme)
        self.assertIn("Desenvolvimento do framework", readme)
        self.assertIn("Não rode `python3 scripts/build_framework.py`", readme)
        self.assertIn("framework/agents/specs/", readme)

    def test_readme_documents_why_codex_projection_omits_skills_config(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("`skills.config`", readme)
        self.assertIn("caminho absoluto", readme)
        self.assertIn("`.agents/skills`", readme)


class PluginDistributionTests(unittest.TestCase):
    def test_build_all_emits_package_ready_plugin_distribution_and_marketplaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "README.md").write_text("# Repo\n", encoding="utf-8")
            (root / "docs" / "policy").mkdir(parents=True)
            (root / "docs" / "policy" / "quality-definition.md").write_text("# Quality\n", encoding="utf-8")
            (root / "docs" / "policy" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
            (root / "framework" / "rules").mkdir(parents=True)
            (root / "framework" / "rules" / "typescript-zero-bypass.md").write_text("# Rule\n", encoding="utf-8")
            (root / "framework" / "skills" / "quality-index").mkdir(parents=True)
            (root / "framework" / "skills" / "quality-index" / "SKILL.md").write_text(
                "---\nname: quality-index\ndescription: root skill\n---\n",
                encoding="utf-8",
            )
            (root / "framework" / "entrypoints").mkdir(parents=True)
            (root / "framework" / "entrypoints" / "policy.md").write_text(
                "## Prioridade\n\n{{priority_body}}\n\n## Sequência de Inicialização\n\n{{startup_sequence_body}}\n\n## Roteamento de Skills\n\n{{skill_routing_body}}\n\n## Regras de Qualidade\n\n{{quality_rules_body}}\n\n## Fluxo de Revisão\n\n{{review_flow_body}}\n",
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
                        "description": "Pacote de governança estrito.",
                        "author": {"name": "Test Maintainer"},
                        "homepage": "https://example.com/aqp",
                        "repository": "https://example.com/aqp.git",
                        "license": "MIT",
                        "keywords": ["governance", "agents"],
                        "claudeMarketplace": {
                            "name": "agent-quality-police",
                            "owner": {"name": "Test Maintainer"},
                            "metadata": {"description": "Pacote de governança estrito.", "version": "1.2.3"},
                        },
                        "codexMarketplace": {
                            "name": "agent-quality-police",
                            "interface": {"displayName": "Agent Quality Police"},
                            "category": "Coding",
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        },
                        "codexInterface": {
                            "displayName": "Agent Quality Police",
                            "shortDescription": "Pacote de governança estrito",
                            "longDescription": "Pacote de governança estrito para agents de codificação.",
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

            self.assertEqual(["AGENTS.md"], built_entrypoints)
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
            publish_workflow = (root / ".github" / "workflows" / "publish-package.yml").read_text(encoding="utf-8")

            self.assertEqual("agent-quality-police", package_manifest["name"])
            self.assertEqual({"aqp": "bin/aqp.mjs"}, package_manifest["bin"])
            self.assertEqual(["AGENTS.md", "CLAUDE.md", "opencode.json", "docs", "rules", "skills", "agents", ".claude-plugin", ".codex-plugin", "framework", "bin", "lib", "README.md", "LICENSE"], package_manifest["files"])
            self.assertEqual({"node": ">=22.14.0"}, package_manifest["engines"])
            self.assertIn("npx agent-quality-police install", package_readme)
            self.assertIn("MIT License", package_license)
            self.assertEqual("./skills", claude_manifest["skills"])
            self.assertEqual("./agents", claude_manifest["agents"])
            packaged_claude = (root / "plugins" / "agent-quality-police" / "CLAUDE.md").read_text(encoding="utf-8")
            packaged_agents = (root / "plugins" / "agent-quality-police" / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Prefira código local atual e documentação oficial atual sobre memória.", packaged_claude)
            self.assertIn("Carregue as skills exigidas antes de propor edits ou escrever código.", packaged_claude)
            self.assertIn("Arquivos de responsabilidade única são exigidos", packaged_claude)
            self.assertIn("`helpers.ts`", packaged_claude)
            self.assertIn("parâmetros e propriedades omitíveis", packaged_claude)
            self.assertIn("`T | undefined`", packaged_claude)
            self.assertIn("uma forma estável de topo", packaged_claude)
            self.assertIn("`T[] | { data: T[]; total: number }`", packaged_claude)
            self.assertIn("a execução deve passar por `implementer`", packaged_claude)
            self.assertIn("Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados.", packaged_claude)
            self.assertIn("Antes de commit, push, merge request, release ou aprovação, valide os receipts exigidos em `.aqp/receipts/`.", packaged_claude)
            self.assertIn("Não substitua invocação de agent de auditoria nominal por autorreview inline.", packaged_claude)
            self.assertIn("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`.", packaged_claude)
            self.assertIn("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos.", packaged_claude)
            self.assertIn("Se `implementer`, algum auditor exigido, ou a validação de receipts não puder rodar no runtime atual, pare e reporte `BLOCKED`.", packaged_claude)
            self.assertIn("skills/grounding-first/SKILL.md", packaged_claude)
            self.assertNotIn("## Claude Code", packaged_claude)
            self.assertNotIn("Always-on rules live under", packaged_claude)
            self.assertNotIn("Skills live under", packaged_claude)
            self.assertNotIn("Claude subagents live under", packaged_claude)
            self.assertNotIn("If a skill and a rule both apply, the stricter instruction wins.", packaged_claude)
            self.assertNotIn("Use the repository workflow in `docs/policy/workflow.md` before finalizing any change.", packaged_claude)
            self.assertIn("Prefira código local atual e documentação oficial atual sobre memória.", packaged_agents)
            self.assertNotIn(
                "Não modifique configuração global, estado de diretório home, contas ou ferramentas fora deste repositório sem permissão explícita do usuário.",
                packaged_agents,
            )
            self.assertNotIn(
                "Não publique releases, tags, pacotes ou outros efeitos externos sem permissão explícita do usuário.",
                packaged_agents,
            )
            self.assertNotIn("python3 scripts/build_framework.py", packaged_claude)
            self.assertNotIn("Codex should enter", packaged_claude)
            self.assertNotIn("OpenCode should enter", packaged_claude)
            self.assertEqual("./skills", codex_manifest["skills"])
            self.assertEqual("Agent Quality Police", codex_manifest["interface"]["displayName"])
            self.assertEqual(
                '{\n  "$schema": "https://opencode.ai/config.json",\n  "instructions": [\n    "docs/policy/workflow.md"\n  ]\n}\n',
                (root / "plugins" / "agent-quality-police" / "opencode.json").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "## Prioridade\n\n{{priority_body}}\n\n## Sequência de Inicialização\n\n{{startup_sequence_body}}\n\n## Roteamento de Skills\n\n{{skill_routing_body}}\n\n## Regras de Qualidade\n\n{{quality_rules_body}}\n\n## Fluxo de Revisão\n\n{{review_flow_body}}\n",
                (root / "plugins" / "agent-quality-police" / "framework" / "entrypoints" / "policy.md").read_text(encoding="utf-8"),
            )
            self.assertIn("npm publish", publish_workflow)
            self.assertIn("plugins/agent-quality-police", publish_workflow)


if __name__ == "__main__":
    unittest.main()
