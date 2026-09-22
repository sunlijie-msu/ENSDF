---
name: data-cross-check
description: "Checks target data in ENS files against source data for exact consistency after data entry. Use when validating target data in ENS files against source data from CSV, Markdown, MRG, ENS, or ADP files, including values, uncertainties, signs, limits, decimal digits, units, provenance comments, strings, XREFs, and completeness."
---

# Data Cross-Check

Verify 100% consistency between source data and target `.ens` data. Report every mismatch.

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

Actively leverage coding, scripts, and programming tools when necessary to effectively deliver your data tasks.

## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to source .mrg/.adp/.ens/.md/.csv file]`
- Target: `[path to target .ens file]`

### Field Mapping *(source → ENS)*
- `[Data A]` → `[record type]` `[field name]`
- `[Data B]` → `[record type]` `[field name]`
- `[Data C]` → `[record type]` `[comment]`

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV
- G-records: `[ ]` exact Eγ  `[ ]` Eγ within ±[N] keV  `[ ]` matching parent Level first, matching then γ

### Checks
  [ ] value and sign
  [ ] uncertainty and format
  [ ] decimal places and trailing zeros
  [ ] limits / qualifiers (GT, LT, ?, S)
  [ ] XREF strings character-for-character (asterisk * or ? is semantically significant) if applicable
  [ ] provenance in cL/cG comments
  [ ] completeness (missing/extra)

### Special Handling
- `[ ]` [describe non-standard cases]

## Recommended Operating Procedure:

```
- [ ] 1. Confirm Task Configuration
- [ ] 2. Carefully parse and extract data needed from source
- [ ] 3. Carefully parse and extract data needed from target
- [ ] 4. Carefully match data items between source and target
- [ ] 5. Compare item-by-item source against target
- [ ] 6. Identify mismatches.
- [ ] 7. Run reproducible 15% random spot-check (`.github/copilot-instructions.md` § Random Spot Check)
- [ ] 8. Report all mismatches with locations
```

## Required Matching Rules

- Never match a gamma by Eγ alone; match parent L-record first. For near-equal energies, use both level energy and transition energy for accurate matching.
- Numerical Exactness: see `.github/agents/ENSDF-Agent.agent.md` § Numerical Exactness.

## Adopted E(level) Traceability

- Read provenance notes before judging a level undocumented: unqualified general `cL E$` sets the fit default for all levels; letter-qualified general notes (`cL E(X)$`) cover every level whose L-record **column 77 flag letter** is X (the flag letter, not the XREF letters, matches the note identifier).
- A fit basis exists only if the level has ≥1 gamma with DE; with no G-records or DE-less gammas, E must be a dataset-measured level energy — compare byte-exact E and DE against the level's XREF datasets, honoring `Letter(value)`/`Letter(*)`/`Letter(?)` letter-by-letter (parentheses bind to the preceding letter only).
- The XREF notation itself pins the source: a plain unparenthesised letter means that dataset's E agrees with the adopted value, while `Letter(value)` deliberately records a dataset energy that was **not** adopted. If exactly one plain letter's dataset L-record matches adopted E and DE byte-exact, the level is traceable by reading the adopted file alone — never report it as undocumented; reserve the note/flag check for levels with no unique byte-exact plain source.
- A plain L-record has columns 6–7 blank and `L` in column 8; `X` or another letter in column 6 marks an XREF/continuation record and must not start a new level block when attaching comments.
- Report only levels a reader cannot resolve from the adopted file: no unique byte-exact plain XREF source, and no fit basis, own `cL E$` note, or col-77 flag note. Flag DE blank/non-blank mismatch with the source level as advisory.


## Report Output

| Type | What to report |
|---|---|
| Value mismatch | source value vs target value (exact text) |
| Uncertainty mismatch | source uncertainty vs target uncertainty (exact text) |
| Format mismatch | sign, decimal precision, trailing zero, qualifier (`GT`/`LT`/`?`/`S`) |
| XREF mismatch | full XREF string: source vs target (note: `(3330*)` ≠ `(3330)` — `*` is semantically significant) |
| Provenance mismatch | wrong or missing NSR key / cL-cG quoted value |
| Completeness mismatch | missing or extra level/gamma — check whether it is a level split (`1 MRG → 2 ENS`) or merge (`2 ENS → 1 MRG`) before calling it an error |
