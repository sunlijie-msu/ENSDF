---
name: l-transfer-comments-standardization
description: >
  Standardizes L-transfer phrases in ENSDF cL J$ comments when converting
  legacy notation, cross-reaction discrepancies, or ambiguous same-reaction
  notation. Preserves non-L-transfer J$ arguments and uses the comment-only
  workflow without ruler or column validation.
argument-hint: [ENSDF file or level energy]
---

# ENSDF L-Transfer Comments Standardization

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose
Standardize only the L-transfer portion of cL J$ comments. Preserve all other J$ arguments exactly.

## Standard Formats

### One L Value
**Format:** `L=VALUE from INITIAL_JPI in REACTION.`
**Example:** `L=2 from 0+ in ({+3}He,|a) gives 3/2+,5/2+.`

### One L Value in Multiple Reactions
**Format:** `L=VALUE from INITIAL_JPI in REACTION1, REACTION2, and REACTION3.`
**Example:** `L=2 from 0+ in (p,d), (d,t), and ({+3}He,|a) gives 3/2+,5/2+.`

### Different L Values Across Reactions
**Format:** `L=VALUE1 from INITIAL_JPI in REACTION1. Other: L=VALUE2 from INITIAL_JPI in REACTION2.`
**Example:** `L=2 from 0+ in ({+3}He,|a). Other: L=3 from 0+ in (p,d).`

### Multiple L Values in One Reaction
**Preferred format:** `L=VALUE1+VALUE2 from INITIAL_JPI in REACTION: L=VALUE1 gives JPI_LIST1; L=VALUE2 gives JPI_LIST2.`

**Example:** `L=0+2 from 3/2+ in ({+3}He,d): L=0 gives 1+,2+; L=2 gives 0+,1+,2+,3+,4+.`


## Rules

- **Preservation:** Standardize only the L-transfer phrase. Keep all other J$ text, punctuation, and ordering unchanged.
- **Uniformity:** Convert `L(p,d)=L(d,t)=2` to `L=2 from INITIAL_JPI in (p,d) and (d,t).`
- **Cross-reaction rule:** Use `Other:` only when different reactions report different L values.
- **Same-reaction ambiguity rule:** Do not collapse `L=1+3` or `L=0+2` into one combined Jπ list unless the source explicitly states an AND meaning. Use separate `gives` clauses.
- **Initial State:** Always specify "from INITIAL_JPI" (e.g., from 0+).
- **Reaction List:** Comma-separated list with "and" before the last item.
- **Oxford Comma:** Use the Oxford comma.
- **Max Line Length:** No need to wrap lines. Users will wrap manually.
- **Validation Shortcut:** Skip ruler, column validation, and gamma-ordering checks. This skill applies to comment-only edits.
- **XREF → dataset:** Each XREF letter in an adopted L-record identifies a reaction dataset. L-transfers measured in that dataset are valid Jπ constraints for the level.

## Task Configuration
- **Source:** Individual reaction dataset `.ens` files.
- **Target:** Adopted `.ens` file.
