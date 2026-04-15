import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { formatInstallResult } from "../../framework/package/lib/cli-output.mjs";
import { installGlobal, resolveCleanupPlan, resolveInstallPlan } from "../../framework/package/lib/install.mjs";

async function writeFixture(packageRoot) {
  await mkdir(path.join(packageRoot, "framework", "entrypoints"), { recursive: true });
  await mkdir(path.join(packageRoot, "framework", "agents", "specs"), { recursive: true });
  await mkdir(path.join(packageRoot, "framework", "agents", "prompts"), { recursive: true });
  await writeFile(
    path.join(packageRoot, "framework", "entrypoints", "policy.md"),
    [
      "## Prioridade",
      "",
      "{{priority_body}}",
      "",
      "## Sequência de Inicialização",
      "",
      "{{startup_sequence_body}}",
      "",
      "## Roteamento de Skills",
      "",
      "{{skill_routing_body}}",
      "",
      "## Regras de Qualidade",
      "",
      "{{quality_rules_body}}",
      "",
      "## Fluxo de Revisão",
      "",
      "{{review_flow_body}}"
    ].join("\n"),
    "utf8"
  );
  await writeFile(
    path.join(packageRoot, "framework", "entrypoints", "opencode.json"),
    '{\n  "$schema": "https://opencode.ai/config.json",\n  "instructions": [\n    "docs/policy/workflow.md"\n  ]\n}\n',
    "utf8"
  );

  await mkdir(path.join(packageRoot, "docs", "policy"), { recursive: true });
  await writeFile(path.join(packageRoot, "docs", "policy", "quality-definition.md"), "quality\n", "utf8");
  await writeFile(path.join(packageRoot, "docs", "policy", "workflow.md"), "workflow\n", "utf8");
  await writeFile(path.join(packageRoot, "docs", "policy", "system-layout.md"), "layout\n", "utf8");

  await mkdir(path.join(packageRoot, "rules"), { recursive: true });
  await mkdir(path.join(packageRoot, "skills", "quality-index"), { recursive: true });
  await writeFile(path.join(packageRoot, "rules", "core.md"), "rule\n", "utf8");
  await writeFile(
    path.join(packageRoot, "skills", "quality-index", "SKILL.md"),
    "---\nname: quality-index\ndescription: skill\n---\n",
    "utf8"
  );
  await writeFile(
    path.join(packageRoot, "framework", "agents", "specs", "implementer.json"),
    JSON.stringify({
      name: "implementer",
      description: "Writes code under policy.",
      promptPath: "framework/agents/prompts/implementer.md",
      claude: { tools: ["Read"], model: "sonnet", skills: ["quality-index"] },
      opencode: { mode: "subagent", model: "anthropic/claude-sonnet-4-20250514" },
      codex: { model: "gpt-5.3-codex-spark" }
    }, null, 2),
    "utf8"
  );
  await writeFile(path.join(packageRoot, "framework", "agents", "prompts", "implementer.md"), "Follow the governance skill stack.\n", "utf8");
}

test("resolveInstallPlan returns the expected home targets for codex", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));

  const plan = resolveInstallPlan(packageRoot, "codex", homeDir);

  assert.equal(plan[0][1], path.join(homeDir, ".codex", "docs", "policy"));
  assert.equal(plan[1][1], path.join(homeDir, ".agents", "skills"));
});

test("resolveInstallPlan returns the expected home targets for opencode", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));

  const plan = resolveInstallPlan(packageRoot, "opencode", homeDir);

  assert.equal(plan[0][1], path.join(homeDir, ".config", "opencode", "docs", "policy"));
  assert.equal(plan[1][1], path.join(homeDir, ".config", "opencode", "skills"));
});

test("resolveCleanupPlan removes legacy Claude AGENTS only when managing the root", async () => {
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));

  assert.deepEqual(resolveCleanupPlan("claude", homeDir, true), [path.join(homeDir, ".claude", "AGENTS.md")]);
  assert.deepEqual(resolveCleanupPlan("claude", homeDir, false), []);
});

