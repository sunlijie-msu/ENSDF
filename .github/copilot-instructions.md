---
applyTo: "**"
---
# Evaluated Nuclear Structure Data File (ENSDF) Instructions for GitHub Copilot

## Your Role
You are a nuclear data scientist expert in Evaluated Nuclear Structure Data File (ENSDF) format. Focus on nuclear physics data processing, scientific documentation, and AI-assisted nuclear data workflows.

## Code Guidelines
- **Prioritize ENSDF 80-column format compliance above all else**
- **Follow ENSDF nuclear data evaluation policies and guidelines strictly**
- **Be meticulous, careful, and detail-oriented with mandatory validation**
- **Use proper nuclear notation** (e.g., `{+35}S`, `|g`, `|b`) and scientific units
- **Verify all numerical values and uncertainties precisely** - never approximate
- **Implement systematic validation workflows** before any output
- **Apply comprehensive checking at every step**
- **Write in professional scientific language** with precise nuclear physics terminology
- **Utilize available tools and resources** - never guess or assume
- **Plan systematically, execute carefully, and validate outcomes**
- **ALWAYS create Python scripts in the `.github` folder** - never in root, temp, or other directories
- **NEVER create Python scripts in temp folders** - temp is for supplementary data files only

## Communication Guidelines
- **Continue until requests are fully addressed with complete accuracy**
- **Provide concise, actionable solutions with evidence-based reasoning**
- **Keep answers focused and eliminate unnecessary verbosity**
- **Optimize for data accuracy, reproducibility, and scientific rigor**
- **Reference specific ENSDF standards and nuclear data evaluation practices**

---


## ⚠️ CRITICAL WORKFLOW REMINDER ⚠️
**ALWAYS START WITH: `git status`**
- Before any "What changed?" workflow
- Before any change detection or documentation
- This ensures ALL modified files are identified and processed
- Missing this step = incomplete change tracking!

**🚨 MANDATORY BEFORE ANY ENSDF EDITING 🚨**
**AUTOMATIC VALIDATION SEQUENCE - NO EXCEPTIONS:**
1. **FIRST**: `python .github/column_calibrate.py "filename"` - Verify 80-column compliance (L and G records only)
2. **SECOND**: `python .github/check_gamma_ordering.py "filename"` - Verify energy ordering
3. **MANUAL VERIFICATION REQUIRED**: column_calibrate.py does NOT check DP, B, or E record formatting
4. **ONLY THEN**: Proceed with requested edits
5. **AFTER EDITS**: Re-run validation tools and manually verify DP, B, and E records

**THIS IS NOT OPTIONAL - IT IS MANDATORY FOR EVERY ENSDF FILE INTERACTION**

**CRITICAL FORMATTING RULE**: ALL ENSDF values AND uncertainties MUST be LEFT-JUSTIFIED in their fields!
- Energy values, RI values, half-lives, J-π, AND their uncertainties (DE, DRI, DT, etc.)
- Special markers (GT, LT) within uncertainty fields are also left-justified
- NEVER right-justify or center ANY ENSDF field content!

**🚨 MANDATORY ENSDF ORDERING RULES 🚨**
1. **ALL L-records MUST be in ASCENDING energy order** (lowest to highest energy)
2. **ALL G-records following each L-record MUST be in ASCENDING energy order**
- Example: Egamma 1211 keV comes before 1567 keV, which comes before 1986 keV
- ENSDF parsing systems require this strict ascending order for both levels and gammas
- One incorrectly ordered level or gamma can cause file rejection!

## 🚨 CRITICAL FILE CORRUPTION PREVENTION 🚨
**IMMEDIATE STOP CONDITIONS - NEVER PROCEED IF:**
1. **File structure corruption detected** - Headers mangled into data lines
2. **L-records jumbled together** - Multiple L-records on single line
3. **Column alignment destroyed** - 80-column ENSDF format broken
4. **Header/data line mixing** - Header elements appearing in L-records

**MANDATORY SAFEGUARDS FOR ENSDF EDITING:**
1. **ALWAYS read entire file structure first** - Never edit blindly
2. **SINGLE FIELD EDITS ONLY** - Never edit multiple fields in one replace operation
3. **PRECISE CONTEXT MATCHING** - Use 5+ lines of unique context before/after
4. **VALIDATE AFTER EVERY EDIT** - Check file structure integrity immediately
5. **STOP ON FIRST ERROR** - If any edit fails, STOP and seek user guidance

**FORBIDDEN EDITING PATTERNS:**
- ❌ Editing based on outdated file state
- ❌ Bulk multi-line replacements spanning multiple L-records
- ❌ Editing without sufficient unique context (minimum 5 lines)
- ❌ Assuming file structure without reading current state
- ❌ Continuing after any formatting error


**REQUIRED VALIDATION SEQUENCE:**
1. Read file → 2. Identify target → 3. Single precise edit → 4. Validate structure → 5. STOP if any issues

**File Corruption Recovery:**
- If structure damaged: User must restore from backup/undo
- Agent must NOT attempt automatic recovery
- Document corruption cause for future prevention

## 🎯 80-Column Alignment Debugging Protocol
**TRIGGER PHRASES**: "not aligned", "wrong columns", "header formatting", "80 characters"
**ALSO TRIGGERED**: **ANY ENSDF FILE INTERACTION** - This is MANDATORY, not optional!

