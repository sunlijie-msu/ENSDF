### Signature Quantum Number and Splitting

#### 1. Definitions
**Signature ($\alpha$)** defines the wave function symmetry of an axially deformed nucleus under a $180^\circ$ rotation ($R_x$) about an axis perpendicular to the symmetry axis.
*   **Operator:** $R_x(\pi) = e^{-i\pi J_x}$
*   **Eigenvalue:** $r = e^{-i\pi \alpha}$

#### 2. Signature Splitting
The **Coriolis interaction** acts on high-$j$ valence particles (intruder orbitals), splitting the rotational band ($\Delta I = 1$) into two branches ($\Delta I = 2$) with different energies.
*   **Observation:** Energy level staggering (odd-even shift).
*   **Mechanism:** An energy term $\propto (-1)^{I+K}$ shifts the **favored branch** lower and the **unfavored branch** higher.
*   **Signature Inversion:** Anomaly where the theoretically unfavored branch is lower in energy at low spins.

#### 3. Allowed Values and Favored Rules
The table below maps signature values to spin sequences and defines the favored branch rule.

| Nucleus Type | Signature ($\alpha$) | Spin Sequence ($I$) | Favored Signature Rule ($\alpha_f$) | Favored Branch |
| :--- | :--- | :--- | :--- | :--- |
| **Odd Mass** | $+1/2$ | $1/2, 5/2, 9/2, 13/2, 17/2, 21/2, 25/2, 29/2, 33/2, \dots$ | $\alpha_f = \frac{1}{2} (-1)^{j - 1/2}$ | **Depends on $j$** (Match $\alpha_f$) |
| | $-1/2$ | $3/2, 7/2, 11/2, 15/2, 19/2, 23/2, 27/2, 31/2, 35/2, \dots$ | | |
| **Even Mass** | $0$ | $0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, \dots$ | **Odd-Odd:** $\alpha_f = \frac{1}{2} [ (-1)^{j_p - 1/2} + (-1)^{j_n - 1/2} ]$ | **Even $I$** if $\alpha_f=0$ |
| | $1$ | $1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, \dots$ | | **Odd $I$** if $\alpha_f=1$ |

**Key:**
*   **$j$**: Total angular momentum of the odd particle (Odd-A).
*   **$j_p, j_n$**: Total angular momentum of the odd proton/neutron (Odd-Odd).
*   **Favored Branch:** Lower energy branch.
*   **Spin Sequence:** Allowed spins satisfy $I \equiv \alpha \pmod 2$.

#### 4. Application Example
**Scenario:** Odd-Odd nucleus with configuration $\pi h_{11/2} \otimes \nu i_{13/2}$.
*   **Parameters:** $j_p = 11/2$, $j_n = 13/2$.
*   **Calculation:**
    $$ \alpha_f = \frac{1}{2} \left[ (-1)^{11/2 - 1/2} + (-1)^{13/2 - 1/2} \right] = \frac{1}{2} [ (-1)^5 + (-1)^6 ] = \frac{-1 + 1}{2} = 0 $$
*   **Result:** The **$\alpha=0$** branch is favored.
*   **Conclusion:** **Even $I$** states ($0, 2, 4 \dots$) lie lower in energy than Odd $I$ states.
