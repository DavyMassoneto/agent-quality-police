import { existsSync } from "node:fs";
import { cp, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const PACKAGE_NAME = "agent-quality-police";
const MANAGED_BLOCK_START = "<!-- agent-quality-police:start -->";
const MANAGED_BLOCK_END = "<!-- agent-quality-police:end -->";

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
  reviewFlowBody
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
    review_flow_body: reviewFlowBody
  };
}

function globalPolicySections() {
  return {
    priorityBody: [
      "- Direct system, developer, and user instructions override this file.",
      "- Prefer current local code and current official documentation over memory.",
      "- Treat the required skills and auditors in this file as mandatory workflow requirements."
    ].join("\n"),
    startupSequenceBody: [
      "1. Read [quality-definition]({{quality_definition_path}}) when the task needs repository policy context.",
      "2. Read [workflow]({{workflow_path}}) when the repository defines one.",
      "3. Load the smallest required skill set from `{{primary_skill_root}}` before proposing edits or writing code."
    ].join("\n"),
    skillRoutingBody: [
      "- Use [quality-index]({{quality_index_skill_path}}) when the task spans multiple concerns or when you are unsure which validators apply.",
      "- Use [typescript-zero-bypass]({{typescript_zero_bypass_skill_path}}) for `.ts` or `.tsx` changes.",
      "- Use [vite-vitest-tdd]({{vite_vitest_tdd_skill_path}}) for Vite or Vitest TDD.",
      "- Use [react-public-api-testing]({{react_public_api_testing_skill_path}}) for React behavior tests.",
      "- Use [anti-bypass-audit]({{anti_bypass_audit_skill_path}}) when reviewing diffs, suspicious helpers, weakened configs, or type/config-heavy changes.",
      "- Use [refactoring-with-safety]({{refactoring_with_safety_skill_path}}) for refactors that are not pure bug fixes.",
      "- Use [governance-installation]({{governance_installation_skill_path}}) when installing or updating this governance package."
    ].join("\n"),
    qualityRulesBody: [
      "- Load the required skills before proposing edits or writing code.",
      "- If a required skill is unavailable in the current runtime, stop and report `BLOCKED`.",
      "- Use behavior-first tests when tests are viable.",
      "- Avoid type bypasses, comment bypasses, config weakening, and fake greens.",
      "- Prefer named types and explicit models over inline structural shortcuts."
    ].join("\n"),
    reviewFlowBody: [
      "- For code changes, explicitly invoke the required auditors before final approval.",
      "- For code changes, do not finalize until the required auditors have run and their results were reviewed.",
      "- Do not substitute inline self-review for a required audit agent invocation.",
      "- For typing, config, mocks, helpers, or suspicious diffs, run `bypass-auditor`.",
      "- For behavior changes or bug fixes, run `tdd-warden` and `bypass-auditor`.",
      "- For final approval, release, or merge decisions, run `pr-gatekeeper` after the other required auditors.",
      "- If a required skill or auditor cannot run in the current runtime, stop and report `BLOCKED`."
    ].join("\n")
  };
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
      ...globalPolicySections()
    });
  }
  if (target === "codex") {
    return entrypointReplacements({
      qualityDefinitionPath: "docs/policy/quality-definition.md",
      workflowPath: "docs/policy/workflow.md",
      primarySkillRoot: "../.agents/skills/",
      skillRoot: "../.agents/skills",
      systemLayoutPath: "docs/policy/system-layout.md",
      ...globalPolicySections()
    });
  }
  if (target === "opencode") {
    return entrypointReplacements({
      qualityDefinitionPath: "docs/policy/quality-definition.md",
      workflowPath: "docs/policy/workflow.md",
      primarySkillRoot: "skills/",
      skillRoot: "skills",
      systemLayoutPath: "docs/policy/system-layout.md",
      ...globalPolicySections()
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

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function managedBlockPattern() {
  return new RegExp(
    `${escapeRegExp(MANAGED_BLOCK_START)}[\\s\\S]*?${escapeRegExp(MANAGED_BLOCK_END)}\\n?`,
    "m"
  );
}

function renderManagedBlock(content) {
  return [MANAGED_BLOCK_START, content.trimEnd(), MANAGED_BLOCK_END, ""].join("\n");
}

async function readOptionalText(destination) {
  try {
    return await readFile(destination, "utf8");
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

function mergeManagedRoot(existingContent, managedContent, legacyFullRoot) {
  const managedBlock = renderManagedBlock(managedContent);
  if (existingContent === null) {
    return managedBlock;
  }

  const existingTrimmed = existingContent.trim();
  if (existingTrimmed.length === 0) {
    return managedBlock;
  }

  const legacyTrimmed = legacyFullRoot.trim();
  if (existingTrimmed === legacyTrimmed) {
    return managedBlock;
  }

  const pattern = managedBlockPattern();
  if (pattern.test(existingContent)) {
    return existingContent.replace(pattern, managedBlock).trimEnd() + "\n";
  }

  return `${existingContent.trimEnd()}\n\n${managedBlock}`;
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
      const existingContent = await readOptionalText(destination);
      const managedContent = await renderRootSnippet(packageRoot, target);
      const legacyFullRoot = await renderRootFile(packageRoot, target);
      const content = mergeManagedRoot(existingContent, managedContent, legacyFullRoot);
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
