# Comment Quoted Values Cross-Check Workflow

## Purpose

Verify all quoted values in ENSDF cL J$ comments match exact data in G-records and L-records. Ensure no approximations, rounding, or misinterpretations occur.

**Four Value Types Verified:**
1. **Gamma Energy:** Quoted γ energy matches G-record energy
2. **Multipolarity:** Quoted multipolarity matches G-record multipolarity field (columns 33-41)
3. **Level Energy:** Quoted level energy matches L-record energy  
4. **J-π Notation:** Quoted J-π matches L-record J-π (including parentheses)

**Patterns Checked:**
- `energy|g multipolarity from level_energy, J-π` (feeding gammas with multipolarity)
- `energy|g to level_energy, J-π` (outgoing gammas)  
- `energy|g multipolarity to/from J-π` (gamma with multipolarity)
- `level_energy, J-π level` (level references)

**Requirements:** Exact character-for-character matching for all values.

---

## Prerequisites

- Python 3.11+
- Detection script: `.github/temp/check_quoted_values.py`
- UTF-8 encoding support

---

## Critical Rules

### Gamma Energy Precision

**Exact matching required:** Every quoted gamma energy must match a G-record energy exactly (within 0.5 keV tolerance for identification).

**Examples:**
- Comment `1572.327|g` must match G-record with energy `1572.327` keV
- Comment `2061.6|g` must match G-record with energy `2061.6` keV
- NO rounding: `1572` requires G-record `1572.0±0.5`, not `1572.327`

### Multipolarity Notation Precision

**G-Record Format Rules:**
- Multipolarity field is at **columns 33-41** (1-based indexing)
- Column 32 must be blank (readability space)
- Multipolarity can be: `M1`, `E2`, `M1+E2`, `D`, `(M1)`, `[E2]`, etc.

**Common Errors:**
- ❌ Multipolarity at column 32 instead of 33+ (formatting error)
- ❌ Comment quotes "D" but G-record has "(M1)" or empty field

**Exact matching required:** Comment must quote G-record multipolarity exactly.

**Examples:**
- Comment `1824.7|g M1+E2` requires G-record multipolarity `M1+E2` (NOT `M1`, NOT `D`)
- Comment `2061.6|g D` requires G-record multipolarity `D` (NOT empty, NOT `(M1)`)
- Brackets/parentheses matter: `(M1)` ≠ `M1` ≠ `[M1]`

### J-π Notation Precision

**Parentheses indicate uncertainty:**
- `1/2+` = Definite assignment
- `1/2(+)` = Tentative positive parity  
- `(1/2+)` = Tentative spin AND parity
- `(1/2)+` = Tentative spin, definite parity
- `(1/2)-` = J uncertain, parity negative and certain (minus OUTSIDE)
- `(1/2-)` = Both J and parity uncertain (minus INSIDE)

**WRONG:** Treating `1/2(+)` and `1/2+` or `(1/2)-` and `(1/2-)` as equivalent  
**CORRECT:** Match character-for-character including all parentheses

### Level Energy Precision

**NO approximations:** Every energy must match exact L-record value (within acceptable rounding <0.5 keV).

**Examples:**
- Comment `1991` may match L-record `1991.27` (acceptable rounding)
- Comment `7178.6` must match L-record `7178.6` (not `7178` or `7179`)
- Warnings issued for rounding >0.01 keV, errors for >0.5 keV

---

## Workflow Steps

### 1. Create/Use Detection Script

Use comprehensive detection script: `.github/temp/check_quoted_values.py`

**Core Functions:**
- `parse_ensdf_levels()`: Build level dictionary from L-records (energies, J-π, line numbers)
- `parse_ensdf_gammas()`: Build gamma list from G-records (energies, multipolarities, parent levels)
  - **Critical:** Must check column 6 and 7 are blank (not continuation or comment records)
  - Multipolarity from columns 33-41, NOT column 32
- `find_quoted_values()`: Extract all four value types from cL J$ comments
- `verify_quoted_values()`: Cross-check all quoted values against L/G-records

**Four Value Types Verified:**
1. **gamma_energy:** Match against G-record energies (tolerance 0.5 keV)
2. **multipolarity:** Match against G-record multipolarity field exactly
3. **level_energy:** Match against L-record energies (acceptable rounding <0.5 keV)
4. **level_jpi:** Match against L-record J-π exactly (character-for-character)

**Tolerances:**
- Gamma/level energy identification: 0.5 keV
- Level energy rounding warning: >0.01 keV
- Multipolarity & J-π: Zero tolerance (exact match required)

