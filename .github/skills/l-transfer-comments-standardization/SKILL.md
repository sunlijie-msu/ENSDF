---
name: l-transfer-comments-standardization
description: >
  Standardizes L-transfer phrases in ENSDF cL J$ comments. Use when deducing Jπ from L-transfers in XREF-identified reaction datasets using angular momentum coupling rules. Comment-only workflow; no ruler or column validation required.
argument-hint: [ENSDF file or level energy]
---

# ENSDF L-Transfer Comments Standardization

ENSDF rules and column positions: `.github/copilot-instructions.md`.
## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to reaction dataset .ens file(s)]`
- Target: `[path to adopted .ens file]`

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV  `[ ]` XREF letter → dataset
  If an XREF letter is followed by asterisk (*) or (energy*), it is usually not considered for Jπ assignment.

### Operations
- **Write/Update** cL J$ L-transfer phrase in adopted target
- **Keep** all non-L-transfer J$ arguments unchanged

## Purpose
Standardize only the L-transfer portion of cL J$ comments. Preserve all other J$ arguments exactly. Preserve all other existing comments.

## Workflow

1. Map each non-asterisk XREF letter to its reaction dataset.
2. Read the L-transfer field (cols 56–64) from the matched source L-record. **Never** use old adopted comment text as the L value source.
3. Run `python .github/scripts/angular_momentum_coupling.py Jπ_target Jπ_particle` to compute allowed Jπ for each L value.
   > **Two-layer accuracy check:** (a) quoted L-value must match source cols 56–64 — never trust existing comment text; (b) deduced Jπ range must be correct per the script. L=A+B (simultaneous) requires AND intersection, not union. L=A,B (alternative) requires separate sub-clauses, and then the union of their Jπ results. Every L-transfer clause must include an explicit `gives <Jπ_results>`.
4. Write standardized cL J$ comment, preserving all non-L-transfer arguments exactly.
5. **Completeness:** Each non-asterisk XREF letter with non-blank L-field must appear in the cL J$ comment; angular momentum couplings yielding too many Jπ values may be omitted if other stronger constraints exist.

## Standard Comment Formats

### L values from reactions (period between each clause)

L=<L1> from <Jπ_target1> in <reaction1> gives <Jπ_results1>. L=<L2> from <Jπ_target2> in <reaction2> gives <Jπ_results2>.

Append `for <E_level> {I<Unc>} level` after <Jπ_results> for possible doublets/multiplets that are indicated by aterisk in its XREF.

### Multiple L values in one reaction (colon, semicolons between sub-clauses, final period)
L=L1,L2 or L=L1+L2 or L=L1,L2+L3 is an inseparable list.
L in parentheses indicates less firm L assignment due to data quality or less certain transfer reaction mechanism, e.g., (p,3He), (3He,p).


cL J$L=<L1,L2> from <Jπ_target> in <reaction>: L=<L1> gives <Jπ_results1>; L=<L2> gives <Jπ_results2>.

<Jπ_results> is the OR of {<Jπ_results1>; <Jπ_results2>}.

cL J$L=<L1+L2> from <Jπ_target> in <reaction> gives <Jπ_results>.
<Jπ_results> = AND intersection only. Never show individual sub-clauses for '+' simultaneous transfers.

cL J$L=<L1+L2,L3> from <Jπ_target> in <reaction>: L=<L1+L2> gives <Jπ_results1AND2>; L=<L3> gives <Jπ_results3>.

<Jπ_results> is the OR of {<Jπ_results1AND2>; <Jπ_results3>}.

cL J$L=<L1+L2,L3+L4> from <Jπ_target> in <reaction>: L=<L1+L2> gives <Jπ_results1AND2>; L=<L3+L4> gives <Jπ_results3AND4>.

<Jπ_results> is the OR of {<Jπ_results1AND2>; <Jπ_results3AND4>}.

Final Jπ results that go to the Level-record J|p field usually take the AND of each <Jπ_results> from different datasets into account.


### Analyzing power constraint
From polarized-beam data: `L=<L> from <Jπ> in <pol reaction> with <L±1> transfer from analyzing power gives <Jπ_results>.`

*Comment-only edits: skip ruler, column, and ordering validation.*
