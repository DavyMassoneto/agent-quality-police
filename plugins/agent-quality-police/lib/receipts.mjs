import { readFile } from "node:fs/promises";
import path from "node:path";

export const RECEIPT_DIRECTORY = path.join(".aqp", "receipts");

export const REQUIRED_VERDICTS = {
  "implementer": "COMPLETED",
  "bypass-auditor": "PASS",
  "tdd-warden": "PASS",
  "pr-gatekeeper": "APPROVED"
};

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function receiptPath(repoRoot, agent) {
  return path.join(repoRoot, RECEIPT_DIRECTORY, `${agent}.json`);
}

export async function loadReceipt(repoRoot, agent) {
  const raw = await readFile(receiptPath(repoRoot, agent), "utf8");
  return JSON.parse(raw);
}

export function validateReceipt(agent, receipt) {
  if (!isObject(receipt)) {
    return ["Receipt must be a JSON object."];
  }

  const errors = [];
  if (receipt.schemaVersion !== 1) {
    errors.push("schemaVersion must be 1.");
  }
  if (receipt.agent !== agent) {
    errors.push(`agent must equal ${agent}.`);
  }
  if (typeof receipt.task !== "string" || receipt.task.trim().length === 0) {
    errors.push("task must be a non-empty string.");
  }
  if (typeof receipt.timestamp !== "string" || Number.isNaN(Date.parse(receipt.timestamp))) {
    errors.push("timestamp must be a valid ISO 8601 string.");
  }

  const requiredVerdict = REQUIRED_VERDICTS[agent];
  if (!requiredVerdict) {
    errors.push(`Unknown agent: ${agent}.`);
  } else if (receipt.verdict !== requiredVerdict) {
    errors.push(`verdict must equal ${requiredVerdict}.`);
  }

  return errors;
}

export async function validateRequiredReceipts(repoRoot, requiredAgents) {
  const missing = [];
  const invalid = [];

  for (const agent of requiredAgents) {
    try {
      const receipt = await loadReceipt(repoRoot, agent);
      const errors = validateReceipt(agent, receipt);
      if (errors.length > 0) {
        invalid.push({ agent, errors });
      }
    } catch (error) {
      if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
        missing.push(agent);
        continue;
      }
      if (error instanceof SyntaxError) {
        invalid.push({ agent, errors: ["Receipt is not valid JSON."] });
        continue;
      }
      throw error;
    }
  }

  return {
    valid: missing.length === 0 && invalid.length === 0,
    missing,
    invalid
  };
}
