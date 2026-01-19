# ENSDF Lifetime Comments Standardization

## Purpose
Standardize T$ (lifetime) comment lines for clarity and numerical rigor. Maintain a single-line format for external wrapping.

## Comment Formats

**All T$ comments use this structure: `T$lifetime |t=...` (no "from")**

### Single Measurement
`T$lifetime |t=VALUE UNIT {IUNC} (NSR, METHOD).`

### Two Measurements
`T$lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2).`

### Three or More Measurements
`T$lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).`

### Mixed Measurements and Limits
`T$lifetime |t=ADOPTED UNIT {IUNC} (NSR1, METHOD1). Other: LIMIT UNIT (NSR2, METHOD2).`

## Standard Rules

### Formatting and Grammar
*   **Logical Single Line**: Comment content newly added by AI agent must be a complete single thought ending with a period. The human evaluator will manually wrap long comments across ENSDF continuation records using VS Code's editor extension.
*   **No Manual Line Breaks**: Do NOT insert deliberate line breaks into the comment content itself.
*   **External Wrapping OK**: Comment lines wrapped across continuation records (e.g., `cL`, `2cL`, `3cL`) may already exist in the .ens file being edited, which are expected and correct.
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

## Examples
*   **Single (fs)**: `T$lifetime |t=115 fs {I35} (1973Ca15, DSAM).`
*   **Single limit**: `T$lifetime |t>2 ps (1973Ca15, DSAM).`
*   **Asymmetric**: `T$lifetime |t=1.3 ps {I+17-6} (1973Ca15, DSAM).`
*   **Mixed**: `T$lifetime |t=22 ps {I4} (1971Ba98, RDM). Other: >14 ps (1970Br10, DSAM).`
*   **Three Values**: `T$lifetime |t=0.172 ps {I20}: weighted average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 0.080 ps {I40} (1971Wi13, RDM).`
*   **Multiple Others**: `T$lifetime |t=4.5 ps {I5} (2021Vi01). Others: >3 ps (1970Br10) and 4.2 ps {I10} (1968An02).`