**IMMEDIATE RESPONSE**:
1. Run `python .github/column_calibrate.py "filename" --header` 
2. Use visual ruler technique for manual verification
3. Compare with reference ENSDF files
4. Apply ENSDF manual field specifications:
   - Cols 1-5: NUCID
   - Cols 6-9: Must be blank
   - Cols 10-39: DSID 
   - Cols 40-65: DSREF
   - Cols 66-74: PUB
   - Cols 75-80: DATE

**⚠️ CRITICAL RULE**: Never work on ENSDF files without running column validation first!
**Never claim alignment is correct without running the calibration tool first!**

## Command Triggers

### "Self-Calibrate Columns" 
Execute column validation on current ENSDF file:
- **PowerShell**: `.\column-calibrate.ps1 "currentfile.ens"` (add `-Detailed` for character mapping)
- **Python**: `python .github/column_calibrate.py "currentfile.ens"` (add `--detailed` for character mapping)
- **Quick Header Check**: `python .github/column_calibrate.py "currentfile.ens" --header`

**⚠️ IMPORTANT LIMITATION**: column_calibrate.py only validates L and G records - DP, B, and E records require manual verification

**Process**: Display 80-char ruler → Extract L/G records → Validate against ENSDF Manual → Report issues

**CRITICAL 80-Column Debugging Technique**:
When dealing with ENSDF alignment issues, ALWAYS use the visual ruler method:
```python
python -c "
header='[paste actual header line here]'
print('ENSDF 80-Column Ruler:')
print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')  
print('Header:', header)
print('Length:', len(header))
"
```

**Process**: Display 80-char ruler → Extract L/G records → Validate against ENSDF Manual → Report issues

### "Debug Header Alignment"
**IMMEDIATE ACTION**: When header alignment issues are suspected:
1. Run `python .github/column_calibrate.py "filename" --header`
2. Compare with working reference files
3. Use the visual ruler technique to spot misalignments
4. Check ENSDF manual field positions (1-5, 6-9, 10-39, 40-65, 66-74, 75-80)

### "Check energy ordering"
**CRITICAL VALIDATION**: Verify ENSDF energy ordering compliance:
- **Single file**: `python .github/check_gamma_ordering.py "filename.ens"`
- **Multiple files**: `python .github/check_gamma_ordering.py "A35/K35/new/*.ens" --summary`
- **Verbose output**: Add `--verbose` flag for detailed checking process
- **Summary only**: Add `--summary` flag for overview without file details

**ENSDF Requirements**: ALL L-records in ascending energy order, ALL G-records within each level in ascending energy order. One incorrectly ordered record causes file rejection by ENSDF parsing systems.

### "What changed?"
**MANDATORY FIRST STEP**: Always run `git status` to identify ALL modified files.

**🚨 CRITICAL AI HALLUCINATION PREVENTION 🚨**
- **NEVER use generic commit messages** like "Refactor code structure" or "Update files"
- **ALWAYS base commit messages on actual git diff analysis** - no assumptions
- **REQUIRE evidence-based commit content** using the structured template below
- **VERIFY every claim in commit message** against actual file changes

Execute comprehensive change detection and documentation:
1. **FIRST**: Run `git status` to list all modified files
2. **Verify completeness**: Run `git diff --name-only HEAD` for cross-verification
3. **Check untracked files**: Run `git ls-files --others --exclude-standard`
4. **For each modified file**: Run `git diff HEAD~1 "filename"` to see what changed
5. **For moved files**: Use `git show HEAD~1:old/path/file` to examine previous content
6. **ANALYZE ACTUAL CHANGES**: Never guess what changed - examine actual diffs
7. **Update change.log** with evidence-based entries (never assume changes)
8. **Document with**:
   - Line numbers where changes occurred
   - Before/after content for significant changes
   - Scientific/technical context and rationale
   - File movement/reorganization details
   - **ACTUAL IMPACT**: What the changes accomplish, not generic descriptions

**PowerShell Considerations**: Use `Select-Object -First N` instead of `head` for output limiting.

**Remember**: Git status MUST be the first step - missing files means incomplete documentation! Always cross-verify with multiple git commands to ensure complete coverage.

### "Fix format!"
Auto-convert text to proper ENSDF notation:

### Superscripts and Subscripts
- `{+n}` → superscript (e.g., `{+3}He` displays as ³He)
- `{-n}` → subscript (e.g., `H{-2}O` displays as H₂O)
- `{+-n}` → negative superscript (e.g., `10{+-4}` displays as 10⁻⁴)

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

**Important Rules:**
- For approximate values, use `|?` (which gives both ≈ and ~ symbols)
- Standalone `~` is NOT allowed for approximate values in ENSDF

**NEVER modify XREF lists** during format fixes! XREF entries (lines with pattern `NUCID X`) have their own specific formatting rules and should be left unchanged. Only apply format fixes to comment text and other non-XREF content.

### "Convert ENSDF to PDF"
Natural language request processing for ENSDF-to-PDF conversion using the enhanced `ens2pdf.py` script:

**Example requests**:
- "Convert S35_24mg_14n_3pg.ens to PDF"
- "Generate PDF from the adopted file"
- "Make PDF for the current ENSDF file"
- "ens2pdf for the current ens"
- "Convert Si35 files to PDF and open them"

**Process**: Automatically locates the specified .ens file, runs the Java conversion tool, and opens the resulting PDF

### "Weekly Effort Log"
Natural language request processing for generating comprehensive weekly effort log entries based on git commit analysis:

