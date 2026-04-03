---
name: lifetime-comments-standardization
description: >
  Standardize cL T$ lifetime comments in ENSDF files. Use (NSR, METHOD) format for individual datasets 
  and "in REACTION from NSR with METHOD" for adopted datasets. Handles single values, weighted averages, 
  limits, and mixed patterns. Applies Oxford comma, chronological ordering, {IUNC} uncertainty (limit 99 
  for lifetime full precision).
argument-hint: "[list of lifetimes, uncertainties, NSR keys, and methods]"
---

# ENSDF Lifetime Comments Standardization

## Purpose
Extract lifetime data from .mrg raw data files or
standardize existing T$ (lifetime) comment structure in cL lines of an .ens file.
List all available data with proper formatting; do not perform averaging or calculations.

**Key Distinction:**

- **Individual datasets:** `(NSR, METHOD)` format
- **Adopted datasets:** `in REACTION from NSR with METHOD` format

---

## Individual Dataset Comments

Each subsection shows the template (uppercase placeholders) followed by a concrete example.

### Single Value
`T$lifetime |t=VALUE UNIT {IUNC} (NSR, METHOD).`
`T$lifetime |t=a fs {Ib} (1973Ca15, DSAM).`

### Two Values
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2).`
`T$lifetime |t=a ps {Ib}: weighted average of 0.29 ps {I4} (1973Wa10, DSAM) and 0.27 ps {I5} (1969In04, DSAM).`

### Three or More Values
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).`
`T$lifetime |t=a ps {Ib}: weighted average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 0.080 ps {I40} (1971Wi13, RDM).`

### Single Limit
`T$lifetime |t>VALUE UNIT (NSR, METHOD).`
`T$lifetime |t>a ps (1973Ca15, DSAM).`

### Two Limits
`T$lifetime |t>VALUE1 UNIT (NSR1, METHOD1). Other: >VALUE2 UNIT (NSR2, METHOD2).`
`T$lifetime |t>a ps (1970Br10, DSAM). Other: >2.8 ps (1968An02, DSAM).`

### Mixed Value and Limit
`T$lifetime |t=VALUE UNIT {IUNC} (NSR1, METHOD1). Other: >VALUE2 UNIT (NSR2, METHOD2).`
`T$lifetime |t=a ps {Ib} (1971Ba98, RDM). Other: >14 ps (1970Br10, DSAM).`

### Three or More Mixed
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2). Others: >VALUE3 UNIT (NSR3, METHOD3) and >VALUE4 UNIT (NSR4, METHOD4).`
`T$lifetime |t=a ps {Ib}: weighted average of 3.3 ps {I5} (1973Wa10, DSAM) and 3.5 ps {I2} (2022Gr07, DRDM). Others: >1.8 ps (1970Bu18, DSAM) and >1.6 ps (1972Fr11, DSAM).`

---

## Adopted Dataset Comments

### Single Value
`T$lifetime |t=VALUE UNIT {IUNC} in REACTION from NSR with METHOD.`
`T$lifetime |t=a fs {Ib} in {+34}S(d,p|g) from 1973Ca15 with DSAM.`

### Two Values
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1 and VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2.`
`T$lifetime |t=a ns {Ib}: weighted average of 1.7 ns {I3} in (d,p|g) from 2024Co04 with p|g-delayed coin and 1.47 ns {I7} in (d,p|g) from 1971Pr11 with p|g-delayed coin.`

