---
name: gamma-properties-standardization
description: Standardize multipolarity (M), mixing ratio (MR), angular correlation coefficients (A2, A4, A6), and polarization (POL) in ENSDF gamma transition G-records. Extracts data from messy raw comment text, creates properly formatted G-records, adds standardized cG M,MR$ and cG $A{-2}= comment lines. Validates 80-column compliance with column_calibrate.py after every edit. Use when setting up or cleaning up G-record multipolarity data.
argument-hint: [ENSDF file path]
---

# ENSDF Gamma Properties Standardization

## Task
Standardize multipolarity (M), mixing ratio (MR), angular correlation coefficients (A2, A4, A6), and polarization (POL) in ENSDF gamma transition records. Extract data from messy raw data and create properly formatted G-records with standardized cG comments.

## Prerequisites
1. Read `.github/agents/FRIBND.agent.md` from start to end
2. Read `.github/copilot-instructions.md` from start to end
3. Review G-record format specifications (columns 10-19: E, 33-41: M, 42-49: MR, 50-55: DMR)
4. Understand cG comment scope (applies only to immediately preceding G-record)

## Input Patterns
Identify M, MR, A2/A4, and POL data embedded in messy raw data.

## Standard Format

### G-Record Structure
- **M field** (col 33-41): Multipolarity, left-justified
- **MR field** (col 42-49): Mixing ratio, left-justified  
- **DMR field** (col 50-55): MR uncertainty, left-justified

### cG Comment Templates
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

### Formatting Rules
- Subscripts: `A{-2}`, `A{-4}`, `A{-6}` (NOT `A2`, `A4`, `A6`)
- Separate coefficients: `, ` (comma + space)
- Uncertainties: `{Iunc}` format (NOT parentheses)
- End statements with period
- Reference NSR in parentheses

## Workflow

### 1. Assessment
- Read target file completely
- Identify levels with M, MR, A2A4, POL data in comments
- Create inventory table

### 2. Extraction
- Extract M, MR, DMR from cL/cG lines or inline text
- Extract A2, A4, A6 coefficients and uncertainties
- Extract POL values and uncertainties
- Note NSR references

### 3. G-Record Update
- Create missing G-records or update existing ones
- Position M at column 33, MR at column 42, DMR at column 50
- Ensure 80-character line length

### 4. cG Comment Standardization
- Add `M,MR$` line referencing NSR and method
- Add `$A{-2}=...` line with subscript notation
- Add `$POL=...` line if polarization data exists
- Use proper `{Iunc}` format for all uncertainties

### 5. Validation
```bash
python .github/scripts/column_calibrate.py "FILE_PATH"
python .github/scripts/check_gamma_ordering.py "FILE_PATH" --verbose
```
Both commands must return exit code 0.

## Example

### Before
```
 34CL  L 3600.00   10 (2,3)            23 PS     5
 34CL cL $MR=-0.02 {I3} (1978Ba61) for 879 keV |g with Q(+O) with A2=0.40(2)
 34CL2cL A4=-0.14(3).
```

### After
```
 34CL  L 3600.00   10 (2,3)            23 PS     5                              
 34CL cL T$lifetime |t=23 ps {I5} (1978Ba61, RDM).                              
 34CL  G 879                    Q(+O)    -0.02   3                              
 34CL cG M,MR$ from |g(|q) in 1978Ba61.                                         
 34CL cG $A{-2}=0.40 {I2}, A{-4}=-0.14 {I3} (1978Ba61).                         
```

## Multipolarity Notations
- `M1+E2` = Magnetic dipole + Electric quadrupole
- `E1(+M2)` = Electric dipole + Magnetic quadrupole
- `D(+Q)` = Dipole + Quadrupole
- `Q(+O)` = Quadrupole + Octupole
- `O(+H)` = Octupole + Hexadecapole
- `E2` = Electric quadrupole

## Validation Checklist
- [ ] All G-records exactly 80 characters
- [ ] M field at column 33
- [ ] MR field at column 42
- [ ] DMR field at column 50
- [ ] cG uses `A{-2}`, `A{-4}`, `A{-6}`, `POL` notation
- [ ] All uncertainties use `{Iunc}` format
- [ ] Energy ordering preserved
- [ ] Both validation tools return exit code 0

## Critical Rules
- **Edit-Validate-Repeat:** Validate after EVERY G-record edit
- **Level Block Integrity:** G-records attach to preceding L-record only
- **Left-Justification:** Field values start at leftmost column
- **No Versioning:** Edit in place; never create backup files
- **VS Code Diff:** Preserve diff view for user review

## Forbidden
- Creating version files (`_v2.ens`, `_fixed.ens`, `_updated.ens`)
- Batch editing without per-line validation
- Using `git restore` or `git checkout` for recovery
- Mixing `(unc)` with `{Iunc}` notation
- Right-justifying or centering values

## More Examples
```
35CL  L 4347.8    12 9/2-             2.0 PS   +10-5
35CL cL T$Lifetime |t=2.9 ps {I+14-7} (1972Br33, DSAM).
35CL  G 1184.6    10 100.0  31 M1+E2    -0.36   3
35CL cG M,MR$ from |g(|q) in 1974Lo17.
35CL cG $A{-2}=+0.19 {I11}, A{-4}=-0.01 {I13} (1974Lo17).
35CL cG $POL=-0.40 {I14} (1974Lo17).
35CL  G 2244       3 100.0  22 E2
35CL cG M$Q(+O) with |d(O/Q)=0.00 {I3} from p|g(|q) in 1974Lo17.
35CL cG $A{-2}=+0.44 {I3}, A{-4}=-0.19 {I3} (1974Lo17).
```
