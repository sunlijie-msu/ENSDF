---
name: lifetime-comments-standardization
description: >
  Standardize cL T$ lifetime comments in ENSDF files. Use (NSR, METHOD) format for individual datasets 
  and "in REACTION from NSR with METHOD" for adopted datasets. Handles single values, weighted averages, 
  limits, and mixed patterns. Applies Oxford comma, chronological ordering, {IUNC} uncertainty (limit 99 
  for lifetime full precision).
argument-hint: "[list of values, uncertainties, NSR keys, and methods]"
---

# ENSDF Lifetime Comments Standardization

## Purpose

Standardize T$ (lifetime) comment structure in cL lines for clarity and consistency.

**Key Distinction:**
- **Individual datasets:** `(NSR, METHOD)` format
- **Adopted datasets:** `in REACTION from NSR with METHOD` format

------

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

**Format:** `T$lifetime |t>VALUE1 UNIT (NSR1, METHOD1). Other: >VALUE2 UNIT (NSR2, METHOD2).`

**Example:** `T$lifetime |t>3.5 ps (1970Br10, DSAM). Other: >2.8 ps (1968An02, DSAM).`

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

### Single Limit with Others

**Rule:** When only limits are available, adopt the **strictest** limit (largest for `>`, smallest for `<`) as the adopted value, and move the other limits to "Other:". Limits cannot join for averaging.

**Format:** `T$lifetime |t>VALUE UNIT in REACTION from NSR with METHOD. Others: >VALUE1 UNIT in REACTION1 from NSR1 with METHOD1, >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2, and >VALUE3 UNIT in REACTION3 from NSR3 with METHOD3.`

**Example:** >2 ps (1973Ca15), >1.5 ps (1985La16), >0.4 ps (1977Da02), >1 ps (1973An13) — adopt >2 ps (strictest).

`T$lifetime |t>2 ps in {+32}S({+3}He,p|g) from 1973Ca15 with DSAM. Others: >1.0 ps in {+33}S(p,|g) from 1973An13 with DSAM, >400 fs in {+33}S(p,|g) from 1977Da02 with DSAM, and >1500 fs in {+33}S(p,|g) from 1985La16 with DSAM.`

### Two Limits

**Format:** `T$lifetime |t>VALUE UNIT: >VALUE1 UNIT in REACTION1 from NSR1 with METHOD1 and >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`

**Example:** `T$lifetime |t>3 ps: >3.5 ps in (d,p|g) from 1970Bu18 with DSAM and >2.8 ps in ({+34}S,p|g) from 1968An02 with DSAM.`

### Mixed Value and Limit

**Format:** `T$lifetime |t=VALUE UNIT {IUNC} in REACTION1 from NSR1 with METHOD1. Other: >VALUE2 UNIT in REACTION2 from NSR2 with METHOD2.`

**Example:** `T$lifetime |t=3.3 ps {I2} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Other: >4.5 ps in (d,p|g) from 1970Bu18 with DSAM.`

### Three or More Mixed

**Format:** `T$lifetime |t=ADOPTED UNIT {IUNC}: weighted average of VALUE1 UNIT {IUNC1} in REACTION1 from NSR1 with METHOD1 and VALUE2 UNIT {IUNC2} in REACTION2 from NSR2 with METHOD2. Others: >VALUE3 UNIT in REACTION3 from NSR3 with METHOD3 and >VALUE4 UNIT in REACTION4 from NSR4 with METHOD4.`

**Example:** `T$lifetime |t=3.4 ps {I3}: weighted average of 3.3 ps {I5} in ({+34}S,p|g) from 1973Wa10 with DSAM and 3.5 ps {I2} in {+208}Pb({+36}S,{+35}S|g) from 2022Gr07 with DRDM. Others: >1.8 ps in (d,p|g) from 1970Bu18 with DSAM and >1.6 ps in (d,p|g) from 1972Fr11 with DSAM.`

> **Note:** "Others:" items may be limits or finite values (with {IUNC}), specified by the human evaluators.



---

## Standard Rules

### Formatting and Grammar

-   **Single line format:** New comments must be a logically complete single line ending with a period. Manual wrapping across continuation records (cL, 2cL, 3cL) is the human evaluator's responsibility.
-   **No manual breaks:** Do not insert breaks within comment content.
-   **Oxford comma:** Include final comma in lists of three or more items.
-   **Pluralization:** Use "Other:" for one item; "Others:" for multiple.
-   **End punctuation:** Every comment ends with a period.

### Numerical Rigor

-   **Preserve values:** Do not round or alter values, uncertainties, or NSR keys.
-   **ENSDF Comment Notation:** Use {IUNC} for symmetric; {I+n-m} for asymmetric uncertainties.
-   **Unit consistency:** Convert component units to match the adopted result (e.g., fs to ps if adopting ps).
-   **Limits:** Use `>` or `<` without parentheses or uncertainties.
-   **Lifetime uncertainty limit:** Use **99** (not default 35) for full precision.
-   **Adopted average is a placeholder:** Do not derive adopted τ from the L-record T field (T₁/₂). Compute weighted average for the adopted τ is in a separate Skill, and not part of this comment standardization task.

| Input | Standard (Limit 35) | Lifetime (Limit 99) |
|:---:|:---:|:---:|
| 197 ± 50 | `2.0E2 {I5}` | `197 fs {I50}` |

### Bibliographic Standards

-   **Chronology:** In the Adopted datasets: list measurements by dataset XREF alphabetically. In individual datasets: list by the Year in NSR keynumber chronologically.
-   **Method tags:** Use standard abbreviations (e.g., DSAM, RDM, DRDM).

---

## Critical Rules

### Scope: cL T$ Comment Format Standardization Only.
**Do NOT modify other lines or records in the data file.**

-   **Averaging decisions are final:** The evaluator has already decided which values to average and which to place in "Others:". Preserve these decisions.
-   **Your task:** Standardize FORMAT only (e.g., fix "from lifetime=" to "lifetime |t=", add "in REACTION from NSR with METHOD" for adopted datasets).

### Half-Life vs Lifetime Terminology

**CRITICAL DISTINCTION for T$ comments:**

-   **Lifetime (τ):** Mean lifetime (symbol: |t). Relation: τ = T₁/₂ / ln(2) ≈ 1.443 × T₁/₂
-   **Half-life (T₁/₂):** Time for half decay. What goes in ENSDF T field.
-   **T$ comment rule:** Use "lifetime |t=" when referring to lifetime value. Omit for T₁/₂ references (T comment inherently indicates half-life).
-   **No τ ↔ T₁/₂ conversion:** Do not convert τ ↔ T₁/₂ unless explicitly instructed. If τ(weighted average) ≠ τ derived from the T field (T₁/₂), do not reconcile—preserve both values as-is.
