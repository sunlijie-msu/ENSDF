---
name: large-scale-data-entry
description: Bulk data entry from CSV tables into ENSDF L-records and G-records. Extracts level energies, gamma energies, intensities, DCO ratios, and multipolarities. Enforces bidirectional column mapping, blank-cell counting, ascending energy ordering, and random 5% spot-check validation. Use for large datasets of 50+ numeric data points from papers, tables, or CSV files.
argument-hint: [CSV file] [ENSDF file]
---

# Large-Scale Data Entry for ENSDF

## Task Description
Extract E(level) for each initial level from the provided CSV file and populate the corresponding L-records in the ENSDF file.
Extract Eγ, Iγ, Initial level, DCO ratio, Multipolarity data for each γ-ray transition from the provided CSV file and populate the corresponding E and RI fields in ENSDF G-records.
DCO ratios should be added as comments following a G-record.

### Constraints
- **Edit scope**: Only modify data below the line `PN` record
- **Script reuse**: Leverage existing scripts for similar data entry tasks when available

---

## CRITICAL ENSDF REQUIREMENTS

### Data Fidelity
Meticulously extract all numerical data from the CSV table, ensuring absolute numerical exactness to the original source. Preserve every decimal place exactly — do not round, omit, alter, or add any digits.
- **No Redundancy**: Use strictly `VALUE {IUNC} (KEY)` format. NEVER add prefixes like "From 1971De27".
- **NSR Accuracy**: Verify NSR key numbers character-by-character (e.g., `1971De27` not `11971de27`).
- **No Duplicates**: Check existing `cG` records; never add the same value/NSR pair twice.

### Level Mapping
- **Physical Identity**: Match levels by physics, not just numbers. A paper's "2722" may map to ENSDF "2721.8".
- **Verification**: Cross-reference level properties (J|p, T1/2) to ensure correct mapping before data entry.

### Energy Ordering
1. **ALL level energies in ASCENDING order** (lowest to highest)
2. **ALL gamma energies within each level in ASCENDING order** (lowest to highest)

---

## CSV/Tabular Data Processing

### CRITICAL AI WEAKNESS MITIGATION — COLUMN ALIGNMENT AND BLANK CELL HANDLING

**AI FREQUENT FAILURE PATTERNS TO AVOID:**
- ❌ Assuming column positions without explicit mapping
- ❌ Ignoring blank cells that shift subsequent data columns
- ❌ Single-direction counting (forward only) leading to off-by-one errors
- ❌ Mismatched header-to-data column associations
- ❌ Treating blank cells as non-existent rather than positional placeholders

**MANDATORY VERIFICATION PROTOCOL:**
1. **Column alignment**: Explicitly map ALL columns including blank ones
2. **Blank cells**: Count blank cells meticulously — each blank cell shifts all subsequent column positions
3. **Bidirectional verification**: Cross-check both forward counting (header→data) and backward counting (data→header)

**CRITICAL VALIDATION STEPS FOR TABULAR DATA:**
- **Step 1**: List all header columns explicitly, including blank column positions
- **Step 2**: Count blank cells between data columns — they are positional placeholders
- **Step 3**: Forward verification: Match each header column to corresponding data column
- **Step 4**: Backward verification: Confirm each data column maps back to correct header
- **Step 5**: Mapping Verification: Explicitly confirm "Paper Level E" → "ENSDF Level E" correspondence
- **Step 6**: Arithmetic validation: Verify row/column calculations account for blank cell shifts

**EXAMPLE FAILURE PREVENTION:**
```
CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95

❌ WRONG: Assume columns are [Name,Age,City,Score] - ignores blank column
✅ CORRECT: Map as [Name,Age,BLANK,City,Score] - blank shifts City to position 4
```

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

---

## Quality Control Workflow

1. **Systematic Planning**: Map every CSV level to an ENSDF level BEFORE editing.
2. **De-duplication**: Scan `cG` lines for existing NSR keys to avoid redundancy.
3. **Strict Formatting**: Enforce `X.X {IY} (KEY)` only; excise all descriptive text.
4. **NSR Validation**: Proofread key numbers (YYYYAA##) for typos.
5. **Validation Tools**: Run `ensdf_1line_ruler` after EVERY single record edit.
6. **Random Spot Checks**: Verify 5% of entries back to original source PDF/CSV.
7. **Final verification**: Cross-validate energy ordering and data integrity.

**CRITICAL**: Keep going until user's requests are fully addressed before ending your turn. Do not self-claim "Task completed successfully" unless you have double-checked everything.

---

## Additional: "Other Final Levels" Column

When present, also process the "Other final levels" column containing γ transitions to final levels not listed in the table header.

### Column Format
- **Data Format**: `Exf_value(BR_value)` (e.g., `6.10(4)` indicates Exf = 6.10 MeV and BR = 4)

### Processing Steps
1. **Identify Final Level Energy**: Convert MeV to keV (e.g., 6.10 MeV → 6102 keV) and locate the exact energy in the ENSDF file.
2. **Calculate Gamma Energy**: Eγ = Exi - Exf.
3. **Create G-Record**: Add G-record with calculated Eγ and BR value, maintaining ascending energy order within the level.