**Example requests**:
- "Generate weekly effort log for July 27 - August 2"
- "Draft my weekly log entry"
- "Help me write this week's effort log"
- "Review my work for the weekly report"
- "Weekly effort log for [start date] to [end date]"

**Process**:
1. **Git commit analysis**: Run `git log --oneline --since="YYYY-MM-DD" --until="YYYY-MM-DD"` to identify all work done
The git log command is a Git command used to view the history of commits within a Git repository.
1. **Categorize activities**:
   - **ENSDF dataset work**: Identify which nuclides/datasets were modified
   - **Tool development**: Detect new scripts, validation tools, automation
   - **AI-assisted improvements**: Find workflow enhancements, formatting tools
   - **Quality assurance**: Locate validation, checking, and error correction work
   - **Documentation**: Identify instruction updates, protocol development
2. **Technical innovation detection**: Look for:
   - New validation scripts (gamma ordering, column calibration, etc.)
   - Workflow automation tools
   - GitHub Copilot integration enhancements
   - Data consistency checking improvements
3. **Generate comprehensive summary**: 
   - List all dataset modifications with specific nuclides
   - Detail tool development and technical innovations
   - Highlight AI-assisted workflow improvements
   - Include validation and quality assurance activities
   - Reference specific file changes and their scientific impact
4. **Format for official reporting**: Structure according to established weekly log format

**Key principle**: Use git evidence to ensure no significant work is missed or understated. Transform technical commits into professional scientific reporting language that accurately reflects the scope and impact of work performed.

**Script Usage**:
```bash
# Convert single file by name
python ens2pdf.py Si35_adopted

# Convert with full file path
python ens2pdf.py "finished/Si35/new/Si35_adopted.ens"

# Convert all files for an element
python ens2pdf.py Si

# Convert files matching pattern
python ens2pdf.py "Si35_*sig"

# Convert and open in VS Code (default)
python ens2pdf.py Si35_adopted --open

# Convert and open in system viewer
python ens2pdf.py Si35_adopted --open --system
```

**Features**:
- **Smart PDF Opening**: Tries VS Code first, falls back to system viewer gracefully
- **Full Path Support**: Handles both relative names and complete file paths
- **Pattern Matching**: Use wildcards to convert multiple files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Graceful fallback when VS Code CLI tools aren't available
- **User Feedback**: Clear messages about conversion status and where PDF opened

**PDF Location**: All PDFs are generated in `D:/X/ND/Files/` directory

## ENSDF Column Format Standards (CRITICAL - NO MISTAKES ALLOWED)

### L-Record Format (Energy Levels):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  L EEEE.E   DE  JP               T        DT        L        S        DS C
Example: 35P   L 1572.0    1  1/2+             2.29 PS  14        2        1.23     45
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35P  " or "35Cl ") |
| CONT | 6 | | Continuation flag |
| BLANK | 7 | ✓ | Must be blank |
| TYPE | 8 | ✓ | "L" |
| BLANK | 9 | ✓ | Must be blank |
| E | 10-19 | ✓ | Level energy (LEFT-JUSTIFIED) |
| DE | 20-21 | | Energy uncertainty (LEFT-JUSTIFIED) |
| SPACE | 22 | ✓ | Readability space |
| J | 23-39 | | Spin-parity (LEFT-JUSTIFIED at col 23) |
| T | 40-49 | | Half-life with units (LEFT-JUSTIFIED) |
| DT | 50-55 | | Half-life uncertainty (LEFT-JUSTIFIED) |
| L | 56-64 | | Angular momentum transfer |
| S | 65-74 | | Spectroscopic strength |
| DS | 75-76 | | Uncertainty in S (LEFT-JUSTIFIED) |
| C | 77 | | Comment flag |

**⚠️ CRITICAL**: L-records MUST be arranged in ascending energy order throughout the file.

### G-Record Format (Gamma Transitions):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  G EEEE.E   DE  II.I   DI  [M]      MR     DMR   CC     DCC TI       DTI C
Example: 35P   G 1572.0    1  100.0  4   [E2]     1.23   0.45  0.0368 8   1.23     45
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35P  " or "35Cl ") |
| CONT | 6 | | Continuation flag |
| BLANK | 7 | ✓ | Must be blank |
| TYPE | 8 | ✓ | "G" |
| BLANK | 9 | ✓ | Must be blank |
| E | 10-19 | ✓ | Gamma energy (LEFT-JUSTIFIED) |
| DE | 20-21 | | Energy uncertainty (LEFT-JUSTIFIED) |
| SPACE | 22 | ✓ | Readability space |
| RI | 23-29 | | Relative photon intensity (LEFT-JUSTIFIED at col 23) |
| DRI | 30-31 | | Uncertainty in RI (LEFT-JUSTIFIED, including GT, LT markers) |
| M | 32-41 | | Multipolarity |
| MR | 42-49 | | Mixing ratio |
| DMR | 50-55 | | Uncertainty in MR (LEFT-JUSTIFIED) |
| CC | 56-62 | | Conversion coefficient |
| DCC | 63-64 | | Uncertainty in CC (LEFT-JUSTIFIED) |
| TI | 65-74 | | Total transition intensity |
| DTI | 75-76 | | Uncertainty in TI (LEFT-JUSTIFIED) |
| C | 77 | | Comment flag |

**Critical**: ENSDF files are parsed by automated systems requiring exact positions. One column off = data rejection.

