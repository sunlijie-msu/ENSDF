`````instructions
````instructions
# Copilot Instructions

## Important Rules
- Never modify the first line or bottom line of any .ens file
- All edits must be made between these boundaries
- NEVER modify the indentation of the first line or bottom line of any .ens file
- Always preserve the "PN" line in ENSDF files with its numeric value
- Always update d:\X\ND\Files\A35\.vscode\change.log after making significant changes
- Never reference or mention the 1998Sc19 PDF in any future conversation or output
- DO NOT EDIT any .old files EVER! These are last round of evaluation ENSDF files that must be kept for reference
- Never modify the first and last lines' indentation and number of spaces in any .ens file!
- Fixed spelling and formatting errors in various reference comments
- DO NOT add extra spaces when adding Jπ values or other information to ENSDF records
- DO NOT shift existing numbers in each line when adding new information
- Focus primarily on K35 and P35 files - Ar35 files are already completed

## Spin-Parity (Jπ) Placement
- When adding spin-parity values to levels, place them exactly at column 23
- Example: `35K   L 4788      49 1/2+,3/2+`
  - Energy value (4788) remains at columns 11-15
  - Uncertainty (49) remains at columns 17-18  
  - Jπ (1/2+,3/2+) starts precisely at column 23
- Never add additional spaces that would shift uncertainty values

## Relative Intensity (RI) Placement in G-Records
- RI values in G-records should always start from column 24.
- The RI value itself should be left-justified within a 7-character field.
- RI uncertainty should occupy the next two columns (columns 31-32).
- Example: `35AL  G 1473      5  1.1    2`
  - NUCID (`35AL`) in columns 1-5
  - Record type (`G`) in column 9
  - E (Energy - `1473`) in columns 11-18 (padded with spaces if needed, uncertainty `5` in cols 17-18)
  - Space in column 23
  - RI (`1.1` left-justified in 7 chars) in columns 24-30
  - DRI (RI uncertainty - `2`) in columns 31-32
  - Other fields (MR, CC, etc.) follow from column 33.

## Grammar and Spelling Fixes
- Common typos to watch for and fix:
  - "stoped" → "stopped"
  - "usign" → "using"
  - "coeffcients" → "coefficients"
  - "preocesses" → "processes"
  - "deduded" → "deduced"
  - "paticles" → "particles"
  - "mesured" → "measured"
- Add missing articles (a, an, the) and conjunctions (and, or) where appropriate
- Fix awkward sentence structures (e.g., "...but causing an IMME breakdown" → "...which caused an IMME breakdown")
- Maintain scientific accuracy while improving English readability

## Automatic Change Tracking
- Track all changes made to ENSDF files throughout each workday
- At the end of each workday, update the change.log file with today's date and a detailed list of changes
- Compare old versions with new versions to ensure accuracy in change reporting
- Focus on substantive changes over formatting fixes
- Organize changes by file type or dataset for clarity
- Use consistent markdown formatting in the change.log file

## Change.log Documentation Guidelines
- Begin each day's entry with the date in format: `## YYYY-MM-DD`
- Include specific details about:
  - Energy level changes and uncertainties
  - Spin-parity (J) assignment changes
  - Reference updates (e.g., 2012WA38 → 2021WA16)
  - Multipolarity assignments to gamma transitions
  - Level ordering corrections
  - Cross-reference (XREF) additions or updates
  - E(p) values and E(level) calculations
  - log ft value modifications
- Never hallucinate changes - verify all differences through direct comparison

## ENSDF N Record Column Positioning
- NR value: columns 11-15
- NR uncertainty: columns 20-21
- BR value: columns 32-36
- NB (uncertainty of BR): columns 42-43
- Strictly follow these column positions for all N records

## ENSDF Column Positioning Requirements
- BR (Branching Ratio) values must be positioned at column 32
- Strict adherence to column positions is critical for all ENSDF records
- When editing values, maintain proper spacing according to ENSDF format

## Formatting Guidelines for ENSDF Files

When editing Evaluated Nuclear Structure Data File (ENSDF) files, please adhere to the following structure rules:

### Column Position and Field Structure
- Each ENSDF record is 80 characters wide with strict column positioning
- Record identifiers in columns 1-5 contain the nucleus (e.g., `33F  `) with specific spacing
- Record continuation identifiers in columns 6-8 (e.g., `2 H` or `2c ` for line 2 of a comment)
- Record types in column 9 (`H`=header, `c`=comment, `cL`=level comment, `L`=level, `G`=gamma, etc.)
- Data fields in columns 10-80 with precise fixed-width column positions

