---
name: merge-adopted-levels
description: Merges two or more adopted ENSDF L-records (or a dataset's level into an existing adopted level) into one record with union XREF and each dataset's owned fields. Use when one physical level but wrongly split into separate records.
---
# Merge Adopted Levels
ENSDF 80-column record/field definitions, structural rules, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.
*Fill in:* adopted file; the L-records to group; dataset letters and source files.
1. Read each source dataset; confirm one physical level (E within DE, compatible Jπ); never group levels a dataset reports as distinct.
2. Build the ownership map first: which dataset supplies E/DE, Jπ, T/DT, L, S/DS, each G-record, continuation and comment.
3. Emit one L-record: single E/DE and Jπ, every field filled from its owner, blank what no dataset reported; comments in `E$`, `J$`, `T$`, `S$`, general order, one value and citation per source.
4. `XREF` = union of grouped labels in alphabetical order, each label's `(energy)`, `(*)`, `(?)` notation preserved; drop `(*)` when grouping removes the partner level, and keep `(*)` only if it stays on two or more levels.
5. Merge G-records in ascending energy, one per unique transition, flag multiply placed `*`/`&`/`@`, keep each `cG` and `FL=` with its transition; where datasets disagree on intensity, keep the owner's RI in the field and cite the other dataset's RI in a `cG RI$other:` comment.
6. Validate each edited line, then column calibration and gamma ordering; edit in place, never scripts.
7. Relocating a record can drop its trailing padding: re-run `column_calibrate.py --fix` (data records only, comments are skipped) and pad comment lines by hand, then re-check every moved line's length.
**Pitfall** - keep merges reversible (comment ownership) so a later split can restore each dataset's fields; every merged E/DE must trace to an owning dataset, and col-77 flags declared in the top general-comment section are global, not orphans. When the file default claims a |g-fit origin, a merged E that no single dataset level or fit reproduces needs an `E$` note or general comment naming each source value (do not invent the fit). Inverse: `.github/skills/split-adopted-levels/SKILL.md`.
