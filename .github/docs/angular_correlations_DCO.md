# Guidelines on Directional Correlations of γ-rays from Oriented States (DCO)

## 1. General Selection Rules for Gamma Transitions

The conservation of angular momentum governs the allowed transitions between an initial nuclear state ($J_i$) and a final state ($J_f$) via radiation of multipolarity $L$:

$$ |J_i - J_f| \leq L \leq J_i + J_f $$
$$|J_i - L| \leq J_f \leq J_i + L$$

*   **Multipolarity ($L$):** Dipole transitions correspond to $L=1$, while quadrupole transitions correspond to $L=2$.
*   **Spin Change ($\Delta J$):** Defined as the absolute difference $|J_i - J_f|$.
*   **Vector Coupling:** The radiation carries away angular momentum $L$, which must be the vector sum of the initial and final nuclear spins.

## 2. Classification of Transitions

Transitions are classified by the relationship between radiation multipolarity ($L$) and the change in nuclear spin ($\Delta J = |J_i - J_f|$).

### Stretched Transitions ($|\Delta J| = L$)

The γ-ray carries the maximum angular momentum allowed by its multipole order. Angular momentum vectors of the initial state, final state, and photon are aligned.

*   **Stretched Quadrupole ($L=2$):** $\Delta J = 2$ (e.g., $4^+ \to 2^+$).
*   **Stretched Dipole ($L=1$):** $\Delta J = 1$ (e.g., $4^+ \to 3^+$).

### Unstretched Transitions ($|\Delta J| < L$)

The nuclear spin changes by less than the multipole order. The angular momentum vectors are not fully aligned (vector reorientation).

*   **For Dipole ($L=1$):** Transition is unstretched if $\Delta J = 0$.
*   **For Quadrupole ($L=2$):** Transition is unstretched if $\Delta J = 1$ or $\Delta J = 0$.

## 3. Application Examples

Initial state spin: $J_i = 9/2$

| Classification | Spin Change ($\Delta J$) | Final Spin ($J_f$) |
| :--- | :---: | :--- |
| **Stretched Quadrupole** | $2$ | $5/2$ or $13/2$ |
| **Unstretched Quadrupole** | $1$ | $7/2$ or $11/2$ |
| **Unstretched Quadrupole** | $0$ | $9/2$ |
| **Stretched Dipole** | $1$ | $7/2$ or $11/2$ |
| **Unstretched Dipole** | $0$ | $9/2$ |

## 4. DCO Ratios

The DCO ratio ($R_{DCO}$) is an experimental observable used to determine the multipolarity and electromagnetic character of γ-ray transitions. By comparing intensities measured at different angles relative to the beam axis, physicists can deduce the change in nuclear spin ($\Delta J$) between energy levels.

The ratio is defined as:

$$ R_{DCO} = \frac{I_{\gamma}(\theta_1 \text{ gated at } \theta_2)}{I_{\gamma}(\theta_2 \text{ gated at } \theta_1)} $$

*   **Assumed geometry:** $\theta_1 \approx 37^\circ$ and $\theta_2 \approx 79^\circ$.
*   **Like-to-Like Gates:** When gating on a transition of known multipolarity, the observed $R_{DCO}$ values for the same multipolarity transitions are expected to be close to unity.

## 5. Interpretation Rules (ENSDF 2021 Guidelines)

### A. Gate on Stretched Quadrupole Transition

*Reference Transition:* $\Delta J = 2$

| Observed Transition Type | Spin Change ($\Delta J$) | Expected $R_{DCO}$ |
| :--- | :--- | :--- |
| **Stretched Quadrupole** | $\Delta J = 2$ | $\approx 1.0$ |
| **Stretched Dipole** | $\Delta J = 1$ | $\approx 0.56$ |
| **Mixed Dipole + Quadrupole** | $\Delta J = 1$ | $0.2 \text{ -- } 1.3$ (Depends on mixing ratio $\delta$) |
| **Unstretched Dipole** | $\Delta J = 0$ | $\approx 1.0$ |
| **Mixed Unstretched** | $\Delta J = 0$ | $0.6 \text{ -- } 1.0$ |

