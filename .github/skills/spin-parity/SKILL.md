---
name: spin-parity
description: >
  Use this skill as a reference guide for ENSDF spin-parity (Jπ) notation
  rules. Covers L-transfer field positioning at column 56, J-π assignment
  confidence levels using parentheses, single/multiple/range spin
  assignments, and critical parentheses placement rules. Suitable for
  writing J-π values in L-records or J$ comment lines.
argument-hint: [spin-parity expression or L-record line]
---

# ENSDF Spin-Parity Interpretation Reference

## L-Transfer Field Positioning

### L-Transfer Field Positioning Rule

- L always starts from column 56 (EXACT rule for L transferred angular momentum fields)
- `L=1` → `1` at column 56
- `L=1+2` → `1` at column 56, `+2` at columns 57-58
- `L=1,2` → `1` at column 56, `,2` at columns 57-58
- ONLY the first L-value must be at column 56; subsequent values follow sequentially

### L-Transfer from 0+ for J-π Assignment Rules

Physics mapping (single-nucleon transfer from a 0+ even-even target):
- j = L ± 1/2
- π = (−1)^L

L-Transfer values and corresponding J-π assignments:
- L=0 → J-π: `1/2+`
- L=1 → J-π: `1/2-,3/2-`
- L=2 → J-π: `3/2+,5/2+`
- L=3 → J-π: `5/2-,7/2-`
- L=4 → J-π: `7/2+,9/2+`

---

## J-π Assignment Notation

### Fundamental Rule

**CRITICAL**: J = spin; π = parity

- **WITHOUT parentheses**: Firm, well-established assignments (e.g., `3/2+`, `7/2-`, `0+`, `5-`)
- **WITH parentheses**: Less certain, tentative assignments (e.g., `(3/2+)`, `(7/2)-`, `0(+)`, `(5-)`)
- **Parentheses indicate uncertainty in the assignment confidence, not the measurement precision**
- **With/without parentheses and the placement of parentheses are critical for conveying the confidence level of the assignment**



#### Basic Single Assignments

| Notation | Spin | Parity | Other Spin? | Other Parity? | Expands To |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1/2-` | Firm | Firm | Impossible | Impossible | — |
| `(9/2+)` | Tentative | Tentative | Possible | Possible | — |
| `7/2(+)` | Firm | Tentative | Impossible | Possible | — |
| `(5/2)-` | Tentative | Firm | Possible | Impossible | — |
| `(11/2)` | Tentative | Unknown | Possible | Possible | — |
| `+` | Unknown | Firm | Possible | Impossible | — |
| `(+)` | Unknown | Tentative | Possible | Possible | — |

#### Multiple Spin Assignments

| Notation | Spin | Parity | Other Spin? | Other Parity? | Expands To |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1/2-,3/2-` | Firm | Firm | Impossible | Impossible | 1/2- or 3/2- |
| `(5/2+,7/2+)` | Tentative | Tentative | Possible | Possible | 5/2+ or 7/2+ or low-probability other Jπ |
| `(7/2,9/2)-` | Tentative | Firm | Possible | Impossible | 7/2- or 9/2- or low-probability other J- |
| `1/2,3/2(+)` | Firm | Tentative | Impossible | Possible | 1/2± or 3/2+ or low-probability 3/2- |
| `(1/2,3/2,5/2)-` | Tentative | Firm | Possible | Impossible | 1/2- or 3/2- or 5/2- or low-probability other J- |
| `(3/2,5/2,7/2+)` | Tentative | Mixed | Possible | Possible | 3/2± or 5/2± or 7/2+ or low-probability other Jπ |

#### Range Assignments

**Range Parity Rules**:
- `A:B+` or `A:B-` — parity applies ONLY to endpoint B; intermediate values have ±
- `(A:B)+` or `(A:B)-` — parity applies to ALL values A through B
- `A:B(+)` or `A:B(-)` — tentative parity applies ONLY to endpoint B

**Column Definitions**:
- **Other Spin?**: Whether spin values beyond those explicitly shown in the expansion are possible
- **Other Parity?**: Whether parity values beyond those explicitly shown in the expansion are possible (note: ± notation counts as showing both parities)

