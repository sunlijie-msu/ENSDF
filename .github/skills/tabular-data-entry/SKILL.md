---
name: tabular-data-entry
description: "Performs bulk data entry from CSV or Markdown tables into ENSDF dataset L-records and G-records. Enforces bidirectional column mapping and mandatory 15% spot-check validation. Use when transferring ≥10 numeric data points from CSV or Markdown tables into an ENSDF dataset file."
---

# Tabular Data Entry for ENSDF

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Task Customization & Configuration

**User fills in this block at the start of each task. Update as needed.**

```
SOURCE:   [path to CSV or Markdown file]
TARGET:   [path to .ens file]

COLUMN MAPPING  (source column → ENSDF field)
  [Column A]  →  L-record E    (level energy, keV)
  [Column B]  →  L-record DE   (energy uncertainty)
  [Column C]  →  L-record J    (spin parity)
  [Column D]  →  L-record S    (spectroscopic factor)
  [Column E]  →  G-record E    (gamma energy, keV)
  [Column F]  →  G-record DE   (gamma energy uncertainty)
  [Column G]  →  G-record RI   (gamma intensity; Eγ = Ei − Ef)
  [...]       →  [field]

OPERATIONS
  [ ] Unit conversion:  [e.g., MeV × 1000 → keV] if needed
  [ ] Eγ calculation:   Eγ = Ei − Ef if needed
  [ ] ΔEγ assumption:  [Uncertainty of Eγ = 0.5 keV for all transitions.]

SPECIAL HANDLING
  [ ] "Other Ef" column   Ef(Iγ) format if needed
  [ ] Limit markers       < or > in RI cells → GT/LT in DRI field
  [ ] DCO or ADO ratios → cG comments only, not data fields
  [ ] POL values → cG comments only, positive needs + and negative needs - signs
  [ ] Other:              [describe]
```

## Standard Operating Procedure

- [ ] 1. Column map confirmed (all columns enumerated, including blanks)
- [ ] 2. Bidirectional positional check: forward (header→data) and backward (data→header)
- [ ] 3. Data entry: generate all new records with Python functions (preferred); assert `len(record) == 80` for each
- [ ] 4. Records entered in ascending energy order in  `multi_replace_string_in_file` call
- [ ] 4. `column_calibrate.py` — exit code 0; `check_gamma_ordering.py` — exit code 0
- [ ] 5. 15% spot-check passed (seed and sample size documented)
- [ ] 6. Report issued

**Column map rule:** Enumerate ALL columns including blank separators — each blank is a positional placeholder; miscounting one shifts all subsequent columns.

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

---
