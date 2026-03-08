---
name: data-consistency-cross-check
description: Perform meticulous data consistency validation between ENSDF files and CSV source data. Systematically verifies L-record completeness, energy ordering, G-record accuracy, and structural compliance using bidirectional positional checks and random spot-check sampling.
mode: check-only
applies-to: ENSDF datasets with corresponding source CSV files
---

# Data Consistency Cross-Check (ENSDF vs CSV)

## Overview

This skill provides a systematic workflow for conducting rigorous data consistency validation between Evaluated Nuclear Structure Data File (ENSDF) records and their corresponding Comma-Separated Value (CSV) source tables. The workflow prioritizes **data accuracy and integrity** over formatting concerns, employing a multi-tier validation approach to detect discrepancies at both structural and numerical levels.

**Scope:** Applicable to any ENSDF file undergoing data entry from tabular sources (CSV, Excel converted to CSV, or PDF-extracted tables).

**Mode:** **CHECK-ONLY** — This skill validates existing data without modifying files.

---

## Key Principles

### Primary Objectives

1. **Verify Completeness:** Confirm all source data (levels, transitions) are present in the ENSDF file
2. **Validate Accuracy:** Cross-check numerical values, uncertainties, and derived quantities (e.g., $E_\gamma = E_i - E_f$)
3. **Ensure Consistency:** Verify that source column mappings and energy derivations are correctly implemented
4. **Detect Anomalies:** Identify missing or spurious entries using systematic bidirectional checks
5. **Quantify Results:** Report with exact metrics and reproducible sampling

### Quality Assurance Mindset

- **Zero tolerance for assumptions:** Verify every claim with evidence
- **Numerical exactness:** Match values character-for-character; report no approximations or rounding
- **Bidirectional verification:** Count both forward (header→data) and backward (data→header)
- **Reproducible sampling:** Use fixed random seeds for 5% spot-checks
- **Transparent reporting:** Disclose validation pass/fail status for each check

---

## Core Workflow

### Phase 1: File Preparation and Discovery

**Step 1.1 – Identify Source and Target Files**

Locate the following files in your workspace:

| File Type | Pattern | Purpose |
|-----------|---------|---------|
| ENSDF target | `*.ens` | Contains entered/existing data to validate |
| CSV source (Bound) | `*_Bound.csv` or `*_bound.csv` | Lower-lying levels (typically ground state region) |
| CSV source (Unbound) | `*_Unbound.csv` or `*_unbound.csv` | Higher-lying levels (decay/reaction region) |
| Optional: Documentation | `*.txt`, `*.md` | Methodology references for data entry |

**Step 1.2 – Note File Paths**

Record absolute or workspace-relative paths for all files. Example:

```
ENSDF:   A34/Cl34/raw/1983WA27.ens
Bound:   A34/Cl34/raw/1983WA27_Bound.csv
Unbound: A34/Cl34/raw/1983WA27_Unbound.csv
```

---

### Phase 2: Data Extraction and Parsing

**Step 2.1 – Parse ENSDF File**

Extract all nuclear level and gamma-ray data from the ENSDF file:

- **L-records:** Nuclear level excitation energies ($E_i$) in columns 10–19
  - Record all present $E_i$ values
  - Verify correct field positioning (left-justified)
  - Count total L-records and their energy range

- **G-records:** Gamma transition energies ($E_\gamma$) in columns 10–19 (belonging to preceding L-record)
  - Extract all $E_\gamma$ values per level
  - Record relative intensity (RI) from columns 23–29 (if present)
  - Identify "Eg-only" transitions (no RI/uncertainty values)
  - Count total G-records

**Implementation Tip:**  
Use Python with line-by-line parsing to extract fields:

```python
if len(line) > 10 and line[7:8] == 'L':
    e_str = line[9:19].strip()  # Energy in columns 10-19
    current_ei = float(e_str)
    levels[current_ei] = []

elif len(line) > 10 and line[7:8] == 'G' and current_ei in levels:
    eg_str = line[9:19].strip()
    ri_str = line[22:29].strip()
    levels[current_ei].append({'Eg': float(eg_str), 'RI': ri_str})
```

