---
name: gamma-selection-rules
description: >
  Use this skill when deducing multipolarities for gamma transitions and then Jπ for
  nuclear levels by combining constraints from deexciting and feeding gamma transitions
  using electromagnetic selection rules. Applies D/E2 rules to primary capture
  transitions, D/E2 rules to deexciting gammas (if RUL applies), and takes AND
  intersection of all constraints. Handles multi-valued initial Jπ via union before
  intersection.
---

# Gamma Transition Selection Rules: Deducing Multipolarities and Jπ

- ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`.
- Spot-check policy: `.github/copilot-instructions.md`.
- γ-ray multipolarity selection rules: `.github/docs/gamma_selection_rules.md`.
- DCO and ADO interpretation rules: `.github/docs/angular_correlations_DCO.md`.
- γ-ray angular distribution, mixing ratios, and polarization: `.github/docs/gamma_angular_distribution_mixing_ratio_polarization.md`.
- M and MR field notation: `.github/skills/multipolarity-mixing-ratio/SKILL.md`.

---

## Goal

Deduce the multipolarity of γ-ray transitions from experimental data.
Deduce the Jπ of levels by combining constraints from:
- **Deexciting transitions** — γ rays depopulating the level (to lower-lying levels)
- **Feeding transitions** — γ rays populating the level (from higher-lying levels)

---

## Multipolarity Assignment Reasoning Logic in Individual Datasets

### Scenario A: Only Mixing Ratios and Spins Given in Literature

- If level scheme indicates ΔJ = 0 or 1, assign D+Q in M field.
- If level scheme indicates ΔJ = 2, assign Q+O in M field.
- If level scheme indicates ΔJ = 3, assign O in M field and note O+H and δ value in cG M,MR comment.

### Scenario B: DCO Ratios, Mixing Ratio, and Spins Given in Literature

#### Step 1: Look at DCO Ratios

**DCO Reference Gates**

- Gating on a stretched dipole (ΔJ = 1) transition yields $R_{DCO}(D)$.
- Gating on a stretched quadrupole (ΔJ = 2) transition yields $R_{DCO}(Q)$.
- Expected DCO values depend on experimental detection setups (see `.github/docs/angular_correlations_DCO.md`). The values below are for example purposes.

**DCO Decision Rules**

**If $R_{DCO}(D)$ ≈ 1.0 or $R_{DCO}(Q)$ ≈ 0.5:**

- Transition is stretched dipole (ΔJ = 1) dominant.
- Mark as **D**.

**If $R_{DCO}(Q)$ ≈ 1.0 or $R_{DCO}(D)$ ≈ 2.0:**

- Transition is stretched quadrupole (ΔJ = 2) dominant and with a possibly weaker dipole or octupole component.
- Mark as **Q**.
- Then look at spins, a less common case is if the level scheme indicates $J_i = J_f$:
- Mark as **ΔJ=0**.

**If $R_{DCO}$ is between two expected values or inconsistent with all expected values:**

- Mark as **Mixed**.

#### Step 2: Look at Mixing Ratio (δ) and Level Scheme Spin Change (ΔJ)

Based on the Step 1 classification:

**For Transitions Marked D**

- If δ is not given, assign D in M field.
- If |δ| < 1 is given, assign D+Q in M field.

**For Transitions Marked Q**

- If δ is not given, assign Q in M field.
- If |δ| < 1 is given, assign Q+O in M field.
- Then look at spins, the level scheme should indicate ΔJ = 2; but if it indicates ΔJ = 1, assign D+Q in M field and flag this discrepancy for user review.
- If |δ| > 1 is given, assign D+Q in M field because dipole is the weaker component.

**For Transitions Marked ΔJ=0**

- If δ is not given, assign D in M field and note "consistent with |DJ=0" in the cG comment after the DCO value.
- If |δ| < 1 is given, assign D+Q in M field and note "consistent with |DJ=0" in the cG comment after the DCO value.

**For Transitions Marked Mixed**

- If δ is not given, no need to assign M field.
- If δ is given:
    - If level scheme indicates ΔJ = 0 or 1, assign D+Q in M field.
    - If level scheme indicates ΔJ = 2, assign Q+O in M field.
    - If level scheme indicates ΔJ = 3, assign O in M field and note O+H and δ value in cG M,MR comment.

#### Step 3: Mixing Ratio Refinement

- If δ is given and does not overlap with 0, D+Q or Q+O remains unchanged.
- If δ is given and overlaps with 0, place the higher-order multipolarity in parentheses:
    - D+Q changes to D(+Q).
    - Q+O changes to Q(+O).

#### Step 4: Polarization Refinement

Apply these rules based on measured POL to assign electromagnetic character:

**Positive POL (Dominant Electric Character)**

- D → E1
- Q → E2
- D+Q → E1+M2
- D(+Q) → E1(+M2)
- Q+O → E2+M3
- Q(+O) → E2(+M3)

**Negative POL (Dominant Magnetic Character)**

- D → M1
- Q → M2
- D+Q → M1+E2
- D(+Q) → M1(+E2)
- Q+O → M2+E3
- Q(+O) → M2(+E3)

**If No POL Data Available**

- Do not assign E or M labels.
- Assign only D, Q, O multipolarities based on DCO decision rules above.

---

## Multipolarity Assignment Reasoning Logic in the Adopted Dataset

### Overview

To further constrain multipolarities (G-record M field) and then use them to deduce Jπ for each level (L-record Jπ field).

### Conversion Decision Table

| Individual G | Measurement                      | Adopted G | For G record M field     | For L record Jπ field          |
| ------------ | -------------------------------- | --------- | ------------------------ | ------------------------------ |
| M1           | DCO stretched D, POL             | M1        |                          | M1, ΔJ=1, Δπ=no                |
| E1           | DCO stretched D, POL             | E1        |                          | E1, ΔJ=1, Δπ=yes               |
| E2           | DCO stretched Q, POL             | E2        |                          | E2, ΔJ=2, Δπ=no                |
| M2           | DCO stretched Q, POL             | M2        |                          | M2, ΔJ=2, Δπ=yes               |
| Q            | DCO stretched Q                  | E2        | M2 ruled out by RUL      | E2, ΔJ=2, Δπ=no                |
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

If a lifetime is available and the Java transition-strength code run by humans excludes M2 by RUL, convert D+Q to firm M1+E2, and state the clause in the record's `cG M$`/`cG M,MR$` comment, e.g., `M2 ruled out by RUL.`

If RUL does not rule out M2, and if the level scheme gives a firm Δπ, convert D+Q to tentative (M1+E2), adding `|D|p=no from level scheme.` to cG comment.

No conversion: if neither basis exists, i.e., RUL does not exclude M2 and Δπ is unknown from level scheme, keep the measured assignment with only D and Q labels, and do not cite a conversion in the comment.

### Comment Examples

- `cG M$D+Q from |g(|q) in NSR_keynumber or Reaction_Dataset.`

- `cG M$M1, |DJ=1, from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`
- `cG M$E2, |DJ=2, from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`
- `cG M$M1+E2, |DJ=1, from |g|g(|q)(DCO) and |g|g(|q)(POL) in dataset.`

- `cG M$D+Q from |g(|q) in dataset. M2 ruled out by RUL.`
- `cG M$D+Q, |DJ=1, from |g|g(|q)(DCO) in dataset. M2 ruled out by RUL.`

- `cG M$D+Q from |g(|q) in dataset. |D|p=no from level scheme.`
- `cG M$D+Q, |DJ=1, from |g|g(|q)(DCO) in dataset. |D|p=no from level scheme.`

Use γ properties in `cL J$` comments to deduce Jπ:

- `cL J$<G-energy>|g to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, M1+E2, to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, M1+E2, |DJ=1 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, E2, |DJ=2 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, D, |DJ=1 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, Q, |DJ=2 to <Jπ>, <L-energy> level`

If D(+Q) is firm, the corresponding converted form is M1(+E2). The same logic applies to E1+M2.

A general comment in the ens file top block (`cG M,MR$`, `cG M(A)$`) can hardly cover all cases. So, to ensure data traceability, add a per-record `cG M$`/`cG MR$`/`cG M,MR$` comment to specify the source method and dataset.

Bracketed `[...]` multipolarities are solely deduced from level-scheme Jπ changes between the transition initial and final levels and need no provenance comment.

---

## Transitions

γ transitions are assumed to be dominated by the three lowest multipoles (E1, M1, E2). Higher orders are suppressed.

- D including E1 or M1: ΔJ = 0, 1; Δπ = Yes or No
- E2: ΔJ = 2; Δπ = No

### Examples: Deducing Jπ of a Final Level from Multipolarity and Jπ of the Initial Level

γ transition from 5/2+ Initial via D or E2:

- D {E1, M1}: Final 3/2±, 5/2±, 7/2±
- E2: Final 1/2+, 9/2+
- Combination: 1/2+, 3/2±, 5/2±, 7/2±, 9/2+

γ transition from 7/2- Initial via D or E2:

- D {E1, M1}: Final 5/2±, 7/2±, 9/2±
- E2: Final 3/2-, 11/2-
- Combination: 3/2-, 5/2±, 7/2±, 9/2±, 11/2-

If two γ transitions from 5/2+ and 7/2-, the "AND" intersection of the above two sets:

- Jπ of the final level: 3/2-, 5/2±, 7/2±, 9/2+

Considering the multipolarity is not directly determined by experimental evidence, the final Jπ is put in parentheses to indicate the assumptions made:

- Adopted: (3/2-, 5/2±, 7/2±, 9/2+)

---

## Spin and Parity Assignment Reasoning Logic in the Adopted Dataset

### Scenario C: No Angular Distribution DCO Ratios or Mixing Ratios Given in Literature

#### Workflow Algorithm

```text
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

