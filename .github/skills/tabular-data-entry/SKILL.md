---
name: tabular-data-entry
description: "Performs bulk data entry from CSV or Markdown tables into ENSDF dataset L-records and G-records. Enforces bidirectional column mapping and mandatory 15% spot-check validation. Use when transferring ≥10 numeric data points from CSV or Markdown tables into an ENSDF dataset file."
---

# Tabular Data Entry for ENSDF

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

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
  [ ] Intensity uncertainty rounding: 3-digit DRI (e.g., 1.43) → round to ≤2 digits (1.4); round RI to matching decimal place
  [ ] Other:              [describe]
```

## Recommended Operating Procedures
1. [ ] **Map:** Enumerate all source columns (including blanks) for precise source-to-field mapping.
2. [ ] **Extract:** Extract required data via codes or scripts; verify numeric exactness, including values, uncertainties, signs, limits, decimal digits, units, parentheses, and completeness.
3. [ ] **Generate:** Generate ENSDF records and/or comments via code or scripts, ensuring correct column placement without shifting other fields.
4. [ ] **Cross-Check:** Perform bidirectional positional check (forward: header→data; backward: data→header) to confirm alignment.
5.  [ ] **Spot-Check:** Perform 15% random sample validation; trace each entry to source (value, uncertainty, position).
6.  [ ] **Report:** Issue final compliance report with seed and verification results.

### Bidirectional Positional Check

Verify the column map in both directions before entering data, counting blank cells as positional placeholders:

1. List all header columns explicitly, including blank positions.
2. Forward: header → data (column and row); Backward: data → header.
3. Confirm each cell by counting from top-left and again from bottom-right.
4. When fixing a quantity's position, adjust only field spacing — never move other field data to wrong columns.


### Random Spot Check
Trace entries to source: verify value, uncertainty, row, column, header, and units. (Protocol: `.github/copilot-instructions.md` § Random Spot Check)

### Bulk Insertion into `.ens` (diff-safe)

- Write a generator script in `.github/temp/...` that emits the expected 80-column block to a text file; use it as ground truth.
- Insert with the diff-aware edit tool in chunks (~85 records), anchoring each chunk on the current last line of the block. Verify the anchor is unique (energy search) before editing.
- After each chunk, compare the file block byte-for-byte against the expected file; report mismatches with wanted/got lines, then repair by re-editing (never `git restore`/`checkout`).
- Never let a script write to the `.ens`; a script may only produce the expected block.
- Classify records by cols 6–8 (continuation char + type; `PN` occupies cols 7–8), not col 8 alone. Check line endings with a binary read (Python text mode masks CRLF).

### Placement of Unplaced Gammas

- Unplaced G-records form one ascending-energy block immediately after the `PN` record and before the first `L`-record (precede with a blank line if the file does so).
- Set col-77 flag letters from the dataset's own field-flagged general comment (e.g. `cG E(X)$…` defines flag `X`); reproduce the author's existing flagged record byte-for-byte to confirm the mapping.
- Intensities absent in the source leave RI/DRI blank; never fabricate.
- A value too wide for the 7-char RI field (cols 23–29) becomes E-notation (`1.82E-4`) with DRI unchanged.

---
