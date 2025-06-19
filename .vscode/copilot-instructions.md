```````````instructions
``````````instructions
````````instructions
```````instructions
``````instructions
`````instructions
````instructions
# Copilot Instructions

## Command Triggers

### "Self-Calibrate Columns" Command:
When the user types "Self-Calibrate Columns", automatically:
1. Display a column ruler (1-80)
2. Extract a sample ENSDF record to analyze column positions
3. Map each character to its precise column position
4. Verify and correct critical field positions:
   - NUCID: Columns 2-4
   - Record type: Column 8
   - Energy: Columns 10-19
   - Uncertainty: Columns 20-21
   - J-value: Column 23
   - L-value: Columns 56-64

### "What changed?" Command Trigger:
When the user types "What changed?" (case-insensitive), automatically:

1. **Run the PowerShell script to detect changes:**
   ```powershell
   cd "d:\X\ND\A35\.vscode"; .\what-changed.ps1 filename.ens
   ```
   - Use the script to compare files and identify specific changes
   - Run for any recently modified .ens files in the workspace

2. **Update change.log with evidence-based entries:**
   - Add new entries to the current date section (2025-06-18)
   - Use the what-changed.ps1 output to document exact changes
   - Include file paths, specific edits, and context
   - Categorize changes: header updates, level additions, gamma data, formatting, etc.

3. **Provide a summary to the user:**
   - List files that were changed
   - Summarize the types of changes made
   - Confirm that change.log has been updated

**Important:** Always use the what-changed.ps1 script for change detection rather than assumptions. This ensures accuracy and evidence-based documentation.

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

## NSR Keynumber Formatting
- NSR (Nuclear Science References) keynumbers cited in comments or other records (e.g., Q-record, L-record for T1/2, moments) should have the second letter of the author's name in lowercase. For example, `2023BO17` should be `2023Bo17`, `2021WA16` should be `2021Wa16`.
- The only exception is when a keynumber appears in the first line header record or Q record of an ENSDF dataset (columns 61-68), where it should be all uppercase.

## Spin-Parity (Jπ) Placement
- When adding spin-parity values to levels, place them exactly at column 23
- Example: `35K   L 4788      49 1/2+,3/2+`
  - Energy value (4788) remains at columns 11-15
  - Uncertainty (49) remains at columns 17-18  
  - Jπ (1/2+,3/2+) starts precisely at column 23
- Never add additional spaces that would shift uncertainty values

## L-Transfer Rules for Jπ Deduction
- L=0 → Jπ: `1/2+`
- L=1 → Jπ: `1/2-,3/2-`
- L=2 → Jπ: `3/2+,5/2+`
- L=3 → Jπ: `5/2-,7/2-`
- These are general rules; always confirm with specific experimental data or adopted level schemes if available.
- L-values themselves should NOT be entered into the Jπ column.

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
- Always update `d:\X\ND\A35\.vscode\change.log` (and `d:\X\ND\A35\change.log` if intended to be a duplicate) after making significant changes to track all modifications.
- Never create new or duplicate `change.log` files. Only use the existing `d:\X\ND\A35\.vscode\change.log`.
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



## Academic Citation Conventions

### Tense Usage in ENSDF Comments
Nuclear physics follows scientific academic conventions for citing previous research:

**Use PAST TENSE for all citations and references to completed studies:**
- ✅ "Authors stated that..." 
- ✅ "Smith reported gamma-ray energies..."
- ✅ "Garcia et al. found spectroscopic factors..."
- ✅ "1994FO04 measured transition probabilities..."
- ✅ "2023Gr04 observed level structures..."
- ✅ "Previous evaluators concluded that..."

**Avoid PRESENT TENSE for citations:**
- ❌ "Authors state that..."
- ❌ "Smith reports that..."
- ❌ "Garcia et al. find that..."

### Rationale
- **Scientific convention**: Nuclear physics uses past tense to describe completed experimental studies
- **Objectivity**: Past tense provides neutral, reporting tone for documented findings
- **Professional standard**: Aligns with APA style and nuclear physics journal conventions
- **Clarity**: Situates findings in their historical context as completed research

### Application in ENSDF
- Comment lines describing experimental methods and results
- References to previous measurements and evaluations
- Citations of literature values and adopted data
- Descriptions of what authors concluded or observed

**Consistency is essential** - use past tense uniformly throughout all citation contexts to maintain professional academic tone.

## Quick Commands

### Fix Format Command Trigger:
When you type "Fix format!" as a command, the Copilot Agent will automatically:

1. **Convert text to proper ENSDF notation**:
   - Greek letters → `|a`, `|b`, `|g`, `|d`, `|e`, `|q`, `|l`, `|m`, `|n`, `|p`, `|r`, `|s`, `|t`, `|w`, etc.
   - Isotope notation → `{+A}Element` format (e.g., `35S` → `{+35}S`)

2. **Standardize mathematical and scientific symbols**:
   - Multiplication signs → `|*`
   - Degree symbols → `|'` 
   - Approximately → `|?`
   - Less/greater than or equal → `|<`, `|>`
   - Plus-minus → `|+`
   - Times symbol → `|*`