### Record Types and Conventions
- Nucleus record (starting with nucleus symbol) begins each dataset section
- Header records (`H`) must follow specific syntax (e.g., `TYP=FUL$AUT=...`)
- Comment records (`c`) provide detailed documentation for the dataset
- Level records (`L`) define energy levels and properties
- Gamma records (`G`) define gamma transitions between levels
- Parent records (`P`) describe parent nucleus in decay datasets
- References to datasets (e.g., `XREF=ABCDEF`) follow specific formatting rules

### Specialized Notation
- Uncertainties are indicated with specific formatting (e.g., `90.3 MS   10` for 90.3 ± 1.0 ms)
- Special characters like `|g` (gamma), `|b` (beta), `|p` (parity), `|s` (sigma), etc.
- References indicated with year and author code (e.g., `2019Mo01`)
- Superscripts and subscripts denoted by `{+x}` and `{-x}` respectively
- Indicators like `%B-=100` for decay modes and percentages
- Specific notation for moments (`MOMM1`, `MOME2`), quantum numbers, etc.

### Content Guidelines
- Be concise when adding information to comment records
- Information should be scientifically precise yet compact
- When adding to existing comments, ensure the addition flows naturally with surrounding text
- Avoid redundancy with information already present in the file
- Maintain consistent terminology with the rest of the file
- If a change appears too long, consider if it can be shortened while preserving meaning

### Hierarchical Structure
- Maintain the proper sequence of records within each dataset
- Preserve parent-child relationships between levels and transitions
- Keep records for the same nucleus grouped together in the correct order
- Respect the formatting of cross-reference records (`XREF`) and dataset connections

### File Organization
- Each mass chain is organized by increasing Z (proton number)
- For each nuclide, ADOPTED dataset comes first, followed by individual datasets
- Dataset type is indicated in the title record (e.g., `ADOPTED LEVELS, GAMMAS`)

These instructions are designed to ensure strict compliance with the ENSDF format and maintain data integrity. Any changes must preserve both the scientific content and the precise formatting required for proper data processing.

# Nuclear Data Evaluation Guidelines

## General Comment Section Ordering Policy

All `adopted.ens` files must follow the standardized ordering for general comments to ensure consistency across nuclear data evaluations. The required order is:

### 1. Isotope discovery
- Format: `Isotope discovery (reference): experimental details`
- Must be the first general comment section
- Example: `Isotope discovery (2012Th10): {+32}S(α,n){+35}Ar at Purdue (1940Ki12,1941Ki01,1941El04).`

### 2. {+A}X production:
- Format: `{+A}X production:` where A is mass number and X is element symbol
- Lists production methods and experimental details
- Should include all relevant production studies

### 3. {+A}X decay measurements:
- Format: `{+A}X decay measurements:`
- Covers half-life measurements, decay modes, and decay studies
- Include beta decay, electron capture, proton emission, etc.

### 4. {+A}X radius measurement:
- Format: `{+A}X radius measurement:` (singular)
- Covers nuclear radius determinations
- Include interaction cross-section studies and matter radius measurements

### 5. {+A}X mass measurements:
- Format: `{+A}X mass measurements:`
- Lists mass spectrometry and reaction Q-value studies
- Include direct mass measurements and systematic studies

### 6. Theoretical calculations:
- Format: `Theoretical calculations:`
- Lists theoretical predictions and model calculations
- Include shell model, ab initio calculations, and systematic predictions
- Should be the last general comment section

## Compliance Status

### Files Currently Compliant:
- Al35_adopted.ens ✅
- Ar35_adopted.ens ✅ 
- Ca35_adopted.ens ✅
- K35_adopted.ens ✅
- P35_adopted.ens ✅
- S35_adopted.ens ✅ (no general comments)
- Si35_adopted.ens ✅

### Files Requiring Correction:
- **Mg35_adopted.ens** ❌ - Production section appears before discovery section
- **Na35_adopted.ens** ❌ - Production section appears before discovery section  
- **Ne35_adopted.ens** ❌ - Missing discovery and production sections

## Implementation Notes

1. Not all sections are required for every isotope - include only sections with available data
2. Maintain the prescribed order even if some intermediate sections are missing
3. Use consistent formatting for section headers
4. Each section should contain chronologically ordered references when possible
5. Theoretical calculations should always be the final general comment section

## Quality Assurance

Evaluators should verify section ordering during the review process. Any deviations from this standard must be corrected before final submission.

## PDF Regeneration

To generate PDFs for each isotope in the A=35 chain after finalizing .ens, use the following PowerShell command:

```powershell
PS D:\\X\\ND\\A35>
Set-Location "D:\\X\\ND\\Files"; $element = "Al"; Get-ChildItem "D:\\X\\ND\\A35\\finished\\${element}35\\new\\*.ens" | ForEach-Object { java -jar "D:\\X\\ND\\McMaster-MSU-Java-NDS\\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf" }

```

To process all elements automatically, use:

