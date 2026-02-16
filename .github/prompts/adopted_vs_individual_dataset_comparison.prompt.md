# Adopted vs Individual Dataset Comparison

## Purpose

Systematically verify that quantities in Adopted datasets match their source individual reaction datasets. Detect discrepancies between Adopted values and the experimental measurements that inform them.

**Scope:**
- **Checks:** J-π assignments, energies, half-lives, branching ratios, or other physical quantities
- **Method:** Character-by-character string matching (not numerical tolerance)
- **Output:** Tabular mismatch report with error categorization
- **Validation:** CHECK-ONLY mode — report findings without editing files

---

## Prerequisites

- Understanding of ENSDF cross-reference (XREF) notation
- Access to both Adopted and individual reaction dataset files
- Python 3.8+ for automated comparison scripts (optional)

---

## ENSDF Cross-Reference (XREF) System

### XREF Notation

XREF lines identify which datasets observe a given level:

```
 58MNX L XREF=ABDF
```

**Interpretation:**
- Dataset A observes this level
- Dataset B observes this level
- Dataset D observes this level
- Dataset F observes this level

### Dataset Identifier Mapping

Each mass chain defines dataset identifiers in the header:

```
 58MN  XA58CR B- DECAY (7.0 S)
 58MN  XB58MN IT DECAY (65.4 S)
 58MN  XC48CA(13C,2NPG)
 58MN  XD58FE(T,3HE)
 58MN  XE238U(70ZN,XG)
 58MN  XF13C(48CA,P2NG),14C(48CA,P3NG)
```

**Key identifier:** First character after `X` (e.g., `XD` → identifier `D`)

---

## Comparison Methodology

### Step 1: Identify Levels from Target Dataset

Extract all levels from Adopted with XREF containing target identifier:

```
 58MN  L 183       10  1+
 58MNX L XREF=D
```

**Target dataset:** D (58FE(T,3HE))  
**Adopted energy:** 183 keV  
**Adopted J-π:** 1+

### Step 2: Match Levels by Energy

Find corresponding level in individual dataset:

**Matching tolerance:**
- Primary: Exact energy string match preferred
- Fallback: Within 20 keV for ambiguous cases
- Note energy differences in report

### Step 3: Compare Quantities Character-by-Character

**Critical:** Use exact string matching, not numerical equivalence.

**Example mismatches:**
- `1+` ≠ `(1+)` (parentheses indicate tentative assignment)
- `4+` ≠ `(4)+` (different uncertainty encoding)
- `3+,4+` ≠ `(3,4)+` (comma placement and parentheses)
- `1991.27` ≠ `1991.3` (decimal place mismatch)

---

## J-π Assignment Conventions

### Parentheses Encoding

| Notation | Meaning | Physical Interpretation |
|:---------|:--------|:------------------------|
| `1+` | Definite J and π | Firmly established |
| `(1+)` | Tentative J and π | Both uncertain |
| `1(+)` | Definite J, tentative π | J known, π uncertain |
| `(1)+` | Tentative J, definite π | J uncertain, π known |
| `(1,2)+` | Multiple possible J values | Common parity, uncertain J |
| `1+,2+` | Alternative assignments | Comma separates distinct options |

### Comparison Rules

**Exact match required:** Every character including spaces, parentheses, commas, signs.

**Common errors:**
- Treating `4+` and `(4)+` as equivalent (they are not)
- Ignoring comma placement: `3+,4+` ≠ `(3,4)+`
- Decimal precision: `1991` ≠ `1991.27`

---

## Error Classification

| Code | Severity | Description |
|:-----|:---------|:------------|
| `EXACT_MATCH` | INFO | Quantities match character-for-character |
| `PARENTHESES_MISMATCH` | ERROR | Tentative/definite encoding differs (e.g., `4+` vs `(4)+`) |
| `FORMAT_MISMATCH` | ERROR | Notation style differs (e.g., `3+,4+` vs `(3,4)+`) |
| `VALUE_MISMATCH` | ERROR | Numerical or textual content differs |
| `MISSING_IN_ADOPTED` | ERROR | Individual dataset has value, Adopted blank |
| `MISSING_IN_INDIVIDUAL` | ERROR | Adopted has value, individual dataset blank |
| `ENERGY_MISMATCH` | WARNING | Level energy differs between datasets |

---

## Workflow

### Step 1: Identify Comparison Target

Determine which dataset to verify against:

```bash
# List XREF identifiers from Adopted file header
grep "^.....X[A-Z]" Mn58_adopted.ens
```

**Example output:**
```
 58MN  XD58FE(T,3HE)
```

**Target:** Dataset D

### Step 2: Extract Levels with Target XREF

Scan Adopted file for levels with XREF containing target identifier:

**Pattern:**
```
 58MN  L [energy] [J-π]
 58MNX L XREF=[contains D]
```

**Record:** Energy and J-π from Adopted

### Step 3: Extract Corresponding Levels from Individual Dataset

Open individual reaction dataset (e.g., `Mn58_58fe_t_3he.ens`):

**Pattern:**
```
 58MN  L [energy] [J-π]
```

**Match by energy:** Find closest match within 20 keV tolerance

### Step 4: Character-by-Character Comparison

Compare extracted quantities:

