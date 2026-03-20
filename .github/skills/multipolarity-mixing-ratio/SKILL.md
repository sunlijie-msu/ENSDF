---
name: multipolarity-mixing-ratio
description: >
  Use this skill as a reference guide for ENSDF multipolarity (M) and mixing
  ratio (MR) field notation. Covers E1/M1/E2/M2 designations, shorthand
  D/Q/O, mixed M1+E2 formatting, symmetric and asymmetric DMR
  uncertainties, and exact column positions 33-41 (M) and 42-49 (MR).
  Suitable for writing or reviewing G-record multipolarity fields.
argument-hint: [multipolarity expression or G-record line]
---

# ENSDF Multipolarity and Mixing Ratio Reference

## Multipolarity Field Notation

### Multipolarity Field (M Field, Columns 33-41)

**ENSDF Shorthand Notation**: The multipolarity field uses standard abbreviations for electromagnetic transition types.

#### Single Multipolarities

- **D**: Dipole transition (electric E1 or magnetic M1)
- **Q**: Quadrupole transition (electric E2 or magnetic M2)
- **O**: Octupole transition (electric E3 or magnetic M3)
- **E1, E2, E3, ...**: Electric multipole transitions (full notation)
- **M1, M2, M3, ...**: Magnetic multipole transitions (full notation)

#### Mixed Multipolarities (Combinations)

- **D+Q**: Mixed dipole and quadrupole (e.g., M1+E2)
- **D(+Q)**: Predominantly dipole with small quadrupole admixture
- **(D+Q)**: Tentative or uncertain mixed transition assignment
- **Q+O**: Mixed quadrupole and octupole
- **M1+E2**: Explicit mixed magnetic dipole and electric quadrupole
- **M2+E3**: Explicit mixed magnetic quadrupole and electric octupole

### Critical Formatting Rules

- **LEFT-JUSTIFIED** in columns 33-41
- **Shorthand (D, Q, O) is valid ENSDF notation** — do NOT auto-replace with full notation unless specified
- **Parentheses indicate uncertainty** in multipolarity assignment
- **Plus sign (+)** indicates mixed transitions with comparable amplitudes
- **Full notation (E1, M1, E2, etc.) provides explicit multipole type specification**

### Examples

```
Column:  33333333334
         3456789012
Format:  
Q                   → Pure quadrupole (shorthand)
D                   → Pure dipole (shorthand)
E2                  → Electric quadrupole (full notation)
M1+E2               → Mixed magnetic dipole + electric quadrupole
D+Q                 → Mixed dipole + quadrupole (shorthand)
(D+Q)               → Tentative mixed dipole + quadrupole
D(+Q)               → Predominantly dipole with small quadrupole component
```

---

## Multipole Mixing Ratios

### Mixing Ratio Field (MR Field, Columns 42-49)

**Nuclear Physics Definition**: Multipole mixing ratios (δ) quantify the degree to which different angular momentum multipoles (like E1 and M2) are mixed in a gamma-ray transition. They represent the amplitude ratio between different electromagnetic transition modes.

#### Physical Significance

- **δ = 0**: Pure transition (single multipolarity, e.g., pure E2)
- **δ ≠ 0**: Mixed transition (multiple multipolarities contributing)
- **δ(E2/M1)**: Ratio of electric quadrupole to magnetic dipole amplitudes
- **δ(M1/E2)**: Ratio of magnetic dipole to electric quadrupole amplitudes
- **Angular correlation**: Mixing ratios determine gamma-ray angular distributions and correlations

#### MR Field Examples (Columns 42-49)

```
+1.23           → δ = +1.23
-0.45           → δ = -0.45  
>+2.1           → δ > +2.1
<-0.8           → δ < -0.8
+0.123          → δ = +0.123
-12.3           → δ = -12.3
```

#### Multiple Mixing Ratios

Mixing ratios are spin dependent. For transitions from levels with multiple possible spins, list all allowed mixing ratios in a cG comment line.

Example:
```
 35CL cG MR$+0.7 {I+12-2} for J=5/2; -0.40 {I+8-9} for J=9/2
```

### Mixing Ratio Uncertainties (DMR Field, Columns 50-55)

The DMR field supports both symmetric and asymmetric uncertainties.

#### Symmetric Uncertainties (1-2 Digits)
- **Format**: Left-justified digits with trailing spaces

#### Asymmetric Uncertainties (+X-Y Format)
- **Format**: `+X-Y` notation left-justified in 6-character field
- **Examples**: `+0.5-0.3`, `+2.1-1.8`, `+15-8`, `+0.12-0.09`
- **Physics context**: Common when systematic effects dominate or when theoretical calculations have asymmetric confidence intervals

#### Special DMR Field Cases
- **Limit measurements**: Use GT/LT when MR field has a lower/upper limit

### Critical Formatting Rules for Mixing Ratios

- **Always include sign** in MR field (+ or -)
- **LEFT-JUSTIFY all values** in both MR and DMR fields
- **Asymmetric uncertainties** use full 6-character DMR field
- **No exponential notation** — use decimal format only
- **Space padding** for values shorter than field width
