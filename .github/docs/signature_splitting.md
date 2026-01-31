### Signature Quantum Number and Splitting

#### 1. Definitions and Origin
**Signature ($\alpha$ or $r$)** defines the symmetry of the wave function for an axially deformed nucleus under a $180^\circ$ rotation ($R_x$) about an axis perpendicular to the symmetry axis.
*   **Operator:** $R_x(\pi) = e^{-i\pi J_x}$
*   **Eigenvalue:** $r = e^{-i\pi \alpha}$

#### 2. Signature Splitting
In deformed nuclei, the **Coriolis interaction** acts on high-$j$ valence particles (intruder orbitals), causing the total rotational band ($\Delta I = 1$) to split into two branches ($\Delta I = 2$) with different energies.
*   **Observation:** "Odd-even staggering" in energy levels.
*   **Mechanism:** An energy term proportional to $(-1)^{I+K}$ shifts one branch lower (**favored**) and the other higher (**unfavored**).
*   **Signature Inversion:** An anomalous phenomenon where the theoretically favored branch lies higher in energy at low spins, often reverting to the normal ordering at higher rotational frequencies.

#### 3. Allowed Values, Spin Sequences, and Favored Rules
The following table outlines the allowed signatures, detailed spin sequences, and rules for identifying the favored branch in rotational bands.

| Nucleus Type | Signature ($\alpha$) | Expanded Spin Sequence ($I$) | Favored Signature Rule ($\alpha_f$) | Favored Spins |
| :--- | :--- | :--- | :--- | :--- |
| **Odd Mass** | $\alpha = +1/2$ | $1/2, 5/2, 9/2, 13/2, 17/2, 21/2, \dots$ | $\alpha_f = \frac{1}{2} (-1)^{j - 1/2}$ | Depends on $j$ |
| | $\alpha = -1/2$ | $3/2, 7/2, 11/2, 15/2, 19/2, 23/2, \dots$ | | |
| **Even Mass** | $\alpha = 0$ | $0, 2, 4, 6, 8, 10, 12, \dots$ | **Odd-Odd:** $\alpha_f = \frac{1}{2} [ (-1)^{j_p - 1/2} + (-1)^{j_n - 1/2} ]$ | Even $I$ if $\alpha_f=0$ |
| | $\alpha = 1$ | $1, 3, 5, 7, 9, 11, 13, \dots$ | | Odd $I$ if $\alpha_f=1$ |

**Key Definitions:**
*   **$j$**: Total angular momentum of the odd particle (Odd-A nuclei).
*   **$j_p, j_n$**: Total angular momentum of the odd proton and neutron (Odd-Odd nuclei).
*   **Favored Branch:** The signature branch shifted lower in energy by the Coriolis force.
*   **Unfavored Branch:** The signature branch shifted higher in energy.

#### 4. Application Example
**Case:** Odd-Odd nucleus with configuration $\pi h_{11/2} \otimes \nu i_{13/2}$.
*   **Parameters:** $j_p = 11/2$, $j_n = 13/2$.
*   **Calculation:**
    $$ \alpha_f = \frac{1}{2} \left[ (-1)^{11/2 - 1/2} + (-1)^{13/2 - 1/2} \right] = \frac{1}{2} [ (-1)^5 + (-1)^6 ] = 0 $$
*   **Result:** The $\alpha=0$ branch is favored, indicating that the **Even $I$** states ($0, 2, 4 \dots$) are lower in energy than the Odd $I$ states.
