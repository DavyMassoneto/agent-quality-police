import { existsSync } from "node:fs";
import { cp, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const PACKAGE_NAME = "agent-quality-police";

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

function homePath(homeDir, ...segments) {
  return path.join(homeDir, ...segments);
}

function packagePath(packageRoot, ...segments) {
  return path.join(packageRoot, ...segments);
}

function targetConfigRoot(target, homeDir) {
  if (target === "claude") {
    return homePath(homeDir, ".claude");
  }
  if (target === "codex") {
    return homePath(homeDir, ".codex");
  }
  if (target === "opencode") {
    return homePath(homeDir, ".config", "opencode");
  }
  throw new Error(`Unsupported target: ${target}`);
}

export function supportedTargets() {
  return ["claude", "codex", "opencode"];
}

async function loadEntrypointPolicy(packageRoot) {
  return (await readFile(packagePath(packageRoot, "framework", "entrypoints", "policy.md"), "utf8")).trimEnd();
}

function renderTemplate(content, replacements) {
  let rendered = content;
  while (true) {
    let updated = rendered;
    for (const [key, value] of Object.entries(replacements)) {
      updated = updated.replaceAll(`{{${key}}}`, value);
    }
    if (updated === rendered) {
      return updated;
    }
    rendered = updated;
  }
}

function entrypointReplacements({
  qualityDefinitionPath,
  workflowPath,
  primarySkillRoot,
  skillRoot,
  systemLayoutPath,
  priorityBody,
  startupSequenceBody,
  skillRoutingBody,
  qualityRulesBody,
  reviewFlowBody,
  toolSpecificNotes
}) {
  return {
    quality_definition_path: qualityDefinitionPath,
    workflow_path: workflowPath,
    primary_skill_root: primarySkillRoot,
    quality_index_skill_path: `${skillRoot}/quality-index/SKILL.md`,
    typescript_zero_bypass_skill_path: `${skillRoot}/typescript-zero-bypass/SKILL.md`,
    vite_vitest_tdd_skill_path: `${skillRoot}/vite-vitest-tdd/SKILL.md`,
    react_public_api_testing_skill_path: `${skillRoot}/react-public-api-testing/SKILL.md`,
    anti_bypass_audit_skill_path: `${skillRoot}/anti-bypass-audit/SKILL.md`,
    refactoring_with_safety_skill_path: `${skillRoot}/refactoring-with-safety/SKILL.md`,
    governance_installation_skill_path: `${skillRoot}/governance-installation/SKILL.md`,
    system_layout_path: systemLayoutPath,
    priority_body: priorityBody,
    startup_sequence_body: startupSequenceBody,
    skill_routing_body: skillRoutingBody,
    quality_rules_body: qualityRulesBody,
    review_flow_body: reviewFlowBody,
    tool_specific_notes: toolSpecificNotes
  };
}

function globalPolicySections() {
  return {
    priorityBody: [
      "- Direct system, developer, and user instructions override this file.",
      "- Prefer current local code and current official documentation over memory.",
      "- Load only the smallest relevant skill set for the task."
    ].join("\n"),
    startupSequenceBody: [
      "1. Read [quality-definition]({{quality_definition_path}}) when the task needs repository policy context.",
      "2. Read [workflow]({{workflow_path}}) when the repository defines one.",
      "3. Load only the relevant skill set from `{{primary_skill_root}}`."
    ].join("\n"),
    skillRoutingBody: [
      "- Use [quality-index]({{quality_index_skill_path}}) when the task spans multiple concerns.",
      "- Use [typescript-zero-bypass]({{typescript_zero_bypass_skill_path}}) for `.ts` or `.tsx` changes.",
      "- Use [vite-vitest-tdd]({{vite_vitest_tdd_skill_path}}) for Vite or Vitest TDD.",
      "- Use [react-public-api-testing]({{react_public_api_testing_skill_path}}) for React behavior tests."
    ].join("\n"),
    qualityRulesBody: [
      "- Use behavior-first tests when tests are viable.",
      "- Avoid type bypasses, comment bypasses, config weakening, and fake greens.",
      "- Prefer named types and explicit models over inline structural shortcuts."
    ].join("\n"),
    reviewFlowBody: [
      "- Before final approval, run the relevant auditors for the actual risk surface.",
      "- Use `bypass-auditor` for typing, config, mocks, helpers, or suspicious diffs.",
      "- Use `tdd-warden` when behavior or tests changed or should have changed.",
      "- Use `pr-gatekeeper` only for final approve-or-reject review."
    ].join("\n")
  };
}

function toolNotesFor(target, { claudeEntrypointLabel = "CLAUDE.md", claudeRulesRoot = "rules/", codexSkillsRoot = "skills/", codexAgentsRoot = "agents/", opencodeConfigPath = "opencode.json" } = {}) {
  if (target === "claude") {
    return `- Claude Code should enter through \`${claudeEntrypointLabel}\` and \`${claudeRulesRoot}\`.`;
  }
  if (target === "codex") {
    return `- Codex should enter through this file and use \`${codexSkillsRoot}\` plus \`${codexAgentsRoot}\`.`;
  }
  if (target === "opencode") {
    return `- OpenCode should enter through this file and load extra instructions from \`${opencodeConfigPath}\`.`;
  }
  return "";
}

function renderAgentsRoot(policy, replacements) {
  return `# AGENTS.md\n\n${renderTemplate(policy, replacements).trimEnd()}\n`;
}

function renderAgentsSnippet(policy, replacements) {
  return `${renderTemplate(policy, replacements).trimEnd()}\n`;
}

function renderClaudeRoot(policy, replacements) {
  return [
    "# CLAUDE.md",
    "",
    renderTemplate(policy, replacements).trimEnd(),
    "",
    "## Claude Code",
    "",
    "- Always-on rules live under `rules/`.",
    "- Skills live under `skills/`.",
    "- Claude subagents live under `agents/`.",
    "- If a skill and a rule both apply, the stricter instruction wins.",
    "- Use the repository workflow in `docs/policy/workflow.md` before finalizing any change.",
    ""
  ].join("\n");
}

function renderClaudeSnippet(policy, replacements) {
  return [
    renderTemplate(policy, replacements).trimEnd(),
    "",
    "## Claude Code",
    "",
    "- Always-on rules live under `rules/`.",
    "- Skills live under `skills/`.",
    "- Claude subagents live under `agents/`.",
    "- If a skill and a rule both apply, the stricter instruction wins.",
    "- Use the repository workflow in `docs/policy/workflow.md` before finalizing any change.",
    ""
  ].join("\n");
}

function globalRootDestination(target, homeDir) {
  if (target === "claude") {
    return homePath(homeDir, ".claude", "CLAUDE.md");
  }
  if (target === "codex") {
    return homePath(homeDir, ".codex", "AGENTS.md");
  }
  if (target === "opencode") {
    return homePath(homeDir, ".config", "opencode", "AGENTS.md");
  }
  throw new Error(`Unsupported target: ${target}`);
}

function rootReplacements(target) {
  if (target === "claude") {
    return entrypointReplacements({
      qualityDefinitionPath: "docs/policy/quality-definition.md",
      workflowPath: "docs/policy/workflow.md",
      primarySkillRoot: "skills/",
      skillRoot: "skills",
      systemLayoutPath: "docs/policy/system-layout.md",
      ...globalPolicySections(),
      toolSpecificNotes: toolNotesFor("claude", { claudeEntrypointLabel: "CLAUDE.md", claudeRulesRoot: "rules/" })
    });
  }
  if (target === "codex") {
    return entrypointReplacements({
      qualityDefinitionPath: "docs/policy/quality-definition.md",
      workflowPath: "docs/policy/workflow.md",
      primarySkillRoot: "../.agents/skills/",
      skillRoot: "../.agents/skills",
      systemLayoutPath: "docs/policy/system-layout.md",
      ...globalPolicySections(),
      toolSpecificNotes: toolNotesFor("codex", { codexSkillsRoot: "../.agents/skills/", codexAgentsRoot: "agents/" })
    });
  }
  if (target === "opencode") {
    return entrypointReplacements({
      qualityDefinitionPath: "docs/policy/quality-definition.md",
      workflowPath: "docs/policy/workflow.md",
      primarySkillRoot: "skills/",
      skillRoot: "skills",
      systemLayoutPath: "docs/policy/system-layout.md",
      ...globalPolicySections(),
      toolSpecificNotes: toolNotesFor("opencode", { opencodeConfigPath: "opencode.json" })
    });
  }
  throw new Error(`Unsupported target: ${target}`);
}

async function renderRootFile(packageRoot, target) {
  const policy = await loadEntrypointPolicy(packageRoot);
  if (target === "claude") {
    return renderClaudeRoot(policy, rootReplacements(target));
  }
  return renderAgentsRoot(policy, rootReplacements(target));
}

async function renderRootSnippet(packageRoot, target) {
  const policy = await loadEntrypointPolicy(packageRoot);
  if (target === "claude") {
    return renderClaudeSnippet(policy, rootReplacements(target));
  }
  return renderAgentsSnippet(policy, rootReplacements(target));
}

export function resolveInstallPlan(packageRoot, target, homeDir = os.homedir()) {
  if (target === "claude") {
    return [
      [packagePath(packageRoot, "docs", "policy"), homePath(homeDir, ".claude", "docs", "policy")],
      [packagePath(packageRoot, ".claude", "rules"), homePath(homeDir, ".claude", "rules")],
      [packagePath(packageRoot, ".claude", "skills"), homePath(homeDir, ".claude", "skills")],
      [packagePath(packageRoot, ".claude", "agents"), homePath(homeDir, ".claude", "agents")],
      [packagePath(packageRoot, ".claude", "commands"), homePath(homeDir, ".claude", "commands"), true]
    ];
  }

  if (target === "codex") {
    return [
      [packagePath(packageRoot, "docs", "policy"), homePath(homeDir, ".codex", "docs", "policy")],
      [packagePath(packageRoot, ".agents", "skills"), homePath(homeDir, ".agents", "skills")],
      [packagePath(packageRoot, ".codex", "agents"), homePath(homeDir, ".codex", "agents")]
    ];
  }

  if (target === "opencode") {
    return [
      [packagePath(packageRoot, "docs", "policy"), homePath(homeDir, ".config", "opencode", "docs", "policy")],
      [packagePath(packageRoot, ".opencode", "skills"), homePath(homeDir, ".config", "opencode", "skills")],
      [packagePath(packageRoot, ".opencode", "agents"), homePath(homeDir, ".config", "opencode", "agents")],
      [packagePath(packageRoot, ".opencode", "commands"), homePath(homeDir, ".config", "opencode", "commands"), true]
    ];
  }

  throw new Error(`Unsupported target: ${target}`);
}

export function resolveCleanupPlan(target, homeDir = os.homedir(), manageGlobalRoot = false) {
  if (!manageGlobalRoot) {
    return [];
  }

  if (target === "claude") {
    return [homePath(homeDir, ".claude", "AGENTS.md")];
  }

  return [];
}

function normalizePlan(plan) {
  return plan
    .filter(([source, , optional]) => !optional || existsSync(source))
    .map(([source, destination]) => ({ source, destination }));
}

async function ensureParent(destination) {
  await mkdir(path.dirname(destination), { recursive: true });
}

function backupDestinationPath(destination, backupRoot, homeDir) {
  return path.join(backupRoot, path.relative(homeDir, destination));
}

async function backupExisting(destination, backupRoot, homeDir) {
  try {
    const backupDestination = backupDestinationPath(destination, backupRoot, homeDir);
    await ensureParent(backupDestination);
    await rename(destination, backupDestination);
    return true;
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return false;
    }
    throw error;
  }
}

