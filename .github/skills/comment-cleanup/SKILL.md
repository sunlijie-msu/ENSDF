---
name: comment-cleanup
description: >
  Use this skill when reviewing, writing, or reordering comments for an ENSDF
  dataset. Establishes a single default-source general cG E,RI$ comment and adds
  individual exception comments only where needed. Covers weighted averages,
  non-default dataset sources, and enforces ENSDF comment-unit ordering
  (cL: E$ → J$ → T$ → S$ → general; cG: E$ → RI$ → M$ → MR$ → general), including
  the safe whole-unit reorder procedure.
argument-hint: [ENSDF file or dataset name]
---

# ENSDF Comment Cleanup Instructions

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## General cG E,RI Comment Strategy

**Principle:** Establish the most common data source as default in a general comment, then document exceptions individually.

### General Comment Format
```
 NUCID cG E,RI$From {DOMINANT_DATASET} unless otherwise noted. E|g values 
 NUCID2cG without uncertainties are deduced from level-energy differences.       
```

### Individual Comment Rules

| Scenario | Action |
|----------|--------|
| E or RI from default dataset only | No individual comment needed |
| E|g without uncertainty | No comment needed (deduced from level difference) |
| Weighted/unweighted average from multiple datasets | Add cG E$ or cG RI$ with average details |
| Intensities normalized to different references | Rescale to one reference, adopt its RI/DRI, move others to `RI$other` → `.github/skills/rescaling-gamma-ri/SKILL.md` |
| Value from non-default dataset | Add cG E$ or cG RI$ stating source |
| Other values exist but not used for averaging | Add "other: VALUE from DATASET" |

### Comment Ordering (per ENSDF rules)

Within one level block all `cL` units and within one gamma block all `cG` units must
appear in this order; the general comment (no identifier before `$`) is always last:

```
cL: E$ → J$ → T$ → S$ → general (no identifier)
cG: E$ → RI$ → M$ → MR$ → general (no identifier)
```

- A **unit** is a `cX` first line plus its `2cX`, `3cX`, … continuation lines — an
  inseparable whole. Column 7 holds the flag (`c`/`C` = comment, `d`/`D` = hidden
  message — records kept in the file but ignored by the processing codes); column 8
  holds the record type being commented. Any other character in column 7 is invalid,
  and only `c`/`C`/`d`/`D` mark a comment-style record.
- Composite identifiers (e.g. `E,RI$`, `E(E),J(E)$`) rank by their **first** field.
- Only the category order is enforced; sub-order inside one category is free.
- Units with other identifiers (e.g. `BE2$`, `MOMM1$`) follow the listed categories.
- Alphabetical sub-order among dataset-scoped identifiers is not required.

### Reordering Procedure

1. Reload the file, then map each unit's span (first line + continuations) before editing.
2. Move **whole units** only; never split a unit, never touch data records.
3. Continuation markers restart at `2` for every unit — moving units needs **no renumbering**.
4. Keep comment text byte-identical and every line exactly 80 columns.
5. Validate in order: `ensdf_1line_ruler.py`, `check_gamma_ordering.py`,
   `column_calibrate.py` (`.github/scripts/`), then confirm `git diff` touches comment lines only.

### What to Avoid

- ❌ Redundant comments restating the default source
- ❌ Individual cG E,RI$ for gammas that match the general comment default
- ❌ Comments for deduced energies (no uncertainty = level difference)

## Execution Checklist

1. Identify dominant dataset for E,RI and set it in the general `cG E,RI$` comment.
2. For each gamma with quoted uncertainty:
	- From default only → no individual `cG E$`/`cG RI$` comment
	- From multiple datasets → add weighted/unweighted average comment
	- From non-default dataset → add source comment, with `Other:` values when applicable
3. Remove redundant individual comments that merely restate the default source.
4. Preserve ENSDF ordering for each level/gamma comment block:
	- `cL`: `cL E$` → `cL J$` → `cL T$` → `cL S$` → general (no identifier)
	- `cG`: `cG E$` → `cG RI$` → `cG M$` → `cG MR$` → general (no identifier)
	- Move whole units (first line + continuations) with the reordering procedure above.
5. Keep deduced E|g values (no uncertainty) undocumented at per-gamma level unless an explicit exception is required.

## Completion Criteria

- One clear default-source general comment exists for E,RI.
- Exception comments exist only where source differs from default or averaging is required.
- No redundant per-gamma default-source comments remain.
- Comment ordering follows ENSDF sequence rules for both `cL` and `cG` units, with the
  general comment last.

For general comment ordering at the beginning of Adopted files, see
`.github/skills/general-comments-ordering/SKILL.md`. Full record/column rules:
`.github/agents/ENSDF-Agent.agent.md`.

