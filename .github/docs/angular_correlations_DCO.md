# Guidelines on Directional Correlations of γ-rays from Oriented States (DCO)

## 1. General Selection Rules for Gamma Transitions

The conservation of angular momentum governs the allowed transitions between an initial nuclear state ($J_i$) and a final state ($J_f$) via radiation of multipolarity $L$:

$$ |J_i - J_f| \leq L \leq J_i + J_f $$
$$|J_i - L| \leq J_f \leq J_i + L$$

*   **Multipolarity ($L$):** Dipole transitions correspond to $L=1$, while quadrupole transitions correspond to $L=2$.
*   **Spin Change ($\Delta J$):** Defined as the absolute difference $|J_i - J_f|$.
*   **Vector Coupling:** The radiation carries away angular momentum $L$, which must be the vector sum of the initial and final nuclear spins.

## 3. Classification of Transitions
Transitions are classified by the relationship between radiation multipolarity ($L$) and the change in nuclear spin ($\Delta J = |J_i - J_f|$).

### Stretched Transitions ($|\Delta J| = L$)
The γ-ray carries the maximum angular momentum allowed by its multipole order. Angular momentum vectors of the initial state, final state, and photon are aligned.
*   **Stretched Quadrupole ($L=2$):** $\Delta J = 2$ (e.g., $4^+ \to 2^+$).
*   **Stretched Dipole ($L=1$):** $\Delta J = 1$ (e.g., $4^+ \to 3^+$).

### Unstretched Transitions ($|\Delta J| < L$)
The nuclear spin changes by less than the multipole order. The angular momentum vectors are not fully aligned (vector reorientation).
*   **For Dipole ($L=1$):** Transition is unstretched if $\Delta J = 0$.
*   **For Quadrupole ($L=2$):** Transition is unstretched if $\Delta J = 1$ or $\Delta J = 0$.

## 2. Introduction to DCO Ratios

The DCO ratio ($R_{DCO}$) is an experimental observable used to determine the multipolarity and electromagnetic character of γ-ray transitions. By comparing intensities measured at different angles relative to the beam axis, physicists can deduce the change in nuclear spin ($\Delta J$) between energy levels.

The ratio is defined as:

$$ R_{DCO} = \frac{I_{\gamma}(\theta_1 \text{ gated at } \theta_2)}{I_{\gamma}(\theta_2 \text{ gated at } \theta_1)} $$

*   **Assumed geometry:** $\theta_1 \approx 37^\circ$ and $\theta_2 \approx 79^\circ$.
*   **Like-to-Like Gates:** When gating on a transition of known multipolarity, the observed $R_{DCO}$ values for the same multipolarity transitions are expected to be close to unity.

## 4. Interpretation Rules (ENSDF 2021 Guidelines)

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

## 5. Application Examples

Initial state spin: $J_i = 9/2$

| Classification | Spin Change ($\Delta J$) | Final Spin ($J_f$) |
| :--- | :---: | :--- |
| **Stretched Quadrupole** | $2$ | $5/2$ or $13/2$ |
| **Unstretched Quadrupole** | $1$ | $7/2$ or $11/2$ |
| **Unstretched Quadrupole** | $0$ | $9/2$ |
| **Stretched Dipole** | $1$ | $7/2$ or $11/2$ |
| **Unstretched Dipole** | $0$ | $9/2$ |