### B. Gate on Stretched Dipole Transition

*Reference Transition:* $\Delta J = 1$.

| Observed Transition Type | Spin Change ($\Delta J$) | Expected $R_{DCO}$ |
| :--- | :--- | :--- |
| **Stretched Quadrupole** | $\Delta J = 2$ | $\approx 1.8$ |
| **Stretched Dipole** | $\Delta J = 1$ | $\approx 1.0$ |
| **Unstretched Dipole** | $\Delta J = 0$ | $\approx 1.8$ |

### C. Ambiguities

*   **Overlap:** An unstretched dipole transition ($\Delta J = 0$) exhibits similar $R_{DCO}$ values to a stretched quadrupole transition ($\Delta J = 2$) in both gating configurations ($1.0$ in Quad gate; $1.8$ in Dipole gate).
*   **Resolution:** Linear polarization measurements are required to distinguish these cases by determining the electromagnetic character (Electric vs. Magnetic).

## 6. Multipolarity Assignment Reasoning Logic

### DCO Reference Gates

*   Gating on a stretched dipole ($\Delta J = 1$) transition yields $R_{DCO}(D)$.
*   Gating on a stretched quadrupole ($\Delta J = 2$) transition yields $R_{DCO}(Q)$.
*   Expected DCO values depend on experimental detection setups.

### If $R_{DCO}(D) \approx 1.0$ or $R_{DCO}(Q) \approx 0.5$

*   The transition is stretched dipole ($\Delta J = 1$) dominant.
*   If $\delta$ is not given, assign D in the M field.
*   If $\delta$ is given, assign D+Q in the M field.

### If $R_{DCO}(Q) \approx 1.0$ or $R_{DCO}(D) \approx 2.0$

*   The transition is stretched quadrupole ($\Delta J = 2$) dominant.
*   If level scheme indicates $|J_i - J_f| = 2$ and $\delta$ is not given, assign Q ($\Delta J = 2$) in the M field.
*   If level scheme indicates $J_i = J_f$ and $\delta$ is not given, assign D in the M field and note consistent with $\Delta J = 0$ in the cG comment.
*   If level scheme indicates $J_i = J_f$ and $\delta$ is given, assign D+Q in the M field and note consistent with $\Delta J = 0$ in the cG comment.
*   If level scheme indicates $|J_i - J_f| = 1$ and $\delta$ is given, assign D+Q in the M field.
*   If level scheme indicates $|J_i - J_f| = 2$ and $\delta$ is given, assign Q+O in the M field.

### If $R_{DCO}$ is Far from Any Expected Values

*   If level scheme indicates $|J_i - J_f| = 0$ or $|J_i - J_f| = 1$ and $\delta$ is given, assign D+Q.
*   If level scheme indicates $|J_i - J_f| = 2$ and $\delta$ is given, assign Q+O.
*   If level scheme indicates $|J_i - J_f| = 3$ and $\delta$ is given, assign O in the M field and put O+H and $\delta$ in the cG comment.

### Mixing Ratio Refinement

*   If $\delta$ is given and does not overlap with zero, D+Q or Q+O remains unchanged.
*   If $\delta$ is given and overlaps with zero, place the higher-order multipolarity in parentheses: D+Q changes to D(+Q), and Q+O changes to Q(+O).

### Polarization

*   **Positive POL** (dominant electric character):
    *   D → E1
    *   Q → E2
    *   D+Q → E1+M2
    *   D(+Q) → E1(+M2)
    *   Q+O → E2+M3
    *   Q(+O) → E2(+M3)
*   **Negative POL** (dominant magnetic character):
    *   D → M1
    *   Q → M2
    *   D+Q → M1+E2
    *   D(+Q) → M1(+E2)
    *   Q+O → M2+E3
    *   Q(+O) → M2(+E3)
*   **No POL data available:** Do not assign E or M. Use only D, Q, and/or O based on DCO data.

