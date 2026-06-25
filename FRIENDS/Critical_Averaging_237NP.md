Deep Explanation of the V.AveLib Bug

**1. The Statistical Truth ($\nu = n - 1$)**
*   **Definition:** Degrees of freedom ($\nu$) equal the number of observations ($n$) minus the number of estimated parameters. 
*   **Application:** Averaging your 15 data points consumes 1 parameter (the mean itself). Therefore, $\nu = 15 - 1 = \mathbf{14}$.

**2. The Software's Correct Step (Calculating Experimental $\chi^2$)**
*   **Math:** $\chi^2_{red} = \frac{1}{\nu} \sum w_i (x_i - \bar{x})^2$
*   **Execution:** The software correctly divides your data's weighted sum of squares by $14$, yielding the printed `chi**2/(n-1)=2.215`.

**3. The Software's Incorrect Step (Threshold Lookup)**
*   To determine if the data is overdispersed, the software queries a hardcoded table or function for the 99% confidence limit of a $\chi^2$ distribution. 
*   **The Bug:** The programmer mistakenly passed the variable `n` (15) instead of the variable `nu` (14) to the threshold lookup function. 
*   **Mathematical Proof:**
    *   Correct threshold for $\nu=14$: $\chi^2_{crit}(0.99, 14) / 14 = \mathbf{2.082}$
    *   Bugged threshold for $n=15$: $\chi^2_{crit}(0.99, 15) / 15 = \mathbf{2.039}$
*   Because the software passed $15$, it printed `[critical=2.039]`. 

**4. Implication for Research Papers**
*   A critical threshold of $2.039$ mathematically corresponds to an experiment with $16$ data points ($\nu=15$). 
*   Reporting $2.039$ alongside $n=15$ is a mathematical contradiction that peer reviewers can verify instantly via standard statistical tables. You must cite **$2.082$**.