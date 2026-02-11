# Comment Quoted Values Cross-Check Workflow

## Purpose

Verify all quoted level energies and J-π values in ENSDF cL J$ comments match exact data records.

**Patterns Checked:**
- `energy|g from level_energy, J-π` (feeding gammas)
- `energy|g to J-π` (outgoing gammas)  
- `level_energy, J-π level` (level references)
- Any quoted level energy + J-π combination

**Requirements:** Exact matching:
- Level energy matches L-record exactly
- J-π notation matches exactly (including parentheses)
- Level exists in file

---

## Prerequisites

- Python 3.11+
- Access to detection scripts in `.github/temp/`
- UTF-8 encoding support

---

## Critical Rules

### J-π Notation Precision

**Parentheses indicate uncertainty:**
- `1/2+` = Definite assignment
- `1/2(+)` = Tentative positive parity  
- `(1/2+)` = Tentative spin AND parity
- `(1/2)+` = Tentative spin, definite parity

**WRONG:** Treating `1/2(+)` and `1/2+` as equivalent  
**CORRECT:** Match character-for-character including all parentheses

### Energy Precision

**NO approximations:** Every energy must match exact L-record value.

**Examples:**
- Comment `7178.6` must match L-record `7178.6` (not `7178` or `7179`)
- Comment `7194.6` must match L-record `7194.6` (not `7194` or `7195`)

---

## Workflow Steps

### 1. Create Detection Script

Generate script in `.github/temp/`:

**Core Functions:**
- `parse_ensdf_file()`: Build level dictionary with energies, J-π, line numbers
- `find_quoted_levels()`: Extract all level energy + J-π patterns from cL J comments
- `verify_matches()`: Check each quoted value against L-records
**Core Functions:**
- `parse_ensdf_file()`: Build level dictionary with energies, J-π, line numbers
- `find_quoted_levels()`: Extract all level energy + J-π patterns from cL J comments
- `verify_matches()`: Check each quoted value against L-records

**Tolerances:**
- Level energy identification: 0.5 keV
- Level existence: 1.0 keV

**Output:** Line number, pattern type, quoted energy, quoted J-π, L-record energy, L-record J-π, match status.

---

### 2. Run Detection

```bash
python .github\temp\check_quoted_jpi.py "A35\Cl35\new\Cl35_adopted.ens" > results.txt
```

**Analyze Error Types:**
- `energy_mismatch`: Quoted energy ≠ L-record energy  
- `jpi_mismatch`: Quoted J-π ≠ L-record J-π
- `level_not_found`: No matching level exists

---

### 3. Investigate Issues

For each reported issue:

**Read Context:**
```bash
# Comment line and surrounding context
python -c "lines=open('file.ens',encoding='utf-8').readlines(); print(''.join(lines[line-5:line+5]))"

# Find L-record
Select-String -Path "file.ens" -Pattern "^ 35CL  L quoted_energy"
```

**Verify L-Record:**
- Check exact energy value
- Check exact J-π notation (including parentheses)
- Confirm level exists

---

### 4. Fix Critical Errors

**Energy Mismatch:**
- Find actual L-record energy
- Update comment to match exact value

**J-π Mismatch:**
- Verify L-record J-π notation  
- Correct parentheses exactly (e.g., `1/2+` → `1/2(+)`)
- Never remove or add parentheses without checking L-record

**Level Not Found:**
- Search nearby energies (`±5 keV`)
- Update comment to match actual level energy
- Or remove reference if level doesn't exist

---

### 5. Apply Corrections

Use `multi_replace_string_in_file` with EXACT context (3-5 lines before/after):

```python
replacements = [{
    "filePath": "d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_adopted.ens",
    "oldString": " 35CL cL J$from primary |g transitions in (p,|g): 2339.4|g from 7178.6, 1/2+   \n 35CL2cL level, 2355.4|g from 7194.6",
    "newString": " 35CL cL J$from primary |g transitions in (p,|g): 2339.4|g from 7178.6, 1/2(+) \n 35CL2cL level, 2355.4|g from 7194.6"
}]
```

**Edit-Validate-Repeat:** After each fix:
```bash
python .github\scripts\ensdf_1line_ruler.py --line "exact 80-char line"
```

---

### 6. Re-run Detection

```bash
python .github\temp\check_quoted_jpi.py "file.ens"
```

Expected: Zero critical errors.

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

### Exact Matching Requirements

**NO approximations:** Every value must match character-for-character.

**Level Energy:**
- Use EXACT L-record value (e.g., `7194.6`, not `7195` or `7194`)
- Match uncertainty precision

**J-π Notation:**
- Preserve parentheses exactly: `1/2(+)` ≠ `1/2+`
- Match all characters including spaces
- `(1/2+)` ≠ `1/2(+)` ≠ `1/2+`

---

## Common Pitfalls

1. **Ignoring parentheses:** J-π `1/2(+)` means tentative parity, not same as `1/2+`
2. **Rounding energies:** Use exact L-record values, not rounded
3. **Using calculated levels:** Always verify actual L-record exists
4. **Multiple edits without validation:** Validate EACH edit immediately

---

## Issue Triage

### Critical (Must Fix)
- Energy mismatch >0.5 keV
- J-π notation mismatch (any character difference)
- Level not found in file

### Acceptable (Negligible)
- Energy tolerances <0.1 keV due to ENSDF rounding
- Display artifacts from 80-column truncation

---

## Success Criteria

✅ Detection script reports 0 critical errors  
✅ All quoted energies match exact L-records  
✅ All J-π notations match exactly (including parentheses)  
✅ All referenced levels exist in file  
✅ Column formatting validation passes  
✅ Energy ordering validation passes

---

## Example Session

```bash
# 1. Run detection
python .github\temp\check_quoted_jpi.py "Cl35_adopted.ens"
# Found: 3 J-π mismatches

# 2. Investigate  
# Issue: Comment says "1/2+" but L-record shows "1/2(+)"

# 3. Fix
multi_replace_string_in_file([{
    "filePath": "...",
    "oldString": "7178.6, 1/2+",
    "newString": "7178.6, 1/2(+)"
}])

# 4. Validate
python .github\scripts\ensdf_1line_ruler.py --line "..."

# 5. Re-run detection
python .github\temp\check_quoted_jpi.py "Cl35_adopted.ens"
# Found: 0 critical errors ✅
```

---

## Notes

- Always use subagent for verification when requested
- Never skip validation after edits
- Document all changes in compliance checklist
- Preserve VS Code diff viewer for human review
-   Parentheses in J-π have specific physical meaning - never change without verification
