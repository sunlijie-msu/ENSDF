---
name: average
description: >
  Use this skill when calculating weighted or unweighted averages for ENSDF
  nuclear data using Java_Average.py. Enforces exact transcription of the
  Suggested Adopted Result, minimum-uncertainty rule, and lifetime
  uncertainty limit 99. Suitable for adopting measured values from multiple
  publications.
argument-hint: [VALUE1 UNC1 VALUE2 UNC2 ...]
---

# ENSDF Averaging Rules

## CLI Tool

```bash
python .github/scripts/Java_Average.py VALUE1 UNC1 [VALUE2 UNC2 ...]
```

**Algorithm:** Replicates `AverageTool_22January2025.jar`.

## Workflow

1. **Collect Data**: Gather values and uncertainties from original papers.
2. **Execute**: `python .github/scripts/Java_Average.py 280 50 215 70 130 60 120 65`
3. **Adopt Result**: Use exact "Suggested Adopted Result" and uncertainty.
4. **Update File**: Apply to L-record and standardize cL comment.

## Data Selection Rules

### One Value Per Paper
Use one primary value per original publication. If multiple methods exist in one paper, select the most reliable result.

### Mixed Measurements and Limits
*   **Consistency**: If a measurement (e.g., 22 ps) is consistent with a limit (e.g., >14 ps), adopt the measurement. Move the limit to "Other:" in the comment list.
*   **Discrepancy**: If inconsistent (e.g., 10 ps vs. >14 ps), flag the discrepancy. Prioritize the most modern or high-precision study.
*   **Multiple Limits**: Adopt the most restrictive boundary (largest for `>`, smallest for `<`).

### Unit Normalization
*   **Threshold**: Java Average converts values >99 to the next unit (e.g., 101 fs → 0.101 ps).
*   **Matching**: Ensure all listed components in the comment match the unit of the adopted result for consistency.

## Java Output Rules (Zero Tolerance)

| Component | Action |
| :--- | :--- |
| **Adopted Result** | Use character-for-character; no rounding or adjustment. |
| **Uncertainty** | Use exactly as provided (applies minimum uncertainty rule). |
| **Method** | Use the suggested average (Weighted vs. Unweighted) explicitly. |

**FORBIDDEN**: Recalculating or modifying averages or substituting suggested uncertainties.

### Minimum Uncertainty Rule

**ENSDF-Specific Requirement**: The final adopted uncertainty must be greater than or equal to any individual input uncertainty.

**Rationale**: This rule ensures that averaging never artificially reduces systematic uncertainty below the best single measurement, and maintains conservative uncertainty estimates in nuclear data evaluation. The Java averaging tool automatically enforces this constraint.

- **Statistical average** < **minimum input uncertainty** → Adopted uncertainty = minimum input uncertainty
- **Statistical average** ≥ **minimum input uncertainty** → Adopted uncertainty = statistical average

**Example**: Averaging 665.56±0.05 and 665.6±0.1 yields statistical uncertainty 0.0447, but the adopted uncertainty becomes 0.05 (matching the smallest input uncertainty).


## Lifetime Uncertainty Format
Lifetimes use uncertainty limit **99** (not default 35).

| Input | Standard (Limit 35) | Lifetime (Limit 99) |
| :--- | :--- | :--- |
| 197 ± 50 | `2.0E2 {I5}` (Scientific) | `197 fs {I50}` (Full precision) |


**Rationale:** Full precision preserves information; scientific notation loses it.
