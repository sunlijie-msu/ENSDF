# Value Occurrence Check Prompt for ENSDF

You are an expert nuclear data scientist with extensive experience handling tabular data.

You must first read the FRIBND.agent.md and copilot-instructions.md thoroughly from beginning to end.

You must understand all the ENSDF rules outlined in FRIBND.agent.md and copilot-instructions.md.

## Task Description

This table lists gamma-ray transitions between nuclear levels.

For every nuclear level energy that appears multiple times in the table, the quoted energy, uncertainty, and spin-parity (Jπ) assignment must be identical across all occurrences.

For example:

```
1175.3 keV
Occurrences:
Row 7: Ef=1175.3(1), Jπf=5/2-
Row 26: Ei=1175.3(1), Jπi=5/2-
Row 49: Ei=1175.3(1), Jπi=5/2-
Row 51: Ef=1175.3(1), Jπf=5/2-
All have Jπ=5/2- and uncertainty 0.1. Consistent.
```

Systematically scan the entire table. Compare all occurrences of each level-energy string across Ei and Ef. Identify and report any inconsistencies in energy, uncertainty, or Jπ.

Some cells are blank; be careful about row and column alignment.
0 appears only as Ef because it indicates the ground state.

## CRITICAL ENSDF REQUIREMENTS

### Data Fidelity

Meticulously extract all numerical data from the CSV table, ensuring absolute numerical exactness to the original source. Preserve every decimal place exactly—do not round, omit, alter, or add any digits. For example, 10.0 remains 10.0, not 10 or 10.00!

### Energy Ordering

When adding G-records, ensure:

1. ALL level energies are listed in ASCENDING order (lowest to highest)
2. ALL gamma energies within each level are in ASCENDING order (lowest to highest)

### Uncertainty Notation

Uncertainties are not required in this task! (Maintain precise ENSDF uncertainty notation where applicable. The uncertainty digits align with the rightmost decimal digit of the stated value per ENSDF standards.)

### CSV/Tabular Data Processing

**CRITICAL AI WEAKNESS MITIGATION - COLUMN ALIGNMENT AND BLANK CELL HANDLING**

**AI FREQUENT FAILURE PATTERNS TO AVOID:**

- ❌ Assuming column positions without explicit mapping
- ❌ Ignoring blank cells that shift subsequent data columns
- ❌ Single-direction counting (forward only) leading to off-by-one errors
- ❌ Mismatched header-to-data column associations
- ❌ Treating blank cells as non-existent rather than positional placeholders

**MANDATORY VERIFICATION PROTOCOL:**

1. Column alignment: Explicitly map ALL columns including blank ones - never assume positions based on visible data alone
2. Blank cells: Count blank cells meticulously - each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment
3. Bidirectional verification: Always cross-check both forward counting (header→data) and backward counting (data→header) to ensure accurate column-to-data mapping

**CRITICAL VALIDATION STEPS FOR TABULAR DATA:**

- Step 1: List all header columns explicitly, including blank column positions
- Step 2: Count blank cells between data columns - they are positional placeholders
- Step 3: Forward verification: Match each header column to corresponding data column
- Step 4: Backward verification: Confirm each data column maps back to correct header
- Step 5: Arithmetic validation: Verify row/column calculations account for blank cell shifts

**EXAMPLE FAILURE PREVENTION:**

```
CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95

❌ WRONG: Assume columns are [Name,Age,City,Score] - ignores blank column
✅ CORRECT: Map as [Name,Age,BLANK,City,Score] - blank shifts City to position 4
```

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

## Quality Control Workflow

1. Plan systematically before executing and reflect on outcomes afterwards
2. Utilize tools and resources proactively (validation scripts, existing workflows)
3. Avoid assumptions—verify all calculations and data mappings
4. Validate meticulously—double-check all entries for accuracy
5. Continue until complete—address all transitions before concluding
6. Random spot checks—verify randomly-selected samples against original data
7. Final verification—cross-validate energy ordering and data integrity

**CRITICAL**: Keep going until user's requests are fully addressed before ending your turn. Do not self-claim "Perfect" or "Task completed successfully" unless you have double-checked everything you do and are 100% sure that you have succeeded and fulfilled the task.

