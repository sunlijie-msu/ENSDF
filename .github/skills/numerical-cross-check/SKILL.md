---
name: numerical-cross-check
description: "Validates exact consistency between source data files (CSV, Markdown, MRG, ENS) and target ENSDF files after data entry or reconciliation. Checks values, uncertainties, signs, limits, decimal precision, units, provenance comments, strings, and completeness."
---

# Numerical Cross-Check

Verify 100% consistency between source data and target `.ens` records. Report every mismatch.

Data record and field definitions, column positions, uncertainty notation, structural rules, and spot-check policy: `.github/copilot-instructions.md`.

## Task Configuration

**User fills this block at task start. Update as needed.**

```
SOURCE:   [path]
TARGET:   [path]
SCOPE:    [levels / gammas / comments / XREF]

MAPPING  (source → ENSDF)
  [Data A]  -> [record.field]
  [Data B]  -> [record.field]

CHECKS
  [ ] value and sign
  [ ] uncertainty and format
  [ ] decimal places and trailing zeros
  [ ] limits / qualifiers (GT, LT, ?, S)
  [ ] XREF strings character-for-character (asterisk * is semantically significant)
  [ ] provenance in cL/cG comments
  [ ] completeness (missing/extra)

MATCHING
  L-records: [ ] exact E   [ ] E within ±[N] keV
  G-records: [ ] parent L first, then Eγ   [ ] Eγ within ±[N] keV
```

## Workflow

```
Cross-Check Progress
- [ ] 1. Confirm Task Configuration
- [ ] 2. Carefully parse source and target within scope
- [ ] 3. Extract the data needed for the task.
- [ ] 4. Carefully compare mapped data character-for-character
- [ ] 5. Run reproducible 15% random spot-check (copilot-instructions.md § 5)
- [ ] 6. Report all mismatches with locations
```

## Required Matching Rules

- Never match a gamma by Eγ alone; match parent L-record first.
- For CSV/Markdown tables, include blank separator columns in the mapping.
- For near-equal energies, use both level energy and transition energy.

## Report Output

| Type | What to report |
|---|---|
| Value mismatch | source value vs target value (exact text) |
| Uncertainty mismatch | source uncertainty vs target uncertainty (exact text) |
| Format mismatch | sign, decimal precision, trailing zero, qualifier (`GT`/`LT`/`?`/`S`) |
| XREF mismatch | full XREF string: source vs target (note: `(3330*)` ≠ `(3330)` — `*` is semantically significant) |
| Provenance mismatch | wrong or missing NSR key / cL-cG quoted value |
| Completeness mismatch | missing or extra level/gamma — check whether it is a level split (`1 MRG → 2 ENS`) or merge (`2 ENS → 1 MRG`) before calling it an error |
