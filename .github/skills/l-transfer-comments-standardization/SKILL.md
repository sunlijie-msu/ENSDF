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
4. Write standardized cL J$ comment, preserving all non-L-transfer arguments exactly.
5. **Completeness:** For each adopted level, user-specified non-asterisk XREF letter with a non-blank L-field must appear in the cL J$ comment.

## Standard Comment Formats

### L values from reactions (period between each clause)
```
L=<L1> from <Jπ_target1> in <reaction1> gives <Jπ_results1>. L=<L2> from <Jπ_target2> in <reaction2> gives <Jπ_results2>.
```

### Multiple L values in one reaction (colon, semicolons between sub-clauses, final period)
L=L1,L2 or L=L1+L2 is an inseparable list — all sub-clauses share the colon group.
```
L=<L1,L2> from <Jπ_target> in <reaction>: L=<L1> gives <Jπ_results1>; L=<L2> gives <Jπ_results2>.
L=<L1+L2> from <Jπ_target> in <reaction>: L=<L1> gives <Jπ_results1>; L=<L2> gives <Jπ_results2>.
L=<L1+L2,L3> from <Jπ_target> in <reaction>: L=<L1> gives <Jπ_results1>; L=<L2> gives <Jπ_results2>; L=<L3> gives <Jπ_results3>.
```

Existing comments by human evaluators may include `for <E_level> {I<Uncertainty>}` appended. Do not delete the energy information.


### Analyzing power constraint
The analyzing power (J=<L-1>, <L>, <L+1> transfer) from polarized beam data further constrains the final Jπ.
```
L=<L1> from <Jπ_target1> in <pol reaction1> and <L±1> transfer from analyzing power gives <Jπ_results1>.
```

*Comment-only edits: skip ruler, column, and ordering validation.*
