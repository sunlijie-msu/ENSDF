---
name: rounding
description: >
  Use this skill when applying rounding and uncertainty conventions in nuclear data evaluation.
argument-hint: [source.ens] [adopted.ens]
---

# Rounding and Uncertainty Conventions

**Context:** Nuclear physics data evaluation.
**Objective:** Standardize the successive rounding protocols for general calculated values and their associated uncertainties.

## 1. Core Methodology: Successive (Sequential) Rounding
All rounding operations must employ a **Successive Rounding** (step-wise) methodology.
*   **Directionality:** Process values digit-by-digit, starting from the rightmost decimal place and moving strictly leftward.
*   **Dependency:** Each rounding step depends on the immediate right-adjacent digit produced by the preceding step.

## 2. General Calculated Values: Standard Round Half-Up (5-Up)
Apply the 5-Up threshold convention for all general data values (excluding uncertainties).

| Action | Trigger Digits | Effect on Preceding (Left) Digit |
| :--- | :---: | :--- |
| **Round Down** | `0, 1, 2, 3, 4` | Truncated; preceding digit remains unchanged. |
| **Round Up** | `5, 6, 7, 8, 9` | Truncated; preceding digit increments by $+1$. |

### 2.1. Application Examples (General Values)
*   **$0.344 \rightarrow 0.3$** 
    *   *Step 1:* Rightmost `4` rounds down $\rightarrow 0.34$
    *   *Step 2:* Next `4` rounds down $\rightarrow 0.3$
*   **$0.345 \rightarrow 0.4$**
    *   *Step 1:* Rightmost `5` rounds up $\rightarrow 0.35$
    *   *Step 2:* New `5` rounds up $\rightarrow 0.4$

## 3. Uncertainty Values: Conservative Rounding (4-Up)
Apply a modified 4-Up threshold convention strictly for uncertainty digits. 

| Action | Trigger Digits | Effect on Preceding (Left) Digit |
| :--- | :---: | :--- |
| **Round Down** | `0, 1, 2, 3` | Truncated; preceding digit remains unchanged. |
| **Round Up** | `4, 5, 6, 7, 8, 9` | Truncated; preceding digit increments by $+1$. |

*   **Rationale:** Standard rounding can artificially deflate uncertainty. The 4-up rule acts as a conservative safeguard to prevent the overstatement of measurement precision.

### 3.1. Precision Alignment Rule
The final reported general value **must** be rounded to match the exact decimal place of the least significant digit of the rounded uncertainty.

### 3.2. Application Examples (Value + Uncertainty)
*   **$100.00(333) \rightarrow 100.0(33)$**
    *   Rightmost `3` in uncertainty rounds down. Uncertainty becomes `33`. Final value aligns to the tenths place.
*   **$100.00(334) \rightarrow 100.0(34)$**
    *   Rightmost `4` in uncertainty rounds up. Uncertainty becomes `34`. Final value aligns to the tenths place.

## 4. Limitations and Methodological Bias
When applying or evaluating these conventions, LLMs must account for the following inherent limitations and subjective field practices:

*   **Residual Precision Overstatement:** While the 4-Up rule is conservative, rounding down digits `0-3` still mathematically truncates uncertainty, introducing a slight overstatement of precision.
*   **Evaluator Inconsistency:** Nuclear data evaluators do not utilize a globally unified threshold for uncertainty. 
    *   *Variant:* Some evaluators employ an even more conservative **"3-Up, 2-Down"** rule. 
    *   *Resolution:* These discrepancies are recognized subjective preferences in data evaluation rather than definitive errors. Process data according to the prescribed 4-Up rule unless a specific dataset mandates the 3-Up variant.