*Parentheses in ENSDF denote tentative assignments based on assumed multipolarities.*

#### Example 1: Fed by γ from 7/2-, 7/2+, and 5/2+ (Lifetime unknown, RUL does not apply)

Fed by γ from 7/2- (D or E2):

3/2-, 5/2±, 7/2±, 9/2±, 11/2-

Fed by γ from 7/2+ (D or E2):

3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Fed by γ from 5/2+ (D or E2):

1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 5/2±, 7/2±, 9/2+

Adopted: (5/2±, 7/2±, 9/2+)

#### Example 2: Fed by γ from 5/2-. Decay γ to 1/2+ and 5/2+ (Lifetime short, RUL applies, M2 ruled out)

Fed by γ from 5/2- (D or E2):

1/2-, 3/2±, 5/2±, 7/2±, 9/2-

Decay γ to 1/2+ {firm D or E2}:

1/2±, 3/2±, 5/2+

Decay γ to 5/2+ {firm D or E2}:

1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 3/2±, 5/2+

Adopted: 3/2±, 5/2+ without parentheses.

#### Example 3: Decay γ to 7/2+. Decay γ to 5/2+ (Lifetime unknown, RUL does not apply)

Decay γ to 7/2+ (D or E2):

3/2+, 5/2±, 7/2±, 9/2±, 11/2+