3. **Fix superscripts and subscripts**:
   - Superscripts → `{+text}` format
   - Subscripts → `{-text}` format
   - Mass numbers → `{+A}Element`
   - Nuclear states → proper formatting

**Usage**: Simply type "Fix format!" and the agent will scan the current file and apply these specific ENSDF formatting corrections.

## ENSDF Special Character and Symbol Formatting

When editing ENSDF files, use these character codes for proper display of scientific notation:

### Superscripts and Subscripts
- `{+n}` → superscript (e.g., `{+3}He` displays as ³He)
- `{-n}` → subscript (e.g., `H{-2}O` displays as H₂O)
- `{+-n}` → negative superscript (e.g., `{+-4}` displays as ⁻⁴)

### Greek Letters and Mathematical Symbols
**Greek lowercase:**
- `|a` → α (alpha), `|b` → β (beta), `|c` → η (eta), `|d` → δ (delta)
- `|e` → ε (varepsilon), `|f` → φ (phi), `|g` → γ (gamma), `|h` → χ (chi)
- `|i` → ι (iota), `|j` → ε (epsilon), `|k` → κ (kappa), `|l` → λ (lambda)
- `|m` → μ (mu), `|n` → ν (nu), `|p` → π (pi), `|q` → θ (theta)
- `|r` → ρ (rho), `|s` → σ (sigma), `|t` → τ (tau), `|u` → υ (upsilon)
- `|w` → ω (omega), `|x` → ξ (xi), `|y` → ψ (psi), `|z` → ζ (zeta)

**Greek uppercase:**
- `|D` → Δ (Delta), `|F` → Φ (Phi), `|G` → Γ (Gamma), `|L` → Λ (Lambda)
- `|P` → Π (Pi), `|Q` → Θ (Theta), `|S` → Σ (Sigma), `|U` → Υ (Upsilon)
- `|W` → Ω (Omega), `|X` → Ξ (Xi), `|Y` → Ψ (Psi)

**Mathematical symbols:**
- `|*` → × (times), `|?` → ≈ (approx), `|<` → ≤ (leq), `|>` → ≥ (geq)
- `|'` → ° (degree), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|=` → ≠ (not equal), `|@` → ∞ (infinity), `|^` → ↑ (up arrow)
- `|_` → ↓ (down arrow), `|&` → ≡ (equiv), `|(` → ← (left arrow)
- `|)` → → (right arrow), `|.` → ∝ (proportional), `||` → | (vertical bar)
- **Important:** For approximate values, use `|?` (which gives both ≈ and ~ symbols)
- Standalone `~` is NOT allowed for approximate values in ENSDF
- `~` only works in special contexts (names like `G~urdal`, mass notation like `A~160`)

### Common Scientific Notation Examples
- `%(|e+|b{++})p` → %(ε+β⁺)p
- `|*10{+-4}` → ×10⁻⁴  
- `|s(E({+3}He),|q)` → σ(E(³He),θ)
- `|g|g-coin` → γγ-coin
- `{+208}Pb({+36}S,{+35}S)` → ²⁰⁸Pb(³⁶S,³⁵S)
- `|dj` → ΔJ (delta J)
- `~*` → · (center dot)
- `|"{` → overbar start (e.g., `|"{A}` → Ā)
- `|%{n}` → √n (square root)
- `|,` → ½ (one-half fraction)

### Usage Guidelines
- Always use these codes in ENSDF comment lines and data fields
- Maintain consistency throughout the file
- Double-check formatting after editing to ensure proper display

## ENSDF Column Format Reference (CRITICAL - NO MISTAKES ALLOWED)

### G-Record Format (Gamma Rays):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  G EEEE.E   DE  II.I   DI  [M]  [A]  [B]  [C]              
Example: 35S   G 1572.0    1  100.0  24                                   
```