**Output:** Line number, pattern type, quoted value, L/G-record value, match status

---

### 2. Run Detection

```bash
python .github\temp\check_quoted_values.py "A35\S35\new\S35_adopted.ens"
```

**Analyze Error Types:**
- `GAMMA_NOT_FOUND`: Quoted gamma energy has no matching G-record
- `GAMMA_ENERGY_APPROX`: Gamma energy rounding >0.01 keV (warning only)
- `MULTIPOLARITY_MISMATCH`: Quoted multipolarity ≠ G-record multipolarity
- `LEVEL_NOT_FOUND`: Quoted level energy has no matching L-record
- `LEVEL_ENERGY_MISMATCH`: Level energy difference >0.5 keV (critical)
- `LEVEL_ENERGY_ROUNDED`: Level energy rounding 0.01-0.5 keV (warning)
- `JPI_MISMATCH`: Quoted J-π ≠ L-record J-π (any character difference)

---

### 3. Investigate Issues

For each reported issue:

**Read Context:**
```bash
# Comment line and surrounding context
python -c "lines=open('file.ens',encoding='utf-8').readlines(); print(''.join(lines[line-5:line+5]))"

# Find L-record for level
Select-String -Path "file.ens" -Pattern "^ 35S   L quoted_energy"

# Find G-record for gamma
Select-String -Path "file.ens" -Pattern "^ 35S   G gamma_energy"
```

**Verify L-Record:**
- Check exact energy value
- Check exact J-π notation (including parentheses)
- Confirm level exists

**Verify G-Record:**
- Check exact gamma energy value
- Check multipolarity field at columns 33-41 (NOT column 32)
- Confirm column 32 is blank (readability space)
- Verify multipolarity characters match exactly

---

### 4. Fix Critical Errors

**Gamma Energy Mismatch:**
- Find actual G-record energy
- Update comment to match exact value

**Multipolarity Mismatch:**
- **If G-record has multipolarity at column 32:** Fix G-record formatting (shift right to column 33)
- **If G-record multipolarity differs from comment:** Update comment to match G-record exactly
- Preserve brackets/parentheses: `(M1)` ≠ `M1` ≠ `D`

**Level Energy Mismatch:**
- Find actual L-record energy
- Update comment to match exact value (acceptable rounding <0.5 keV)

**J-π Mismatch:**
- Verify L-record J-π notation  
- Correct parentheses exactly:
  - `(7/2+)` → `7/2(+)` if L-record shows `7/2(+)`
  - `(11/2-)` → `(11/2)-` if L-record shows `(11/2)-` (minus position critical!)
- Never remove or add parentheses without checking L-record

**Level/Gamma Not Found:**
- Search nearby energies (`±5 keV`)
- Update comment to match actual energy
- Or remove reference if level/gamma doesn't exist

---

### 5. Apply Corrections

Use `multi_replace_string_in_file` with EXACT context (3-5 lines before/after):

```python
replacements = [{
    "filePath": "d:\\X\\ND\\ENSDF\\A35\\S35\\new\\S35_adopted.ens",
    "oldString": " 35S X L XREF=DE                                                                \n 35S  cL J$1228.1|g D, |DJ=1 to 3594.6, (7/2+); 1055.1|g D, |DJ=1 from 5877.7,  \n 35S 2cL (11/2+); 9/2+ from shell-model calculations (2021Go09).",
    "newString": " 35S X L XREF=DE                                                                \n 35S  cL J$1228.1|g D, |DJ=1 to 3594.6, 7/2(+); 1055.1|g D, |DJ=1 from 5877.7,  \n 35S 2cL (11/2+); 9/2+ from shell-model calculations (2021Go09)."
}]
```

**G-Record Formatting Fixes (column 32 → 33):**
```python
replacements = [{
    "filePath": "...",
    "oldString": " 35S   G 2061.6    4 100     5 D                                                ",
    "newString": " 35S   G 2061.6    4 100     5  D                                               "
    # Note: Added space before "D" to shift from column 32 to column 33
}]
```

**Edit-Validate-Repeat:** After each fix:
```bash
python .github\scripts\ensdf_1line_ruler.py --line "exact 80-char line"
```

---

### 6. Re-run Detection

```bash
python .github\temp\check_quoted_values.py "file.ens"
```

Expected: Zero critical errors (warnings acceptable for level energy rounding <0.5 keV).

---

### 7. Final Validation

```bash
# Column formatting
python .github\scripts\column_calibrate.py "file.ens"

# Energy ordering
python .github\scripts\check_gamma_ordering.py "file.ens"
```

