# ENSDF Nuclear Data Evaluation Instructions

## ⚠️ CRITICAL WORKFLOW REMINDER ⚠️
**ALWAYS START WITH: `git status`**
- Before any "What changed?" workflow
- Before any change detection or documentation
- This ensures ALL modified files are identified and processed
- Missing this step = incomplete change tracking!

**CRITICAL FORMATTING RULE**: ALL ENSDF values AND uncertainties MUST be LEFT-JUSTIFIED in their fields!
- Energy values, RI values, half-lives, J-π, AND their uncertainties (DE, DRI, DT, etc.)
- Special markers (GT, LT) within uncertainty fields are also left-justified
- NEVER right-justify or center ANY ENSDF field content!

## Command Triggers

### "Self-Calibrate Columns"
Execute column validation on current ENSDF file:
- **PowerShell**: `.\column-calibrate.ps1 "currentfile.ens"` (add `-Detailed` for character mapping)
- **Python**: `python column_calibrate.py "currentfile.ens"` (add `--detailed` for character mapping)

**Process**: Display 80-char ruler → Extract L/G records → Validate against ENSDF Manual → Report issues

### "What changed?"
**MANDATORY FIRST STEP**: Always run `git status` to identify ALL modified files.

Execute comprehensive change detection and documentation:
1. **FIRST**: Run `git status` to list all modified files
2. Run `.\.vscode\what-changed.ps1 "filename.ens"` for each modified .ens file  
3. Update `change.log` with evidence-based entries (never assume changes)
4. Document with line numbers, before/after content, and scientific context

**Remember**: Git status MUST be the first step - missing files means incomplete documentation!

### "Fix format!"
Auto-convert text to proper ENSDF notation:
- Greek letters: `35S` → `{+35}S`, `α` → `|a`, `β` → `|b`, etc.
- Math symbols: `×` → `|*`, `≈` → `|?`, `±` → `|+`, etc.
- Superscripts/subscripts: Use `{+n}` and `{-n}` format

## ENSDF Column Format Standards (CRITICAL - NO MISTAKES ALLOWED)

### L-Record Format (Energy Levels):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  L EEEE.E   DE  JP               T        DT        L        S        DS C
Example: 35P   L 1572.0    1  1/2+             2.29 PS  14        2        1.23     45 
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35P  ") |
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

### G-Record Format (Gamma Transitions):
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  G EEEE.E   DE  II.I   DI  [M]      MR     DMR   CC     DCC TI       DTI C
Example: 35P   G 1572.0    1  100.0  4   [E2]     1.23   0.45  0.0368 8   1.23     45  
```

| Field | Columns | Required | Description |
|-------|---------|----------|-------------|
| NUCID | 1-5 | ✓ | Nucleus (e.g., "35P  ") |
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

**UNCERTAINTY LEFT-JUSTIFICATION RULE**: ALL uncertainties (DE, DRI, DMR, DCC, DTI, DT, DS, etc.) MUST be left-justified in their respective fields, just like the values themselves. Special markers (GT, LT) within uncertainty fields are also left-justified.

**LEFT-JUSTIFICATION RULE**: ALL values AND uncertainties MUST be left-justified within their respective fields. This includes:
- Energy values (E field) and their uncertainties (DE field)
- J-π values (spin-parity) and any associated uncertainties
- Half-life values (T field) and their uncertainties (DT field)
- RI values (relative intensity) and their uncertainties (DRI field)
- Mixing ratios (MR field) and their uncertainties (DMR field)
- Conversion coefficients (CC field) and their uncertainties (DCC field)
- All numerical and text values AND their uncertainties
Never right-justify or center ANY values OR uncertainties in ENSDF records!

## Essential Rules

### File Protection
- **NEVER** edit `.old` files (reference files from previous evaluation rounds)
- **NEVER** modify first/last line indentation or spacing in .ens files
- **ALWAYS** preserve "PN" line with its numeric value
- Make all edits between first and last line boundaries only

### Column Positioning
- **J-π placement**: Always start at column 23, LEFT-JUSTIFIED (never add spaces that shift uncertainties)
- **Energy values**: LEFT-JUSTIFIED in their designated columns (10-19)
- **RI values**: Start at column 23, **LEFT-JUSTIFIED** in 7-char field (23-29)
- **DRI values**: Position at columns 30-31 (including special markers like GT, LT)
- **Half-life values**: LEFT-JUSTIFIED in T field (columns 40-49)
- **BR values**: Position at column 32 (N-records), LEFT-JUSTIFIED
- **NR values**: Columns 11-15 (N-records), LEFT-JUSTIFIED

**CRITICAL**: ALL values must be LEFT-JUSTIFIED within their respective fields - never right-justified or centered!

### NSR Keynumber Formatting
- **In comments/records**: Second letter lowercase (`2023Bo17`, `2021Wa16`)
- **In headers/Q-records**: All uppercase (`2023BO17`, `2021WA16`)

### Change Tracking
- **Always** update `.vscode/change.log` after significant changes
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

## Nuclear Data Evaluation

### General Comment Ordering (adopted.ens files)
1. **Isotope discovery** (reference): experimental details
2. **{+A}X production**: production methods and studies  
3. **{+A}X decay measurements**: half-life, decay modes
4. **{+A}X radius measurement**: nuclear radius determinations
5. **{+A}X mass measurements**: mass spectrometry, Q-values
6. **Theoretical calculations**: models, predictions (always last)

### L-Transfer Rules for J-π Assignment
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

### Verification Checklist
- [ ] **FIRST**: `git status` - identify ALL modified files (MANDATORY)
- [ ] `git diff --name-only HEAD` - complete list verification
- [ ] `git ls-files --others --exclude-standard` - untracked files
- [ ] `what-changed.ps1` on each modified ENSDF file from git status
- [ ] Update `change.log` with evidence-based entries
- [ ] Comprehensive commit message

**Remember**: Start every workflow with git status!

### Git Commit Template
```
Title: Brief description of main changes

Summary:
- Enhanced/improved/fixed major components
- Scientific content updates in specific files

ENSDF Tools:
- tool_name.py: Specific improvements and validation results

Scientific Content:
- file_name.ens: Changes with line numbers and rationale

Processing Artifacts:
- PDF files: Regenerated files listed
- Temp files: Expected analysis output updates

Files changed: X modified, Y untracked
Brief scope and impact summary
```

## Project Structure

### Core Files (Most Critical)
- `finished/[Element]/new/*.ens` - Primary ENSDF source files
- `.vscode/change.log` - Comprehensive change tracking

### Generated Files (Expected to Change)  
- `finished/[Element]/pdf/*.pdf` - Generated from .ens files
- `finished/[Element]/temp/*.*` - Analysis tool artifacts

### Tools
- `.vscode/column-calibrate.ps1` - PowerShell column validator
- `.vscode/column_calibrate.py` - Python column validator
- `.vscode/check_averages.py` - Average calculation validator  
- `.vscode/what-changed.ps1` - Change detection script

### Reference Files (NEVER EDIT)
- `*.old` files - Previous evaluation rounds, keep untouched

---

## Focus Areas

**Current Priority**: K35 and P35 files (Ar35 completed)

**Quality Assurance**: Use Self-Calibrate Columns before any ENSDF edits, use What changed? after any modifications

**Remember**: Nuclear data accuracy is critical - when in doubt, verify with tools and cross-check against ENSDF Manual specifications.
