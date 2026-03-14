# Scale Factor Prompt for Nuclear Structure Data

Use this prompt to guide scaling and data entry for relative intensity (RI) comments in ENSDF datasets.

## 1. Normalization Principle
Scaling the strongest RI to 100 is the normalization process.
- **Goal:** Normalize the strongest observed transition from the source dataset to exactly 100.
- **Reference Transition:** The transition with the highest original intensity.
- **Proposed Scaled Value:** 100.
- **Scale Factor ($SF$):** $SF = \frac{100}{\text{Original reference intensity}}$

## 2. Parameters
- **Source Dataset:** [Citation, e.g., 1964Gl04]
- **Normalization Point:** [Energy, e.g., 666 keV] ($RI_{orig} \to RI_{norm} = 100$)

## 3. Calculation Table
| Final Level $E_f$ (keV) | $E_\gamma = E_i - E_f$ (keV) | Original RI | $SF \times \text{Original RI}$ | Scaled RI (2 Sig Figs) |
| :--- | :--- | :--- | :--- | :--- |
| [Target Ef] | [Calculation] | [Value] | [Result] | [Rounded] |

## 4. Implementation Steps
1. **Identify Target Record:** Locate the `G` record in the ENSDF file corresponding to $E_\gamma$.
   - Note: $E_\gamma$ may vary slightly between experiments; find the closest match in the Adoped dataset.
2. **Retrieve Current Comment:** Identify the existing `cG RI$other` line for that transition.
3. **Appended Scaled Value:** Append the new scaled value and source citation to the comment line.
   - Format: `cG RI$other: [existing values], [new value] ([source NSR])`
   - Omit entries where original RI is 'none' or 'unknown'.
4. **80-Column Validation:** Ensure the modified line is exactly 80 characters long using `ensdf_1line_ruler.py`.
5. **Quality Assurance:** Verify all calculations and energy differences before claiming completion.

---
*Note: Always use precision-preserving rounding (1.233 -> 1.2) for ENSDF compliance.*
