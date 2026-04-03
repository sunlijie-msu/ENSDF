---
name: numerical-cross-check
description: "Validates data consistency between ENSDF records and tabular data sources such as CSV files, Markdown tables, MRG files, and raw ENS dataset files. Use after large-scale data entry tasks to verify that values, uncertainties, and quoted data in comments were transferred correctly. Checks completeness, numerical exactness, provenance comments, and field positioning."
---

# Numerical Cross-Check

Verify 100% numerical exactness between a source file (CSV, Markdown, `.mrg`, `.ens`) and a target `.ens` file. Every discrepancy must be reported — none ignored or rounded away.

Field definitions, column positions, uncertainty notation, and ENSDF structural rules: `.github/copilot-instructions.md`.

## Workflow

```
Cross-Check Progress
- [ ] 1. Confirm scope: source file, target file, quantities, energy range
- [ ] 2. Build explicit field map (source → ENSDF record and field)
- [ ] 3. Compare character-for-character: value, uncertainty, decimal places, digits
- [ ] 4. Verify provenance comments (NSR key, quoted values in cL/cG)
- [ ] 5. 15% reproducible spot-check — see copilot-instructions.md § 5
- [ ] 6. Report all discrepancies
```

## Matching Rules

**Match parent L-record first, then G-record within that level block.** Never match gammas by Eγ alone.

For table sources: map every column explicitly including blank separator columns — each blank cell shifts all subsequent column positions.

## Numerical Exactness Checklist

For each matched record, verify:
- Value: exact digits and decimal places
- Uncertainty: exact digits, decimal places, asymmetric format (`+n-m`), and `GT`/`LT` markers
- NSR key and quoted values in `cL`/`cG` comments
- No missing or spurious entries within scope

## Source-Specific Notes

| Source | Key check |
|---|---|
| MRG | Identify which prefixed record is the adopted value; verify G-record RI/DRI against it |
| ENS | Use both initial-level energy and Eγ to resolve near-equal gamma energies |
| CSV/MD table | Account for OCR-joined cells, blank separator columns, and limit markers (`GT`/`LT`) |