**Step 2.2 – Parse CSV Source File(s)**

Extract initial ($E_i$) and final ($E_f$) level energies and intensities:

- **Header row:** Identify columns containing $E_f$ values (usually numeric column headers)
- **Data rows:** Extract $I_\gamma$ values aligned with $E_f$ columns
- **"Other Ef" column:** Parse secondary transitions in format `Ef(Iγ)` or similar
- **Special markers:** Note cells marked as "X" (Eg-only), "<number>" (less-than), ">number>" (greater-than), or "unknown"

**Bidirectional Mapping Requirement:**  
For each row and column, verify position by:
1. **Forward count:** Header column index → corresponding data row cell
2. **Backward count:** Data cell → corresponding header column index
3. **Blank cell handling:** Count blank cells explicitly; each blank shifts subsequent column positions

**Implementation Tip:**  
Use Python CSV reader with explicit column indexing:

```python
with open('source.csv') as f:
    reader = csv.reader(f)
    headers = next(reader)  # Extract header columns
    for row_idx, row in enumerate(reader):
        ei = float(row[col_idx_Ei])  # Ei in specific column
        for col_idx, ef_value in enumerate(headers):
            if col_idx < len(row):
                iγ = extract_intensity(row[col_idx])  # Map row cell to Ef header
```

**Step 2.3 – Derive Gamma Energies from CSV**

Calculate expected $E_\gamma$ values from CSV data:

$$E_\gamma = E_i - E_f$$

