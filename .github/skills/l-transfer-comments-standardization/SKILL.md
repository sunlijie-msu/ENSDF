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
  If an XREF letter is followed by asterisk (*), it is usually not considered for Jπ assignment.

### Operations
- **Write/Update** cL J$ L-transfer phrase in adopted target
- **Keep** all non-L-transfer J$ arguments unchanged

## Purpose
Standardize only the L-transfer portion of cL J$ comments. Preserve all other J$ arguments exactly. Preserve all other existing comments.

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

### Different L Values Across Reactions
`L=V1 from INITIAL_JPI in R1 gives LIST1. L=V2 from INITIAL_JPI in R2 gives LIST2.`
Example: `L=2 from 0+ in ({+3}He,|a) gives 3/2+,5/2+. L=3 from 0+ in (p,d) gives 5/2-,7/2-.`

### Multiple L Values in One Reaction
Do not collapse L=V1+V2 into one Jπ list; use separate `gives` clauses.
`L=V1+V2 from INITIAL_JPI in REACTION: L=V1 gives JPI_LIST1; L=V2 gives JPI_LIST2.`
Example: `L=0+2 from 3/2+ in ({+3}He,d): L=0 gives 1+,2+; L=2 gives 0+,1+,2+,3+,4+.`

### Off-Energy ("Other") Dataset Level Notes
Existing comments by users may include `for E_dataset {IU}` appended directly to the `gives` clause. Do not remove the energy information.
Correct: `L=0+2 from 0+ in {+36}Ar(d,|a),(pol d,|a): L=0 gives 1+; L=2 gives 1+,2+,3+ for 2382 {I20}.`

### Period Separator Rule
Each independent Jπ argument must end with a period (.). Arguments from different reactions or evidence types are separated by periods, not semicolons.
Correct: `L=2 from 0+ in R1 gives 1+,2+,3+. L=4 from 0+ in R2 gives 3+,4+,5+.`

### Analyzing Power (Polarized Beam) Spin Constraint
The analyzing power (L+1 or L-1 transfer) from polarized beam data constrains the final Jπ independently of the unpolarized L-transfer. NEVER remove or merge this argument. It is a distinct physics constraint with its own sentence.
Example: `L=2 from 0+ in {+36}Ar(d,|a),(pol d,|a) and L+1 transfer from analyzing power gives 3+.`

### XREF → Source L-Field Cross-Check (Mandatory)
Before writing any L-transfer comment, ALWAYS read the actual L-field (cols 56–64) of the matched L-record in the source dataset. NEVER use L values from old adopted comment text as a proxy. Old comments may be wrong.

### Completeness Check (Mandatory)
For each adopted level, examine ALL non-asterisk XREF letters. Every letter with a non-blank, non-asterisk L-field in the source dataset must have a corresponding clause in the adopted cL J$ comment.

*Comment-only edits: skip ruler, column, and ordering validation.*
