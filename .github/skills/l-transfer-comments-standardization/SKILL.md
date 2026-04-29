---
name: l-transfer-comments-standardization
description: >
  Standardizes L-transfer phrases in ENSDF cL J$ comments. Use when converting
  legacy notation, resolving cross-reaction discrepancies, or deducing Jπ from
  L-transfers in XREF-identified reaction datasets using angular momentum
  coupling. Comment-only workflow; no ruler or column validation required.
argument-hint: [ENSDF file or level energy]
---

# ENSDF L-Transfer Comments Standardization

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to reaction dataset .ens file(s)]`
- Target: `[path to adopted .ens file]`

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV  `[ ]` XREF letter → dataset

### Operations
- **Write/Update** cL J$ L-transfer phrase in adopted target
- **Keep** all non-L-transfer J$ arguments unchanged

## Purpose
Standardize only the L-transfer portion of cL J$ comments. Preserve all other J$ arguments exactly.

## XREF → Jπ Deduction Workflow

Each XREF letter in an adopted L-record maps to a source reaction dataset. L-transfers from that dataset constrain final-state Jπ. To compute `gives JPI_LIST`:

1. Map the XREF letter to its reaction dataset; read L from cols 56-64 of the matched level.
2. Verify the `target J^π` and `s_particle^π` for the reaction type in `.github/docs/angular_momentum_coupling.md` §6.
3. Run `python .github/scripts/angular_momentum_coupling.py`; enter target J^π and particle s^π.
4. Read the allowed Jπ list for the measured L value and write to the comment.

## Standard Formats

Always specify "from INITIAL_JPI" (e.g., from 3/2+). Use Oxford comma in reaction lists.

### One L Value
`L=VALUE from INITIAL_JPI in REACTION gives JPI_LIST.`
Example: `L=2 from 0+ in ({+3}He,|a) gives 3/2+,5/2+.`

### One L Value, Multiple Reactions
`L=VALUE from INITIAL_JPI in R1, R2, and R3 gives JPI_LIST.`
Example: `L=2 from 0+ in (p,d), (d,t), and ({+3}He,|a) gives 3/2+,5/2+.`

### Different L Values Across Reactions
Use `Other:` only when different reactions give different Jπ values.
`L=V1 from INITIAL_JPI in R1 gives LIST1. Other: L=V2 from INITIAL_JPI in R2 gives LIST2.`
Example: `L=2 from 0+ in ({+3}He,|a) gives 3/2+,5/2+. Other: L=3 from 0+ in (p,d) gives 5/2-,7/2-.`

### Multiple L Values in One Reaction
Do not collapse L=V1+V2 into one Jπ list; use separate `gives` clauses.
`L=V1+V2 from INITIAL_JPI in REACTION: L=V1 gives JPI_LIST1; L=V2 gives JPI_LIST2.`
Example: `L=0+2 from 3/2+ in ({+3}He,d): L=0 gives 1+,2+; L=2 gives 0+,1+,2+,3+,4+.`

*Comment-only edits: skip ruler, column, and ordering validation.*
