---
name: l-transfer-comments-standardization
description: >
  Standardizes L-transfer angular momentum comments in cL J$ lines in ENSDF
  files. Converts legacy formats such as L(reaction)=value to the standard
  form L=value from initial-Jπ in reaction. Applies to single and multiple
  L values, ambiguous same-reaction notations such as L=1+3, discrepancies
  between reactions, Oxford comma usage, reaction lists, and 80-column line
  wrapping. Comment-only workflow; skip ruler and column validation.
argument-hint: [ENSDF file or level energy]
---

# ENSDF L-Transfer Comments Standardization

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose
Standardize L-transfer comments used in J$ lines for clarity and consistency.

## Standard Formats

### Single L Value for Multiple Reactions
**Format:** `L=VALUE from INITIAL_JPI in REACTION1, REACTION2, and REACTION3.`
**Example:** `L=2 from 0+ in (p,d), (d,t), and ({+3}He,|a).`

### Single L Value for Single Reaction
**Format:** `L=VALUE from INITIAL_JPI in REACTION.`
**Example:** `L=2 from 0+ in ({+3}He,|a).`

### Different L Values Across Reactions
**Format:** `L=VALUE1 from INITIAL_JPI in REACTION1. Other: L=VALUE2 from INITIAL_JPI in REACTION2.`
**Example:** `L=2 from 0+ in ({+3}He,|a). Other: L=3 from 0+ in (p,d).`

### Ambiguous Multi-L in One Reaction
**Rule:** If a paper gives `L=1+3`, `L=0+2`, etc. for the same reaction and does not explicitly define whether this means simultaneous transfer or alternative assignments, treat it as ambiguous and state each L scenario separately.
**Format:** `L=VALUE1+VALUE2 from INITIAL_JPI in REACTION: L=VALUE1 gives JPI_LIST1; L=VALUE2 gives JPI_LIST2.`
**Example:** `L=0+2 from 3/2+ in ({+3}He,d): L=0 gives 1+,2+; L=2 gives 0+, 1+, 2+, 3+, 4+.`

### Complex Cases with Additional Info
**Format:** `L=VALUE from INITIAL_JPI in REACTION. Additional info.`
**Example:** `L=2 from 0+ in (pol p,d) and L+1/2 transfer from analyzing power. L+1/2 transfer from J-dependence in (p,d).`

## Rules

- **Preservation:** **CRITICAL:** Standardize ONLY the L-transfer phrase (e.g., `L(reac)=val` → `L=val from jpi in reac.`). Keep all preceding and following comments, punctuation (semicolons, etc.), case sensitivity, and descriptive words (e.g., "Discrepancy:", "Possible mirror level", "allowed beta transitions", "and spin=", gamma transition arguments, shell-model calculations, etc.) EXACTLY as they are. Do not modify, rephrase, or remove other J-related arguments.
- **Uniformity:** Convert `L(p,d)=L(d,t)=2` to `L=2 from INITIAL_JPI in (p,d) and (d,t).`
- **Ambiguous Same-Reaction Multi-L:** Do not compress `L=1+3` or `L=0+2` in one reaction into a single `gives ...` list unless the source explicitly states an AND meaning. Default to `L=1+3 from ...: L=1 gives ...; L=3 gives ...` with separate `gives` clauses for each L value.
- **Initial State:** Always specify "from INITIAL_JPI" (e.g., from 0+).
- **Reaction List:** Comma-separated list with "and" before the last item.
- **Oxford Comma:** Use the Oxford comma.
- **Max Line Length:** Keep within 80 columns. If needed, wrap to continuation lines (`2cL`, etc.).
- **Validation Shortcut:** Skip ruler, column validation, and gamma ordering checks — this is a pure comment-editing task.
