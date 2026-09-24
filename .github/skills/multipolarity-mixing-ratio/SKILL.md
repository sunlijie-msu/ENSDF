---
name: multipolarity-mixing-ratio
description: >
  Use this skill as a reference guide for ENSDF multipolarity (M) and mixing ratio (MR) field notation. 
  Suitable for writing or reviewing G-record multipolarity and mixing ratio fields.
argument-hint: [multipolarity (M) and mixing ratio (MR) or G-record line]
---

# ENSDF Multipolarity and Mixing Ratio Reference

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.


### Multipolarity Field (M Field, Columns 33-41)

**ENSDF Shorthand Notation**: The multipolarity field uses standard abbreviations for electromagnetic transition types.

## Multipolarity Field Notation

    -   Comma `,` = OR (alternative multipolarities)
    -   Plus `+` = AND (mixed multipolarity)
    -   Parentheses `()` = tentative multipolarity
    -   Square brackets `[]` = tentative multipolarity inferred purely from level scheme spin-parity changes

#### Single Multipolarities

E1
E2
E3
E4
M1
M2
M3
M4
D (Dipole, L=1): E1 or M1
Q (Quadrupole, L=2): E2 or M2
O (Octupole, L=3): E3 or M3
H (Hexadecapole, L=4): E4 or M4


#### Mixed Multipolarities
D+Q
Q+O
O+H (rare)
M1+E2
M2+E3
E1+M2
E2+M3
D(+Q)
Q(+O)
O(+H) (rare)
M1(+E2)
E1(+M2)
M2(+E3)
E2(+M3)


---

## Multipole Mixing Ratios

### Mixing Ratio Field (MR Field, Columns 42-49)

**Nuclear Physics Definition**: Multipole mixing ratios (δ) quantify the degree to which different angular momentum multipoles are mixed in a gamma-ray transition. They represent the amplitude ratio between different electromagnetic transition modes.

#### Physical Significance

- **δ = 0 or blank**: Pure transition (single multipolarity, e.g., pure E1)
- **δ ≠ 0**: Mixed transition (multiple multipolarities contributing)
- **δ(E2/M1)**: Ratio of electric quadrupole to magnetic dipole amplitudes
- **δ(M1/E2)**: Ratio of magnetic dipole to electric quadrupole amplitudes

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