**Precision Rules:**
- Decimal places in $E_\gamma$ = max(decimal places in $E_i$, decimal places in $E_f$)
- Round to nearest at output precision (banker's rounding preferred)
- Example: $E_i = 5576$ keV, $E_f = 2375.7$ keV → $E_\gamma = 5576 - 2375.7 = 3200.3$ keV (1 decimal)

---

### Phase 3: Structural Validation

**Step 3.1 – L-Record Completeness Check**

Verify that all initial energies from CSV are present in the ENSDF file:

| Check | Method | Expected Result |
|-------|--------|-----------------|
| **Ei presence** | Extract all CSV $E_i$ values; match against ENSDF L-record energies | 100% of CSV $E_i$ present in ENSDF |
| **Missing levels** | Set difference: CSV $E_i$ − ENSDF $E_i$ | Empty set (no missing values) |
| **Extra levels** | Set difference: ENSDF $E_i$ − CSV $E_i$ | None (or documented additions per user clarification) |

**Example reporting:**

```
✓ Unbound CSV levels:  41 entries
✓ ENSDF L-records:     41 entries
✓ Match:               41/41 (100%)
✗ Missing in ENSDF:    0
✗ Extra in ENSDF:      0
```

**Step 3.2 – Energy Ordering Compliance**

Verify strict ascending energy order using ENSDF validation tools:

```bash
python .github/scripts/check_gamma_ordering.py <filename.ens>
```

Expected output:
```
[OK] <filename>: All energy records are correctly ordered!
```

**What is checked:**
- L-records in ascending $E_i$ order
- G-records under each L-record in ascending $E_\gamma$ order
- No inversions or out-of-sequence energies

**Exit codes:**
- `0` = PASS (all records correctly ordered)
- `1` = FAIL (ordering violations detected)

**Step 3.3 – Column Formatting and Field Positioning**

Validate ENSDF structural compliance:

```bash
python .github/scripts/column_calibrate.py <filename.ens>
```

Expected output includes:
```
SUCCESS: All ENSDF field positions appear correct!
SUCCESS: All data record lines are exactly 80 characters!
[OK] SUCCESS: All ... values correctly LEFT-JUSTIFIED
```

**What is checked:**
- All lines exactly 80 characters (fixed-format ENSDF requirement)
- Energy values left-justified in columns 10–19
- Intensity (RI) values left-justified at column 23
- Uncertainty fields (DE, DRI, etc.) correctly positioned
- All field content complies with ENSDF column specifications

**Note:** This check does NOT edit files; it only validates positioning.

---

### Phase 4: Data Accuracy Validation

**Step 4.1 – Bidirectional Positional Check**

Systematically verify column alignment between CSV headers and data rows:

**Required steps:**

1. **List all header columns explicitly**, including blank column positions
2. **Count blank cells meticulously** between data columns
3. **Perform forward verification:** For each header column, confirm the data row cell aligns correctly
4. **Perform backward verification:** For each data row cell, confirm it maps back to the correct header
5. **Arithmetic validation:** Verify $E_\gamma$ calculations account for blank cell shifts

**Example:**

```
CSV Header Row:   ,Ef keV,Ef keV,Ef keV,Ef keV,Other Ef(Ig)
                  1       2      3      4      5
Data Row:         ,0      ,146.4 ,461.0 ,665.6 ,"2375.7(0.4), ..."
                  1       2      3      4      5
Bidirectional:    ✓ Col 2 header (0 keV) ↔ Col 2 data (0 keV) — MATCH
                  ✓ Col 3 header (146.4 keV) ↔ Col 3 data (146.4 keV) — MATCH
```

**Step 4.2 – Random Spot-Check (5% Minimum Sampling)**

Select random samples from your data to verify accuracy:

**Sample Size Calculation:**

$$\text{Sample size} = \max\left(5, \left\lceil 0.05 \times \text{Total entries} \right\rceil\right)$$

Example: 200 transitions → 10 samples (5%)

**Reproducible Sampling:**

```python
import random
random.seed(20260308)  # Fixed seed for reproducibility
sample_indices = random.sample(range(total_entries), sample_size)
```

**Verification Checklist (100% Pass Rate Required):**

For each sampled entry:

- ✅ **Value accuracy:** CSV value matches ENSDF value (character-for-character)
- ✅ **Uncertainty accuracy:** CSV uncertainty matches ENSDF uncertainty
- ✅ **Arithmetic correctness:** $E_\gamma = E_i - E_f$ computed correctly
- ✅ **Decimal place matching:** $E_\gamma$ decimal places = max($E_i$ decimals, $E_f$ decimals)
- ✅ **Field positioning:** Value in correct ENSDF columns (left-justified)
- ✅ **Alignment:** No off-by-one errors in row/column mapping

**Example spot-check entry:**

```
Sample: Ei = 5576 keV, Ef = 2375.7 keV
Expected Eγ = 5576 − 2375.7 = 3200.3 keV
CSV value: Iγ = 0.4
ENSDF entry: G 3200.3      0.4
Result: ✓ PASS (arithmetic, positioning, and alignment correct)
```

**Error Handling:**

If any errors are found in the spot-check:

1. **Stop immediately** and do not claim completion
2. **Identify root cause:** Systematic error (affects all entries) or isolated?
3. **Analyze error pattern:** Column mapping error? Decimal place miscalculation? Off-by-one indexing?
4. **Correct all instances** of the identified error type
5. **Rerun automated validators** (`column_calibrate.py` and `check_gamma_ordering.py`)
6. **Perform new spot-check** with different random samples
7. **Repeat until 100% pass rate** is achieved

---

### Phase 5: Special Cases and Anomalies

**Eg-Only Transitions**

Some CSV rows may contain "X" or blank intensity cells with an $E_\gamma$ value. These are entered as **Eg-only G-records** (no RI/DRI fields):

- **CSV indicator:** "X" or missing intensity value in a column with a non-blank $E_\gamma$
- **ENSDF representation:** G-record with $E_\gamma$ value only; RI and DRI columns left blank
- **Validation:** Confirm Eg-only G-records are present under the correct L-record

**Example:**

```
CSV: Ei=4461.4 keV, Ef=0 keV, Iγ=X
ENSDF: 34CL  L 4461.4
       34CL  G 4315.0                                                 
           (note: no RI/DRI values)
```

**PDF OCR Artifacts**

CSV files extracted from PDF images may contain OCR join errors:

- **Artifact pattern:** `2580.4(4.9).3129.13(2.1)` instead of `2580.4(4.9), 3129.13(2.1)`
- **Normalization:** Replace `.` with `,` and re-parse individual (Ef, Iγ) pairs
- **ENSDF result:** Each parsed pair appears as a separate G-record

**Verification method:**

1. Identify cells with missing commas or irregular delimiters
2. Normalize artifacts using string replacement
3. Re-parse to extract individual transition pairs
4. Verify each parsed transition is present as a separate G-record in ENSDF
5. **Document:** Note which rows contain artifacts; flag them as "expected OCR normalization"

**Less-Than and Greater-Than Intensity Values**

CSV may contain `<1.6` or `>5.2` for intensity bounds:

- **ENSDF representation:** RI field contains numerical value; DRI field contains "LT" or "GT" marker
- **Example:** CSV `<1.6` → ENSDF G-record with RI=1.6 and DRI="LT"

---

## Validation Tools Reference

### Tool: `column_calibrate.py`

**Purpose:** Validate ENSDF field positioning and 80-character line format

**Usage:**
```bash
python .github/scripts/column_calibrate.py <filename.ens>
```

**Output interpretation:**

| Signal | Meaning | Action |
|--------|---------|--------|
| `SUCCESS: All ENSDF field positions appear correct!` | All fields positioned correctly | ✓ Proceed |
| `ERROR: Field positioning errors found` | Field alignment violations detected | ✗ Abort; fix manually |
| `DATA RECORD LINE LENGTH ISSUES DETECTED` | Lines not exactly 80 characters | ✗ Abort; investigate |
| `0 errors` in summary | All checks passed | ✓ Proceed |

**Exit codes:** `0` = PASS; `1` = FAIL

### Tool: `check_gamma_ordering.py`

**Purpose:** Verify L-record and G-record energy ordering

**Usage:**
```bash
python .github/scripts/check_gamma_ordering.py <filename.ens>
```

**Output interpretation:**

| Signal | Meaning | Action |
|--------|---------|--------|
| `[OK] All energy records are correctly ordered!` | All records in ascending order | ✓ Proceed |
| `[ERROR] Energy ordering violation found` | Out-of-sequence entries detected | ✗ Abort; reorder |

**Exit code:** `0` = PASS; `1` = FAIL

### Tool: `ensdf_1line_ruler.py`

**Purpose:** Validate individual line format against ENSDF specification

**Usage (single-line check):**
```bash
python .github/scripts/ensdf_1line_ruler.py --line "your 80-char line"
```

**Output:** Visual ruler overlay + field validation + exit code 0 (PASS) or 1 (FAIL)

---

## Comparison Checklist

Use the following table during validation to track all checks:

| Check | Method | Status | Notes |
|-------|--------|--------|-------|
| **Unbound L-record count** | CSV row count vs ENSDF L-count | ✓ or ✗ | |
| **Bound L-record count** | CSV row count + documented additions | ✓ or ✗ | |
| **L-record energy matching** | Set intersection (100% expected) | ✓ or ✗ | |
| **G-record count** | Total parsed vs imported | ✓ or ✗ | |
| **Energy ordering (L)** | `check_gamma_ordering.py` | ✓ or ✗ | |
| **Energy ordering (G)** | `check_gamma_ordering.py` | ✓ or ✗ | |
| **Column formatting** | `column_calibrate.py` | ✓ or ✗ | |
| **Field positioning** | `column_calibrate.py` | ✓ or ✗ | |
| **80-char lines** | `column_calibrate.py` | ✓ or ✗ | |
| **Bidirectional mapping** | Forward + backward count | ✓ or ✗ | |
| **Arithmetic ($E_\gamma$)** | Spot-check sample (5%) | ✓ or ✗ | |
| **Spot-check pass rate** | Minimum 100% | ✓ or ✗ | |

---

## Example Output Report

```
========================================
DATA CONSISTENCY CROSS-CHECK REPORT
========================================

File: A34/Cl34/raw/1983WA27.ens
Sources: 1983WA27_Bound.csv + 1983WA27_Unbound.csv

[PHASE 1] FILE DISCOVERY
✓ ENSDF:   Found (87 L-records, 692 G-records)
✓ Bound:   Found (44 Ei rows)
✓ Unbound: Found (41 Ei rows)

[PHASE 2] DATA EXTRACTION
✓ ENSDF L-records parsed:     87 levels (0.0 – 7080.0 keV)
✓ ENSDF G-records parsed:     692 transitions
✓ Bound CSV Ei values:        44 initial energies
✓ Unbound CSV Ei values:      41 initial energies

[PHASE 3] STRUCTURAL VALIDATION
✓ L-record completeness:      41/41 unbound (100%)
✓ Bound additions:            2 documented (Ei=4606, 4610)
✓ Energy ordering (L):        PASS (87 levels in ascending order)
✓ Energy ordering (G):        PASS (all 692 transitions ordered)
✓ Column formatting:          PASS (all 80-char, left-justified)
✓ Field positioning:          PASS (all fields correct)

[PHASE 4] DATA ACCURACY
✓ Bidirectional check:        PASS (forward ↔ backward mapping verified)
✓ Spot-check sample size:     5 transitions (5% of 100+)
✓ Spot-check results:         5/5 PASS (100% accuracy)
✓ Eg-only transitions:        4 levels verified (4461.4, 4606, 4610, 5171.6)

[PHASE 5] ANOMALIES
✓ OCR artifacts handled:      Yes (normalized PDF join artifacts)
✓ Less-than/greater-than:     Yes (LT/GT markers in DRI fields)

========================================
FINAL STATUS: ✓ ALL CHECKS PASSED
========================================
```

---

## Recommendations for Future Use

1. **Automate the workflow:** Consider wrapping the multi-phase process in a Python script for repeated use
2. **Document assumptions:** Clearly state which CSV columns map to which $E_f$ values
3. **Track anomalies:** Maintain a log of PDF OCR artifacts and X-marked entries for each dataset
4. **Version tracking:** Use git to track changes between validation runs
5. **Preserve metadata:** Record validation date, random seed, sample count, and pass/fail status
6. **Escalate errors:** If spot-checks fail, investigate the root cause before proceeding to the next dataset

---

## Related Skills

- **large-scale-data-entry:** For initial CSV → ENSDF data import
- **comment-quoted-values-check:** For validating comment references (cG J$ lines)
- **xref-label-update:** For updating cross-reference labels when levels are added/removed

---

## Technical Notes

### ENSDF Column Specifications (Reference)

| Record | Field | Columns | Description |
|--------|-------|---------|-------------|
| L, G | E | 10–19 | Energy (keV), left-justified |
| G | RI | 23–29 | Relative intensity, left-justified |
| G | DRI | 30–31 | RI uncertainty or GT/LT marker |

### CSV → ENSDF Derivation Formula

$$E_\gamma = E_i - E_f$$

Precision: $\text{decimals}(E_\gamma) = \max(\text{decimals}(E_i), \text{decimals}(E_f))$

---

## Glossary

- **$E_i$:** Excitation energy of initial (parent) nuclear level
- **$E_f$:** Excitation energy of final (daughter) nuclear level
- **$E_\gamma$:** Gamma-ray transition energy
- **$I_\gamma$:** Relative photon intensity
- **L-record:** ENSDF level record defining a nuclear state
- **G-record:** ENSDF gamma-ray transition record (always follows an L-record)
- **Eg-only:** Gamma-ray transition with known energy but unknown intensity
- **Bidirectional check:** Verification in both forward and reverse directions to detect position errors
- **Spot-check:** Random sampling validation (typically 5% of total entries)

---

**Last Updated:** March 8, 2026  
**Status:** Finalized based on Cl-34 cross-check validation
