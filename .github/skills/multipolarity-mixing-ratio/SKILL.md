---
name: multipolarity-mixing-ratio
description: >
  Use this skill as a reference guide for ENSDF multipolarity (M) and mixing ratio (MR)
  field notation. Suitable for writing or reviewing G-record multipolarity and mixing
  ratio fields.
argument-hint: [multipolarity (M) and mixing ratio (MR) of gamma (G-record)]
---

# ENSDF Multipolarity and Mixing Ratio Reference

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Multipolarity Field (M Field, Columns 33-41)

**ENSDF Shorthand Notation**: The multipolarity field uses standard abbreviations for electromagnetic transition types.

### Multipolarity Field Notation

- Comma `,` = OR (alternative multipolarities)
- Plus `+` = AND (mixed multipolarity)
- Parentheses `()` = tentative multipolarity
- Square brackets `[]` = tentative multipolarity inferred purely from level scheme spin-parity changes

#### Single Multipolarities

- E1
- E2
- E3
- E4
- M1
- M2
- M3
- M4
- D (Dipole, L=1): E1 or M1
- Q (Quadrupole, L=2): E2 or M2
- O (Octupole, L=3): E3 or M3
- H (Hexadecapole, L=4): E4 or M4

#### Mixed Multipolarities

- D+Q
- Q+O
- O+H (rare)
- M1+E2
- M2+E3
- E1+M2
- E2+M3
- D(+Q)
- Q(+O)
- O(+H) (rare)
- M1(+E2)
- E1(+M2)
- M2(+E3)
- E2(+M3)

---

## Multipole Mixing Ratios

### Mixing Ratio Field (MR Field, Columns 42-49)

**Nuclear Physics Definition**: Multipole mixing ratios (δ) quantify the degree to which different angular momentum multipoles are mixed in a gamma-ray transition. They represent the amplitude ratio between different electromagnetic transition modes. δ is generally defined as the ratio of the reduced transition matrix element of the higher multipole (L+1) to that of the lower multipole (L).

#### Physical Significance

- **δ = 0**: Pure transition (single multipolarity, e.g., pure E1); the MR field is blank.
- **δ > 0 or δ < 0**: Mixed transition (higher multipolarities contributing).
- **δ compatible with 0**: Lower-order transition dominant, with small or negligible contributions from higher-order multipoles. The corresponding M field should reflect the dominant multipolarity and the small / negligible higher multipolarity should be put in parentheses. e.g., `M1(+E2)` or `E1(+M2)`.

### Mixing Ratio Uncertainties (DMR Field, Columns 50-55)

#### Symmetric Uncertainties (1-2 Digits)

#### Asymmetric Uncertainties (+X-Y Format)

- **Format**: `+X-Y` notation, left-justified in a 6-character field.

#### Special DMR Field Cases

- **Limit measurements**: Use `GT`/`LT` when the MR field has a lower/upper limit.

### Formatting Rules for Mixing Ratios

- **Always include sign** in the MR field (+ or -), except for MR=0.0.
