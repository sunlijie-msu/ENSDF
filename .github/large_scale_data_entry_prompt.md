# Large-Scale Data Entry Prompt for ENSDF

You are an expert nuclear data scientist with extensive experience handling ENSDF-formatted data.

Read `copilot-instructions.md` carefully and thoroughly.

## Task Description

Extract Eγ and branching ratio data for each gamma ray transition from the provided CSV file and populate the corresponding E and RI fields in ENSDF G-records.

### Example Workflow
- **Initial level**: Ep = 716 keV, excitation energy Exi = 7063 keV
- **CSV headers**: Indicate gamma transition final level energies (Exf)
  - `0` = ground state
  - `1219.1` = first excited state
- **Gamma energy calculation**: Eγ = Exi - Exf (e.g., 7063 - 1219.1 = 5843.9 keV)
- **ENSDF record creation**: Add G-record with Eg=5843.9 and RI=48 (uncertainties not required)
- **Continue pattern**: Process each Exf column systematically, inserting corresponding Eγ and BR values into E and RI fields

### Constraints
- **Edit scope**: Only modify data below the line `35CL cL $Resonances starting at 7.0 MeV`
- **Script reuse**: Leverage existing scripts for similar data entry tasks when available

## CRITICAL ENSDF REQUIREMENTS

### Data Fidelity
Meticulously extract all numerical data from the CSV table, ensuring absolute fidelity to the original source. Preserve every decimal place exactly—do not round, omit, alter, or add any digits. For example, 10.0 remains 10.0, not 10 or 10.00!

### Energy Ordering
When adding G-records, ensure:
1. **ALL level energies are listed in ASCENDING order** (lowest to highest)
2. **ALL gamma energies within each level are in ASCENDING order** (lowest to highest)

### Uncertainty Notation
Uncertainties are not required in this task! (Maintain precise ENSDF uncertainty notation where applicable. The uncertainty digits align with the rightmost decimal digit of the stated value per ENSDF standards.)

## Quality Control Workflow

1. **Plan systematically** before executing and reflect on outcomes afterwards
2. **Utilize tools and resources proactively** (validation scripts, existing workflows)
3. **Avoid assumptions**—verify all calculations and data mappings
4. **Validate meticulously**—double-check all entries for accuracy
5. **Continue until complete**—address all transitions before concluding
6. **Final verification**—cross-validate energy ordering and data integrity

**CRITICAL**: Keep going until user's requests are fully addressed before ending your turn. Do not self-claim "Perfect" or "Task completed successfully" unless you have double-checked everything you do and are 100% sure that you have succeeded and fulfilled the task.