Decay γ to 5/2+ (D or E2):

1/2+, 3/2±, 5/2±, 7/2±, 9/2+

**AND:** 3/2+, 5/2±, 7/2±, 9/2+

Adopted: (3/2+, 5/2±, 7/2±, 9/2+)

#### Example 4: Fed by primary γ from 1/2+,3/2+ (multi-valued initial). Decay γ to 1/2+ and 3/2+ (Lifetime short, RUL applies, M2 ruled out)

Fed by primary γ from **1/2+,3/2+** (D or E2):

- From 1/2+ via D or E2: 1/2±, 3/2±, 5/2+
- From 3/2+ via D or E2: 1/2±, 3/2±, 5/2±, 7/2+
- **OR (union):** 1/2±, 3/2±, 5/2±, 7/2+

Decay γ to 1/2+ (D or E2):

1/2±, 3/2±, 5/2+

Decay γ to 3/2+ (D or E2):

1/2±, 3/2±, 5/2±, 7/2+

**AND:** 1/2±, 3/2±

Adopted: (1/2,3/2)

*Note: When initial level has multiple Jπ values (e.g., 1/2+,3/2+), calculate allowed final states for EACH initial value separately, then take OR (union) before applying AND with other constraints.*

#### `cL J$` Comment Style Rules

When writing primary transition lists in `cL J$` comments:

1. For gamma transitions used to deduce Jπ of a level, do not use weak γ rays (Iγ < 5), γ rays with upper-limit intensity (`LT` in the `DRI` field), γ rays with questionable placement (`?` in col 80), or γ rays to final levels with uncertain or multi-valued Jπ.
2. List transitions in descending order of intensity, with the strongest first, to reflect the most probable deexcitation paths. If there are γ transitions to final levels with the same Jπ, include only the strongest one for that Jπ, as this is sufficient for Jπ deduction.
3. Example for one γ transition: `cL J$<E_gamma1>|g to <Jπ1> g.s.`
4. Example for multiple γ transitions: `cL J$<E_gamma1>|g to <Jπ1> g.s.; <E_gamma2>|g to <Jπ2>, <E_level2>; <E_gamma3>|g to <Jπ3>, <E_level3>.` Or, with specified intensities: `cL J$transitions with I|g>10: <E_gamma1>|g to <Jπ1> <E_level1>; <E_gamma2>|g to <Jπ2>, <E_level2>.` Or, with specified multipolarities: `cL J$<E_gamma1>|g, D(+Q), to <Jπ1>, <E_level1>; <E_gamma2>|g, D(+Q), to <Jπ2>, <E_level2>.`
5. Write existing other Jπ arguments end with period. Then list the γ transitions. Example: `cL J$spin=1:4 from |g(|q) in {+33}S(p,|g). 4328.7|g to 2+, 2157.9 level; 6486.2|g to 0+ g.s.; 6025.3|g to 1+, 461.01 level.`
