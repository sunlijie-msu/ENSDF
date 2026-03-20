---
name: numerical-cross-check
description: >
  Use this skill when validating data consistency between ENSDF records and
  tabular or comparison sources such as CSV files, Markdown tables, MRG
  merge files, and raw ENSDF datasets. Checks completeness, numerical
  exactness, provenance comments, energy ordering, and field positioning.
  CHECK-ONLY — reports findings without editing files.
mode: check-only
applies-to: "**"
---

# Numerical Cross-Check

## Overview

Use this skill to verify that ENSDF data matches a source of truth without editing files.

Use it for:
- ENSDF vs CSV or Markdown table
- ENSDF vs `.mrg` or raw `.ens`
- One-quantity audits such as level energy, gamma energy, RI, MR, or quoted comments

Keep the work minimal and exact:
- Match values and uncertainties character-for-character
- Verify mapping, not just arithmetic
- Stay inside the requested scope
- Use a reproducible 5% spot-check

## Workflow

Copy this checklist while working:

```text
Cross-Check Progress
- [ ] Confirm scope and files
- [ ] Parse target ENSDF fields
- [ ] Parse the correct source type
- [ ] Compare values, uncertainties, and provenance
- [ ] Do bidirectional mapping for table-like sources
- [ ] Do reproducible 15% spot-check
- [ ] Report exact findings
```

### 1. Confirm Scope

Record the target file, source file, quantity under review, and any user-specified line range, level set, or energy range.

Do not expand beyond the requested scope.

### 2. Parse Target ENSDF

Extract only the fields needed for the task.

Common targets:
- L-record energy or Jπ
- G-record energy, RI, DRI, M, or MR
- `cL` or `cG` comments quoting source values

Preserve ENSDF grouping rules:
- G-records belong to the preceding L-record
- `cL` applies only to the preceding L-record
- `cG` applies only to the preceding G-record
- Never match a source gamma to ENSDF by gamma energy alone; match the parent L-record first, then the specific G-record within that level block.

### 3. Parse the Source

Choose the matching source path.

For tables:
- Identify the real columns, including blank columns
- Map each row and column explicitly
- Treat blank cells as positional placeholders
- Derive quantities only when the source requires it

For `.mrg`, raw `.ens`, or comparison text:
- Identify the actual source record being quoted
- Compare the adopted field against that record
- Compare quoted comment text against the cited source record
- When multiple similar gamma energies exist, use both the initial level and the gamma energy to identify the correct record.

### 4. Compare Data

Check exactly what the user asked for.

Required checks:
- Exact value match
- Exact uncertainty match, including alternate solutions and `GT`/`LT`
- Correct source attribution in comments
- Missing or spurious entries in scope

Typical findings:
- Missing level or gamma
- Extra adopted entry not present in source scope
- Value mismatch
- Uncertainty mismatch
- Wrong source cited
- Correct field value but incorrect quoted comment text

### 5. Bidirectional Mapping

Mandatory for table-like sources.

Verify both directions:
- Source header/key to source cell to ENSDF field
- ENSDF field back to source row and source column

Confirm blank-column counting, row alignment, and derived-quantity mapping.

### 6. Reproducible 15% Spot-Check

Minimum sample size:

$$
\max\left(5, \lceil 0.15 \times N \rceil\right)
$$

Use a fixed seed, report the seed and sample size, and require a 100% pass rate in the sample.

If any sampled entry fails, stop and re-check the affected class before reporting final status.

### 7. Report Findings

Use a compact report with exact counts.

```text
CROSS-CHECK REPORT

Target: <target file>
Source: <source file or files>
Scope: <quantity and range>

Results:
- Source entries in scope: <count>
- Matching ENSDF entries: <count>
- Missing entries: <count>
- Extra entries: <count>
- Value mismatches: <count>
- Uncertainty mismatches: <count>
- Provenance/comment mismatches: <count>

Spot-check:
- Seed: <seed>
- Sample size: <count>
- Result: PASS/FAIL

Final status: PASS/FAIL
```

## Source-Specific Notes

### MRG RI audits

- Identify which prefixed record supplies the adopted value
- Check the adopted G-record RI/DRI against that record
- Check each `cG RI$` quoted value against the cited source record

### MR or multipolarity audits

Check the MR value, uncertainty, sign, and exact wording of `cG M,MR$` or `cG MR$` when source values are quoted there.

### Completeness audits

Check that all source levels or gammas in scope are present and attached to the correct parent level.

### Table artifacts

Handle and document OCR-joined cells, blank separator columns, Eg-only entries, limit markers, and alternate solutions quoted in one cell.

## Output Rules

- CHECK-ONLY: do not edit files
- Report exact values, not paraphrases
- State what was checked and what was intentionally not checked
- If the source is ambiguous, say so explicitly

## Related Skills

- `large-scale-data-entry`
- `comment-quoted-values-check`
- `adopted-vs-individual-dataset-comparison`
