# Quick Reference: Gamma Transition Selection Rules

This document provides a fast lookup for nuclear electromagnetic transitions based on multipolarity, spin change ($\Delta J$), and parity change ($\Delta \pi$).

## 1. Multipolarity to $\Delta J$ and $\Delta \pi$
Use this table when you know the transition type (multipolarity) and need to determine the allowed spin and parity changes.

| Type | Order ($L$) | Spin Change ($\Delta J$) | Parity Change ($\Delta \pi$)? | Transformation |
| :---: | :---: | :---: | :---: | :--- |
| **E1** | $1$ | $0, 1$ | **Yes** | $\pi_i \neq \pi_f$ |
| **M1** | $1$ | $0, 1$ | **No**  | $\pi_i = \pi_f$  |
| **E2** | $2$ | $0, 1, 2$ | **No**  | $\pi_i = \pi_f$  |
| **M2** | $2$ | $0, 1, 2$ | **Yes** | $\pi_i \neq \pi_f$ |
| **E3** | $3$ | $0, 1, 2, 3$ | **Yes** | $\pi_i \neq \pi_f$ |
| **M3** | $3$ | $0, 1, 2, 3$ | **No**  | $\pi_i = \pi_f$  |
| **E4** | $4$ | $0 \dots 4$ | **No**  | $\pi_i = \pi_f$  |
| **M4** | $4$ | $0 \dots 4$ | **Yes** | $\pi_i \neq \pi_f$ |

---

## 2. $\Delta J$ and $\Delta \pi$ to Multipolarity
Use this table to find the lowest-order (most probable) allowed multipolarities given the experimental spin and parity change.

| $\Delta J$ | $\Delta \pi = \text{No}$ (Same Parity) | $\Delta \pi = \text{Yes}$ (Opposite Parity) |
| :---: | :--- | :--- |
| **0** | M1, E2, M3, E4... | E1, M2, E3, M4... |
| **1** | M1, E2, M3, E4... | E1, M2, E3, M4... |
| **2** | E2, M3, E4, M5... | M2, E3, M4, E5... |
| **3** | M3, E4, M5, E6... | E3, M4, E5, E6... |
| **4** | E4, M5, E6, M7... | M4, E5, E6, M7... |

*Note: For $\Delta J = 0$, $J_i = J_f = 0$ transitions are strictly forbidden.*

---

## 3. General Laws
*   **Conservation of Angular Momentum:** $|\Delta J| \leq L \leq J_i + J_f$
*   **Parity Election Rules:**
    *   **Electric ($EL$):** $\Delta \pi = (-1)^L$
    *   **Magnetic ($ML$):** $\Delta \pi = (-1)^{L+1}$