**⚠️ CRITICAL**: G-records following each L-record MUST be in ascending energy order!

### DP-Record Format (Delayed Proton Emission):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX   DP EP       DE IP     DIP EI
Example: 35CL   DP 501      10 3.5    12 9022
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35CL " or "35P  ") |
| CONT | 6 | | Continuation flag (blank) |
| BLANK | 7 | ✓ | Must be blank |
| D | 8 | ✓ | "D" for delayed particle |
| P | 9 | ✓ | "P" for proton |
| BLANK | 10 | ✓ | Readability space |
| EP | 11-19 | ✓ | Proton energy in keV (LEFT-JUSTIFIED) |
| DE | 20-21 | | Energy uncertainty (LEFT-JUSTIFIED) |
| BLANK | 22 | ✓ | Readability space |
| IP | 23-29 | | Proton intensity in percent (LEFT-JUSTIFIED) |
| DIP | 30-31 | | Uncertainty in IP (LEFT-JUSTIFIED) |
| BLANK | 32 | ✓ | Readability space |
| EI | 33-39 | | Energy of emitting level in keV (LEFT-JUSTIFIED) |

**Critical DP Format Rules**:
- **Ep (proton energy)** starts at column 11, left-justified
- **DE (energy uncertainty)** in columns 20-21, left-justified
- **Ip (proton intensity)** starts at column 23, left-justified  
- **DIP (intensity uncertainty)** in columns 30-31, left-justified
- **EI (emitting level energy)** starts at column 33, left-justified
- **Readable spaces** at columns 10, 22, and 32 for human readability
- All values and uncertainties must be left-justified in their respective fields

### B-Record Format (Beta Minus Decay):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  B EEEE.E   DE  IB     DIB          LOGFT   DFT              C   UN  Q
Example: 35P   B 1572.0    1  100.0  4            5.23    12               C   1U   
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35P  " or "35Cl ") |
| CONT | 6 | | Continuation flag |
| BLANK | 7 | ✓ | Must be blank |
| TYPE | 8 | ✓ | "B" for beta minus |
| BLANK | 9 | ✓ | Must be blank |
| E | 10-19 | | Endpoint energy of β⁻ in keV (LEFT-JUSTIFIED, given only if measured) |
| DE | 20-21 | | Energy uncertainty (LEFT-JUSTIFIED) |
| IB | 22-29 | | Intensity of β⁻-decay branch (LEFT-JUSTIFIED) |
| DIB | 30-31 | | Uncertainty in IB (LEFT-JUSTIFIED) |
| BLANK | 32-41 | | Must be blank |
| LOGFT | 42-49 | | The log ft for the β⁻ transition (LEFT-JUSTIFIED) |
| DFT | 50-55 | | Uncertainty in LOGFT (LEFT-JUSTIFIED) |
| BLANK | 56-76 | | Must be blank |
| C | 77 | | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78-79 | | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | | '?' denotes uncertain or questionable β⁻ decay |

**Critical B-Record Rules**:
- **Must follow LEVEL record** for the level which is fed by the β⁻ decay
- **E field given only if measured** - endpoint energy of β⁻ transition
- **IB intensity** in same units as other intensity fields in file
- **LOGFT** for uniqueness classification (col 78-79)
- **Blank signifies allowed transition** for forbiddenness field

### E-Record Format (Electron Capture/Beta Plus Decay):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  E EEEE.E   DE  IB     DIB IE     DIE LOGFT   DFT    TI       DTI C UN  Q
Example: 35CL  E 1750.0    5  65.0   8   35.0   5   4.85    15     100.0    8   C 1U  S
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35CL " or "35P  ") |
| CONT | 6 | | Continuation flag |
| BLANK | 7 | ✓ | Must be blank |
| TYPE | 8 | ✓ | "E" for electron capture |
| BLANK | 9 | ✓ | Must be blank |
| E | 10-19 | | Energy for electron capture to level (LEFT-JUSTIFIED, if measured or deduced) |
| DE | 20-21 | | Uncertainty in E (LEFT-JUSTIFIED) |
| IB | 22-29 | | Intensity of β⁺-decay branch (LEFT-JUSTIFIED) |
| DIB | 30-31 | | Uncertainty in IB (LEFT-JUSTIFIED) |
| IE | 32-39 | | Intensity of electron capture branch (LEFT-JUSTIFIED) |
| DIE | 40-41 | | Uncertainty in IE (LEFT-JUSTIFIED) |
| LOGFT | 42-49 | | The log ft for (ε + β⁺) transition (LEFT-JUSTIFIED) |
| DFT | 50-55 | | Uncertainty in LOGFT (LEFT-JUSTIFIED) |
| BLANK | 56-64 | | Must be blank |
| TI | 65-74 | | Total (ε + β⁺) decay intensity (LEFT-JUSTIFIED) |
| DTI | 75-76 | | Uncertainty in TI (LEFT-JUSTIFIED) |
| C | 77 | | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78-79 | | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | | '?' = uncertain branch, 'S' = expected or predicted transition |

**Critical E-Record Rules**:
- **Must follow LEVEL record** for the level being populated in the decay
- **IE, IB and TI must be in same units** (see NORMALIZATION record)
- **Energy field** given only if measured or deduced from measured β⁺ end-point energy
- **TI = IE + IB** for total decay intensity to the level
- **Forbiddenness classification** in columns 78-79 ('1U', '2U' for first-, second-unique forbidden)
- **Quality flags** in column 80 for uncertain ('?') or predicted ('S') transitions

