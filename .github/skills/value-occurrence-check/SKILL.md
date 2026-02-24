---
name: value-occurrence-check
description: Check consistency of nuclear level energies that appear multiple times in a gamma-ray transition CSV table. Verifies energy, uncertainty, and J-π are identical across all occurrences as both initial (Ei) and final (Ef) levels. Mandates explicit column mapping including blank cells, bidirectional forward/backward verification, and reporting all inconsistencies.
argument-hint: [CSV or table file]
---

# Value Occurrence Check for ENSDF

## Task Description

This table lists gamma-ray transitions between nuclear levels.

For every nuclear level energy that appears multiple times in the table, the quoted energy, uncertainty, and spin-parity (Jπ) assignment must be identical across all occurrences.

**Example of consistent entries:**
```
1175.3 keV
Occurrences:
Row 7:  Ef=1175.3(1), Jπf=5/2-
Row 26: Ei=1175.3(1), Jπi=5/2-
Row 49: Ei=1175.3(1), Jπi=5/2-
Row 51: Ef=1175.3(1), Jπf=5/2-
All have Jπ=5/2- and uncertainty 0.1. Consistent. ✅
```

Systematically scan the entire table. Compare all occurrences of each level-energy string across Ei and Ef. Identify and report any inconsistencies in energy, uncertainty, or Jπ.

Some cells are blank; be careful about row and column alignment.
0 appears only as Ef because it indicates the ground state.

## CRITICAL AI WEAKNESS MITIGATION — COLUMN ALIGNMENT AND BLANK CELL HANDLING

**AI FREQUENT FAILURE PATTERNS TO AVOID:**
- ❌ Assuming column positions without explicit mapping
- ❌ Ignoring blank cells that shift subsequent data columns
- ❌ Single-direction counting (forward only) leading to off-by-one errors
- ❌ Mismatched header-to-data column associations
- ❌ Treating blank cells as non-existent rather than positional placeholders

**MANDATORY VERIFICATION PROTOCOL:**
1. **Column alignment**: Explicitly map ALL columns including blank ones — never assume positions based on visible data alone
2. **Blank cells**: Count blank cells meticulously — each blank cell shifts all subsequent column positions
3. **Bidirectional verification**: Cross-check both forward counting (header→data) and backward counting (data→header)

**CRITICAL VALIDATION STEPS:**
- **Step 1**: List all header columns explicitly, including blank column positions
- **Step 2**: Count blank cells between data columns — they are positional placeholders
- **Step 3**: Forward verification: Match each header column to corresponding data column
- **Step 4**: Backward verification: Confirm each data column maps back to correct header
- **Step 5**: Arithmetic validation: Verify row/column calculations account for blank cell shifts

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

## Data Fidelity Rules

- Preserve every decimal place exactly — do not round, omit, alter, or add any digits
- 10.0 remains 10.0, not 10 or 10.00
- Uncertainty notation in last digits (ENSDF standard)

## Quality Control Workflow

1. Plan systematically before executing, reflect on outcomes afterwards
2. Utilize tools and resources proactively
3. Avoid assumptions — verify all data mappings
4. Random spot checks — verify randomly-selected samples against original data
5. Final verification — cross-validate all inconsistencies reported

**CRITICAL**: Do not claim task completion unless 100% of occurrences have been checked.