**Column Positions:**
- 1-5: NUCID (35S, 35SI, etc.)
- 9: Record type (G)
- 10-19: E gamma (right-justified, with uncertainty)
- 20-29: Intensity (left-justified in 10-char field)
- 30-31: Intensity uncertainty
- 32+: Additional fields (multipolarity, etc.)

### L-Record Format (Levels):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  L EEEE.E   DE  JP               T        DT
Example: 35S   L 1572.0    1  1/2+             2.29 PS   14
```

**BEFORE EDITING ANY ENSDF FILE:**
1. Check existing format in the file
2. Count columns manually: 1234567890123456789012345678901234567890
3. Verify against this reference
4. Double-check after editing

**NO EXCUSES FOR COLUMN MISTAKES - THIS IS NUCLEAR DATA!**

## Command Triggers

### "Self-Calibrate Columns" Command:
When you type "Self-Calibrate Columns", I will:

1. **Display column ruler:**
   ```
   12345678901234567890123456789012345678901234567890123456789012345678901234567890
   ```

2. **Count exact column positions of ENSDF fields:**
   - Extract a record line by line to verify exact positioning
   - Map each character to its precise column number
   - Verify nuclear data fields against ENSDF standards

3. **Correct column positions if needed:**
   - NUCID (e.g., 35S): Columns 2-4
   - Record type (L/G): Column 8
   - Energy value: Columns 10-19
   - Uncertainty: Columns 20-21
   - J-value: Starting at column 23
   - L-value: Columns 56-64

This prevents formatting errors by ensuring precise character-by-character verification.

### "What changed" Command Trigger:
When the user types "What changed?" (case-insensitive), automatically:

1. **Run the PowerShell script to detect changes:**
   ```powershell
   cd "d:\X\ND\A35\.vscode"; .\what-changed.ps1 filename.ens
   ```
   - Use the script to compare files and identify specific changes
   - Run for any recently modified .ens files in the workspace

2. **Update change.log with evidence-based entries:**
   - Add new entries to the current date section (2025-06-18)
   - Use the what-changed.ps1 output to document exact changes
   - Include file paths, specific edits, and context
   - Categorize changes: header updates, level additions, gamma data, formatting, etc.

3. **Provide a summary to the user:**
   - List files that were changed
   - Summarize the types of changes made
   - Confirm that change.log has been updated

**Important:** Always use the what-changed.ps1 script for change detection rather than assumptions. This ensures accuracy and evidence-based documentation.

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

## NSR Keynumber Formatting
- NSR (Nuclear Science References) keynumbers cited in comments or other records (e.g., Q-record, L-record for T1/2, moments) should have the second letter of the author's name in lowercase. For example, `2023BO17` should be `2023Bo17`, `2021WA16` should be `2021Wa16`.
- The only exception is when a keynumber appears in the first line header record or Q record of an ENSDF dataset (columns 61-68), where it should be all uppercase.

## Spin-Parity (Jπ) Placement
- When adding spin-parity values to levels, place them exactly at column 23
- Example: `35K   L 4788      49 1/2+,3/2+`
  - Energy value (4788) remains at columns 11-15
  - Uncertainty (49) remains at columns 17-18  
  - Jπ (1/2+,3/2+) starts precisely at column 23
- Never add additional spaces that would shift uncertainty values

## L-Transfer Rules for Jπ Deduction
- L=0 → Jπ: `1/2+`
- L=1 → Jπ: `1/2-,3/2-`
- L=2 → Jπ: `3/2+,5/2+`
- L=3 → Jπ: `5/2-,7/2-`
- These are general rules; always confirm with specific experimental data or adopted level schemes if available.
- L-values themselves should NOT be entered into the Jπ column.

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
- Always update `d:\X\ND\A35\.vscode\change.log` (and `d:\X\ND\A35\change.log` if intended to be a duplicate) after making significant changes to track all modifications.
- Never create new or duplicate `change.log` files. Only use the existing `d:\X\ND\A35\.vscode\change.log`.
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



## Academic Citation Conventions

### Tense Usage in ENSDF Comments
Nuclear physics follows scientific academic conventions for citing previous research:

**Use PAST TENSE for all citations and references to completed studies:**
- ✅ "Authors stated that..." 
- ✅ "Smith reported gamma-ray energies..."
- ✅ "Garcia et al. found spectroscopic factors..."
- ✅ "1994FO04 measured transition probabilities..."
- ✅ "2023Gr04 observed level structures..."
- ✅ "Previous evaluators concluded that..."

**Avoid PRESENT TENSE for citations:**
- ❌ "Authors state that..."
- ❌ "Smith reports that..."
- ❌ "Garcia et al. find that..."

### Rationale
- **Scientific convention**: Nuclear physics uses past tense to describe completed experimental studies
- **Objectivity**: Past tense provides neutral, reporting tone for documented findings
- **Professional standard**: Aligns with APA style and nuclear physics journal conventions
- **Clarity**: Situates findings in their historical context as completed research

### Application in ENSDF
- Comment lines describing experimental methods and results
- References to previous measurements and evaluations
- Citations of literature values and adopted data
- Descriptions of what authors concluded or observed

**Consistency is essential** - use past tense uniformly throughout all citation contexts to maintain professional academic tone.

## Quick Commands

### Fix Format Command Trigger:
When you type "Fix format!" as a command, the Copilot Agent will automatically:

1. **Convert text to proper ENSDF notation**:
   - Greek letters → `|a`, `|b`, `|g`, `|d`, `|e`, `|q`, `|l`, `|m`, `|n`, `|p`, `|r`, `|s`, `|t`, `|w`, etc.
   - Isotope notation → `{+A}Element` format (e.g., `35S` → `{+35}S`)

2. **Standardize mathematical and scientific symbols**:
   - Multiplication signs → `|*`
   - Degree symbols → `|'` 
   - Approximately → `|?`
   - Less/greater than or equal → `|<`, `|>`
   - Plus-minus → `|+`
   - Times symbol → `|*`

