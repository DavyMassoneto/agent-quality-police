#!/usr/bin/env node

import path from "node:path";
import process from "node:process";
import readline from "node:readline/promises";
import { fileURLToPath } from "node:url";

import { installGlobal, supportedTargets } from "../lib/install.mjs";

function usage() {
  console.log(
    [
      "Usage:",
      "  aqp install",
      "  aqp install --targets claude,codex,opencode [--manage-global-root claude,codex] [--home <dir>] [--json]"
    ].join("\n")
  );
}

function parseCommaList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function normalizeTargets(value) {
  const requestedTargets = value === "all" ? supportedTargets() : parseCommaList(value);
  const validTargets = new Set(supportedTargets());
  for (const target of requestedTargets) {
    if (!validTargets.has(target)) {
      throw new Error(`Unsupported target: ${target}`);
    }
  }
  return requestedTargets;
}

async function promptTargets(rl) {
  const answer = await rl.question("Install for [claude,codex,opencode,all]: ");
  return normalizeTargets(answer || "all");
}

async function promptManageRoot(rl, target) {
  const rootLabel = target === "claude" ? "CLAUDE.md" : "AGENTS.md";
  const answer = await rl.question(`Manage the global ${rootLabel} for ${target}? [y/N]: `);
  return /^y(es)?$/i.test(answer.trim());
}

function renderResult(result, useJson) {
  if (useJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`Backup: ${result.backupRoot}`);
  for (const entry of result.installed) {
    console.log(`${entry.action}: ${entry.relativeDestination}`);
  }
  if (result.manualSteps.length > 0) {
    console.log("Manual steps:");
    for (const step of result.manualSteps) {
      console.log(JSON.stringify(step, null, 2));
    }
  }
}

async function main(argv) {
  const [command, ...rest] = argv;
  if (!command || command === "--help" || command === "-h") {
    usage();
    return 0;
  }

  if (command !== "install") {
    usage();
    return 1;
  }

  let homeDir;
  let targets;
  let manageGlobalRootTargets = new Set();
  let useJson = false;

  for (let index = 0; index < rest.length; index += 1) {
    const current = rest[index];
    if (current === "--home") {
      homeDir = rest[index + 1];
      index += 1;
      continue;
    }
    if (current === "--targets") {
      targets = normalizeTargets(rest[index + 1]);
      index += 1;
      continue;
    }
    if (current === "--manage-global-root") {
      manageGlobalRootTargets = new Set(normalizeTargets(rest[index + 1]));
      index += 1;
      continue;
    }
    if (current === "--json") {
      useJson = true;
      continue;
    }
    throw new Error(`Unknown argument: ${current}`);
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  try {
    const resolvedTargets = targets ?? (await promptTargets(rl));
    if (manageGlobalRootTargets.size === 0) {
      for (const target of resolvedTargets) {
        if (await promptManageRoot(rl, target)) {
          manageGlobalRootTargets.add(target);
        }
      }
    }

    const decisions = resolvedTargets.map((target) => ({
      target,
      manageGlobalRoot: manageGlobalRootTargets.has(target)
    }));

    const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
    const result = await installGlobal(packageRoot, decisions, homeDir);
    renderResult(result, useJson);
    return 0;
  } finally {
    rl.close();
  }
}

const exitCode = await main(process.argv.slice(2));
process.exit(exitCode);