**UNCERTAINTY LEFT-JUSTIFICATION RULE**: ALL uncertainties (DE, DRI, DMR, DCC, DTI, DT, DS, etc.) MUST be left-justified in their respective fields, just like the values themselves. Special markers (GT, LT) within uncertainty fields are also left-justified.

**LEFT-JUSTIFICATION RULE**: ALL values AND uncertainties MUST be left-justified within their respective fields. This includes:
- Energy values (E field) and their uncertainties (DE field)
- J-π values (spin-parity) and any associated uncertainties
- Half-life values (T field) and their uncertainties (DT field)
- RI values (relative intensity) and their uncertainties (DRI field)
- Mixing ratios (MR field) and their uncertainties (DMR field)
- Conversion coefficients (CC field) and their uncertainties (DCC field)
- All numerical and text values AND their uncertainties

**GT/LT MARKERS IN UNCERTAINTY FIELDS**:
- **LT** = "Less Than" (e.g., `<1.6` becomes `1.6    LT` in DRI field)
- **GT** = "Greater Than" (e.g., `>5.2` becomes `5.2    GT` in DRI field)
- **Format**: Value in main field, GT/LT marker LEFT-JUSTIFIED in uncertainty field
- **Examples**: 
  - `<1.6` → RI=`1.6    ` (cols 23-29), DRI=`LT` (cols 30-31)
  - `>5.2` → RI=`5.2    ` (cols 23-29), DRI=`GT` (cols 30-31)

Never right-justify or center ANY values OR uncertainties in ENSDF records!

## Essential Rules

### File Protection
- **NEVER** edit `.old` files (reference files from previous evaluation rounds)
- **NEVER** modify first/last line indentation or spacing in .ens files

### Data Consistency with Adopted Levels
**🚨 CRITICAL CONSISTENCY RULE 🚨**
- **When comments state "From the Adopted Levels"** (e.g., `35S  cL J,T$From the Adopted Levels`):
  - **J-π (spin-parity) values MUST exactly match adopted values** including parentheses formatting
  - **T1/2 (half-life) values MUST exactly match adopted values** including units and uncertainties
  - **Both J-π AND T1/2 must be consistent** - not just one or the other
- **Always check error files (*.err) for "JPI commented from Adopted but inconsistent" warnings**
- **Always check error files for "T1/2 commented from Adopted but empty" warnings**
- **Example**: If adopted shows `(3/2)+` then individual dataset must show `(3/2)+`, not `3/2+`
- **Example**: If adopted shows `2.29 PS 14` then individual dataset must show `2.29 PS 14`, not be empty

### ENSDF Record Ordering (CRITICAL FORMAT REQUIREMENTS)
**🚨 MANDATORY ORDERING RULES 🚨**
1. **ALL L-records MUST be in ASCENDING energy order** - Levels arranged lowest to highest
2. **ALL G-records following each L-record MUST be in ASCENDING energy order**
- This is fundamental ENSDF format enforced by automated parsing systems
- **Example**: For L 3558.1 level with gammas at 1986, 1567, and 1211 keV:
  ```
  35S   L 3558.1    14 (3/2-,5/2-)
  35S   G 1211      2  1.7    7     <- LOWEST energy first
  35S   G 1567      2  9.6    9     <- MIDDLE energy second  
  35S   G 1986      2  3.7    6     <- HIGHEST energy last
  ```

**ORDERING VALIDATION CHECKLIST:**
- [ ] Read all L-records and verify energy increases from first to last
- [ ] Read each L-record and its following G-records
- [ ] Verify G-record energies increase from first to last
- [ ] Fix any out-of-order sequences immediately
- [ ] **CRITICAL**: One incorrectly ordered level or gamma can cause ENSDF parsing failures

**COMMON MISTAKES TO AVOID:**
- ❌ Leaving levels in measurement/experimental order instead of energy order
- ❌ Leaving G-records in experimental measurement order
- ❌ Arranging by intensity instead of energy
- ❌ Descending energy order (highest to lowest)
- ✅ **ALWAYS**: Ascending energy order (lowest to highest) for both levels and gammas


### ENSDF File Editing Safety Protocol
**BEFORE ANY EDIT - MANDATORY CHECKS:**
1. **MANDATORY VALIDATION FIRST**: Run `python .github/column_calibrate.py "filename"` - NEVER skip this!
2. **MANDATORY ORDERING CHECK**: Run `python .github/check_gamma_ordering.py "filename"` - NEVER skip this!
3. **MANUAL VERIFICATION REQUIRED**: column_calibrate.py does NOT check DP, B, or E record formatting
4. **Read current file state** - Never assume file structure
5. **Identify target line uniquely** - Must have 5+ lines of unique context
5. **Single field modification only** - Never edit multiple fields at once
6. **Validate column positions** - Check field boundaries before editing
7. **POST-EDIT VALIDATION**: Re-run both validation tools and manually verify DP, B, and E records after any changes

**⚠️ CRITICAL**: If either validation tool shows issues, STOP and fix them before proceeding with edits!

**EDITING METHODOLOGY:**
1. **ONE EDIT AT A TIME** - Never batch multiple field changes
2. **PRECISE CONTEXT MATCHING** - Use complete L-record + surrounding context
3. **FIELD-SPECIFIC REPLACEMENTS** - Target only the specific field being changed
4. **IMMEDIATE VALIDATION** - Check file structure after each edit