3. **Fix superscripts and subscripts**:
   - Superscripts → `{+text}` format
   - Subscripts → `{-text}` format
   - Mass numbers → `{+A}Element`
   - Nuclear states → proper formatting

**Usage**: Simply type "Fix format!" and the agent will scan the current file and apply these specific ENSDF formatting corrections.

## ENSDF Special Character and Symbol Formatting

When editing ENSDF files, use these character codes for proper display of scientific notation:

### Superscripts and Subscripts
- `{+n}` → superscript (e.g., `{+3}He` displays as ³He)
- `{-n}` → subscript (e.g., `H{-2}O` displays as H₂O)
- `{+-n}` → negative superscript (e.g., `{+-4}` displays as ⁻⁴)

### Greek Letters and Mathematical Symbols
**Greek lowercase:**
- `|a` → α (alpha), `|b` → β (beta), `|c` → η (eta), `|d` → δ (delta)
- `|e` → ε (varepsilon), `|f` → φ (phi), `|g` → γ (gamma), `|h` → χ (chi)
- `|i` → ι (iota), `|j` → ε (epsilon), `|k` → κ (kappa), `|l` → λ (lambda)
- `|m` → μ (mu), `|n` → ν (nu), `|p` → π (pi), `|q` → θ (theta)
- `|r` → ρ (rho), `|s` → σ (sigma), `|t` → τ (tau), `|u` → υ (upsilon)
- `|w` → ω (omega), `|x` → ξ (xi), `|y` → ψ (psi), `|z` → ζ (zeta)

**Greek uppercase:**
- `|D` → Δ (Delta), `|F` → Φ (Phi), `|G` → Γ (Gamma), `|L` → Λ (Lambda)
- `|P` → Π (Pi), `|Q` → Θ (Theta), `|S` → Σ (Sigma), `|U` → Υ (Upsilon)
- `|W` → Ω (Omega), `|X` → Ξ (Xi), `|Y` → Ψ (Psi)