Both must exit with code 0.

---

## Critical Rules

## Exact Matching Requirements

**NO approximations:** Every value must match character-for-character (with acceptable tolerances noted).

**Gamma Energy:**
- Within 0.5 keV for identification
- Warnings for >0.01 keV rounding

**Multipolarity:**
- MUST be at columns 33-41 in G-record (column 32 = readability space)
- Exact character match: `D` ≠ `(M1)` ≠ `M1` ≠ `[E2]`
- Brackets/parentheses have physical meaning

**Level Energy:**
- Exact L-record value OR acceptable rounding (<0.5 keV)
- Warnings for 0.01-0.5 keV rounding
- Match uncertainty precision when specified

**J-π Notation:**
- Preserve parentheses exactly: `1/2(+)` ≠ `1/2+` ≠ `(1/2+)` ≠ `(1/2)+`
- Minus position critical: `(11/2)-` ≠ `(11/2-)`
- Match all characters including spaces

---

## Common Pitfalls

1. **Ignoring parentheses in J-π:** `1/2(+)` means tentative parity, not same as `1/2+`; `(11/2)-` ≠ `(11/2-)`
2. **Multipolarity at wrong column:** G-record must have multipolarity at columns 33-41, NOT column 32
3. **Multipolarity approximation:** Comment says "D" but G-record has "(M1)" - these are NOT equivalent
4. **Rounding energies:** Use exact L/G-record values, not rounded (warnings OK for <0.5 keV)
5. **Using calculated levels:** Always verify actual L-record exists
6. **Multiple edits without validation:** Validate EACH edit immediately
7. **Forgetting directionality:** "from level X" vs "to level Y" determines which level to check

---

## Issue Triage

### Critical (Must Fix)
- Gamma energy mismatch >0.5 keV
- Gamma not found in G-records
- Multipolarity mismatch (any character difference)
- Multipolarity at column 32 instead of 33-41 (G-record formatting error)
- Level energy mismatch >0.5 keV
- Level not found in L-records
- J-π notation mismatch (any character difference, including parentheses position)

### Acceptable (Warnings Only)
- Gamma energy rounding 0.01-0.5 keV (warnings issued)
- Level energy rounding 0.01-0.5 keV (warnings issued)
- Display artifacts from 80-column truncation

---

## Success Criteria

✅ Detection script reports 0 critical errors  
✅ All quoted gamma energies match G-records (within 0.5 keV)  
✅ All quoted multipolarities match G-record multipolarity fields exactly  
✅ All multipolarity fields in G-records are at columns 33-41 (NOT column 32)  
✅ All quoted level energies match L-records (acceptable rounding <0.5 keV)  
✅ All J-π notations match exactly (including parentheses position)  
✅ All referenced levels and gammas exist in file  
✅ Column formatting validation passes  
✅ Energy ordering validation passes

---

## Example Session

```bash
# 1. Run detection
python .github\temp\check_quoted_values.py "S35_adopted.ens"
# Found: 8 critical errors (4 J-π mismatches, 4 multipolarity mismatches)

# 2. Investigate  
# Issue #1: Comment says "(7/2+)" but L-record shows "7/2(+)"
# Issue #5: G-record has multipolarity "D" at column 32 instead of 33-41

# 3. Fix J-π error
multi_replace_string_in_file([{
    "filePath": "...",
    "oldString": "1228.1|g D, |DJ=1 to 3594.6, (7/2+)",
    "newString": "1228.1|g D, |DJ=1 to 3594.6, 7/2(+)"
}])

# 4. Fix multipolarity formatting error (shift "D" one column right)
multi_replace_string_in_file([{
    "filePath": "...",
    "oldString": " 35S   G 1055.1    6 80      7 D                                                ",
    "newString": " 35S   G 1055.1    6 80      7  D                                               "
}])

# 5. Validate each edit
python .github\scripts\ensdf_1line_ruler.py --line "..."

# 6. Re-run detection after ALL fixes
python .github\temp\check_quoted_values.py "S35_adopted.ens"
# Found: 0 critical errors, 29 warnings ✅

# 7. Review warnings (acceptable level energy rounding)
# All warnings show level energy differences <0.5 keV - ACCEPTABLE

# 8. Final validation
python .github\scripts\column_calibrate.py "S35_adopted.ens"
# SUCCESS: All ENSDF field positions correct ✅
```

---

## Notes

- Always use subagent for verification when requested
- Never skip validation after edits
- Document all changes in compliance checklist
- Preserve VS Code diff viewer for human review
-   Parentheses in J-π have specific physical meaning - never change without verification
