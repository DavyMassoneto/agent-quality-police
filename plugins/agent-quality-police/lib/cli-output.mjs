function renderInstalledEntry(entry) {
  return `- [${entry.target}] ${entry.action}: ${entry.relativeDestination}`;
}

function renderManualStep(step) {
  return [
    `[${step.target}] ${step.kind}`,
    `Destination: ${step.destination}`,
    "Add this content:",
    "```md",
    step.snippet.trimEnd(),
    "```"
  ].join("\n");
}

export function formatInstallResult(result) {
  const lines = [`Backup: ${result.backupRoot}`];

  if (result.installed.length > 0) {
    lines.push("", "Applied:");
    for (const entry of result.installed) {
      lines.push(renderInstalledEntry(entry));
    }
  }

  if (result.manualSteps.length > 0) {
    lines.push("", "Manual steps:");
    for (const step of result.manualSteps) {
      lines.push("", renderManualStep(step));
    }
  }

  return lines.join("\n");
}