**Mathematical symbols:**
- `|*` → × (times), `|?` → ≈ (approx), `|<` → ≤ (leq), `|>` → ≥ (geq)
- `|'` → ° (degree), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|=` → ≠ (not equal), `|@` → ∞ (infinity), `|^` → ↑ (up arrow)
- `|_` → ↓ (down arrow), `|&` → ≡ (equiv), `|(` → ← (left arrow)
- `|)` → → (right arrow), `|.` → ∝ (proportional), `||` → | (vertical bar)
- **Important:** For approximate values, use `|?` (which gives both ≈ and ~ symbols)
- Standalone `~` is NOT allowed for approximate values in ENSDF
- `~` only works in special contexts (names like `G~urdal`, mass notation like `A~160`)

### Common Scientific Notation Examples
- `%(|e+|b{++})p` → %(ε+β⁺)p
- `|*10{+-4}` → ×10⁻⁴  
- `|s(E({+3}He),|q)` → σ(E(³He),θ)
- `|g|g-coin` → γγ-coin
- `{+208}Pb({+36}S,{+35}S)` → ²⁰⁸Pb(³⁶S,³⁵S)
- `|dj` → ΔJ (delta J)
- `~*` → · (center dot)
- `|"{` → overbar start (e.g., `|"{A}` → Ā)
- `|%{n}` → √n (square root)
- `|,` → ½ (one-half fraction)

### Usage Guidelines
- Always use these codes in ENSDF comment lines and data fields
- Maintain consistency throughout the file
- Double-check formatting after editing to ensure proper display

## ENSDF Column Format Reference (CRITICAL - NO MISTAKES ALLOWED)

### G-Record Format (Gamma Rays):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  G EEEE.E   DE  II.I   DI  [M]  [A]  [B]  [C]              
Example: 35S   G 1572.0    1  100.0  24                                   
```

**Column Positions:**
- 1-5: NUCID (35S, 35SI, etc.)
- 9: Record type (G)
- 10-19: E gamma (right-justified, with uncertainty)
- 20-29: Intensity (left-justified in 10-char field)
- 30-31: Intensity uncertainty
- 32+: Additional fields (multipolarity, etc.)