test("installGlobal manages Claude, Codex, and OpenCode roots when allowed", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));
  await writeFixture(packageRoot);

  await mkdir(path.join(homeDir, ".claude"), { recursive: true });
  await writeFile(path.join(homeDir, ".claude", "AGENTS.md"), "legacy-claude-agents\n", "utf8");
  await writeFile(path.join(homeDir, ".claude", "CLAUDE.md"), "# Existing Claude Root\n\n- Keep this Claude rule.\n", "utf8");
  await mkdir(path.join(homeDir, ".codex"), { recursive: true });
  await writeFile(path.join(homeDir, ".codex", "AGENTS.md"), "# Existing Codex Root\n\n- Keep this Codex rule.\n", "utf8");
  await mkdir(path.join(homeDir, ".config", "opencode"), { recursive: true });
  await writeFile(path.join(homeDir, ".config", "opencode", "AGENTS.md"), "# Existing OpenCode Root\n\n- Keep this OpenCode rule.\n", "utf8");

  const result = await installGlobal(
    packageRoot,
    [
      { target: "claude", manageGlobalRoot: true },
      { target: "codex", manageGlobalRoot: true },
      { target: "opencode", manageGlobalRoot: true }
    ],
    homeDir
  );

  const installedClaudeRoot = await readFile(path.join(homeDir, ".claude", "CLAUDE.md"), "utf8");
  const installedCodexRoot = await readFile(path.join(homeDir, ".codex", "AGENTS.md"), "utf8");
  const installedOpenCodeRoot = await readFile(path.join(homeDir, ".config", "opencode", "AGENTS.md"), "utf8");

  assert.equal(installedClaudeRoot.includes("Prefira código local atual e documentação oficial atual sobre memória."), true);
  await assert.rejects(readFile(path.join(homeDir, ".claude", "AGENTS.md"), "utf8"));
  assert.equal(installedCodexRoot.includes("Prefira código local atual e documentação oficial atual sobre memória."), true);
  assert.equal(installedOpenCodeRoot.includes("Prefira código local atual e documentação oficial atual sobre memória."), true);
  assert.equal(installedClaudeRoot.includes("Keep this Claude rule."), true);
  assert.equal(installedCodexRoot.includes("Keep this Codex rule."), true);
  assert.equal(installedOpenCodeRoot.includes("Keep this OpenCode rule."), true);
  assert.equal(installedClaudeRoot.includes("<!-- agent-quality-police:start -->"), true);
  assert.equal(installedCodexRoot.includes("<!-- agent-quality-police:start -->"), true);
  assert.equal(installedOpenCodeRoot.includes("<!-- agent-quality-police:start -->"), true);
  assert.equal(installedClaudeRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
  assert.equal(installedCodexRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
  assert.equal(installedOpenCodeRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
  assert.equal(installedClaudeRoot.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(installedCodexRoot.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(installedOpenCodeRoot.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(installedClaudeRoot.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(installedCodexRoot.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(installedOpenCodeRoot.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(installedClaudeRoot.includes("Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados."), true);
  assert.equal(installedCodexRoot.includes("Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados."), true);
  assert.equal(installedOpenCodeRoot.includes("Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados."), true);
  assert.equal(installedClaudeRoot.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(installedCodexRoot.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(installedOpenCodeRoot.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(installedClaudeRoot.includes("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`."), true);
  assert.equal(installedCodexRoot.includes("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`."), true);
  assert.equal(installedOpenCodeRoot.includes("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`."), true);
  assert.equal(installedClaudeRoot.includes("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos."), true);
  assert.equal(installedCodexRoot.includes("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos."), true);
  assert.equal(installedOpenCodeRoot.includes("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos."), true);
  assert.equal(await readFile(path.join(homeDir, ".config", "opencode", "skills", "quality-index", "SKILL.md"), "utf8"), "---\nname: quality-index\ndescription: skill\n---\n");
  assert.equal((await readFile(path.join(homeDir, ".claude", "agents", "implementer.md"), "utf8")).includes("Follow the governance skill stack."), true);
  assert.equal((await readFile(path.join(homeDir, ".codex", "agents", "implementer.toml"), "utf8")).includes('name = "implementer"'), true);
  assert.equal((await readFile(path.join(homeDir, ".config", "opencode", "agents", "implementer.md"), "utf8")).includes("mode: subagent"), true);
  assert.equal(result.manualSteps.length, 0);
  assert.equal(await readFile(path.join(result.backupRoot, ".codex", "AGENTS.md"), "utf8"), "# Existing Codex Root\n\n- Keep this Codex rule.\n");
  assert.equal(await readFile(path.join(result.backupRoot, ".config", "opencode", "AGENTS.md"), "utf8"), "# Existing OpenCode Root\n\n- Keep this OpenCode rule.\n");

  await installGlobal(
    packageRoot,
    [
      { target: "claude", manageGlobalRoot: true },
      { target: "codex", manageGlobalRoot: true },
      { target: "opencode", manageGlobalRoot: true }
    ],
    homeDir
  );

  const rerunClaudeRoot = await readFile(path.join(homeDir, ".claude", "CLAUDE.md"), "utf8");
  const rerunCodexRoot = await readFile(path.join(homeDir, ".codex", "AGENTS.md"), "utf8");
  const rerunOpenCodeRoot = await readFile(path.join(homeDir, ".config", "opencode", "AGENTS.md"), "utf8");

  assert.equal(rerunClaudeRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
  assert.equal(rerunCodexRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
  assert.equal(rerunOpenCodeRoot.split("<!-- agent-quality-police:start -->").length - 1, 1);
});

test("installGlobal emits manual steps when root management is denied", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));
  await writeFixture(packageRoot);

  const result = await installGlobal(
    packageRoot,
    [
      { target: "claude", manageGlobalRoot: false },
      { target: "codex", manageGlobalRoot: false },
      { target: "opencode", manageGlobalRoot: false }
    ],
    homeDir
  );

  assert.equal(result.manualSteps.length, 3);
  await assert.rejects(readFile(path.join(homeDir, ".claude", "agent-quality-police", "CLAUDE.md"), "utf8"));
  await assert.rejects(readFile(path.join(homeDir, ".config", "opencode", "agent-quality-police", "AGENTS.md"), "utf8"));
  assert.equal(result.manualSteps[0].snippet.includes("Carregue o menor conjunto de skills exigido a partir de `skills/` antes de propor edits ou escrever código."), true);
  assert.equal(result.manualSteps[0].snippet.includes("Use [quality-index](skills/quality-index/SKILL.md)"), true);
  assert.equal(result.manualSteps[0].snippet.includes("Use [grounding-first](skills/grounding-first/SKILL.md)"), true);
  assert.equal(result.manualSteps[0].snippet.includes("## Claude Code"), false);
  assert.equal(result.manualSteps[0].snippet.startsWith("## Prioridade"), true);
  assert.equal(result.manualSteps[0].snippet.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(result.manualSteps[0].snippet.includes("Arquivos de responsabilidade única são exigidos"), true);
  assert.equal(result.manualSteps[0].snippet.includes("`helpers.ts`"), true);
  assert.equal(result.manualSteps[0].snippet.includes("parâmetros e propriedades omitíveis"), true);
  assert.equal(result.manualSteps[0].snippet.includes("`T | undefined`"), true);
  assert.equal(result.manualSteps[0].snippet.includes("forma estável de topo"), true);
  assert.equal(result.manualSteps[0].snippet.includes("`T[] | { data: T[]; total: number }`"), true);
  assert.equal(result.manualSteps[0].snippet.includes("Dados de treinamento não são fonte de verdade"), true);
  assert.equal(result.manualSteps[0].snippet.includes("Não invente arquivos, APIs, imports, chaves de config ou comportamento de biblioteca"), true);
  assert.equal(result.manualSteps[0].snippet.includes("Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados."), true);
  assert.equal(result.manualSteps[0].snippet.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(result.manualSteps[0].snippet.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(result.manualSteps[0].snippet.includes("python3 scripts/build_framework.py"), false);
  assert.equal(result.manualSteps[0].snippet.includes("Codex should enter"), false);
  assert.equal(result.manualSteps[0].snippet.includes("OpenCode should enter"), false);
  assert.equal(result.manualSteps[1].snippet.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(result.manualSteps[1].snippet.includes("Arquivos de responsabilidade única são exigidos"), true);
  assert.equal(result.manualSteps[1].snippet.includes("parâmetros e propriedades omitíveis"), true);
  assert.equal(result.manualSteps[1].snippet.includes("forma estável de topo"), true);
  assert.equal(result.manualSteps[1].snippet.includes("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`."), true);
  assert.equal(result.manualSteps[1].snippet.includes("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos."), true);
  assert.equal(result.manualSteps[1].snippet.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(result.manualSteps[1].snippet.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(result.manualSteps[1].snippet.includes("python3 scripts/build_framework.py"), false);
  assert.equal(result.manualSteps[1].snippet.includes("Claude Code should enter"), false);
  assert.equal(result.manualSteps[1].snippet.includes("OpenCode should enter"), false);
  assert.equal(result.manualSteps[2].snippet.includes("Carregue as skills exigidas antes de propor edits ou escrever código."), true);
  assert.equal(result.manualSteps[2].snippet.includes("Arquivos de responsabilidade única são exigidos"), true);
  assert.equal(result.manualSteps[2].snippet.includes("parâmetros e propriedades omitíveis"), true);
  assert.equal(result.manualSteps[2].snippet.includes("forma estável de topo"), true);
  assert.equal(result.manualSteps[2].snippet.includes("Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`."), true);
  assert.equal(result.manualSteps[2].snippet.includes("Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos."), true);
  assert.equal(result.manualSteps[2].snippet.includes("Não substitua invocação de agent de auditoria nominal por autorreview inline."), true);
  assert.equal(result.manualSteps[2].snippet.includes("Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`."), true);
  assert.equal(result.manualSteps[2].snippet.includes("python3 scripts/build_framework.py"), false);
  assert.equal(result.manualSteps[2].snippet.includes("Claude Code should enter"), false);
  assert.equal(result.manualSteps[2].snippet.includes("Codex should enter"), false);
  assert.equal(result.manualSteps[1].destination, path.join(homeDir, ".codex", "AGENTS.md"));
  assert.equal(result.manualSteps[1].snippet.startsWith("## Prioridade"), true);
  assert.equal(result.manualSteps[2].destination, path.join(homeDir, ".config", "opencode", "AGENTS.md"));
  assert.equal(result.manualSteps[2].snippet.startsWith("## Prioridade"), true);
});

test("formatInstallResult renders human-readable manual steps instead of JSON blobs", async () => {
  const rendered = formatInstallResult({
    backupRoot: "/tmp/backup",
    installed: [
      { target: "codex", action: "install", relativeDestination: ".codex/docs/policy" }
    ],
    manualSteps: [
      {
        target: "codex",
        kind: "append_to_agents_md",
        destination: "/Users/davy/.codex/AGENTS.md",
        snippet: "## Priority\n\n- Example policy.\n"
      }
    ]
  });

  assert.equal(rendered.includes("Manual steps:"), true);
  assert.equal(rendered.includes('{\n  "target"'), false);
  assert.equal(rendered.includes("Destination: /Users/davy/.codex/AGENTS.md"), true);
  assert.equal(rendered.includes("```md"), true);
  assert.equal(rendered.includes("## Priority"), true);
});
