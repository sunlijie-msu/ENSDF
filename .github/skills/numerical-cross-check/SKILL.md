---
name: numerical-cross-check
description: "Validates data consistency between ENSDF records and tabular or comparison sources such as CSV files, Markdown tables, MRG merge files, and raw ENSDF datasets. Use after large-scale data entry to verify that values, uncertainties, and provenance comments were transferred correctly. Checks completeness, numerical exactness, provenance comments, energy ordering, and field positioning. CHECK-ONLY — reports findings without editing files."
---

# Numerical Cross-Check

## Scope

CHECK-ONLY skill — do not edit any files.

Use to verify ENSDF data against a source of truth after bulk data entry:
- ENSDF vs CSV or Markdown table
- ENSDF vs `.mrg` or raw `.ens`
- One-quantity audits (level energy, gamma energy, RI, MR, quoted comments)

For field definitions, exact column positions, uncertainty notation, ENSDF structural relationships (L→G grouping, cL/cG scope, ascending energy order), and left-justification rules, see `.github/copilot-instructions.md`.

## Workflow

Copy this checklist when starting:

```
Cross-Check Progress
- [ ] 1. Confirm scope and files
- [ ] 2. Parse target ENSDF fields
- [ ] 3. Parse source (correct type)
- [ ] 4. Compare values, uncertainties, and provenance
- [ ] 5. Bidirectional mapping (table sources)
- [ ] 6. Reproducible 15% spot-check
- [ ] 7. Report findings
```

### 1. Confirm Scope

Record: target file, source file, quantity, any user-specified line range, level set, or energy range. Do not expand beyond the stated scope.

### 2. Parse Target ENSDF

Extract only the fields needed.

Common targets: L-record energy or Jπ; G-record energy, RI, DRI, M, MR; `cL`/`cG` comments quoting source values.

**Critical matching rule:** Never match a source gamma to ENSDF by gamma energy alone. Match the parent L-record first, then the specific G-record within that level block.

### 3. Parse the Source

**Tables:**
- Map every column explicitly, including blank columns
- Treat blank cells as positional placeholders — each one shifts all subsequent positions
- Derive quantities only when the source requires it

**`.mrg`, raw `.ens`, comparison text:**
- Identify the actual source record being quoted
- When multiple similar gamma energies exist, use both the initial-level energy and the gamma energy to identify the correct record

### 4. Compare Data

Check exactly what was requested:
- Exact value match (character-for-character)
- Exact uncertainty match, including asymmetric uncertainties and `GT`/`LT` markers
- Correct source attribution in `cL`/`cG` comments
- Missing or spurious entries within scope

Typical findings: missing level/gamma · extra entry · value mismatch · uncertainty mismatch · wrong source cited · correct field value but incorrect quoted comment text.

### 5. Bidirectional Mapping

Mandatory for table sources. Verify both directions:
- Source header → source cell → ENSDF field
- ENSDF field → source row → source column header

Confirm blank-column counting, row alignment, and derived-quantity mapping in both passes.

### 6. Reproducible 15% Spot-Check

$$\text{sample} = \max\!\left(10,\; \lceil 0.15 \times N \rceil\right)$$

- Use a fixed random seed; report the seed and sample size
- Require 100% pass rate
- If any sample fails: stop, identify the error class, re-check all affected entries, then repeat with a new sample

### 7. Report Findings

```
CROSS-CHECK REPORT

Target:  <target file>
Source:  <source file>
Scope:   <quantity and range>

Results:
  Source entries in scope:       <N>
  Matching ENSDF entries:        <n>
  Missing entries:               <n>
  Extra entries:                 <n>
  Value mismatches:              <n>
  Uncertainty mismatches:        <n>
  Provenance/comment mismatches: <n>

Spot-check:
  Seed: <seed>   Sample: <n>/<N>   Result: PASS / FAIL

Final status: PASS / FAIL
```

State explicitly what was checked and what was intentionally excluded from scope.

---

## Source-Specific Notes

### MRG RI audits
Identify which prefixed record supplies the adopted value. Check adopted G-record RI/DRI against that record, and each `cG RI$` quoted value against the cited source record.

### MR or multipolarity audits
Check value, uncertainty, sign, and exact wording of `cG M,MR$` or `cG MR$` when source values are quoted.

### Completeness audits
Confirm all source levels or gammas in scope are present and attached to the correct parent level.

### Table artifacts
Document OCR-joined cells, blank separator columns, Eg-only entries, limit markers (`GT`/`LT`), and alternate solutions quoted in a single cell.

---

## Related Skills

- `large-scale-data-entry`
- `comment-quoted-values-check`
- `adopted-vs-individual-dataset-comparison`
