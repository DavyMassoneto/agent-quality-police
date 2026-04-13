import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { formatInstallResult } from "../../framework/package/lib/cli-output.mjs";
import { installGlobal, resolveCleanupPlan, resolveInstallPlan } from "../../framework/package/lib/install.mjs";

async function writeFixture(packageRoot) {
  await mkdir(path.join(packageRoot, "framework", "entrypoints"), { recursive: true });
  await writeFile(
    path.join(packageRoot, "framework", "entrypoints", "policy.md"),
    [
      "## Priority",
      "",
      "- Policy file: [quality]({{quality_definition_path}})",
      "",
      "## Startup Sequence",
      "",
      "1. Read [workflow]({{workflow_path}}).",
      "2. Load the smallest relevant skill set from `{{primary_skill_root}}`.",
      "",
      "## Mandatory Skill Routing",
      "",
      "- Use [quality-index]({{quality_index_skill_path}}).",
      "",
      "## Repository Layout",
      "",
      "- [system-layout]({{system_layout_path}})",
      "",
      "## Tool-Specific Notes",
      "",
      "- Claude Code should enter through `{{claude_entrypoint_label}}` and `{{claude_rules_root}}`.",
      "- Codex should enter through this file and use `{{codex_skills_root}}` plus `{{codex_agents_root}}`.",
      "- OpenCode should enter through this file and load extra instructions from `{{opencode_config_path}}`."
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

  await mkdir(path.join(packageRoot, ".claude", "rules"), { recursive: true });
  await mkdir(path.join(packageRoot, ".claude", "skills", "quality-index"), { recursive: true });
  await mkdir(path.join(packageRoot, ".claude", "agents"), { recursive: true });
  await writeFile(path.join(packageRoot, ".claude", "rules", "core.md"), "rule\n", "utf8");
  await writeFile(
    path.join(packageRoot, ".claude", "skills", "quality-index", "SKILL.md"),
    "---\nname: quality-index\ndescription: skill\n---\n",
    "utf8"
  );
  await writeFile(path.join(packageRoot, ".claude", "agents", "implementer.md"), "---\nname: implementer\n---\n", "utf8");

  await mkdir(path.join(packageRoot, ".agents", "skills", "quality-index"), { recursive: true });
  await mkdir(path.join(packageRoot, ".codex", "agents"), { recursive: true });
  await writeFile(
    path.join(packageRoot, ".agents", "skills", "quality-index", "SKILL.md"),
    "---\nname: quality-index\ndescription: skill\n---\n",
    "utf8"
  );
  await writeFile(path.join(packageRoot, ".codex", "agents", "implementer.toml"), 'name = "implementer"\n', "utf8");

  await mkdir(path.join(packageRoot, ".opencode", "skills", "quality-index"), { recursive: true });
  await mkdir(path.join(packageRoot, ".opencode", "agents"), { recursive: true });
  await writeFile(
    path.join(packageRoot, ".opencode", "skills", "quality-index", "SKILL.md"),
    "---\nname: quality-index\ndescription: skill\n---\n",
    "utf8"
  );
  await writeFile(path.join(packageRoot, ".opencode", "agents", "implementer.md"), "---\ndescription: implementer\n---\n", "utf8");
}

test("resolveInstallPlan returns the expected home targets for codex", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));

  const plan = resolveInstallPlan(packageRoot, "codex", homeDir);

  assert.equal(plan[0][1], path.join(homeDir, ".codex", "docs", "policy"));
  assert.equal(plan[1][1], path.join(homeDir, ".agents", "skills"));
  assert.equal(plan[2][1], path.join(homeDir, ".codex", "agents"));
});

test("resolveInstallPlan returns the expected home targets for opencode", async () => {
  const packageRoot = await mkdtemp(path.join(os.tmpdir(), "aqp-package-"));
  const homeDir = await mkdtemp(path.join(os.tmpdir(), "aqp-home-"));

  const plan = resolveInstallPlan(packageRoot, "opencode", homeDir);

  assert.equal(plan[0][1], path.join(homeDir, ".config", "opencode", "docs", "policy"));
  assert.equal(plan[1][1], path.join(homeDir, ".config", "opencode", "skills"));
  assert.equal(plan[2][1], path.join(homeDir, ".config", "opencode", "agents"));
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
  await mkdir(path.join(homeDir, ".codex"), { recursive: true });
  await writeFile(path.join(homeDir, ".codex", "AGENTS.md"), "old-codex-agents\n", "utf8");
  await mkdir(path.join(homeDir, ".config", "opencode"), { recursive: true });
  await writeFile(path.join(homeDir, ".config", "opencode", "AGENTS.md"), "old-opencode-agents\n", "utf8");

  const result = await installGlobal(
    packageRoot,
    [
      { target: "claude", manageGlobalRoot: true },
      { target: "codex", manageGlobalRoot: true },
      { target: "opencode", manageGlobalRoot: true }
    ],
    homeDir
  );

  assert.equal((await readFile(path.join(homeDir, ".claude", "CLAUDE.md"), "utf8")).includes("Policy file: [quality](docs/policy/quality-definition.md)"), true);
  await assert.rejects(readFile(path.join(homeDir, ".claude", "AGENTS.md"), "utf8"));
  assert.equal((await readFile(path.join(homeDir, ".codex", "AGENTS.md"), "utf8")).includes("Policy file: [quality](docs/policy/quality-definition.md)"), true);
  assert.equal((await readFile(path.join(homeDir, ".config", "opencode", "AGENTS.md"), "utf8")).includes("Policy file: [quality](docs/policy/quality-definition.md)"), true);
  assert.equal(await readFile(path.join(homeDir, ".config", "opencode", "skills", "quality-index", "SKILL.md"), "utf8"), "---\nname: quality-index\ndescription: skill\n---\n");
  assert.equal(result.manualSteps.length, 0);
  assert.equal(await readFile(path.join(result.backupRoot, ".codex", "AGENTS.md"), "utf8"), "old-codex-agents\n");
  assert.equal(await readFile(path.join(result.backupRoot, ".config", "opencode", "AGENTS.md"), "utf8"), "old-opencode-agents\n");
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
  assert.equal(result.manualSteps[0].snippet.includes("Load the smallest relevant skill set from `skills/`."), true);
  assert.equal(result.manualSteps[0].snippet.includes("Use [quality-index](skills/quality-index/SKILL.md)."), true);
  assert.equal(result.manualSteps[0].snippet.includes("## Claude Code"), true);
  assert.equal(result.manualSteps[0].snippet.startsWith("## Priority"), true);
  assert.equal(result.manualSteps[1].destination, path.join(homeDir, ".codex", "AGENTS.md"));
  assert.equal(result.manualSteps[1].snippet.startsWith("## Priority"), true);
  assert.equal(result.manualSteps[2].destination, path.join(homeDir, ".config", "opencode", "AGENTS.md"));
  assert.equal(result.manualSteps[2].snippet.startsWith("## Priority"), true);
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