### L-Record Format (Levels):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  L EEEE.E   DE  JP               T        DT
Example: 35S   L 1572.0    1  1/2+             2.29 PS   14
```

**BEFORE EDITING ANY ENSDF FILE:**
1. Check existing format in the file
2. Count columns manually: 1234567890123456789012345678901234567890
3. Verify against this reference
4. Double-check after editing

**NO EXCUSES FOR COLUMN MISTAKES - THIS IS NUCLEAR DATA!**

## Command Triggers

### "Self-Calibrate Columns" Command:
When you type "Self-Calibrate Columns", I will:

1. **Display column ruler:**
   ```
   12345678901234567890123456789012345678901234567890123456789012345678901234567890
   ```

2. **Count exact column positions of ENSDF fields:**
   - Extract a record line by line to verify exact positioning
   - Map each character to its precise column number
   - Verify nuclear data fields against ENSDF standards

3. **Correct column positions if needed:**
   - NUCID (e.g., 35S): Columns 2-4
   - Record type (L/G): Column 8
   - Energy value: Columns 10-19 (right-justified)
   - Uncertainty: Columns 20-21
   - J-value: Starting at column 23
   - L-value: Columns 56-64

This prevents formatting errors by ensuring precise character-by-character verification.

### "What changed" Command Trigger:
When the user types "What changed?" (case-insensitive), automatically:

1. **Run the PowerShell script to detect changes:**
   ```powershell
   cd "d:\X\ND\A35\.vscode"; .\what-changed.ps1 filename.ens
   ```
   - Use the script to compare files and identify specific changes
   - Run for any recently modified .ens files in the workspace

2. **Update change.log with evidence-based entries:**
   - Add new entries to the current date section (2025-06-18)
   - Use the what-changed.ps1 output to document exact changes
   - Include file paths, specific edits, and context
   - Categorize changes: header updates, level additions, gamma data, formatting, etc.

3. **Provide a summary to the user:**
   - List files that were changed
   - Summarize the types of changes made
   - Confirm that change.log has been updated

**Important:** Always use the what-changed.ps1 script for change detection rather than assumptions. This ensures accuracy and evidence-based documentation.

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

## NSR Keynumber Formatting
- NSR (Nuclear Science References) keynumbers cited in comments or other records (e.g., Q-record, L-record for T1/2, moments) should have the second letter of the author's name in lowercase. For example, `2023BO17` should be `2023Bo17`, `2021WA16` should be `2021Wa16`.
- The only exception is when a keynumber appears in the first line header record or Q record of an ENSDF dataset (columns 61-68), where it should be all uppercase.

## Spin-Parity (Jπ) Placement
- When adding spin-parity values to levels, place them exactly at column 23
- Example: `35K   L 4788      49 1/2+,3/2+`
  - Energy value (4788) remains at columns 11-15
  - Uncertainty (49) remains at columns 17-18  
  - Jπ (1/2+,3/2+) starts precisely at column 23
- Never add additional spaces that would shift uncertainty values

## L-Transfer Rules for Jπ Deduction
- L=0 → Jπ: `1/2+`
- L=1 → Jπ: `1/2-,3/2-`
- L=2 → Jπ: `3/2+,5/2+`
- L=3 → Jπ: `5/2-,7/2-`
- These are general rules; always confirm with specific experimental data or adopted level schemes if available.
- L-values themselves should NOT be entered into the Jπ column.

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
- Always update `d:\X\ND\A35\.vscode\change.log` (and `d:\X\ND\A35\change.log` if intended to be a duplicate) after making significant changes to track all modifications.
- Never create new or duplicate `change.log` files. Only use the existing `d:\X\ND\A35\.vscode\change.log`.
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



## Academic Citation Conventions

### Tense Usage in ENSDF Comments
Nuclear physics follows scientific academic conventions for citing previous research:

**Use PAST TENSE for all citations and references to completed studies:**
- ✅ "Authors stated that..." 
- ✅ "Smith reported gamma-ray energies..."
- ✅ "Garcia et al. found spectroscopic factors..."
- ✅ "1994FO04 measured transition probabilities..."
- ✅ "2023Gr04 observed level structures..."
- ✅ "Previous evaluators concluded that..."

**Avoid PRESENT TENSE for citations:**
- ❌ "Authors state that..."
- ❌ "Smith reports that..."
- ❌ "Garcia et al. find that..."

### Rationale
- **Scientific convention**: Nuclear physics uses past tense to describe completed experimental studies
- **Objectivity**: Past tense provides neutral, reporting tone for documented findings
- **Professional standard**: Aligns with APA style and nuclear physics journal conventions
- **Clarity**: Situates findings in their historical context as completed research

### Application in ENSDF
- Comment lines describing experimental methods and results
- References to previous measurements and evaluations
- Citations of literature values and adopted data
- Descriptions of what authors concluded or observed

**Consistency is essential** - use past tense uniformly throughout all citation contexts to maintain professional academic tone.

## Quick Commands

### Fix Format Command Trigger:
When you type "Fix format!" as a command, the Copilot Agent will automatically:

1. **Convert text to proper ENSDF notation**:
   - Greek letters → `|a`, `|b`, `|g`, `|d`, `|e`, `|q`, `|l`, `|m`, `|n`, `|p`, `|r`, `|s`, `|t`, `|w`, etc.
   - Isotope notation → `{+A}Element` format (e.g., `35S` → `{+35}S`)

2. **Standardize mathematical and scientific symbols**:
   - Multiplication signs → `|*`
   - Degree symbols → `|'` 
   - Approximately → `|?`
   - Less/greater than or equal → `|<`, `|>`
   - Plus-minus → `|+`
   - Times symbol → `|*`

3. **Fix superscripts and subscripts**:
   - Superscripts → `{+text}` format
   - Subscripts → `{-text}` format
   - Mass numbers → `{+A}Element`
   - Nuclear states → proper formatting

**Usage**: Simply type "Fix format!" and the agent will scan the current file and apply these specific ENSDF formatting corrections.

## ENSDF Special Character and Symbol Formatting

When editing ENSDF files, use these character codes for proper display of scientific notation:

