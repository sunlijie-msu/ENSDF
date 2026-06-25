
## PDG Averaging Method

### Core Procedure (Birge Ratio / Scale Factor Method)

1. **Weighted average** using inverse-variance weights: $w_i = 1/\sigma_i^2$
   $$\bar{x} = \frac{\sum w_i x_i}{\sum w_i}, \quad \sigma_{\text{int}} = \frac{1}{\sqrt{\sum w_i}}$$

2. **Compute reduced χ²** (the Birge ratio):
   $$\chi^2/\nu = \frac{1}{\nu}\sum w_i(x_i - \bar{x})^2, \quad \nu = N-1$$

3. **External uncertainty** (same formula in both PDG and ENSDF):
   $$\sigma_{\text{ext}} = \sigma_{\text{int}} \times \sqrt{\chi^2/\nu}$$

4. **Zone-based decision:**
   - **Zone 1** ($\chi^2/\nu \le 1$): use $\sigma_{\text{int}}$
   - **Zone 2** ($\chi^2/\nu > 1$): use $\sigma_{\text{ext}}$ — scales continuously with $\sqrt{\chi^2/\nu}$
   - **Zone 3** (severely inconsistent): PDG may decline to average, apply **limit of statistical weights** (cap individual weight at 50%), or use unweighted average as last resort

### Contrast with ENSDF Java_Average.py

| Aspect | PDG | ENSDF (Java_Average.py) |
|--------|-----|--------------------------|
| External uncertainty | $\sigma_{\text{int}} \times \sqrt{\chi^2/\nu}$ | **Same formula** — adopts larger of $\sigma_{\text{int}}$, $\sigma_{\text{ext}}$ |
| Zones 1–2 | Weighted avg + $\sigma_{\text{int}}$ or $\sigma_{\text{ext}}$ | **Identical** — weighted avg + larger of $\sigma_{\text{int}}$, $\sigma_{\text{ext}}$ |
| Zone 3 boundary | No fixed threshold | **max(3.5, $\chi^2_{\text{crit}}$)** — floor of 3.5; $\chi^2_{\text{crit}}$(99% CL) used when larger (n ≤ 4) |
| Zone 3 action | Continuous scaling; LWM/UWA as last resort | Binary switch to **unweighted average** when $\chi^2/\nu > \max(3.5, \chi^2_{\text{crit}})$ |
| Critical reference | Various CL available | 99% CL displayed as `[critical=X]` (reference only; decision uses 3.5) |
| Minimum uncertainty | Not enforced | Enforced (adopted $\ge$ min input) |
| Additional methods | — | LWM, NRM, RT available as alternatives |

### Key Difference

Zones 1 and 2 are **identical**: both adopt weighted average with the larger of internal and external uncertainty. The external uncertainty formula ($\sigma_{\text{int}} \times \sqrt{\chi^2/\nu}$) is the same.

Zone 3 is where they diverge: PDG continues with a continuous scale-factor approach, using weighted average with scaled external uncertainty, resorting to LWM or unweighted only when necessary. ENSDF applies a binary switch — if $\chi^2/\nu$ exceeds $\max(3.5, \chi^2_{\text{crit}})$, it abandons the weighted average entirely and adopts the unweighted average. The 3.5 floor is supplemented by the 99% CL critical value for small $n$ (≤4), where the statistical threshold is larger and more conservative. The ENSDF approach is simpler and more conservative for nuclear data evaluation where systematic effects often dominate statistical uncertainties.