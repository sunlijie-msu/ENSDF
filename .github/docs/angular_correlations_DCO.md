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
*   **Resolution:** Linear polarization measurements are required to assign the electromagnetic character (Electric vs. Magnetic).

## 6. Practical Workflow: Multipolarity Assignment Reasoning Logic

### Scenario A: Only Mixing Ratio and Spins Given

When only $\delta$, $J_i$, and $J_f$ are available:

*   If level scheme indicates $\Delta J = 0$ or $1$, assign D+Q in M field.
*   If level scheme indicates $\Delta J = 2$, assign Q+O in M field.
*   If level scheme indicates $\Delta J = 3$, assign O in M field and note O+H and $\delta$ value in cG M,MR comment.

### Scenario B: DCO Ratios, Mixing Ratio, and Spins Given

When DCO ratios, $\delta$, $J_i$, and $J_f$ are available, follow Steps 1 and 2 below.

#### Step 1: Look at DCO Ratios

##### DCO Reference Gates

*   Gating on a stretched dipole ($\Delta J = 1$) transition yields $R_{DCO}(D)$.
*   Gating on a stretched quadrupole ($\Delta J = 2$) transition yields $R_{DCO}(Q)$.
*   Expected DCO values depend on experimental detection setups.

##### DCO Decision Rules

**If $R_{DCO}(D) \approx 1.0$ or $R_{DCO}(Q) \approx 0.5$:**
*   Transition is stretched dipole ($\Delta J = 1$) dominant.
*   Mark as **D**.

**If $R_{DCO}(Q) \approx 1.0$ or $R_{DCO}(D) \approx 2.0$:**
*   Transition is stretched quadrupole ($\Delta J = 2$) dominant.
*   Mark as **Q**.
*   Then look at spins, a lesson common case is if the level scheme indicates $J_i = J_f$:
*   Mark as **DJ=0**.

**If $R_{DCO}$ is between two expected values or inconsistent with all expected values:**
*   Mark as **Mixed**.

#### Step 2: Look at Mixing Ratio and Level Scheme Spin Information

Based on the Step 1 classification:

##### For Transitions Marked D

*   If $\delta$ is not given, assign D in M field.
*   If $|\delta| < 1$ is given, assign D+Q in M field.

##### For Transitions Marked Q

*   If $\delta$ is not given, assign Q in M field.
*   If $|\delta| < 1$ is given, assign Q+O in M field.
*   Then look at spins, the level scheme should indicate $\Delta J = 2$; but if it indicates $\Delta J = 1$, assign D+Q in M field.

##### For Transitions Marked DJ=0

*   If $\delta$ is not given, assign D in M field and note "consistent with |DJ=0" in the cG comment after the DCO value.
*   If $|\delta| < 1$ is given, assign D+Q in M field and note "consistent with |DJ=0" in the cG comment after the DCO value.

##### For Transitions Marked Mixed

*   If $\delta$ is not given, no need to assign M field.
*   If $\delta$ is given:
    *   If level scheme indicates $\Delta J = 0$ or $1$, assign D+Q in M field.
    *   If level scheme indicates $\Delta J = 2$, assign Q+O in M field.
    *   If level scheme indicates $\Delta J = 3$, assign O in M field and note O+H and $\delta$ value in cG M,MR comment.

#### Step 3: Mixing Ratio Refinement

*   If $\delta$ is given and does not overlap with 0, D+Q or Q+O remains unchanged.
*   If $\delta$ is given and overlaps with 0, place the higher-order multipolarity in parentheses:
    *   D+Q changes to D(+Q).
    *   Q+O changes to Q(+O).

#### Step 4: Polarization Refinement

Apply these rules based on measured POL to assign electromagnetic character:

#### Positive POL (Dominant Electric Character)

*   D → E1
*   Q → E2
*   D+Q → E1+M2
*   D(+Q) → E1(+M2)
*   Q+O → E2+M3
*   Q(+O) → E2(+M3)

#### Negative POL (Dominant Magnetic Character)

*   D → M1
*   Q → M2
*   D+Q → M1+E2
*   D(+Q) → M1(+E2)
*   Q+O → M2+E3
*   Q(+O) → M2(+E3)

#### If No POL Data Available

*   Do not assign E or M labels.
*   Assign only D, Q, O multipolarities based on DCO decision rules above.

