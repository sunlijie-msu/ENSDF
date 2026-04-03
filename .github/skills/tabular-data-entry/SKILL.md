---
name: tabular-data-entry
description: "Performs bulk data entry from CSV or Markdown tables into ENSDF L-records and G-records. Enforces bidirectional column mapping,  and mandatory 15% spot-check validation. Use when transferring ≥10 numeric data points from a paper table or CSV file into an ENSDF dataset file."
---

# Tabular Data Entry for ENSDF

## Task Configuration

**User fills in this block at the start of each task. Update as needed.**

```
SOURCE:   [path to CSV or Markdown file]
TARGET:   [path to .ens file]

COLUMN MAPPING  (source column → ENSDF field)
  [Column A]  →  L-record E    (level energy, keV, cols 10–19)
  [Column B]  →  G-record E    (gamma energy, computed Ei − Ef or direct)
  [Column C]  →  G-record RI   (relative photon intensity, cols 23–29)
  [Column D]  →  G-record DRI  (uncertainty in RI, cols 30–31)
  [...]       →  [field]       [description]

OPERATIONS
  [ ] Unit conversion:  [e.g., MeV × 1000 → keV]
  [ ] Eγ calculation:   Eγ = Ei − Ef
  [ ] Other:            [describe]

SPECIAL HANDLING
  [ ] "Other Ef" column   Ef(Iγ) format — see § Other-Ef Column
  [ ] Limit markers       < or > in RI cells → GT/LT in DRI field
  [ ] DCO ratios          → cG comments only, not data fields
  [ ] Mixed-format cells  [e.g., "35±1" — describe parsing]
```

## Workflow

Copy this checklist at task start:

```
Data Entry Progress:
- [ ] 1. Task configuration confirmed
- [ ] 2. Explicit column map built (all columns, including blanks)
- [ ] 3. Bidirectional positional check passed (forward + backward, two endpoints)
- [ ] 4. L-records and G-records entered, ascending energy order maintained. column_calibrate.py — exit code 0. check_gamma_ordering.py — exit code 0
- [ ] 5. 15% spot-check passed (seed and sample size reported)
- [ ] 6. Report issued
```

### Confirm Task Configuration

Resolve any ambiguity with one focused question. Do not proceed with an incomplete or uncertain column map.

### Build the Explicit Column Map

Enumerate ALL columns — including blank separator columns — and assign a position number:

```
Pos | Source Header  | Content            | ENSDF target
----|----------------|--------------------|------------------------------
 1  | Ei (keV)       | Level energy       | L-record E (cols 10–19)
 2  | (blank)        | separator          | skip
 3  | Ef = 0         | Iγ to g.s.         | G-record RI (Eγ = Ei − 0)
 4  | Ef = 847 keV   | Iγ to 847-keV lvl  | G-record RI (Eγ = Ei − 847)
```

**CRITICAL:** Each blank column is a positional placeholder. Miscounting one shifts all subsequent columns.

### Bidirectional Positional Check

Before entering any data, verify the column map in both directions:

1. List all header columns explicitly, including blank positions
2. Count blank cells as positional placeholders
3. Forward verification: Column header → data column; Row header → data row
4. Backward verification: data column → column header; data row → row header
5. Arithmetic validation: verify calculations account for blank-cell shifts

1.  **Column alignment:** Explicitly map ALL columns, including blank ones. Never assume positions based on visible data alone.
2.  **Blank cells:** Count blank cells meticulously. Each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment.
3.  **Bidirectional verification:** Always cross-check both forward counting (header to data) and backward mapping (data to header) to ensure accurate alignment.
4.  **Critical column mapping:** When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).


### Random Spot Check
Full protocol: `copilot-instructions.md` § 5.