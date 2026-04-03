---
name: reconciling-data
description: "Merges, updates, or replaces data in a target ENSDF file using data extracted from a source file (CSV, Markdown table, MRG, ADP, or raw ENS). User specifies per task what to replace, keep, add, merge, or average. Use when synchronizing Adopted files with source data files, updating energies or intensities while preserving other quantities, or reconciling data from multiple sources."
---

# Reconciling ENSDF Data

## Task Configuration

**User fills in this block at the start of each task. Update as needed.**

```
SOURCE:   [path to source file]
TARGET:   [path to target .ens file]

MAPPING  (source data → ENSDF data fields in records/comments)
  [Data A]  →  [record type, field name, comments]
  [Data B]  →  [record type, field name, comments]

OPERATIONS
  REPLACE   [field]  with source value   [e.g., G-record RI, DRI from source]
  KEEP      [field]  from target         [e.g., G-record M, MR, DMR; cG M$ comments]
  ADD       [field]  from source         [e.g., new G-records absent in target]
  MERGE     [field]  from both           [e.g., cG RI$ comments quoting both sources]
  AVERAGE   [field]  across sources      [e.g., weighted average of two RI datasets]

MATCHING
  Match L-records by:   [ ] exact E    [ ] E within ±[N] keV
  Match G-records by:   [ ] exact Eγ   [ ] Eγ within ±[N] keV   [ ] parent L first, then Eγ

SPECIAL HANDLING
  [ ] [specify any non-standard cases]

```

## Workflow

Copy this checklist at task start:

```
Reconciling Progress:
- [ ] 1. Task configuration confirmed
- [ ] 2. Source data parsed and mapped
- [ ] 3. Target fields to keep captured
- [ ] 4. Records matched (log unmatched cases)
- [ ] 5. Operations applied (replace / keep / add / merge / average)
- [ ] 6. Per-line ruler validation — every edited line exit code 0
- [ ] 7. column_calibrate.py — exit code 0
- [ ] 8. check_gamma_ordering.py — exit code 0
- [ ] 9. Report issued
```

### Step 1 — Confirm Task Configuration

Resolve any ambiguity in one focused question. Do not proceed with an incomplete operation list or uncertain matching strategy.

### Step 2 — Parse Source Data

Read source file and extract the fields specified in Task Configuration. For tabular sources, build an explicit column map (all columns including blanks) and verify bidirectionally. See `copilot-instructions.md` § 5 for blank-cell counting rules.

### Step 3 — Capture Target Fields to Keep

Read the target file and cache every field marked KEEP — exact character-for-character values. These must survive the reconciliation unchanged.

### Step 4 — Match Records

- Match L-records first by energy (exact or within stated tolerance).
- Within each matched L-record, match G-records by Eγ (exact or within stated tolerance).
- **Log every unmatched case** — do not silently skip or auto-assign.
- Do not replace a credible existing energy merely because a source value differs within tolerance. Report and confirm with user if ambiguous.

### Step 5 — Apply Operations

For each matched record, apply the operations from Task Configuration in this order:

1. **REPLACE** — overwrite target field with source value (left-justify, exact notation)
2. **KEEP** — restore cached target value (do not touch)
3. **ADD** — insert new records absent in target (maintain ascending energy order)
4. **MERGE** — add `cG` or `cL` comment quoting the other-source value
5. **AVERAGE** — compute weighted average; enter result and uncertainty; add provenance comments


---