async function installEntry(source, destination) {
  await rm(destination, { recursive: true, force: true });
  await ensureParent(destination);
  await cp(source, destination, { recursive: true });
}

async function writeRenderedEntry(content, destination) {
  await rm(destination, { recursive: true, force: true });
  await ensureParent(destination);
  await writeFile(destination, content, "utf8");
}

async function removeLegacyPath(destination, backupRoot, homeDir) {
  const backedUp = await backupExisting(destination, backupRoot, homeDir);
  if (!backedUp) {
    return false;
  }
  await rm(destination, { recursive: true, force: true });
  return true;
}

function renderManualStep(target, homeDir) {
  if (target === "claude") {
    return {
      target,
      kind: "append_to_claude_md",
      destination: homePath(homeDir, ".claude", "CLAUDE.md")
    };
  }

  if (target === "codex") {
    return {
      target,
      kind: "append_to_agents_md",
      destination: homePath(homeDir, ".codex", "AGENTS.md")
    };
  }

  if (target === "opencode") {
    return {
      target,
      kind: "append_to_agents_md",
      destination: homePath(homeDir, ".config", "opencode", "AGENTS.md")
    };
  }

  throw new Error(`Unsupported target: ${target}`);
}

export async function installGlobal(packageRoot, decisions, homeDir = os.homedir()) {
  const backupRoot = homePath(homeDir, `.${PACKAGE_NAME}`, "backups", timestamp());
  const installed = [];
  const manualSteps = [];

  for (const decision of decisions) {
    const { target, manageGlobalRoot } = decision;
    const cleanupPlan = resolveCleanupPlan(target, homeDir, manageGlobalRoot);
    for (const destination of cleanupPlan) {
      const removed = await removeLegacyPath(destination, backupRoot, homeDir);
      if (removed) {
        installed.push({
          target,
          source: null,
          destination,
          relativeDestination: path.relative(homeDir, destination),
          action: "remove"
        });
      }
    }

    const plan = normalizePlan(resolveInstallPlan(packageRoot, target, homeDir));
    for (const entry of plan) {
      const relativeDestination = path.relative(homeDir, entry.destination);
      await backupExisting(entry.destination, backupRoot, homeDir);
      await installEntry(entry.source, entry.destination);
      installed.push({
        target,
        source: entry.source,
        destination: entry.destination,
        relativeDestination,
        action: "install"
      });
    }

    if (manageGlobalRoot) {
      const destination = globalRootDestination(target, homeDir);
      const content = await renderRootFile(packageRoot, target);
      await backupExisting(destination, backupRoot, homeDir);
      await writeRenderedEntry(content, destination);
      installed.push({
        target,
        source: `${target}:rendered-root`,
        destination,
        relativeDestination: path.relative(homeDir, destination),
        action: "write"
      });
      continue;
    }

    const manualStep = renderManualStep(target, homeDir);
    manualStep.snippet = await renderRootSnippet(packageRoot, target);
    manualSteps.push(manualStep);
  }

  return {
    backupRoot,
    installed,
    manualSteps
  };
}
