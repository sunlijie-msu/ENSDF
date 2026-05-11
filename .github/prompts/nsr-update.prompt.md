---
description: "Update NSR keynumbers consistently across ENS content, filename, and tracking docs"
name: "NSR Update Consistency"
argument-hint: "oldUpper newUpper oldMixed newMixed citation"
agent: "agent"
---
Task: Apply exact case-sensitive replacements.
Scope: XUNDL folder and files within.

Inputs: oldUpper, newUpper, oldMixed, newMixed, citation.
Use oldUpper->newUpper and oldMixed->newMixed only; never cross-replace.
Reference .github/agents/ENSDF-Agent.agent.md for NSR definition and conventions.

Update all relevant occurrences in:
1) target ENS file content,
2) ENS filename,
3) tracking markdown (for example Folder_Lijie_Sun_Updating.md).
If old/new filenames both exist, compare hashes and keep only the canonical new filename.
Validate with targeted searches for stale keys on edited ENS files.
Return a concise checklist: files changed, replacements applied, validation results.