---
name: group-adopted-levels
description: Groups two or more adopted ENSDF L-records (or a dataset's level into an existing adopted level) into one record with union XREF and each dataset's owned fields. Use when one physical level but wrongly split into separate records.
---
# Group Adopted Levels
ENSDF 80-column record/field definitions, structural rules, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.
*Fill in:* adopted file; the L-records to group; dataset letters and source files.
1. Read each source dataset; confirm one physical level (E within DE, compatible Jπ); never group levels a dataset reports as distinct.
2. Build the ownership map first: which dataset supplies E/DE, Jπ, T/DT, L, S/DS, each G-record, continuation and comment.
3. Emit one L-record: single E/DE and Jπ, every field filled from its owner, blank what no dataset reported; comments in `E$`, `J$`, `T$`, `S$`, general order, one value and citation per source.
4. `XREF` = union of grouped labels in alphabetical order, each label's `(energy)`, `(*)`, `(?)` notation preserved.
5. Merge G-records in ascending energy, one per unique transition, flag multiply placed `*`/`&`/`@`, keep each `cG` and `FL=` with its transition.
6. Validate each edited line, then column calibration and gamma ordering; edit in place, never scripts.
**Pitfall** - keep merges reversible (comment ownership) so a later split can restore each dataset's fields. Inverse: `.github/skills/split-adopted-levels/SKILL.md`.