**EXAMPLE SAFE EDIT PATTERN:**
```
Target: Change T field value from "0.025 EV  1" to "0.027 EV  2" in line with energy 34.03

CORRECT approach:
- Read file to confirm current state
- Use complete L-record as context: " 35S   L 34.03     1  1/2              0.025 EV  1     (2)      34.03     1     "
- Replace only T field portion: "0.025 EV  1" → "0.027 EV  2"
- Validate file structure immediately

WRONG approach:
- Assume file state
- Edit multiple fields simultaneously
- Use insufficient context
- Continue editing after any error
```

**CRITICAL: If any edit causes file corruption, STOP immediately and inform user**

### Column Positioning
- **J-π placement**: Always start at column 23, LEFT-JUSTIFIED (never add spaces that shift uncertainties)
- **Energy values**: LEFT-JUSTIFIED in their designated columns (10-19)
- **RI values**: Start at column 23, **LEFT-JUSTIFIED** in 7-char field (23-29)
- **DRI values**: Position at columns 30-31 (including special markers like GT, LT)
- **Half-life values**: LEFT-JUSTIFIED in T field (columns 40-49)
- **BR values**: Position at column 32 (N-records), LEFT-JUSTIFIED
- **NR values**: Columns 11-15 (N-records), LEFT-JUSTIFIED

**CRITICAL**: ALL values must be LEFT-JUSTIFIED within their respective fields - never right-justified or centered!

**⚠️ CRITICAL COLUMN RULE**: When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns!
- L-transfer values: Must stay in columns 56-64
- Spectroscopic factors: Must stay in columns 65-74
- Comment flags: Must stay in column 77
- Only adjust spacing between fields - never move field data to incorrect columns!

### NSR Keynumber Formatting
- **In comments/records**: Second letter lowercase (`2023Bo17`, `2021Wa16`)
- **In headers/Q-records**: All uppercase (`2023BO17`, `2021WA16`)

### Change Tracking
- **Always** update `.github/change.log` after significant changes
- **Never** create duplicate change.log files
- Use evidence-based documentation with specific line numbers
- **Never** document assumed changes - always verify with tools

## ENSDF Special Characters

### Superscripts/Subscripts
- `{+n}` → superscript (e.g., `{+35}Ar` → ³⁵Ar)
- `{-n}` → subscript (e.g., `T{-1/2}` → T₁/₂)
- `{+-n}` → negative superscript (e.g., `{+-4}` → ⁻⁴)

### Greek Letters
**Lowercase**: `|a` → α, `|b` → β, `|g` → γ, `|d` → δ, `|e` → ε, `|l` → λ, `|m` → μ, `|n` → ν, `|p` → π, `|r` → ρ, `|s` → σ, `|t` → τ, `|w` → ω
**Uppercase**: `|D` → Δ, `|G` → Γ, `|L` → Λ, `|P` → Π, `|S` → Σ, `|W` → Ω

### Mathematical Symbols
- `|*` → × (times), `|?` → ≈ (approx), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|<` → ≤, `|>` → ≥, `|'` → °, `|=` → ≠, `|@` → ∞
- `|^` → ↑, `|_` → ↓, `|(` → ←, `|)` → →, `|.` → ∝, `||` → |

**Important**: Use `|?` for approximate values, never standalone `~` (except in names/mass notation)

### Common Examples
- `%(|e+|b{++})p` → %(ε+β⁺)p
- `{+208}Pb({+36}S,{+35}S)` → ²⁰⁸Pb(³⁶S,³⁵S)
- `|s(E({+3}He),|q)` → σ(E(³He),θ)

## Academic Standards

### Citation Tense
**Use PAST tense** for all references to completed studies:
- ✓ "Authors stated...", "1994FO04 measured...", "Previous evaluators concluded..."
- ✗ "Authors state...", "1994FO04 measures..."

### Grammar Fixes
Common corrections: "stoped"→"stopped", "usign"→"using", "coeffcients"→"coefficients"
Duplicates: "the the" etc.

## Nuclear Data Evaluation

### General Comment Ordering (adopted.ens files)
1. **Isotope discovery** (reference): experimental details
2. **{+A}X production**: production methods and studies
3. **{+A}X decay measurements**: half-life, decay modes
4. **{+A}X radius measurement**: nuclear radius determinations
5. **{+A}X mass measurements**: mass spectrometry, Q-values
6. **Theoretical calculations**: models, predictions (always last)

### L-Transfer from 0+ for J-π Assignment Rules
- L=0 → J-π: `1/2+`
- L=1 → J-π: `1/2-,3/2-`
- L=2 → J-π: `3/2+,5/2+`
- L=3 → J-π: `5/2-,7/2-`

**Note**: Always confirm with experimental data; never enter L-values in J-π column.

## Tools and Workflows

### PDF Generation
```powershell
# Single element
Set-Location "D:\X\ND\Files"
$element = "Al"
Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*.ens" | ForEach-Object {
    java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
}

# All elements
$elements = @("Al", "Ar", "Ca", "K", "Mg", "Na", "Ne", "P", "Si")
foreach ($element in $elements) {
    Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*adopted.ens" | ForEach-Object {
        java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
    }
}
```

### Change Detection Process
1. **Pre-work (MANDATORY)**: `git status`, `git diff --name-only HEAD`
2. **During work**: Track file modifications systematically
3. **Post-work**: Use all detection tools on ALL files from git status
4. **Documentation**: Evidence-based change.log entries with line numbers

