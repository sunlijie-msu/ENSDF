---
name: gamma-selection-rules
description: >
  Use this skill when deducing nuclear level Jπ by combining constraints
  from feeding and deexciting gamma transitions using electromagnetic
  selection rules. Applies D/E2 rules to primary capture transitions,
  D/Q or D/E2 to deexciting gammas (lifetime-dependent), and takes AND
  intersection of all constraints. Handles multi-valued initial Jπ via
  union before intersection.
argument-hint: [feeding Jπ list] [deexciting transitions] [lifetime known?]
---

# Gamma Transition Selection Rules — Practical Workflow: Combining Jπ Constraints Logic

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

γ-ray multipolarity selection rules: `.github/docs/gamma_selection_rules.md`.

## Goal

Deduce the Jπ of a level by combining constraints from:
- **Feeding transitions** — γ rays populating the level (from capture resonances above)
- **Deexciting transitions** — γ rays depopulating the level (to lower levels below)

---

## Multipolarity Selection Rules

| Transition Type                          | Apply       | Condition                                  |
| :--------------------------------------- | :---------- | :----------------------------------------- |
| **Primary feeding γ** (from resonances)  | **D or E2** | Always                                     |
| **Deexciting γ** (decay to lower levels) | **D or Q**  | Long or unknown lifetime                   |
| **Deexciting γ** (decay to lower levels) | **D or E2** | Short lifetime (RUL applies: M2 ruled out) |

*Note: Primary γ = capture transition from neutron/proton resonance*

## 7. Practical Workflow: Combining Jπ Constraints Logic

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
3. Example for one γ transition: `cL J$primary transition <E_gamma1>|g to <Jπ1> g.s.`
4. Example for multiple γ transitions: `cL J$primary transitions: <E_gamma1>|g to <Jπ1> g.s., <E_gamma2>|g to <Jπ2>, <E_level2>, and <E_gamma3>|g to <Jπ3>, <E_level3>.` Or, with specified intensities: `cL J$primary transitions with I|g>10: <E_gamma1>|g to <Jπ1> <E_level1> and <E_gamma2>|g to <Jπ2>, <E_level2>.` Or, with specified multipolarities: `cL J$primary transitions: <E_gamma1>|g, D(+Q), to <Jπ1>, <E_level1> and <E_gamma2>|g, D(+Q), to <Jπ2>, <E_level2>.`
5. Use Oxford comma style in multi-transition lists and keep existing other Jπ arguments. Example: `cL J$spin=1:4 from |g(|q) in {+33}S(p,|g). Primary transitions: 4328.7|g to 2+, 2157.9 level, 6486.2|g to 0+ g.s., and 6025.3|g to 1+, 461.01 level.`