# Gamma Transition Selection Rules

Concise reference for nuclear electromagnetic transitions.

---

## 1. Definitions

*   $J, \pi$: Nuclear spin and parity
*   $L$: Multipolarity order (photon angular momentum)
*   $\Delta J$: Spin change, $|J_i - J_f|$
*   $\Delta \pi$: Parity change (Yes/No)
*   Multipolarity Designations:
    *   D (Dipole, $L=1$): E1, M1
    *   Q (Quadrupole, $L=2$): E2, M2
    *   O (Octupole, $L=3$): E3, M3
    *   H (Hexadecapole, $L=4$): E4, M4
*   Notation:
    *   Comma (,) = OR (alternative multipolarities)
    *   Plus (+) = AND (mixed multipolarity)

---

## 2. Fundamental Principles

### Angular Momentum Conservation

Triangle inequality for multipolarity $L$:

$$ |J_i - J_f| \leq L \leq J_i + J_f $$

*Example: For $J_i = J_f = 1/2$, quadrupole ($L \geq 2$) transitions are forbidden.*

### Parity Selection

*   Electric (E$L$): $\Delta \pi = (-1)^L$ (changes for odd $L$)
*   Magnetic (M$L$): $\Delta \pi = (-1)^{L+1}$ (changes for even $L$)

*Note: $0 \to 0$ single photon emission is strictly forbidden.*

---

## 3. Quick Reference: $\Delta J$ and $\Delta \pi$ to Multipolarity

Allowed multipolarities based on spin-parity change:

| $\Delta J$ | No Parity Change | Parity Change |
| :---: | :--- | :--- |
| 0 | M1(+E2) | E1(+M2) |
| 1 | M1(+E2) | E1(+M2) |
| 2 | E2(+M3) | M2(+E3) |
| 3 | M3(+E4) | E3(+M4) |
| 4 | E4(+M5) | M4(+E5) |

---

## 4. Quick Reference: Multipolarity to $\Delta J$ and $\Delta \pi$

Selection rules for each transition type:

| Type | $L$ | Designation | $\Delta J$ Allowed | $\Delta \pi$ |
| :---: | :---: | :---: | :---: | :---: |
| E1 | 1 | D | 0, 1 | Yes |
| M1 | 1 | D | 0, 1 | No |
| E2 | 2 | Q | 0, 1, 2 | No |
| M2 | 2 | Q | 0, 1, 2 | Yes |
| E3 | 3 | O | 0, 1, 2, 3 | Yes |
| M3 | 3 | O | 0, 1, 2, 3 | No |
| E4 | 4 | H | 0, 1, 2, 3, 4 | No |
| M4 | 4 | H | 0, 1, 2, 3, 4 | Yes |

---

## 5. Mixed Multipolarities

Common mixing patterns for $J^\pi$ assignments:

*   M1+E2: $\Delta J = 0, 1$; $\Delta \pi = \text{No}$
*   E1+M2: $\Delta J = 0, 1$; $\Delta \pi = \text{Yes}$
*   D+Q: $\Delta J = 0, 1$
*   E2+M3: $\Delta J = 0, 1, 2$; $\Delta \pi = \text{No}$
*   M2+E3: $\Delta J = 0, 1, 2$; $\Delta \pi = \text{Yes}$

### Examples: Deducing $J^\pi$ Initial from Multipolarity and $J^\pi$ Final

1. M1+E2 transition from/to $3/2^+$:
   - $\Delta J = 0, 1$; $\Delta \pi = \text{No}$
   - Final/Initial: $1/2^+, 3/2^+$, $5/2^+$

2. E1+M2 transition from/to $1/2^-$:
   - $\Delta J = 0, 1$; $\Delta \pi = \text{Yes}$
   - Final/Initial: $1/2^+$, $3/2^+$

3. E2+M3 transition from/to $7/2^+$:
   - $\Delta J = 0, 1, 2$; $\Delta \pi = \text{No}$
   - Final/Initial: $3/2^+, 5/2^+, 7/2^+, 9/2^+$, $11/2^+$

---

## 6. Capture Transitions

Primary $\gamma$ transitions from neutron/proton capture resonances are typically E1, M1, and E2:

*   D (E1, M1): $\Delta J = 0, 1$; $\Delta \pi = \text{Yes or No}$
*   E2: $\Delta J = 0, 1, 2$; $\Delta \pi = \text{No}$

### Examples: Deducing $J^\pi$ Final from Multipolarity and $J^\pi$ Initial

Primary transition from $3/2^+$ initial:
D, E2:
- D (E1, M1): Final $1/2^-, 3/2^-, 5/2^-$, $1/2^+, 3/2^+$, $5/2^+$
- E2: Final $3/2^+, 5/2^+, 7/2^+$