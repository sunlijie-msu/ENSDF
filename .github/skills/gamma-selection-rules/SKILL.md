---
name: gamma-selection-rules
description: >
  Use this skill when deducing multipolarities for gamma transitions and then Jπ for nuclear levels by combining constraints
  from feeding and deexciting gamma transitions using electromagnetic
  selection rules. Applies D/E2 rules to primary capture transitions,
  D/Q or D/E2 to deexciting gammas (if RUL applies), and takes AND
  intersection of all constraints. Handles multi-valued initial Jπ via
  union before intersection.
---

# Gamma Transition Selection Rules: Deducing multipolarities and Jπ

- ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`.
- Spot-check policy: `.github/copilot-instructions.md`.
- γ-ray multipolarity selection rules: `.github/docs/gamma_selection_rules.md`.

## Goal
Deduce the multipolarity of γ-ray transitions from experimental data.
Deduce the Jπ of levels by combining constraints from:
- **Feeding transitions** — γ rays populating the level (from capture resonances above)
- **Deexciting transitions** — γ rays depopulating the level (to lower levels below)

## Multipolarity Assignment Reasoning Logic in Individual Datasets

### Scenario A: Only Mixing Ratios and Spins Given in Literature

*   If level scheme indicates $\Delta J = 0$ or $1$, assign D+Q in M field.
*   If level scheme indicates $\Delta J = 2$, assign Q+O in M field.
*   If level scheme indicates $\Delta J = 3$, assign O in M field and note O+H and $\delta$ value in cG M,MR comment.

### Scenario B: DCO Ratios, Mixing Ratio, and Spins Given in Literature

#### Step 1: Look at DCO Ratios

##### DCO Reference Gates

*   Gating on a stretched dipole ($\Delta J = 1$) transition yields $R_{DCO}(D)$.
*   Gating on a stretched quadrupole ($\Delta J = 2$) transition yields $R_{DCO}(Q)$.
*   Expected DCO values depend on experimental detection setups. The values below are for example purposes.

##### DCO Decision Rules

**If $R_{DCO}(D) \approx 1.0$ or $R_{DCO}(Q) \approx 0.5$:**
*   Transition is stretched dipole ($\Delta J = 1$) dominant.
*   Mark as **D**.

**If $R_{DCO}(Q) \approx 1.0$ or $R_{DCO}(D) \approx 2.0$:**
*   Transition is stretched quadrupole ($\Delta J = 2$) dominant and with a possibly weaker dipole or octupole component.
*   Mark as **Q**.
*   Then look at spins, a less common case is if the level scheme indicates $J_i = J_f$:
*   Mark as **ΔJ=0**.

**If $R_{DCO}$ is between two expected values or inconsistent with all expected values:**
*   Mark as **Mixed**.

#### Step 2: Look at Mixing Ratio ($\delta$) and Level Scheme Spin Change ($\Delta J$)

Based on the Step 1 classification:

##### For Transitions Marked D

*   If $\delta$ is not given, assign D in M field.
*   If $|\delta| < 1$ is given, assign D+Q in M field.

##### For Transitions Marked Q

*   If $\delta$ is not given, assign Q in M field.
*   If $|\delta| < 1$ is given, assign Q+O in M field.
*   Then look at spins, the level scheme should indicate $\Delta J = 2$; but if it indicates $\Delta J = 1$, assign D+Q in M field and flag this discrepancy for user review.
*   If $|\delta| > 1$ is given, assign D+Q in M field because dipole is the weaker component.

##### For Transitions Marked ΔJ=0

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

##### Positive POL (Dominant Electric Character)

*   D → E1
*   Q → E2
*   D+Q → E1+M2
*   D(+Q) → E1(+M2)
*   Q+O → E2+M3
*   Q(+O) → E2(+M3)

##### Negative POL (Dominant Magnetic Character)

*   D → M1
*   Q → M2
*   D+Q → M1+E2
*   D(+Q) → M1(+E2)
*   Q+O → M2+E3
*   Q(+O) → M2(+E3)

##### If No POL Data Available

*   Do not assign E or M labels.
*   Assign only D, Q, O multipolarities based on DCO decision rules above.

---

## Multipolarity Assignment Reasoning Logic in the Adopted Dataset

### Overview

To further constrain multipolarities (G-record M field) and then use them to deduce Jπ for each level (L-record Jπ field).

### Assignment Patterns

Assigning M1+E2 or (M1+E2) in the G-record M field:

1. Assign firm M1+E2 directly based on DCO/ADO and POL data. The `cG M$` comment should cite the specific dataset:

   `cG M$from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`
   `cG M$M1+E2, |DJ=1, from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`

2. Assign firm M1+E2 from D+Q without POL when the level lifetime is short (M2 ruled out by RUL). The `cG M$` comment should cite the dataset and note RUL:

   `cG M$D+Q from |g(|q) in dataset. M2 ruled out by RUL.`
   `cG M$D+Q, |DJ=1, from |g|g(|q)(DCO) in dataset. M2 ruled out by RUL.`

   Use M1+E2 in `cL J$` comments to deduce Jπ:

   `cL J$<G-energy>|g, M1+E2, to <Jπ>, <L-energy> level`
   `cG M$D+Q from |g(|q) in dataset. M2 ruled out by RUL.`

   Use M1+E2, |DJ=1, in `cL J$` comments to deduce Jπ:

   `<G-energy>|g, M1+E2, |DJ=1 to <Jπ>, <L-energy> level`
   `cG M$M1+E2, |DJ=1, from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`
   `cG M$D+Q, |DJ=1, from |g|g(|q)(DCO) in dataset. M2 ruled out by RUL.`

3. Assign tentative (M1+E2) from firm D+Q when the level scheme indicates Δπ=no:

   `cG M$D+Q from |g(|q) in dataset. |D|p=no from level scheme.`
   `cG M$D+Q, |DJ=1, from |g|g(|q)(DCO) in dataset. |D|p=no from level scheme.`

If D(+Q) is firm, the corresponding converted form is M1(+E2). The same logic applies to E1+M2.

### Conversion Decision Table

| Individual G | Measurement                      | Adopted G | For G record M field     | For L record Jπ field          |
| ------------ | -------------------------------- | --------- | ------------------------ | ------------------------------ |
| M1+E2        | DCO stretched D, POL, w/wo δ     | M1+E2     |                          | M1+E2, ΔJ=1, Δπ=no             |
| M1(+E2)      | DCO stretched D, POL, w/wo δ     | M1(+E2)   |                          | M1(+E2), ΔJ=1, Δπ=no           |
| E1+M2        | DCO stretched D, POL, w/wo δ     | E1+M2     |                          | E1+M2, ΔJ=1, Δπ=yes            |
| E1(+M2)      | DCO stretched D, POL, w/wo δ     | E1(+M2)   |                          | E1(+M2), ΔJ=1, Δπ=yes          |
| D+Q          | DCO stretched D with δ<1         | M1+E2     | M2 ruled out by RUL      | M1+E2, ΔJ=1, Δπ=no             |
| D+Q          | DCO stretched D with δ<1         | (M1+E2)   | Δπ=no from level scheme  | D+Q, ΔJ=1                      |
| D+Q          | DCO stretched D with δ<1         | (E1+M2)   | Δπ=yes from level scheme | D+Q, ΔJ=1                      |
| D(+Q)        | DCO stretched D with δ≈0         | (M1(+E2)) | Δπ=no from level scheme  | D(+Q), ΔJ=1                    |
| D(+Q)        | DCO stretched D with δ≈0         | (E1(+M2)) | Δπ=yes from level scheme | D(+Q), ΔJ=1                    |
| D+Q          | DCO seems like Q with δ>1        | M1+E2     | M2 ruled out by RUL      | M1+E2, ΔJ=0,1, Δπ=no           |
| D+Q          | DCO seems like Q with δ>1        | (M1+E2)   | Δπ=no from level scheme  | D+Q, ΔJ=0,1                    |
| D+Q          | DCO seems like Q with δ>1        | (E1+M2)   | Δπ=yes from level scheme | D+Q, ΔJ=0,1                    |
| D+Q          | DCO consistent with ΔJ=0 and δ<1 | M1+E2     | M2 ruled out by RUL      | M1+E2, Δπ=no, Avoid using ΔJ=0 |
| D+Q          | DCO consistent with ΔJ=0 and δ<1 | (M1+E2)   | Δπ=no from level scheme  | Avoid using ΔJ=0               |
| D+Q          | DCO consistent with ΔJ=0 and δ<1 | (E1+M2)   | Δπ=yes from level scheme | Avoid using ΔJ=0               |
| D(+Q)        | DCO consistent with ΔJ=0 and δ≈0 | (M1(+E2)) | Δπ=no from level scheme  | Avoid using ΔJ=0               |
| D(+Q)        | DCO consistent with ΔJ=0 and δ≈0 | (E1(+M2)) | Δπ=yes from level scheme | Avoid using ΔJ=0               |
| D+Q          | γ(θ)/DCO mixed                   | M1+E2     | M2 ruled out by RUL      | M1+E2, ΔJ=0,1, Δπ=no           |
| D+Q          | γ(θ)/DCO mixed                   | (M1+E2)   | Δπ=no from level scheme  | D+Q, ΔJ=0,1                    |
| D+Q          | γ(θ)/DCO mixed                   | (E1+M2)   | Δπ=yes from level scheme | D+Q, ΔJ=0,1                    |
| D(+Q)        | γ(θ)/DCO mixed                   | (M1(+E2)) | Δπ=no from level scheme  | D(+Q), ΔJ=0,1                  |
| D(+Q)        | γ(θ)/DCO mixed                   | (E1(+M2)) | Δπ=yes from level scheme | D(+Q), ΔJ=0,1                  |
|              |                                  | [M1,E2]   | Purely from level scheme | Do not use to deduce Jπ        |

### Conversion Precedence Rules

If lifetime is available and rules out M2 by RUL, then D+Q can be converted to firm M1+E2.
If RUL does not rule out M2, then D+Q can be converted to tentative (M1+E2) if level scheme indicates Δπ=no.
RUL takes precedence over level scheme for this conversion.
If Δπ is unknown from level scheme or RUL does not rule out M2, keep the original multipolarity assignment with only D and Q labels.

---

## Capture Transitions

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

## Spin and Parity Assignment Reasoning Logic in the Adopted Dataset

### Scenario C: No Angular Distribution DCO Ratios or Mixing Ratios Given in Literature

#### Goal

Deduce the Jπ of a level by combining constraints from:
- **Feeding transitions** — γ rays populating the level (from capture resonances above)
- **Deexciting transitions** — γ rays depopulating the level (to lower levels below)

---

#### Multipolarity Selection Rules

| Transition Type                          | Apply       | Condition                                  |
| :--------------------------------------- | :---------- | :----------------------------------------- |
| **Primary feeding γ** (from resonances)  | **D or E2** | Always                                     |
| **Deexciting γ** (decay to lower levels) | **D or Q**  | Long or unknown lifetime                   |
| **Deexciting γ** (decay to lower levels) | **D or E2** | Short lifetime (RUL applies: M2 ruled out) |

*Note: Primary γ = capture transition from neutron/proton resonance*

---

#### Workflow Algorithm

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

#### Example 1: Fed by primary γ from 7/2-, 7/2+, and 5/2+

Fed by primary γ from 7/2- (D or E2):
3/2-, 5/2±, 7/2±, 9/2±, 11/2-

Fed by primary γ from 7/2+ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Fed by primary γ from 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 5/2±, 7/2±, 9/2+

Adopted: (5/2±, 7/2±, 9/2+)

#### Example 2: Fed by primary γ from 5/2-. Decay γ to 1/2+ and 5/2+ (Lifetime short, RUL applies, M2 ruled out)

Fed by primary γ (D or E2):
1/2-, 3/2±, 5/2±, 7/2±, 9/2-

Decay γ to 1/2+ (D or E2):
1/2±, 3/2±, 5/2+

Decay γ to 5/2+ (D or E2):
1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 3/2±, 5/2+

Adopted: (3/2±, 5/2+)

#### Example 3: Fed by primary γ from 7/2+. Decay γ to 5/2+ (Lifetime unknown, RUL does not apply, M2 allowed)

Fed by primary γ (D or E2):
3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Decay γ to 5/2+ (D or Q):
1/2±, 3/2±, 5/2±, 7/2±, 9/2±

**AND:** 3/2+, 5/2±, 7/2±, 9/2±

Adopted: (3/2+, 5/2±, 7/2±, 9/2±)

#### Example 4: Fed by primary γ from 1/2+,3/2+ (multi-valued initial). Decay γ to 1/2+ and 3/2+ (Lifetime short, RUL applies, M2 ruled out)

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

#### cL J$ Comment Style Rules

When writing primary transition lists in `cL J$` comments:

1. For primary transitions used to deduce Jπ of a level, do not use weak γ rays (Iγ < 5), γ rays with upper-limit intensity (`LT` in the `DRI` field), γ rays with questionable placement (`?` in col 80), or γ rays to final levels with uncertain or multi-valued Jπ.
2. List transitions in descending order of intensity, with the strongest first, to reflect the most probable deexcitation paths. If there are γ transitions to final levels with the same Jπ, include only the strongest one for that Jπ, as this is sufficient for Jπ deduction.
3. Example for one γ transition: `cL J$primary transition <E_gamma1>|g to <Jπ1> g.s.`
4. Example for multiple γ transitions: `cL J$primary transitions: <E_gamma1>|g to <Jπ1> g.s., <E_gamma2>|g to <Jπ2>, <E_level2>, and <E_gamma3>|g to <Jπ3>, <E_level3>.` Or, with specified intensities: `cL J$primary transitions with I|g>10: <E_gamma1>|g to <Jπ1> <E_level1> and <E_gamma2>|g to <Jπ2>, <E_level2>.` Or, with specified multipolarities: `cL J$primary transitions: <E_gamma1>|g, D(+Q), to <Jπ1>, <E_level1> and <E_gamma2>|g, D(+Q), to <Jπ2>, <E_level2>.`
5. Use Oxford comma style in multi-transition lists and keep existing other Jπ arguments. Example: `cL J$spin=1:4 from |g(|q) in {+33}S(p,|g). Primary transitions: 4328.7|g to 2+, 2157.9 level, 6486.2|g to 0+ g.s., and 6025.3|g to 1+, 461.01 level.`
