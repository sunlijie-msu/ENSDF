---
name: gamma-properties-standardization
description: >
  Use this skill when standardizing multipolarity (M), mixing ratio (MR),
  angular correlation coefficients (A2, A4, A6), and polarization (POL) in
  ENSDF G-records. Extracts data from messy raw comment text, populates
  G-record fields, and adds standardized cG comment lines with proper
  subscript notation and {I} uncertainties. Validates 80-column compliance
  after every edit.
argument-hint: [ENSDF file path]
---

# ENSDF Gamma Properties Standardization

## Purpose

Extract M, MR, A2/A4/A6, and POL data from raw comments and create properly formatted G-records with standardized `cG` comment lines.

## When to Use

- Setting up G-record multipolarity data for a new dataset
- Cleaning up messy raw comments into structured `cG M,MR$` and `cG $A{-2}=` lines
- Standardizing notation across G-records in a file

## Input Patterns

Identify M, MR, A2/A4, and POL data embedded in messy raw comment text (cL, cG, or inline).

## G-Record Fields

| Field | Columns | Content |
|---|---|---|
| M | 33-41 | Multipolarity, left-justified |
| MR | 42-49 | Mixing ratio, left-justified |
| DMR | 50-55 | MR uncertainty, left-justified |

## cG Comment Templates

**Multipolarity and mixing ratio:**
```
 NUCID cG M,MR$ from |g(|q) in NSR.
```

**Angular correlation coefficients:**
```
 NUCID cG $A{-2}=value {Iunc}, A{-4}=value {Iunc}, A{-6}=value {Iunc} (NSR).
```

**Polarization:**
```
 NUCID cG $POL=value {Iunc} (NSR).
```

## Formatting Rules

- Subscripts: `A{-2}`, `A{-4}`, `A{-6}` — never `A2`, `A4`, `A6`
- Separate coefficients: `, ` (comma + space)
- Uncertainties: `{Iunc}` integer format — never parentheses
- End statements with period
- Reference NSR key in parentheses

## Workflow

### 1. Assess

Read the target file. Identify levels with M, MR, A2/A4, or POL data in comments. Create an inventory table.

### 2. Extract

- M, MR, DMR from cL/cG lines or inline text
- A2, A4, A6 coefficients and uncertainties
- POL values and uncertainties
- NSR references for each measurement

### 3. Update G-Records

- Create missing G-records or update existing ones
- Position M at column 33, MR at column 42, DMR at column 50
- Ensure every line is exactly 80 characters

### 4. Add Standardized cG Comments

- Add `M,MR$` line referencing NSR key and method
- Add `$A{-2}=...` line with subscript notation
- Add `$POL=...` line if polarization data exists
- Use `{Iunc}` format for all uncertainties

### 5. Validate

```bash
python .github/scripts/ensdf_1line_ruler.py --file "FILE_PATH" --show-only-wrong
python .github/scripts/column_calibrate.py "FILE_PATH"
python .github/scripts/check_gamma_ordering.py "FILE_PATH"
```

All must return exit code 0.

## Multipolarity Notation Reference

| Code | Meaning |
|---|---|
| `M1+E2` | Magnetic dipole + Electric quadrupole |
| `E1(+M2)` | Electric dipole + Magnetic quadrupole |
| `D(+Q)` | Dipole + Quadrupole |
| `Q(+O)` | Quadrupole + Octupole |
| `O(+H)` | Octupole + Hexadecapole |
| `E2` | Electric quadrupole |

## Example

**Before:**
```
 34CL  L 3600.00   10 (2,3)            23 PS     5
 34CL cL $MR=-0.02 {I3} (1978Ba61) for 879 keV |g with Q(+O) with A2=0.40(2)
 34CL2cL A4=-0.14(3).
```

**After:**
```
 34CL  L 3600.00   10 (2,3)            23 PS     5                              
 34CL cL T$lifetime |t=23 ps {I5} (1978Ba61, RDM).                              
 34CL  G 879                    Q(+O)    -0.02   3                              
 34CL cG M,MR$ from |g(|q) in 1978Ba61.                                         
 34CL cG $A{-2}=0.40 {I2}, A{-4}=-0.14 {I3} (1978Ba61).                         
```

## Gotchas

- Mixing `(unc)` with `{Iunc}`: publications use parentheses, ENSDF comments use `{I}` — always convert
- Wrong subscript notation: `A2` vs `A{-2}` — ENSDF requires the subscript markup
- Forgetting to create a G-record when only comment data exists — the M/MR fields need a G-record to live in
- Rose-Brink sign convention reversal: if source uses Rose-Brink (1967), reverse the MR sign and swap asymmetric uncertainty bounds (see `copilot-instructions.md` Section 2, DMR field)

## Validation Checklist

- [ ] All G-records exactly 80 characters
- [ ] M at column 33, MR at column 42, DMR at column 50
- [ ] cG uses `A{-2}`, `A{-4}`, `A{-6}` notation
- [ ] All uncertainties use `{Iunc}` integer format
- [ ] Energy ordering preserved
- [ ] All validation tools return exit code 0
