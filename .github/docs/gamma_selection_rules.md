# Gamma Transition Selection Rules

Concise reference for nuclear electromagnetic transitions.

---

## 1. Definitions

*   J, π: Nuclear spin and parity
*   L: Multipolarity order (photon angular momentum)
*   ΔJ: Spin change between initial and final levels (ΔJ = |Ji - Jf|)
*   Δπ: Parity change between initial and final levels (Δπ = πi * πf)
*   Multipolarity Designations:
    *   D (Dipole, L=1): E1, M1
    *   Q (Quadrupole, L=2): E2, M2
    *   O (Octupole, L=3): E3, M3
    *   H (Hexadecapole, L=4): E4, M4
*   Notation:
    -   Comma (,) = OR (alternative multipolarities)
    -   Plus (+) = AND (mixed multipolarity)
    -   Tentative assignments in parentheses, e.g., (5/2+)

---

## 2. Fundamental Principles

### Angular Momentum Conservation

The triangle inequality restricts the possible multipolarity L:

$$ |J_i - J_f| \leq L \leq J_i + J_f $$

*Note: For $J_i = J_f = 1/2$, quadrupole ($L \geq 2$) transitions are strictly forbidden geometrically.*

### Parity Selection

*   Electric (EL): Δπ = $(-1)^L$ (Parity changes for odd L)
*   Magnetic (ML): Δπ = $(-1)^{L+1}$ (Parity changes for even L)

*Note: 0 → 0 single photon emission is strictly forbidden.*

### Dominance of Lowest Multipolarity (Practical Rules)

While geometry permits a range of L, nuclear transition probabilities dictate which are actually observed.

1. *Dominance Rule*: Transitions proceed via the lowest permitted multipolarity ($L_{min}$).
    *   *Practical implication*: Multipolarity assignments like M2+E3 are only practical when Dipole (L=1) is forbidden by selection rules (i.e., ΔJ ≥ 2).
2. *Weisskopf Estimates*: Probability decreases by a factor of approximately $\approx 10^5$ for each unit increase in L.
3. *Mixing*: Electric multipoles are more probable than the same magnetic multipole by a factor of 100.
    *   $L_{min}$ + 1 mixing is common (e.g., M1+E2).

---

## 3. Quick Reference: ΔJ and Δπ to Multipolarity

Allowed multipolarities based on spin-parity change:

|  ΔJ   | No Parity Change | Parity Change |
| :---: | :--------------- | :------------ |
|   0   | M1(+E2)          | E1(+M2)       |
|   1   | M1(+E2)          | E1(+M2)       |
|   2   | E2(+M3)          | M2(+E3)       |
|   3   | M3(+E4)          | E3(+M4)       |
|   4   | E4(+M5)          | M4(+E5)       |

---

## 4. Quick Reference: Multipolarity to ΔJ and Δπ

Selection rules for each transition type:

| Type  |   L   | Designation |  ΔJ Allowed   |  Δπ   |
| :---: | :---: | :---------: | :-----------: | :---: |
|  E1   |   1   |      D      |     0, 1      |  Yes  |
|  M1   |   1   |      D      |     0, 1      |  No   |
|  E2   |   2   |      Q      |    0, 1, 2    |  No   |
|  M2   |   2   |      Q      |    0, 1, 2    |  Yes  |
|  E3   |   3   |      O      |  0, 1, 2, 3   |  Yes  |
|  M3   |   3   |      O      |  0, 1, 2, 3   |  No   |
|  E4   |   4   |      H      | 0, 1, 2, 3, 4 |  No   |
|  M4   |   4   |      H      | 0, 1, 2, 3, 4 |  Yes  |

---

## 5. Mixed Multipolarities

*   D+Q (E1+M2 or M1+E2) → ΔJ = 0, 1
*   Q+O (E2+M3 or M2+E3) → ΔJ = 2
*   M1+E2 → ΔJ = 0, 1; Δπ = No
*   E1+M2 → ΔJ = 0, 1; Δπ = Yes
*   E2+M3 → ΔJ = 2; Δπ = No
*   M2+E3 → ΔJ = 2; Δπ = Yes

