---
name: lifetime-comments-standardization
description: >
  Use this skill when writing or editing cL T$ lifetime comments in ENSDF
  files. Covers individual datasets using (NSR, METHOD) format and adopted
  datasets using "in REACTION from NSR with METHOD" format. Handles single
  values, weighted averages, lower/upper limits, and mixed value+limit
  patterns. Applies Oxford comma, chronological NSR ordering, {IUNC}
  uncertainty notation with limit 99 for full precision.
argument-hint: [ENSDF file or level energy]
---

# ENSDF Lifetime Comments Standardization

## Purpose
Standardize T$ (lifetime) comment lines for clarity and numerical rigor. Maintain a single-line format for external wrapping.

**KEY DISTINCTION:** Individual datasets use `(NSR, METHOD)` | Adopted datasets use `in REACTION from NSR with METHOD`

---

## Individual Dataset Comments

### Single Value
**Format:** `T$lifetime |t=VALUE UNIT {IUNC} (NSR, METHOD).`  
**Example:** `T$lifetime |t=115 fs {I35} (1973Ca15, DSAM).`

### Two Values
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2).`  
**Example:** `T$lifetime |t=0.28 ps {I4}: weighted average of 0.29 ps {I4} (1973Wa10, DSAM) and 0.27 ps {I5} (1969In04, DSAM).`

### Three or More Values
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).`  
**Example:** `T$lifetime |t=0.172 ps {I20}: weighted average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 0.080 ps {I40} (1971Wi13, RDM).`

### Single Limit
**Format:** `T$lifetime |t>VALUE UNIT (NSR, METHOD).`  
**Example:** `T$lifetime |t>2 ps (1973Ca15, DSAM).`

### Two Limits
**Format:** `T$lifetime |t>VALUE UNIT: >VALUE1 UNIT (NSR1, METHOD1). Other: >VALUE2 UNIT (NSR2, METHOD2).`  
**Example:** `T$lifetime |t>3 ps: >3.5 ps (1970Br10, DSAM). Other: >2.8 ps (1968An02, DSAM).`

### Mixed Value and Limit
**Format:** `T$lifetime |t=VALUE UNIT {IUNC} (NSR1, METHOD1). Other: >VALUE2 UNIT (NSR2, METHOD2).`  
**Example:** `T$lifetime |t=22 ps {I4} (1971Ba98, RDM). Other: >14 ps (1970Br10, DSAM).`

### Three or More Mixed
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2). Others: >VALUE3 UNIT (NSR3, METHOD3) and >VALUE4 UNIT (NSR4, METHOD4).`  
**Example:** `T$lifetime |t=3.4 ps {I3}: weighted average of 3.3 ps {I5} (1973Wa10, DSAM) and 3.5 ps {I2} (2022Gr07, DRDM). Others: >1.8 ps (1970Bu18, DSAM) and >1.6 ps (1972Fr11, DSAM).`

---

## Adopted Dataset Comments

### Single Value
**Format:** `T$lifetime |t=VALUE UNIT {IUNC} in REACTION from NSR with METHOD.`  
**Example:** `T$lifetime |t=115 fs {I35} in {+34}S(d,p|g) from 1973Ca15 with DSAM.`

### Two Values
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1 and VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2.`  
**Example:** `T$lifetime |t=1.48 ns {I7}: weighted average of 1.7 ns {I3} in (d,p|g) from 2024Co04 with p|g-delayed coin and 1.47 ns {I7} in (d,p|g) from 1971Pr11 with p|g-delayed coin.`

