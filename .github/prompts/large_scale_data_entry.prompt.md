# Large-Scale Data Entry Prompt for ENSDF

You are an expert nuclear data scientist with extensive experience handling ENSDF-formatted data.

Read `copilot-instructions.md` carefully and thoroughly.

## Task Description
Extract E(level) for each initial level from the provided CSV file and populate the corresponding L-records in the ENSDF file.
Extract Eγ, Iγ, Initial level, DCO ratio, Multipolarity data for each γ-ray transition from the provided CSV file and populate the corresponding E and RI fields in ENSDF G-records.
DCO ratios should be added as comments following a G-record.


### Constraints
- **Edit scope**: Only modify data below the line `PN                                                                     5  `
- **Script reuse**: Leverage existing scripts for similar data entry tasks when available

## CRITICAL ENSDF REQUIREMENTS

### Data Fidelity
Meticulously extract all numerical data from the CSV table, ensuring absolute numerical exactness to the original source. Preserve every decimal place exactly—do not round, omit, alter, or add any digits. For example, 10.0 remains 10.0, not 10 or 10.00!

### Energy Ordering
When adding G-records, ensure:
1. **ALL level energies are listed in ASCENDING order** (lowest to highest)
2. **ALL gamma energies within each level are in ASCENDING order** (lowest to highest)

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
1. **Column alignment**: Explicitly map ALL columns including blank ones - never assume positions based on visible data alone
2. **Blank cells**: Count blank cells meticulously - each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment
3. **Bidirectional verification**: Always cross-check both forward counting (header→data) and backward counting (data→header) to ensure accurate column-to-data mapping

**CRITICAL VALIDATION STEPS FOR TABULAR DATA:**
- **Step 1**: List all header columns explicitly, including blank column positions
- **Step 2**: Count blank cells between data columns - they are positional placeholders
- **Step 3**: Forward verification: Match each header column to corresponding data column
- **Step 4**: Backward verification: Confirm each data column maps back to correct header
- **Step 5**: Arithmetic validation: Verify row/column calculations account for blank cell shifts

**EXAMPLE FAILURE PREVENTION:**
```
CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95

❌ WRONG: Assume columns are [Name,Age,City,Score] - ignores blank column
✅ CORRECT: Map as [Name,Age,BLANK,City,Score] - blank shifts City to position 4
```

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

## Quality Control Workflow

1. **Plan systematically** before executing and reflect on outcomes afterwards
2. **Utilize tools and resources proactively** (validation scripts, existing workflows)
3. **Avoid assumptions**—verify all calculations and data mappings
4. **Validate meticulously**—double-check all entries for accuracy
5. **Continue until complete**—address all transitions before concluding
6. **Random spot checks**—verify randomly-selected samples against original data
7. **Final verification**—cross-validate energy ordering and data integrity

**CRITICAL**: Keep going until user's requests are fully addressed before ending your turn. Do not self-claim "Perfect" or "Task completed successfully" unless you have double-checked everything you do and are 100% sure that you have succeeded and fulfilled the task.





## Additional Data Entry Task

Process the "Other final levels" column in the CSV file, which contains γ transitions to final levels not listed in the header.

### Column Format
- **Header**: `Exf in unit of MeV and BR placed in ()`
- **Data Format**: `Exf_value(BR_value)` (e.g., `6.10(4)` indicates Exf = 6.10 MeV and BR = 4)

### Example
For the level at Exi = 7175 keV (Ep = 832 keV):
```
Ep_keV  Exi_keV  ...  Other final levels
832     7175     ...  6.10(4)
```

### Processing Steps
1. **Identify Final Level Energy**: Convert MeV to keV (e.g., 6.10 MeV → 6102 keV) and locate the exact energy in the low-lying levels of the ENSDF file.
2. **Calculate Gamma Energy**: Eγ = Exi - Exf (e.g., 7175 - 6102 = 1073 keV).
3. **Create G-Record**: Add a new G-record with the calculated Eγ and corresponding BR value, maintaining ascending energy order within the level.

### Existing Records Example
For Exi = 7175 keV, the following L- and G-records were already added:
```
35CL  L 7175.0
35CL  G 3116.6       24
35CL  G 3207.7       10
35CL  G 3257.1       2
35CL  G 4481.0       4
35CL  G 5955.9       16
35CL  G 7175.0       40
```
The new G-record to be added is:
```35CL  G 1073.0       4
```

Apply the same methodology to process additional transitions from the "Other final levels" column.