| Notation | Spin | Parity | Other Spin? | Other Parity? | Expands To |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1/2:7/2` | Firm | Unknown | Impossible | Possible | 1/2± or 3/2± or 5/2± or 7/2± |
| `(1/2:7/2)` | Tentative | Unknown | Possible | Possible | 1/2± or 3/2± or 5/2± or 7/2± or low-probability other Jπ |
| `1/2+:7/2+` | Firm | Mixed | Impossible | Impossible | 1/2+ or 3/2± or 5/2± or 7/2+ |
| `1/2-:7/2+` | Firm | Mixed | Impossible | Impossible | 1/2- or 3/2± or 5/2± or 7/2+ |
| `1/2:7/2+` | Firm | Mixed | Impossible | Impossible | 1/2± or 3/2± or 5/2± or 7/2+ |
| `1/2+:7/2` | Firm | Mixed | Impossible | Impossible | 1/2+ or 3/2± or 5/2± or 7/2± |
| `(1/2+:7/2+)` | Tentative | Mixed | Possible | Possible | 1/2+ or 3/2± or 5/2± or 7/2+ or low-probability other Jπ |
| `1/2(+):7/2(+)` | Firm | Tentative | Impossible | Possible | 1/2+ or 3/2± or 5/2± or 7/2+ or low-probability 1/2-, 7/2- |
| `(1/2:7/2+)` | Tentative | Mixed | Possible | Possible | 1/2± or 3/2± or 5/2± or 7/2+ or low-probability other Jπ |
| `(1/2+:7/2)` | Tentative | Mixed | Possible | Possible | 1/2+ or 3/2± or 5/2± or 7/2± or low-probability other Jπ |
| `1/2:7/2(+)` | Firm | Tentative | Impossible | Possible | 1/2± or 3/2± or 5/2± or 7/2+ or low-probability 7/2- |
| `(1/2:7/2)+` | Tentative | Firm | Possible | Impossible | 1/2+ or 3/2+ or 5/2+ or 7/2+ or low-probability other J+ |
| `(1/2:7/2)(+)` | Tentative | Tentative | Possible | Possible | 1/2+ or 3/2+ or 5/2+ or 7/2+ or low-probability other Jπ |
| `1/2(+),3/2(+),5/2(+),7/2(+)` | Firm | Tentative | Impossible | Possible | 1/2+ or 3/2+ or 5/2+ or 7/2+ or low-probability other 1/2-, 3/2-, 5/2-, 7/2- |

*Note: The last entry is too long for the J field (cols 23-39) and should be placed in the 2 L continuation record.*



#### Mixed Confidence Patterns

| Notation | Spin | Parity | Other Spin? | Other Parity? | Expands To |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1/2+,3/2-` | Firm | Firm | Impossible | Impossible | 1/2+ or 3/2- |
| `3/2-,(5/2-)` | Mixed | Firm | Mixed | Impossible | 3/2- or (5/2-) |
| `(7/2)+,9/2+` | Mixed | Mixed | Mixed | Mixed | (7/2)+ or 9/2+ |
| `1/2(+),3/2-` | Firm | Mixed | Mixed | Mixed | 1/2(+) or 3/2- or low-probability 1/2- |
| `(5/2+,7/2-)` | Tentative | Tentative | Possible | Possible | 5/2+ or 7/2- or low-probability other Jπ |
| `3/2,5/2,7/2` | Firm | Unknown | Impossible | Possible | 3/2± or 5/2± or 7/2± |
| `(1/2,3/2,5/2)` | Tentative | Unknown | Possible | Possible | 1/2± or 3/2± or 5/2± or low-probability other Jπ |

### Critical Formatting Rules

- **Comma separation** for multiple possibilities within same confidence level
- **Parentheses apply to the entire group** when wrapping multiple values
- **Do not include explicit parity on an item inside a grouped tentative list**; if a subset has a different parity or confidence, split it out of the group
- **Mixed notation is allowed** by splitting: e.g., `1/2,3/2,5/2+` (first two tentative, parity unspecified; last firm positive)
- **No spaces** around commas in J-π field
- **Exact reproduction required** — never modify parentheses placement without experimental justification

### Critical Parentheses Matching Rule

Spin-parity with/without parentheses convey different confidence levels. When creating J$ comments or adding values to J fields from reference data sources, ensure parentheses are preserved exactly as written in the source:

- **Source shows `3/2`** → Comment: `J$3/2 from [reference]` (NO parentheses)
- **Source shows `(3/2)`** → Comment: `J$(3/2) from [reference]` (single parentheses preserved)
- **NEVER use double parentheses**: `J$((3/2))` is FORBIDDEN
- **Examples**: `(1/2+)`, `1/2(+)`, `1/2+` represent different assignment confidence levels and the placement of parentheses must be matched accurately and precisely!

### Additional Notation

Ranges: `1/2:7/2` expands to 1/2, 3/2, 5/2, 7/2.
Lists: `3/2, 5/2` expands to set of both.
Parity Inheritance: `(1/2, 3/2)+` applies + parity to both inner items, i.e., `(1/2)+`, `(3/2)+`.
Loose Matching: Parentheses () indicate tentative values.
