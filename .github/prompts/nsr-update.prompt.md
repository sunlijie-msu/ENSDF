---
description: "Update NSR key/citation consistently across ENS content, filename, and tracking docs"
name: "NSR Update Consistency"
argument-hint: "oldUpper newUpper oldMixed newMixed citation"
agent: "agent"
---
Apply exact case-sensitive replacements in ENSDF workflow artifacts.

Inputs: oldUpper, newUpper, oldMixed, newMixed, citation.
Use oldUpper->newUpper and oldMixed->newMixed only; never cross-replace.
Reference .github/copilot-instructions.md for NSR and ENSDF conventions.

Update all relevant occurrences in:
1) target ENS file content,
2) ENS filename,
3) tracking markdown (for example Folder_Lijie_Sun_Updating.md).
If old/new filenames both exist, compare hashes and keep only the canonical new filename.
Validate with targeted searches for stale keys and run ensdf_1line_ruler on edited ENS files.
Return a concise checklist: files changed, replacements applied, validation results.