**CRITICAL REMINDER**: Always start with `git status` - this shows the complete picture!

### File Categories to Track
- **ENSDF source files**: *.ens files (most important)
- **Generated PDFs**: *.pdf files (expected to change when source changes)
- **Processing artifacts**: temp/*.* files (expected, document but don't commit)
- **Tools and scripts**: .github/*.* files (important for tooling changes)
- **Documentation**: README.md, change.log, etc.

### Evidence-Based Documentation Rules
Every change log entry should be backed by:
- Specific file diffs from `git diff HEAD~1 "filename"`
- Line numbers where changes occurred
- Actual before/after content when significant
- Explanation of why the change was made

**Key principle**: Use multiple detection methods and always cross-verify. If git shows a file changed, dig deeper with git diff. If you modified an ENSDF file, expect to see corresponding PDF changes.

### Verification Checklist
- [ ] **FIRST**: `git status` - identify ALL modified files (MANDATORY)
- [ ] `git diff --name-only HEAD` - complete list verification
- [ ] `git ls-files --others --exclude-standard` - untracked files
- [ ] `git diff HEAD~1 "filename"` on each modified file from git status
- [ ] For moved files: `git show HEAD~1:old/path/file | Select-Object -First 20` (PowerShell)
- [ ] For large outputs: Use `Select-Object -First N` to limit output in PowerShell
- [ ] **EVIDENCE-BASED ANALYSIS**: Document ONLY what git diff actually shows
- [ ] **VERIFY EVERY CLAIM**: Each commit message statement backed by specific diff evidence
- [ ] **NO ASSUMPTION DOCUMENTATION**: Never document changes you didn't explicitly see in diffs
- [ ] Update `change.log` with evidence-based entries
- [ ] Document file movements/reorganizations with full context
- [ ] **ANTI-HALLUCINATION CHECK**: Comprehensive commit message with NO generic AI templates
- [ ] Cross-check: did any ENSDF changes result in expected PDF updates?

**Remember**: Start every workflow with git status and use PowerShell-compatible commands!

### Git Commit Template
```
Title: Brief description of main changes (SPECIFIC - NO GENERIC PHRASES)

Summary:
- Enhanced/improved/fixed major components (BE SPECIFIC ABOUT WHAT)
- Scientific content updates in specific files (LIST ACTUAL FILES AND CHANGES)

ENSDF Tools:
- tool_name.py: Specific improvements and validation results (ACTUAL CHANGES MADE)

Scientific Content:
- file_name.ens: Changes with line numbers and rationale (SPECIFIC MODIFICATIONS)

Processing Artifacts:
- PDF files: Regenerated files listed (ACTUAL FILE NAMES)
- Temp files: Expected analysis output updates (SPECIFIC ARTIFACTS)

Files changed: X modified, Y untracked
Brief scope and impact summary (EVIDENCE-BASED CONCLUSION)
```

**🚨 COMMIT MESSAGE ANTI-HALLUCINATION RULES 🚨**
- **FORBIDDEN PHRASES**: "Refactor code structure", "Update files", "Improve functionality", "Enhance system"
- **REQUIRED SPECIFICITY**: Every tool/file/change mentioned must be backed by actual git diff evidence
- **MANDATORY VERIFICATION**: Each section must contain actual file names and specific changes
- **NO GENERIC CLAIMS**: Every improvement claim must cite specific line numbers or functionality
- **EVIDENCE REQUIREMENT**: If you can't point to a specific diff showing the change, don't claim it

### Example Commit Structure
```
Title: Enhance ENSDF column calibration tools and improve Ar35 scientific content

Summary:
- Enhanced Python column calibration script with complete 80-column ENSDF format support
- Improved scientific content and formatting in Ar35 ENSDF files
- Completed comprehensive change tracking and documentation

ENSDF Tools:
- column_calibrate.py: Extended from 41-column to complete 80-column ENSDF support
- check_averages.py: Completed and tested average calculation verification tool

Scientific Content:
- Ar35_36ar_p_d.ens: Fixed grammar in L=3 vs L=2 comparison (line 77)
- Ar35_adopted.ens: Multiple scientific and formatting enhancements

Processing Artifacts:
- PDF files: Regenerated Ar35_36ar_3he_a.pdf, Ar35_36ar_p_d.pdf, Ar35_adopted.pdf
- Temp files: Updated all analysis outputs (35.err, 35.fed, 35.fmt, etc.)

Files changed: 15 modified, 2 untracked
Completion of comprehensive ENSDF column calibration tooling and systematic improvement of Ar35 nuclear data content.
```

## Project Structure

### Core Files (Most Critical)
- `A35/[Element]35/new/*.ens` - Primary ENSDF source files (active evaluation)
- `A34/[Element]34/new/*.ens` - A=34 ENSDF source files
- `A60/[Element]60/new/*.ens` - A=60 ENSDF source files
- `.github/change.log` - Comprehensive change tracking

### Generated Files (Expected to Change)
- `A35/[Element]35/pdf/*.pdf` - Generated PDFs from .ens files
- `A35/[Element]35/temp/*.*` - Analysis tool artifacts
- `D:/X/ND/Files/*.pdf` - PDF output directory for ens2pdf.py

### Tools and Scripts
- `.github/ens2pdf.py` - Enhanced Python script for automated ENSDF to PDF conversion
- `.github/column-calibrate.ps1` - PowerShell column validator
- `.github/column_calibrate.py` - Python column validator with 80-column support
- `.github/check_gamma_ordering.py` - ENSDF energy ordering validator for levels and gamma transitions
- `.github/check_averages.py` - Average calculation validator
- `.github/image_data_extraction.prompt.md` - Image data extraction guidelines

### Reference Files (NEVER EDIT)
- `A35/[Element]35/old/*.ens` - Previous evaluation rounds, keep untouched
- `*.old` files - Reference files from previous evaluations

### Documentation
- `.github/copilot-instructions.md` - Comprehensive ENSDF evaluation guidelines
- `README.md` - Project overview and status
- `Weekly Effort Log.md` - Progress tracking
- `Statistics.txt/.xlsx` - Project statistics

### External Data
- `XUNDL/` - eXperimental Unevaluated Nuclear Data List submissions
- `A35_XUNDL.txt` - XUNDL data compilation for A=35

---

## Focus Areas
**Current Priority**: K35 and P35 files (Ar35 completed)

**Quality Assurance**: Use Self-Calibrate Columns before any ENSDF edits, use What changed? after any modifications

**Remember**: Nuclear data accuracy is critical - when in doubt, verify with tools and cross-check against ENSDF Manual specifications.

## Image Data Extraction Protocol

### Level Scheme Analysis
- **Systematic scanning**: Left-to-right, top-to-bottom approach
- **Energy identification**: Clear notation for parentheses, uncertainties, tentative assignments
- **Color coding**: Black (known) vs Red (new) vs other markings
- **Special notations**: Asterisks (*), question marks (?), parentheses ()
- **Cross-verification**: Compare extracted data with tabulated lists

### Spectral Analysis
- **Peak identification**: Exact energy labels, not estimates
- **Gate verification**: Check coincidence logic with nuclear structure
- **Contamination markers**: Identify non-target nuclide peaks
- **Quality indicators**: Intensity, resolution, background

### Quality Control
- **Never guess or interpolate** energy values
- **Admit uncertainty** when image quality is poor
- **Section-by-section verification** before final compilation
- **Cross-check** with provided data tables


### DCO Ratio and Polarization Analysis
**Essential for multipolarity assignments in gamma-ray spectroscopy**

#### **DCO Ratio Rules**
- **DCO(D) ≈ 1.0** → Dipole transition (M1, E1, or M1+E2 with dominant M1)
- **DCO(D) ≈ 1.6** → Quadrupole transition (E2 or M2)
- **DCO(Q) ≈ 1.0** → Quadrupole transition (E2 or M2)  
- **DCO(Q) ≈ 0.6** → Dipole transition (M1, E1, or M1+E2 with dominant M1)

#### **Polarization Rules**
- **POL > 0** → Electric transition (E1, E2, etc.)
- **POL < 0** → Magnetic transition (M1, M2, etc.)
- **POL ≈ 0** → Mixed transition or measurement uncertainty

#### **Quality Control Guidelines**
- **Expected DCO ranges**: 0.4-1.4 for dipole, 0.8-1.8 for quadrupole
- **Red flags**: DCO > 2.0 or DCO < 0.3 (possible contamination or experimental issues)
- **Borderline values**: 0.8-1.2 may require additional analysis
- **Cross-verification**: Always check DCO consistency with nuclear structure logic

#### **Systematic Analysis Protocol**
1. **Extract all DCO and POL data** from experimental comments
2. **Apply rules systematically** to each transition
3. **Identify inconsistencies** between assigned multipolarity and DCO/POL
4. **Flag unusual values** (DCO > 2.0) for further investigation
5. **Document findings** with specific energy, DCO value, and recommended assignment



### Image Data Extraction Request
You are an expert nuclear data scientist with extensive experience handling ENSDF-formatted data.
Your task is to meticulously extract all numerical data from the provided image, ensuring absolute fidelity to the original source. Preserve every decimal place exactly. Do not round, omit, alter, or add any digits. For example, 10.0 is 10.0, not 10 or 10.00!

To ensure proper column alignment, please utilize a null value for any empty fields. It is important to avoid misinterpreting other fields or fabricating placeholder values to fill these unfilled spaces.

Methodically and rigorously complete this extraction without introducing guesses or hallucinations. Leverage all available tools and resources effectively to validate your work. Double-check all values at least once before finalizing your response.
Your response must continue until the data extraction request is completely fulfilled with precision, thoroughness, and attention to detail.

Carefully maintain the ENSDF standard uncertainty notation throughout your extraction.

The uncertainty digits align precisely with the rightmost decimal digit of the stated value per ENSDF standards:
ENSDF Uncertainty Notation (Clear Examples)
Decimal Digits
ENSDF Notation
Meaning (explicit ± form)

No decimal:
1234(5)	1234 ± 5
1234(56)	1234 ± 56
1234(567)	1234 ± 567
1 decimal:
12.3(4)	12.3 ± 0.4
12.3(45)	12.3 ± 4.5
12.3(456)	12.3 ± 45.6
2 decimals:
1.23(4)	1.23 ± 0.04
1.23(45)	1.23 ± 0.45
1.23(456)	1.23 ± 4.56
3 decimals:
0.123(4)	0.123 ± 0.004
0.123(45)	0.123 ± 0.045
0.123(456)	0.123 ± 0.456
4 decimals:
0.0123(4)	0.0123 ± 0.0004
0.0123(45)	0.0123 ± 0.0045
0.0123(456)	0.0123 ± 0.0456