### Three or More Values
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1, VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2, and VALUE3 UNIT {IUNC3} in REACTION3 from NSR3 with METHOD3.`  
**Example:** `T$lifetime |t=3.2 ps {I3}: weighted average of 3.3 ps {I5} in ({+34}S,p|g) from 1973Wa10 with DSAM, 3.1 ps {I4} in (d,p|g) from 1970Bu18 with DSAM, and 3.2 ps {I6} in (d,p|g) from 1972Fr11 with DSAM.`

### Single Limit
**Format:** `T$lifetime |t>VALUE UNIT in REACTION from NSR with METHOD.`  
**Example:** `T$lifetime |t>4.5 ps in (d,p|g) from 1970Bu18 with DSAM.`

### Two Limits
**Format:** `T$lifetime |t>VALUE UNIT: >VALUE1 UNIT in REACTION1 from NSR1 with METHOD1 and >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`  
**Example:** `T$lifetime |t>3 ps: >3.5 ps in (d,p|g) from 1970Bu18 with DSAM and >2.8 ps in ({+34}S,p|g) from 1968An02 with DSAM.`

### Mixed Value and Limit
**Format:** `T$lifetime |t=VALUE UNIT {IUNC} in REACTION1 from NSR1 with METHOD1. Other: >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`  
**Example:** `T$lifetime |t=3.3 ps {I2} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Other: >4.5 ps in (d,p|g) from 1970Bu18 with DSAM.`

### Three or More Mixed
**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1 and VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2. Others: >VALUE3 UNIT in REACTION3 from NSR3 with METHOD3 and >VALUE4 UNIT in REACTION4 from NSR4 with METHOD4.`  
**Example:** `T$lifetime |t=3.4 ps {I3}: weighted average of 3.3 ps {I5} in ({+34}S,p|g) from 1973Wa10 with DSAM and 3.5 ps {I2} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Others: >1.8 ps in (d,p|g) from 1970Bu18 with DSAM and >1.6 ps in (d,p|g) from 1972Fr11 with DSAM.`

---

## Standard Rules

### Formatting and Grammar
*   **Logical Single Line**: Comment content newly added by AI agent must be a complete single line ending with a period. The human evaluator will manually wrap long comments across ENSDF continuation records using VS Code's editor extension.
*   **No Manual Line Breaks**: Do NOT insert deliberate line breaks into the comment content itself.
*   **External Wrapping OK**: Comment lines wrapped across continuation records (e.g., `cL`, `2cL`, `3cL`) may already exist in the .ens file being edited, which are expected and normal.
*   **Oxford Comma**: Always include the final comma in lists of three or more items.
*   **Pluralization**: Use "Other:" for one item and "Others:" for multiple supporting items (limits or low-weight values).
*   **End Punctuation**: Every comment must end with a period.

### Numerical Rigor
*   **Preservation**: Do not round or alter values, uncertainties, or NSR keys.
*   **Notation**: Use `{IUNC}` for symmetric and `{I+n-m}` for asymmetric uncertainties.
*   **Unit Matching**: Convert component units to match the adopted result (e.g., if the adopted value is in ps, convert component fs values to ps).
*   **Limits**: Use `>` or `<` without parentheses or uncertainties.
*   **Uncertainty Format**: Lifetimes use uncertainty limit **99** (not default 35). This preserves full precision.

| Input | Standard (Limit 35) | Lifetime (Limit 99) |
| :--- | :--- | :--- |
| 197 ± 50 | `2.0E2 {I5}` (Scientific) | `197 fs {I50}` (Full precision) |

### Bibliographic Standards
*   **Chronology**: List measurements in chronological order by NSR year.
*   **Method Tags**: Use standard abbreviations (e.g., DSAM, RDM).

### CRITICAL: Scope of Standardization Task

**DO NOT MODIFY DATA DECISIONS - ONLY STANDARDIZE FORMAT**

*   **Averaging decisions are FINAL**: The evaluator has already decided which values to average and which to place in "Others:". DO NOT change these decisions during comment standardization.

*   **Your task**: Standardize the comment FORMAT only (e.g., fix "from lifetime=" to "lifetime |t=", add "in REACTION from NSR with METHOD" for Adopted datasets). Do NOT alter which measurements are averaged vs listed in "Others:", which is a data decision by the human evaluators.

### Half-Life vs Lifetime Terminology

**CRITICAL DISTINCTION for T$ comments:**

*   **Lifetime (τ)**: Mean lifetime of nuclear state (symbol: |t). Relation: τ = T₁/₂ / ln(2) ≈ 1.443 × T₁/₂
*   **Half-life (T₁/₂)**: Time for half of nuclei to decay (symbol: T{-1/2}). What goes in ENSDF T field.
*   **Rule for T$ comments**: Use "lifetime |t=" when referring to the lifetime value and omit "lifetime |t=" for half-life references.
