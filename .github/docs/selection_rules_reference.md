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

The triangle inequality restricts the possible multipolarity $L$:

$$ |J_i - J_f| \leq L \leq J_i + J_f $$

*Example: For $J_i = J_f = 1/2$, quadrupole ($L \geq 2$) transitions are strictly forbidden geometrically.*

### Parity Selection

*   Electric (E$L$): $\Delta \pi = (-1)^L$ (Parity changes for odd $L$)
*   Magnetic (M$L$): $\Delta \pi = (-1)^{L+1}$ (Parity changes for even $L$)

*Note: $0 \to 0$ single photon emission is strictly forbidden.*

### Dominance of Lowest Multipolarity (Practical Rules)

While geometry permits a range of $L$, nuclear transition probabilities dictate which are actually observed.

1. *Weisskopf Estimates*: Probability decreases by factor of $\approx 10^5$ for each unit increase in $L$.
2. *Dominance Rule*: Transitions proceed via the lowest permitted multipolarity ($L_{min}$).
3. *Mixing*:
    * $L_{min} + 1$ mixing is common (e.g., M1+E2).
    * $L_{min} + 2$ or higher is generally negligible ($< 10^{-5}$ branching).
    * *Practical implication*: Multipolarity assignments like M2+E3 are only practical when Dipole ($L=1$) is forbidden by selection rules (i.e., $\Delta J \geq 2$).

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

Common mixing patterns constrained by the dominance rule:

* D+Q (E1+M2 or M1+E2): $\Delta J = 0, 1$
* Q+O (E2+M3 or M2+E3): $\Delta J = 2$
* M1+E2: $\Delta J = 0, 1$; $\Delta \pi = \text{No}$
* E1+M2: $\Delta J = 0, 1$; $\Delta \pi = \text{Yes}$
* E2+M3: $\Delta J = 2$; $\Delta \pi = \text{No}$
* M2+E3: $\Delta J = 2$; $\Delta \pi = \text{Yes}$

### Examples: Deducing $J^\pi$ Initial from Multipolarity and $J^\pi$ Final

1. D+Q transition from/to $5/2^+$:
   * $\Delta J = 0, 1$
   * Result: $3/2±, 5/2±, 7/2±$
  
2. M1+E2 transition from/to $5/2^+$:
   * $\Delta J = 0, 1$; $\Delta \pi = \text{No}$
   * Result: $3/2^+, 5/2^+, 7/2^+$

3. M2+E3 transition from/to $5/2^+$:
   * $\Delta J = 2$; $\Delta \pi = \text{Yes}$
   * Result: $1/2^-, 9/2^-$

---

## 6. Capture Transitions

Primary $\gamma$ transitions from neutron/proton capture resonances are physically dominated by the lowest multipoles (E1, M1, E2). Higher orders are kinetically and statistically suppressed.

* D (E1, M1): $\Delta J = 0, 1$; $\Delta \pi = \text{Yes or No}$
* E2: $\Delta J = 2$; $\Delta \pi = \text{No}$

### Examples: Deducing $J^\pi$ Final from Multipolarity and $J^\pi$ Initial

Primary transition from $5/2^+$ initial via D or E2:
* D (E1, M1): Final $3/2±, 5/2±, 7/2±$
* E2: Final $1/2^+, 9/2^+$
* Combination: $1/2^+, 3/2±, 5/2±, 7/2±, 9/2^+$

Primary transition from $7/2^-$ initial via D or E2:
* D (E1, M1): Final $5/2±, 7/2±, 9/2±$
* E2: Final $3/2^-, 11/2^-$
* Combination: $3/2^-, 5/2±, 7/2±, 9/2±, 11/2^-$

If two primary transitions from $5/2^+$ and $7/2^-$, the AND of the above two sets:
* Final $3/2^-, 5/2±, 7/2±, 9/2^+$ (common to both sets)

---

## 7. Practical Workflow: Intersection Logic

### Deducing $J^\pi$ from Multiple Constraints

1. List allowed $J^\pi$ from each constraint (primary feeding γ, decay γ)
2. For primary feeding γ, D or E2 are considered:
   * Apply multipolarity selection rules to get possible $J^\pi$
3. For decay γ, D or Q are considered:
   * Apply multipolarity selection rules to get possible $J^\pi$
   * If lifetime is short and RUL applies, exclude M2, i.e., consider D or E2, the same as primary γ
   * If decay γ is also primary γ, apply D or E2 selection rules for that as well
3. Apply AND (intersection) across all constraints
4. Result: Common $J^\pi$ values only

*Note: Parentheses in ENSDF denote tentative assignments, e.g., (5/2+,7/2,9/2+)*

### Example 1: Fed by primary γ from 5/2-. Decay γ to 1/2+ and 5/2+

Fed by primary γ (D or E2):
1/2-, 3/2±, 5/2±, 7/2±, 9/2-

Decay γ to 1/2+ (D or E2):
1/2±, 3/2±, 5/2+

Decay γ to 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 3/2±, 5/2+

### Example 2: Fed by primary γ from 7/2-, 7/2+, and 5/2+

Fed by primary γ from 7/2- (D or E2):
3/2-, 5/2±, 7/2±, 9/2±, 11/2-

Fed by primary γ from 7/2+ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Fed by primary γ from 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 5/2±, 7/2±, 9/2+

### Example 3: Fed by primary γ from 7/2+. Decay γ to 5/2+ (Lifetime unknown, RUL does not apply, M2 allowed)

Fed by primary γ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Decay γ to 5/2+ (D or Q):
1/2±, 3/2±, 5/2±, 7/2±, 9/2±

**AND:** 3/2+, 5/2±, 7/2±, 9/2±