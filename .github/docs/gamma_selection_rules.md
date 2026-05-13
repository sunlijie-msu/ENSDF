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

### Examples: Deducing Jπ Initial from Multipolarity and Jπ Final

1. D+Q transition from/to 5/2+:
   *   ΔJ = 0, 1
   *   Result: 3/2±, 5/2±, 7/2±

2. M1+E2 transition from/to 5/2+:
   *   ΔJ = 0, 1; Δπ = No
   *   Result: 3/2+, 5/2+, 7/2+

3. M2+E3 transition from/to 5/2+:
   *   ΔJ = 2; Δπ = Yes
   *   Result: 1/2−, 9/2−


Assigning M1+E2 or (M1+E2) in G-record M field:

Assign firm M1+E2 directly based on DCO/ADO and POL data:
cG M$from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.

Assign firm M1+E2 based on D+Q from |g(|q)/DCO without POL, and the level lifetime is short:
cG M$D+Q from |g(|q) in dataset. M2 ruled out by RUL.
cG M$D+Q from |g|g(|q)(DCO) in dataset. M2 ruled out by RUL.

Use firm M1+E2 in cL J comments to deduce J|p:
<G-energy>|g, M1+E2, to <Jπ>, <L-energy> level
cG M$D+Q from |g(|q) in dataset. M2 ruled out by RUL.

Use firm M1+E2, |DJ=1 in cL J comments to deduce J|p:
<G-energy>|g, M1+E2, |DJ=1 to <Jπ>, <L-energy> level
cG M$from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.
cG M$D+Q from |g|g(|q)(DCO) in dataset. M2 ruled out by RUL.

Assign tentative (M1+E2) based on firm D+Q and level scheme info.
cG M$D+Q from |g(|q) in dataset. |D|p=no from level scheme.
cG M$D+Q from |g|g(|q)(DCO) in dataset. |D|p=no from level scheme.

If D(+Q) is firm, the corresponding converted form is M1(+E2).
The same logic applies to assigning and using E1+M2.

---

## 6. Capture Transitions

Primary γ transitions from neutron/proton capture resonances are possibly dominated by the lowest multipoles (E1, M1, E2). Higher orders are suppressed.

*   D including E1 or M1: ΔJ = 0, 1; Δπ = Yes or No
*   E2: ΔJ = 2; Δπ = No

### Examples: Deducing Jπ of a final level from multipolarity and Jπ of the initial level

Primary γ transition from 5/2+ Initial via D or E2:
*   D {E1, M1}: Final 3/2±, 5/2±, 7/2±
*   E2: Final 1/2+, 9/2+
*   Combination: 1/2+, 3/2±, 5/2±, 7/2±, 9/2+

Primary γ transition from 7/2- Initial via D or E2:
*   D {E1, M1}: Final 5/2±, 7/2±, 9/2±
*   E2: Final 3/2-, 11/2-
*   Combination: 3/2-, 5/2±, 7/2±, 9/2±, 11/2-

If two primary γ transitions from 5/2+ and 7/2-, the "AND" intersection of the above two sets:
*   Jπ of the final level: 3/2-, 5/2±, 7/2±, 9/2+

Considering the multipolarity is not directly determined by experimental evidence, the final Jπ is put in parentheses to indicate the assumptions made:
*   Adopted: (3/2-, 5/2±, 7/2±, 9/2+)

---

## 7. Practical Workflow: Combining Jπ Constraints Logic

### Goal

Deduce the Jπ of a level by combining constraints from:
- **Feeding transitions** — γ rays populating the level (from capture resonances above)
- **Deexciting transitions** — γ rays depopulating the level (to lower levels below)

---

### Multipolarity Selection Rules

| Transition Type                          | Apply       | Condition                                  |
| :--------------------------------------- | :---------- | :----------------------------------------- |
| **Primary feeding γ** (from resonances)  | **D or E2** | Always                                     |
| **Deexciting γ** (decay to lower levels) | **D or Q**  | Long or unknown lifetime                   |
| **Deexciting γ** (decay to lower levels) | **D or E2** | Short lifetime (RUL applies: M2 ruled out) |

*Note: Primary γ = capture transition from neutron/proton resonance*

---

### Workflow Algorithm