```python
# Pseudocode
if adopted_value == individual_value:
    status = "EXACT_MATCH"
else:
    status = classify_error_type(adopted_value, individual_value)
```

### Step 5: Generate Report

**Required columns:**
- Energy (Adopted)
- Energy (Individual)
- Value (Adopted)
- Value (Individual)
- Match status
- Error type
- Notes

**Format:** Markdown table or CSV for post-processing

### Step 6: Categorize and Summarize

Calculate statistics:
- Total levels compared
- Exact matches (count and percentage)
- Mismatches (count and percentage)
- Error type distribution

---

## Output Format

### Comparison Table

| E_Adopted | E_Individual | Value_Adopted | Value_Individual | Match? | Error Type | Notes |
|:----------|:-------------|:--------------|:-----------------|:------:|:-----------|:------|
| 183 | 183 | 1+ | 1+ | ✓ | — | — |
| 1470 | 1470 | (4)+ | 4+ | ✗ | PARENTHESES_MISMATCH | Tentative vs definite |
| 2259 | 2259 | (3,4)+ | 3+,4+ | ✗ | FORMAT_MISMATCH | Notational style differs |

### Summary Statistics

```
Total levels: 27
Exact matches: 20 (74%)
Mismatches: 7 (26%)

Error type distribution:
  PARENTHESES_MISMATCH: 2
  FORMAT_MISMATCH: 5
```

---

## Common Pitfalls

1. **Numerical tolerance matching:** Do not accept "close enough" values — require exact string match
2. **Ignoring parentheses:** `4+` ≠ `(4)+` encodes different physical meaning (definite vs tentative)
3. **Energy window too wide:** 20 keV tolerance for matching levels, but flag if difference >5 keV
4. **Assuming equivalence:** `3+,4+` and `(3,4)+` are different notations with distinct interpretations
5. **Decimal precision:** `1991` ≠ `1991.27` even if numerically close
6. **XREF interpretation:** `XREF=AD(303)` means datasets A and D observe this level (303 indicates energy in dataset D)
7. **Missing systematic check:** Verify all XREF=D levels, not just subset

---

## Success Criteria

- All levels with target XREF identifier extracted from Adopted
- All corresponding levels found in individual dataset (energy matching)
- Character-by-character comparison performed for each level
- Mismatches categorized by error type
- Summary statistics calculated
- Findings documented in scannable table format
- Zero assumptions or guesses — all data verified from source files

---

## Example: J-π Comparison for 58Mn

**Target:** Verify Adopted J-π against 58FE(T,3HE) dataset (XREF=D)

**Command:**
```bash
# Manual comparison or automated script
python compare_jpi.py Mn58_adopted.ens Mn58_58fe_t_3he.ens --xref=D
```

**Output:**
- 27 levels with XREF=D identified
- 20 exact matches (74%)
- 7 mismatches (26%):
  - 2 parentheses encoding differences
  - 5 notational format differences

**Action:** Report findings to evaluator for review

---

## Extensions

### Other Quantities

This workflow applies to any quantity comparison:

**Energy:**
- Adopted E vs Individual E
- Tolerance: Exact string match preferred
- Flag if difference >1 keV

**Half-life:**
- Adopted T₁/₂ vs Individual T₁/₂
- Include units (PS, NS, S, etc.)
- Compare uncertainty notation

**Branching ratios:**
- Adopted %β⁻ vs Individual %β⁻
- Compare normalization conventions
- Check consistency with other branches

**Multipolarity:**
- Adopted M vs Individual M
- Parentheses encode tentative assignments
- Brackets encode unresolved multiplets

### Automated Scripting

**Template:**
```python
#!/usr/bin/env python3
"""Compare quantities between Adopted and individual datasets."""

import sys

def extract_levels(filename, xref_filter=None):
    """Extract levels with optional XREF filtering."""
    levels = []
    # Parser implementation
    return levels

def match_by_energy(adopted_levels, individual_levels, tolerance=20):
    """Match levels by energy proximity."""
    matches = []
    # Matching logic
    return matches

def compare_quantities(adopted_value, individual_value):
    """Character-by-character comparison."""
    if adopted_value == individual_value:
        return "EXACT_MATCH", None
    else:
        return classify_error(adopted_value, individual_value)

def classify_error(val1, val2):
    """Categorize mismatch type."""
    # Error classification logic
    pass

if __name__ == "__main__":
    adopted_file = sys.argv[1]
    individual_file = sys.argv[2]
    xref_id = sys.argv[3]
    
    # Extract, match, compare, report
```

---

## Document Structure

This document contains 11 main sections:

1. **Purpose** — Verify Adopted quantities against source individual datasets
2. **Prerequisites** — XREF knowledge, file access, Python tools
3. **ENSDF Cross-Reference System** — XREF notation and dataset identifier mapping
4. **Comparison Methodology** — 3-step process (identify, match, compare)
5. **J-π Assignment Conventions** — Parentheses encoding, comparison rules
6. **Error Classification** — 7 error types with severity levels
7. **Workflow** — 6-step process from identification to report generation
8. **Output Format** — Comparison table and summary statistics
9. **Common Pitfalls** — 7 frequent errors to avoid
10. **Success Criteria** — Requirements for complete verification
11. **Extensions** — Other quantities, automated scripting templates
