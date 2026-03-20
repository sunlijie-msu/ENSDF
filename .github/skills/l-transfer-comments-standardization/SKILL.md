---
name: l-transfer-comments-standardization
description: >
  Use this skill when standardizing L-transfer angular momentum comments
  in cL J$ lines in ENSDF files. Converts legacy formats like L(reaction)=
  value to standard format L=value from initial-Jπ in reaction. Handles
  single/multiple L values, discrepancies between reactions, Oxford comma,
  reaction lists, and 80-column line wrapping. Comment-only workflow —
  skip ruler and column validation.
argument-hint: [ENSDF file or level energy]
---

# ENSDF L-Transfer Comments Standardization

## Purpose
Standardize L-transfer comments used in J$ lines for clarity and consistency.

## Standard Format

### Single L Value for Multiple Reactions
**Format:** `L=VALUE from INITIAL_JPI in REACTION1, REACTION2, and REACTION3.`
**Example:** `L=2 from 0+ in (p,d), (d,t), and ({+3}He,|a).`

### Single L Value for Single Reaction
**Format:** `L=VALUE from INITIAL_JPI in REACTION1.`
**Example:** `L=2 from 0+ in ({+3}He,|a).`

### Multiple L Values (e.g. Discrepancies)
**Format:** `L=VALUE1 from INITIAL_JPI in REACTION1. Discrepancy: L=VALUE2 from INITIAL_JPI in REACTION2.`
**Example:** `L=2 from 0+ in ({+3}He,|a). Discrepancy: L=3 from 0+ in (p,d).`

### Complex Cases with Additional Info
**Format:** `L=VALUE from INITIAL_JPI in REACTION. Additional info.`
**Example:** `L=2 from 0+ in (p,d). Spin=(3/2) from J dependence in (p,d).`

## Rules

- **Preservation:** **CRITICAL:** Standardize ONLY the L-transfer phrase (e.g., `L(reac)=val` → `L=val from jpi in reac.`). Keep all preceding and following comments, punctuation (semicolons, etc.), case sensitivity, and descriptive words (e.g., "Discrepancy:", "Possible mirror level", "allowed beta transitions", "and spin=", gamma transition arguments, shell-model calculations, etc.) EXACTLY as they are. Do not modify, rephrase, or remove other J-related arguments.
- **Uniformity:** Convert `L(p,d)=L(d,t)=2` to `L=2 from INITIAL_JPI in (p,d) and (d,t).`
- **Initial State:** Always specify "from INITIAL_JPI" (e.g., from 0+).
- **Reaction List:** Comma-separated list with "and" before the last item.
- **Oxford Comma:** Use the Oxford comma.
- **Max Line Length:** Keep within 80 columns. If needed, wrap to continuation lines (`2cL`, etc.).
- **Validation Shortcut:** Skip ruler, column validation, and gamma ordering checks — this is a pure comment-editing task.
