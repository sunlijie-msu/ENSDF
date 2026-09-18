---
name: split-adopted-levels
description: Splits one adopted ENSDF L-record that wrongly groups two or more datasets' distinct levels.
---
# Split Adopted Levels
ENSDF 80-column record/field definitions, structural rules, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.
*Fill in:* adopted file; dataset letters and source files; the shared L-record.
1. Read each cited dataset; tabulate its E, DE, Jπ, T, DT, L, S, DS, G-records, continuations, comments; confirm the levels are distinct. Grepping each source for the energy is decisive: a dataset lacking that level owns nothing there and must not keep its `(energy)`/`(*)` label.
2. Map ownership of every field, continuation and comment to the dataset that supplies it (often part of the MRG file attached by user); a field no dataset reported stays blank. This includes adopted E/DE: it must trace to an owning dataset, never to the previous evaluation's value.
3. Emit one record per dataset in ascending energy with its own E/DE and owned fields only - never copy a foreign value; another dataset's T/DT or L value belongs in `cL T$`/`cL L$` text.
4. Give each record `XREF=<letter>` plus its comments in `E$`, `J$`, `T$`, `S$`, general order. When a dataset matches exactly one record, keep `Letter(energy)` there and delete that label from all siblings - no `(*)` residue; retain `(energy*)`/`(?)` only where ambiguity truly survives.
5. Re-label every sibling that shared the old label, not just the record being split.
6. Validate each edited line, then column calibration and gamma ordering; edit in place, never scripts.
**Pitfall** - verify ownership against the source datasets themselves; merge files and predicted match lists are only secondary hints - a match list covers only the datasets submitted to it, so its silence about another dataset is not evidence either way. Col-77 flags declared in the top general-comment section are global, not orphans. Reload anchors before editing (partners share XREF text); re-measure every edited line's length after each edit, since padding may be lost; ` 34S  d` delimiter lines trigger a spurious type error in the one-line ruler. Inverse: `.github/skills/group-adopted-levels/SKILL.md`.
