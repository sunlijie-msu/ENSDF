---
name: value-occurrence-check
description: >
  Use this skill when checking consistency of nuclear level energies across
  multiple occurrences in a gamma-ray transition CSV, Markdown, or pipe
  table. Verifies that energy, uncertainty, and J-π are identical wherever
  a level appears as both an initial (Ei) and final (Ef) state. Mandates
  explicit column mapping including blank cells and bidirectional
  forward/backward verification.
argument-hint: [CSV, Markdown, or pipe table file]
---

# Value Occurrence Check

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Verify that every nuclear level energy appearing multiple times in a gamma-ray transition table has consistent energy, uncertainty, and J-π across all occurrences.

## When to Use

- Before entering CSV table data into ENSDF records
- Before entering Markdown or pipe-table data into ENSDF records
- When a gamma-ray transition table lists levels as both initial (Ei) and final (Ef) states
- To catch transcription errors or inconsistent J-π assignments across table entries

## Method

### Step 1: Column Mapping

Follow the bidirectional column mapping protocol from `copilot-instructions.md` Section 5:

1. List all header columns explicitly, including blank positions
2. Count blank cells as positional placeholders
3. For Markdown pipe tables, exclude section titles, separator rows, and repeated headers from the data-row count
4. Forward verification: header → data
5. Backward verification: data → header

### Step 2: Occurrence Scan

For every unique level energy in the table:

1. Use explicit Ei rows as the canonical level registry; do not cluster or average nearby energies
2. Collect all rows where the level appears as Ei or as derived final energy Ef = Ei − Eγ
3. For row-wise transition tables, match derived Ef to the nearest canonical Ei within ≤1.0 keV
4. If two candidates are equally near, flag the row as ambiguous rather than choosing one silently
5. Compare explicit energy strings character-for-character across repeated Ei occurrences
6. Compare uncertainty strings only if the table explicitly provides level uncertainties
7. Compare J-π character-for-character

### Step 3: Report Inconsistencies

For each mismatch:

```
LEVEL: 1175.3 keV
  Row 7:  Ef=1175.3(1), Jπf=5/2-     ✓
  Row 26: Ei=1175.3(1), Jπi=5/2      ✗ parity mismatch (- vs none)
  Row 49: Ei=1175.3(2), Jπi=5/2-     ✗ uncertainty mismatch (1 vs 2)
```

### Step 4: Validate Completeness

- Ground state (0 keV) appears only as Ef
- A missing explicit 0-keV row is not itself an inconsistency if the table encodes the ground state only through Ef≈0
- Every level energy has been checked
- Every data row has been checked against the canonical level registry
- 100% of occurrences verified before claiming completion

## Data Fidelity

Preserve every decimal place exactly — do not round, omit, alter, or add digits. 10.0 remains 10.0, not 10 or 10.00. For energy matching: allow ≤1.0 keV tolerance when (Ei − Eγ) ≠ canonical Ei due to measurement precision.


## Spot-Check Protocol

Use reproducible random sampling: seed (e.g., 12520260409), sample size ≥15% of rows, verify energy-matching residuals and J-π consistency on each sample.
Record for each sampled row: source line, Ei, Eγ, derived Ef, matched canonical level, residual, and PASS/FAIL.

## Gotchas

- Blank cells and non-data rows cause misalignment — exclude and count meticulously
- Markdown pipe tables often repeat headers between sections — do not count those as data rows
- AI models frequently fail at table corners — apply extra scrutiny
- Energy residuals from rounding are expected; focus on J-π consistency
- Near-degenerate levels can be distinct physical states — never merge them just because they are close in energy
- Normalize Unicode variants only for parsing if needed; keep reported source values unchanged
- Terminal (non-depopulated) levels do not indicate errors