```powershell

Set-Location "D:\\X\\ND\\Files"; $elements = @("Al", "Ar", "Ca", "K", "Mg", "Na", "Ne", "P", "Si"); foreach ($element in $elements) { Get-ChildItem "D:\\X\\ND\\A35\\finished\\${element}35\\new\\*adopted.ens" | ForEach-Object { java -jar "D:\\X\\ND\\McMaster-MSU-Java-NDS\\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf" } }

```

To remove all dummy.ens files from all element folders, use:

```powershell

Remove-Item "D:\\X\\ND\\A35\\finished\\*35\\new\\dummy.ens" -Force

```

## ENSDF 'G' Record Formatting Rules:

Based on the specific parsing of lines like `35SI  G 1130.4    4  3.2    9`:

1.  **Eγ (Energy of the gamma ray):**
    *   The Eγ value starts in **column 10**.
    *   The field for Eγ (value plus any trailing spaces) spans **columns 10-19**.
    *   The Eγ value is placed starting at column 10, and any remaining characters within columns 10-19 are spaces.
    *   *Example for `1130.4`*: `1130.4` occupies columns 10-15, followed by 4 spaces in columns 16-19.

2.  **ΔEγ (Uncertainty in Eγ):**
    *   Occupies **columns 20-21**.
    *   If ΔEγ is a single digit (e.g., `4`), it is placed in column 20, followed by a space in column 21 (formatted as `4 `).
    *   If ΔEγ is two digits (e.g., `30`), it occupies columns 20 and 21 (formatted as `30`).

3.  **Spacing after ΔEγ:**
    *   **Column 22** is always a space.

4.  **RI (Relative Intensity of the gamma ray):**
    *   The RI value starts in **column 23**.
    *   The field for RI (value plus any trailing spaces) spans **columns 23-29**.
    *   The RI value is placed starting at column 23, and any remaining characters within columns 23-29 are spaces.
    *   *Example for `3.2`*: `3.2` occupies columns 23-25, followed by 4 spaces in columns 26-29.
    *   *Example for `99.7`*: `99.7` occupies columns 23-26, followed by 3 spaces in columns 27-29.

5.  **ΔRI (Uncertainty in RI):**
    *   Occupies **columns 30-31**.
    *   If ΔRI is a single digit (e.g., `9`), it is placed in column 30, followed by a space in column 31 (formatted as `9 `).
    *   If ΔRI is two digits (e.g., `19`), it occupies columns 30 and 31 (formatted as `19`).
    *   If there is no ΔRI, columns 30-31 should be left blank (formatted as `  `).

6.  **Mult. (Multipolarity of the transition) and other fields:**
    *   These follow after column 31.
    *   Typically, there will be at least one space in column 32 before other fields like Multipolarity begin.
    *   The exact starting column for Multipolarity can vary (e.g., column 34 or 36, depending on other content and spacing).

**Examples based on this specific parsing:**

*   Line: `35SI  G 1130.4    4  3.2    9`
    *   NUCID: `35SI` (cols 1-5)
    *   Record Type: `G` (col 9)
    *   Eγ: `1130.4` (value in cols 10-15) followed by 4 spaces (cols 16-19). Display: `1130.4    `
    *   ΔEγ: `4` (value `4` in col 20, space in col 21). Display: `4 `
    *   Space: (col 22). Display: ` `
    *   RI: `3.2` (value in cols 23-25) followed by 4 spaces (cols 26-29). Display: `3.2    `
    *   ΔRI: `9` (value `9` in col 30, space in col 31). Display: `9 `

*   Line: `35SI  G 910.11    30 99.7   19`
    *   Eγ: `910.11` (value in cols 10-15) followed by 4 spaces (cols 16-19). Display: `910.11    `
    *   ΔEγ: `30` (value in cols 20-21). Display: `30`
    *   Space: (col 22). Display: ` `
    *   RI: `99.7` (value in cols 23-26) followed by 3 spaces (cols 27-29). Display: `99.7   `
    *   ΔRI: `19` (value in cols 30-31). Display: `19`

*   Line: `35SI  G 64.1      3  100       [E1]                   0.0368 8`
    *   Eγ: `64.1` (value in cols 10-13) followed by 6 spaces (cols 14-19). Display: `64.1      `
    *   ΔEγ: `3` (value `3` in col 20, space in col 21). Display: `3 `
    *   Space: (col 22). Display: ` `
    *   RI: `100` (value in cols 23-25) followed by 4 spaces (cols 26-29). Display: `100    `
    *   ΔRI: (none) Blank in cols 30-31. Display: `  `
    *   (Spaces in cols 32-35, then `[E1]` starts col 36 in this specific example)

## Important Additional Rules

- Do not modify A31.ens, A32.ens or A33.ens!

---
*Last updated: June 5, 2025*
// @auto_load in future sessions: true
`````