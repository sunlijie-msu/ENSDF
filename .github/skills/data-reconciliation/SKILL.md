---
name: data-reconciliation
description: "Reconciles source data into a target ENS file by replacing, keeping, adding, merging, or averaging data records and fields. Use when synchronizing ENS files with source CSV, Markdown, MRG, ADP, or raw ENS data, or when updating energies, intensities, and comments while preserving selected target values."
---

# Reconciling ENSDF Data

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to source .mrg/.adp/.ens/.md/.csv file]`
- Target: `[path to target .ens file]`

### Field Mapping *(source → ENS)*
- `[Data A]` → `[record type]` `[field name]`
- `[Data B]` → `[record type]` `[field name]`

### Operations
- **Keep** `[field]` from target (e.g., M, MR, DMR; cG M$ comments)
- **Replace/Update** `[field]` with source value (e.g., RI, DRI)
- **Add/Insert** `[field]` from source (e.g., new G-records absent in target)
- **Merge/Combine** `[field]` from both (e.g., cG RI$ comments quoting both)
- **Average** `[field]` across sources (e.g., weighted average of RI)

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV
- G-records: `[ ]` exact Eγ  `[ ]` Eγ within ±[N] keV  `[ ]` parent L first, then Eγ

### Special Handling
- `[ ]` [describe non-standard cases]


## Workflow

```
Reconciling Procedure:
- [ ] 1. Task Customization & Configuration confirmed
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

For each matched record, apply the operations from Task Customization & Configuration


---

