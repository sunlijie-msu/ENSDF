---
name: data-cross-check
description: "Checks target data in ENS files against source data for exact consistency after data entry. Use when validating target data in ENS files against source data from CSV, Markdown, MRG, ENS, or ADP files, including values, uncertainties, signs, limits, decimal digits, units, provenance comments, strings, XREFs, and completeness."
---

# Data Cross-Check

Verify 100% consistency between source data and target `.ens` data. Report every mismatch.

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to source .mrg/.adp/.ens/.md/.csv file]`
- Target: `[path to target .ens file]`

### Field Mapping *(source → ENS)*
- `[Data A]` → `[record type]` `[field name]`
- `[Data B]` → `[record type]` `[field name]`
- `[Data C]` → `[record type]` `[comment]`

### Checks
  [ ] value and sign
  [ ] uncertainty and format
  [ ] decimal places and trailing zeros
  [ ] limits / qualifiers (GT, LT, ?, S)
  [ ] XREF strings character-for-character (asterisk * is semantically significant) if applicable
  [ ] provenance in cL/cG comments
  [ ] completeness (missing/extra)

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV
- G-records: `[ ]` exact Eγ  `[ ]` Eγ within ±[N] keV  `[ ]` parent L first, then Eγ

### Special Handling
  [ ] [describe non-standard cases]

## Workflow

```
Cross-Check Procedure
- [ ] 1. Confirm Task Configuration
- [ ] 2. Carefully parse source and target within scope
- [ ] 3. Extract the data needed for the task.
- [ ] 4. For ≥20 records: write a script to regenerate all expected ENSDF records from source, compare line-by-line against target, and report mismatches. For <20 records: compare character-by-character manually.
- [ ] 5. Run reproducible 15% random spot-check (copilot-instructions.md § 5)
- [ ] 6. Report all mismatches with locations
```

## Required Matching Rules

- Never match a gamma by Eγ alone; match parent L-record first.
- For CSV/Markdown tables, include blank separator columns in the mapping.
- For near-equal energies, use both level energy and transition energy for matching.
- Script-based regenerate-then-compare is preferred for ≥20 records; it catches format mismatches (sign, trailing zero, `{I}` precision) that manual comparison misses.

## Report Output

| Type | What to report |
|---|---|
| Value mismatch | source value vs target value (exact text) |
| Uncertainty mismatch | source uncertainty vs target uncertainty (exact text) |
| Format mismatch | sign, decimal precision, trailing zero, qualifier (`GT`/`LT`/`?`/`S`) |
| XREF mismatch | full XREF string: source vs target (note: `(3330*)` ≠ `(3330)` — `*` is semantically significant) |
| Provenance mismatch | wrong or missing NSR key / cL-cG quoted value |
| Completeness mismatch | missing or extra level/gamma — check whether it is a level split (`1 MRG → 2 ENS`) or merge (`2 ENS → 1 MRG`) before calling it an error |