```
FOR each feeding γ:
    Apply D or E2 selection rules
    IF feeding level has multi-valued Jπ (e.g., 1/2+,3/2+):
        Calculate allowed Jπ for EACH value separately
        Take OR (union) of results
    ENDIF
ENDFOR

FOR each deexciting γ:
    IF lifetime is short (RUL applies):
        Apply D or E2 selection rules
    ELSE:
        Apply D or Q selection rules
    ENDIF
ENDFOR

Take AND (intersection) of ALL constraints above

RESULT: Common Jπ values → Put in parentheses to indicate tentative assignment
```

*Parentheses in ENSDF denote tentative assignments based on assumed multipolarities*

### Example 1: Fed by primary γ from 7/2-, 7/2+, and 5/2+

Fed by primary γ from 7/2- (D or E2):
3/2-, 5/2±, 7/2±, 9/2±, 11/2-

Fed by primary γ from 7/2+ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Fed by primary γ from 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 5/2±, 7/2±, 9/2+

Adopted: (5/2±, 7/2±, 9/2+)

### Example 2: Fed by primary γ from 5/2-. Decay γ to 1/2+ and 5/2+ (Lifetime short, RUL applies, M2 ruled out)

Fed by primary γ (D or E2):
1/2-, 3/2±, 5/2±, 7/2±, 9/2-

Decay γ to 1/2+ (D or E2):
1/2±, 3/2±, 5/2+

Decay γ to 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 3/2±, 5/2+

Adopted: (3/2±, 5/2+)

### Example 3: Fed by primary γ from 7/2+. Decay γ to 5/2+ (Lifetime unknown, RUL does not apply, M2 allowed)

Fed by primary γ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Decay γ to 5/2+ (D or Q):
1/2±, 3/2±, 5/2±, 7/2±, 9/2±

**AND:** 3/2+, 5/2±, 7/2±, 9/2±

Adopted: (3/2+, 5/2±, 7/2±, 9/2±)

### Example 4: Fed by primary γ from 1/2+,3/2+ (multi-valued initial). Decay γ to 1/2+ and 3/2+ (Lifetime short, RUL applies, M2 ruled out)

Fed by primary γ from **1/2+,3/2+** (D or E2):
*   From 1/2+ via D or E2: 1/2±, 3/2±, 5/2+
*   From 3/2+ via D or E2: 1/2±, 3/2±, 5/2±, 7/2+
*   **OR (union):** 1/2±, 3/2±, 5/2±, 7/2+

Decay γ to 1/2+ (D or E2):
1/2±, 3/2±, 5/2+

Decay γ to 3/2+ (D or E2):
1/2±, 3/2±, 5/2±, 7/2+

**AND:** 1/2±, 3/2±

Adopted: (1/2,3/2)

*Note: When initial level has multiple J-π values (e.g., 1/2+,3/2+), calculate allowed final states for EACH initial value separately, then take OR (union) before applying AND with other constraints.*

---

### cL J$ Comment Style Rules

When writing primary transition lists in `cL J$` comments:

1. For primary transitions used to deduce Jπ of a level, do not use weak γ rays (Iγ < 5), γ rays with upper-limit intensity (`LT` in the `DRI` field), γ rays with questionable placement (`?` in col 80), or γ rays to final levels with uncertain or multi-valued Jπ.
2. List transitions in descending order of intensity, with the strongest first, to reflect the most probable deexcitation paths. If there are γ transitions to final levels with the same Jπ, include only the strongest one for that Jπ, as this is sufficient for Jπ deduction.
3. Example for one γ transition: `Primary transition <E_gamma1>|g to <Jπ1> g.s.`
4. Example for multiple γ transitions: `Primary transitions: <E_gamma1>|g to <Jπ1> g.s., <E_gamma2>|g to <Jπ2>, <E_level2>, and <E_gamma3>|g to <Jπ3>, <E_level3>.` Or, with specified intensities: `Primary transitions with I|g>10: <E_gamma1>|g to <Jπ1> <E_level1> and <E_gamma2>|g to <Jπ2>, <E_level2>.` Or, with specified multipolarities: `Primary transitions: <E_gamma1>|g, D(+Q), to <Jπ1>, <E_level1> and <E_gamma2>|g, D(+Q), to <Jπ2>, <E_level2>.`
5. Use Oxford comma style in multi-transition lists, for example: `Primary transitions: 5805|g to 0+ g.s., 5344|g to 1+, 461 level, 5659|g to 3+, 146 level, and 3430|g to 4+, 2376 level.`