# Statistical Evaluation Rules for Experimental Data

## 1. Types of Averages
*   **Weighted Average (Error-Weighted Mean):** Each measurement is weighted inversely by its variance ($w_i = 1/\sigma_i^2$). A highly precise measurement strongly influences the final mean. Valid only when reported uncertainties are trustworthy.
*   **Unweighted Average (Arithmetic Mean):** Every measurement is weighted equally ($1/N$). Used when reported uncertainties are severely inconsistent, untrustworthy, or dominate the dataset improperly.

## 2. Types of Uncertainties (For Weighted Averages)
*   **Internal Uncertainty ($\sigma_{int}$):** The theoretical mathematical propagation of individual measurement errors ($\sigma_{int} = 1 / \sqrt{\sum w_i}$). Assumes no hidden systematic biases exist.
*   **External Uncertainty ($\sigma_{ext}$):** The empirical scatter of the data points around the calculated mean. Calculated by inflating the internal uncertainty by the Birge Ratio: $\sigma_{ext} = \sigma_{int} \times \sqrt{\chi^2/\nu}$.

## 3. The Three Statistical Zones of Reduced Chi-Square ($\chi^2/\nu$)
The reduced $\chi^2$ dictates which average and uncertainty must be adopted. The critical threshold ($\chi^2_{crit}$) is evaluated at a 99% confidence level for $\nu$ degrees of freedom.

### Zone 1: Ideal Consistency ($\chi^2/\nu \le 1$)
*   **Meaning:** Data points are highly consistent. 
*   **Action:** Adopt the **Weighted Average** and the **Internal Uncertainty**. (Do not multiply by $\sqrt{\chi^2/\nu}$, as it would artificially shrink the uncertainty).

### Zone 2: Moderate Dispersion ($1 < \chi^2/\nu \le \chi^2_{crit}$)
*   **Meaning:** Data points scatter wider than their individual error bars predict, indicating unrecognized systematic errors.
*   **Action:** Adopt the **Weighted Average**, but adopt the larger **External Uncertainty**.

### Zone 3: Severe Discrepancy ($\chi^2/\nu > \chi^2_{crit}$)
*   **Meaning:** The dataset is statistically inconsistent. Individual uncertainties are likely underestimated or influenced by unrecognized systematic effects, rendering the raw weighted average invalid.
*   **Actions:** Evaluators must implement a specialized intervention to mitigate the influence of discrepant data:
    1.  **Limitation of Relative Statistical Weight (LRSW):** The most common ENSDF protocol. The uncertainty of the most precise measurement is increased until its relative weight is capped at 50%.
    2.  **Normalized Residuals Method (NRM):** An iterative procedure that adjusts the uncertainties of measurements with large residuals until the reduced $\chi^2$ approximately equals unity.
    3.  **Rajeval Technique:** A three-stage statistical method that identifies discrepant measurements and adjusts their uncertainties based on their deviation from the population mean.
    4.  **Unweighted Average (UWA):** A conservative fallback utilized when the reported uncertainties are considered fundamentally unreliable or when more complex techniques fail to resolve the discrepancy.

## 4. Universal Procedural Rules
*   **Degrees of Freedom ($\nu$):** For averaging $N$ independent measurements, $\nu = N - 1$.
*   **Minimum Uncertainty Rule:** Regardless of the calculated internal or external uncertainty, the final adopted statistical uncertainty **must be greater than or equal to the most precise (smallest) individual input uncertainty**.