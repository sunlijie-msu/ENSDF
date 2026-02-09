# Gamma Transition Selection Rules

This document provides a concise reference for nuclear electromagnetic transitions.

## Definitions and Notation

*   **$J, \pi$**: Nuclear spin and parity
*   **$L$**: Multipolarity order of the transition
*   **$\Delta J$**: Spin change $|J_i - J_f|$
*   **$\Delta \pi$**: Parity change (Yes/No)
*   **Labels**: D (Dipole, $L=1$), Q (Quadrupole, $L=2$), O (Octupole, $L=3$), H (Hexadecapole, $L=4$)
*   **Notation**:
    *   **Comma (,):** Indicates alternative possibilities (OR).
    *   **Plus (+):** Indicates multipole mixing (AND).

---

## 1. Multipolarity Properties
Relation between transition type, multipolarity order, and selection rules.

| Type | Order ($L$) | Multipolarity  | Allowed $\Delta J$ | Parity Change ($\Delta \pi$) |
| :---: | :---: | :---: | :---: | :---: |
| E1 | 1 | D | 0, 1 | Yes |
| M1 | 1 | D | 0, 1 | No |
| E2 | 2 | Q | 0, 1, 2 | No |
| M2 | 2 | Q | 0, 1, 2 | Yes |
| E3 | 3 | O | 0, 1, 2, 3 | Yes |
| M3 | 3 | O | 0, 1, 2, 3 | No |
| E4 | 4 | H | 0 – 4 | No |
| M4 | 4 | H | 0 – 4 | Yes |

*Note: For $\Delta J = 0$, $0 \to 0$ transitions are forbidden for single photon emission.*
For primary $\gamma$ transitions, the allowed multipolarities are E1, M1, and E2, and the corresponding selection rules are:
*   **D:** $\Delta J = 0, 1$, $\Delta \pi = \text{Yes or No}$
*   **E2:** $\Delta J = 0, 1, 2$, $\Delta \pi = \text{No}$

---

## 2. Selection Rules
Lowest allowed multipolarities based on initial and final state properties.
*Note: Higher allowed orders (e.g., $L+1$) often mix with the lowest allowed order ($L$).*

| $\Delta J$ | No Parity Change ($\Delta \pi = \text{No}$) | Parity Change ($\Delta \pi = \text{Yes}$) |
| :---: | :--- | :--- |
| **0** | M1 (+E2) | E1 (+M2) |
| **1** | M1 (+E2) | E1 (+M2) |
| **2** | E2 (+M3) | M2 (+E3) |
| **3** | M3 (+E4) | E3 (+M4) |
| **4** | E4 (+M5) | M4 (+E5) |

---

## 3. Physics Principles

### Angular Momentum Conservation
The photon carries angular momentum $L$. The triangle inequality must be satisfied:
$$ |J_i - J_f| \leq L \leq J_i + J_f $$

### Parity Selection Rules
*   **Electric ($EL$):** $\Delta \pi = (-1)^L$ (Parity changes for odd $L$)
*   **Magnetic ($ML$):** $\Delta \pi = (-1)^{L+1}$ (Parity changes for even $L$)