### Superscripts and Subscripts
- `{+n}` → superscript (e.g., `{+3}He` displays as ³He)
- `{-n}` → subscript (e.g., `H{-2}O` displays as H₂O)
- `{+-n}` → negative superscript (e.g., `{+-4}` displays as ⁻⁴)

### Greek Letters and Mathematical Symbols
**Greek lowercase:**
- `|a` → α (alpha), `|b` → β (beta), `|c` → η (eta), `|d` → δ (delta)
- `|e` → ε (varepsilon), `|f` → φ (phi), `|g` → γ (gamma), `|h` → χ (chi)
- `|i` → ι (iota), `|j` → ε (epsilon), `|k` → κ (kappa), `|l` → λ (lambda)
- `|m` → μ (mu), `|n` → ν (nu), `|p` → π (pi), `|q` → θ (theta)
- `|r` → ρ (rho), `|s` → σ (sigma), `|t` → τ (tau), `|u` → υ (upsilon)
- `|w` → ω (omega), `|x` → ξ (xi), `|y` → ψ (psi), `|z` → ζ (zeta)

**Greek uppercase:**
- `|D` → Δ (Delta), `|F` → Φ (Phi), `|G` → Γ (Gamma), `|L` → Λ (Lambda)
- `|P` → Π (Pi), `|Q` → Θ (Theta), `|S` → Σ (Sigma), `|U` → Υ (Upsilon)
- `|W` → Ω (Omega), `|X` → Ξ (Xi), `|Y` → Ψ (Psi)

**Mathematical symbols:**
- `|*` → × (times), `|?` → ≈ (approx), `|<` → ≤ (leq), `|>` → ≥ (geq)
- `|'` → ° (degree), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|=` → ≠ (not equal), `|@` → ∞ (infinity), `|^` → ↑ (up arrow)
- `|_` → ↓ (down arrow), `|&` → ≡ (equiv), `|(` → ← (left arrow)
- `|)` → → (right arrow), `|.` → ∝ (proportional), `||` → | (vertical bar)
- **Important:** For approximate values, use `|?` (which gives both ≈ and ~ symbols)
- Standalone `~` is NOT allowed for approximate values in ENSDF
- `~` only works in special contexts (names like `G~urdal`, mass notation like `A~160`)

### Common Scientific Notation Examples
- `%(|e+|b{++})p` → %(ε+β⁺)p
- `|*10{+-4}` → ×10⁻⁴  
- `|s(E({+3}He),|q)` → σ(E(³He),θ)
- `|g|g-coin` → γγ-coin
- `{+208}Pb({+36}S,{+35}S)` → ²⁰⁸Pb(³⁶S,³⁵S)
- `|dj` → ΔJ (delta J)
- `~*` → · (center dot)
- `|"{` → overbar start (e.g., `|"{A}` → Ā)
- `|%{n}` → √n (square root)
- `|,` → ½ (one-half fraction)

### Usage Guidelines
- Always use these codes in ENSDF comment lines and data fields
- Maintain consistency throughout the file
- Double-check formatting after editing to ensure proper display

## ENSDF Column Format Reference (CRITICAL - NO MISTAKES ALLOWED)

### G-Record Format (Gamma Rays):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  G EEEE.E   DE  II.I   DI  [M]  [A]  [B]  [C]              
Example: 35S   G 1572.0    1  100.0  24                                   
```

**Column Positions:**
- 1-5: NUCID (35S, 35SI, etc.)
- 9: Record type (G)
- 10-19: E gamma (right-justified, with uncertainty)
- 20-29: Intensity (left-justified in 10-char field)
- 30-31: Intensity uncertainty
- 32+: Additional fields (multipolarity, etc.)

### L-Record Format (Levels):
```
Columns: 123456789012345678901234567890123456789012345678901234567890123456789012345678
Format:  35XX  L EEEE.E   DE  JP               T        DT
Example: 35S   L 1572.0    1  1/2+             2.29 PS   14
```

**BEFORE EDITING ANY ENSDF FILE:**
1. Check existing format in the file
2. Count columns manually: 1234567890123456789012345678901234567890
3. Verify against this reference
4. Double-check after editing

**NO EXCUSES FOR COLUMN MISTAKES - THIS IS NUCLEAR DATA!**
