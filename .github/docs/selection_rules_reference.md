# Quick Reference: Gamma Transition Selection Rules

This document provides a fast lookup for nuclear electromagnetic transitions based on multipolarity ($L$), spin change ($\Delta J$), and parity change ($\Delta \pi$).

## 1. Multipolarity to Delta-J and Parity
Use this table when the transition type is known.

**Rule:** Delta-J range is $|J_i - J_f| \leq L \leq J_i + J_f$

**Note:** $L > 0$ ($0 \to 0$ photon emission is strictly forbidden).


| Type | Order (L) | Delta-J | Parity Change |
| :---: | :---: | :---: | :---: |
| **E1** | 1 | 0, 1 | **Yes** |
| **M1** | 1 | 0, 1 | **No** |
| **E2** | 2 | 0, 1, 2 | **No** |
| **M2** | 2 | 0, 1, 2 | **Yes** |
| **E3** | 3 | 0, 1, 2, 3 | **Yes** |
| **M3** | 3 | 0, 1, 2, 3 | **No** |
| **E4** | 4 | 0–4 | **No** |
| **M4** | 4 | 0–4 | **Yes** |


---

## 2. $\Delta J$ and $\Delta \pi$ to Multipolarity
Use this table to identify the **lowest order (dominant)** multipolarities allowed by selection rules.

**Dominance:** The lowest allowed $L$ is typically $10^3$ to $10^5$ times more probable than $L+1$.

**Mixing:** **E2** frequently mixes with **M1** due to collective enhancement. Other mixtures (e.g., M2 with E1) are negligible.


| Spin Change (Delta-J) | No Parity Change | Parity Change (Yes) |
| :---: | :--- | :--- |
| **0** | **M1** (E2 mixing possible) | **E1** (M2 negligible) |
| **1** | **M1 + E2** (Mixed) | **E1** (M2 negligible) |
| **2** | **E2** (M3 negligible) | **M2** (E3 negligible) |
| **3** | **M3** (E4 negligible) | **E3** (M4 negligible) |
| **4** | **E4** | **M4** |


*Note: If $J_i = J_f = 0$, single photon emission is forbidden. Decay occurs via internal conversion (E0).*

---

## 3. General Laws

### Conservation of Angular Momentum
The photon carries angular momentum $L$. The triangle inequality must hold:
$$ |J_i - J_f| \leq L \leq J_i + J_f $$

### Parity Selection Rules
*   **Electric ($EL$):** $\Delta \pi = (-1)^L$
    *   Odd $L$ (1, 3...) $\to$ Parity Change.
    *   Even $L$ (2, 4...) $\to$ No Parity Change.
*   **Magnetic ($ML$):** $\Delta \pi = (-1)^{L+1}$
    *   Odd $L$ (1, 3...) $\to$ No Parity Change.
    *   Even $L$ (2, 4...) $\to$ Parity Change.