### Three or More Values
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1, VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2, and VALUE3 UNIT {IUNC3} in REACTION3 from NSR3 with METHOD3.`
`T$lifetime |t=a ps {Ib}: weighted average of 3.3 ps {I5} in ({+34}S,p|g) from 1973Wa10 with DSAM, 3.1 ps {I4} in (d,p|g) from 1970Bu18 with DSAM, and 3.2 ps {I6} in (d,p|g) from 1972Fr11 with DSAM.`

### Single Limit
`T$lifetime |t>VALUE UNIT in REACTION from NSR with METHOD.`
`T$lifetime |t>a ps in (d,p|g) from 1970Bu18 with DSAM.`

### Single Limit with Others
Adopt the **strictest** limit (largest `>`, smallest `<`); move all others to "Others:". Limits cannot be averaged.

`T$lifetime |t>VALUE UNIT in REACTION from NSR with METHOD. Others: >VALUE1 UNIT in REACTION1 from NSR1 with METHOD1, ..., and >VALUEn UNIT in REACTIONn from NSRn with METHODn.`
`T$lifetime |t>a ps in {+32}S({+3}He,p|g) from 1973Ca15 with DSAM. Others: >1.0 ps in {+33}S(p,|g) from 1973An13 with DSAM, >400 fs in {+33}S(p,|g) from 1977Da02 with DSAM, and >1500 fs in {+33}S(p,|g) from 1985La16 with DSAM.`

### Two Limits
`T$lifetime |t>VALUE UNIT: >VALUE1 UNIT in REACTION1 from NSR1 with METHOD1 and >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`
`T$lifetime |t>a ps: >3.5 ps in (d,p|g) from 1970Bu18 with DSAM and >2.8 ps in ({+34}S,p|g) from 1968An02 with DSAM.`

### Mixed Value and Limit
`T$lifetime |t=VALUE UNIT {IUNC} in REACTION1 from NSR1 with METHOD1. Other: >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`
`T$lifetime |t=a ps {Ib} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Other: >4.5 ps in (d,p|g) from 1970Bu18 with DSAM.`

### Three or More Mixed
`T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1 and VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2. Others: >VALUE3 UNIT in REACTION3 from NSR3 with METHOD3 and >VALUE4 UNIT in REACTION4 from NSR4 with METHOD4.`
`T$lifetime |t=a ps {Ib}: weighted average of 3.3 ps {I5} in ({+34}S,p|g) from 1973Wa10 with DSAM and 3.5 ps {I2} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Others: >1.8 ps in (d,p|g) from 1970Bu18 with DSAM and >1.6 ps in (d,p|g) from 1972Fr11 with DSAM.`

> **Note:** "Others:" items may be limits or finite values (with {IUNC}), as determined by the human evaluators.

---

## Standard Rules

### Formatting and Grammar

- **Single line:** Each comment is a complete logical unit ending with a period. Continuation across cL/2cL/3cL records is the human evaluator's responsibility.
- **Oxford comma:** Required in lists of three or more items.
- **Pluralization:** "Other:" for one secondary item; "Others:" for multiple.

### Numerical Rigor

- **Preserve values:** Do not round or alter values, uncertainties, or NSR keys.
- **ENSDF notation:** Use `{IUNC}` for symmetric; `{I+n-m}` for asymmetric uncertainties.
- **Unit consistency:** Convert component units to match the adopted result (e.g., fs → ps).
- **Limits:** Use `>` or `<` without parentheses or uncertainties.
- **Lifetime uncertainty limit:** Use **99** (not default 35) for full precision.
- **Adopted average:** Do not derive adopted τ from the L-record T field (T₁/₂). The the final averaged value is a placeholder. Computing the average is handled by a separate skill. This skill focuses on formatting the available data into the standardized comment structure.

| Input | Standard (Limit 35) | Lifetime (Limit 99) |
|:---:|:---:|:---:|
| 197 ± 50 | `2.0E2 {I5}` | `197 fs {I50}` |

### Bibliographic Standards

- **Chronology:** Adopted datasets: list by dataset XREF alphabetically. Individual datasets: list chronologically by NSR key year.
- **Method tags:** Use standard abbreviations (DSAM, RDM, DRDM).

---

## Critical Rules

### Scope: cL T$ Comment Format Standardization Only

**Do NOT modify other lines or records in the data file.**

- **Averaging decisions are final:** Preserve the evaluator's decisions on which values to average and which to place in "Others:".
- **Format only:** Standardize syntax only (e.g., fix "from lifetime=" → "lifetime |t="; add "in REACTION from NSR with METHOD" for adopted datasets).

### Half-Life vs. Lifetime Terminology

- **Lifetime (τ):** Mean lifetime; symbol |t. Relation: τ = T₁/₂ / ln(2) ≈ 1.443 × T₁/₂.
- **Half-life (T₁/₂):** Time for half decay; goes in the ENSDF T field.
- **T$ comment rule:** Use "lifetime |t=" for τ values. Omit for T₁/₂ references.
- **No conversion:** Do not convert τ ↔ T₁/₂ unless explicitly instructed. If τ (weighted average) ≠ τ derived from the T field, do not reconcile — preserve both values as-is.
