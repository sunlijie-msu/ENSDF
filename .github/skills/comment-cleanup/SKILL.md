---
name: comment-cleanup
description: >
  Use this skill when reviewing, writing, or reordering comments for an ENSDF
  dataset. Establishes a single default-source general cG E,RI$ comment and adds
  individual exception comments only where needed. Covers weighted averages,
  non-default dataset sources, and whole-unit reordering of comment units into
  ENSDF comment order.
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

### Comment Ordering

Order comment units in each `cL`/`cG` block per `.github/agents/ENSDF-Agent.agent.md`
(general comment last). Move whole units (first line plus continuations) unchanged — no
text edits, no renumbering, no data-record changes. Validate with `.github/scripts/`:
`ensdf_1line_ruler.py`, `check_gamma_ordering.py`, `column_calibrate.py`.

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
4. Order each level/gamma comment block per `.github/agents/ENSDF-Agent.agent.md`,
	moving whole units (first line + continuations).
5. Keep deduced E|g values (no uncertainty) undocumented at per-gamma level unless an explicit exception is required.

## Completion Criteria

- One clear default-source general comment exists for E,RI.
- Exception comments exist only where source differs from default or averaging is required.
- No redundant per-gamma default-source comments remain.
- Comment units in every `cL`/`cG` block follow ENSDF order, general comment last.

For general comment ordering at the beginning of Adopted files, see
`.github/skills/general-comments-ordering/SKILL.md`. Full record/column rules:
`.github/agents/ENSDF-Agent.agent.md`.

