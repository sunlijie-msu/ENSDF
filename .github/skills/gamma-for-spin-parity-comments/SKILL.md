---
name: gamma-for-spin-parity-comments
description: >
  Use this skill when writing spin (J) and parity (π) comments for nuclear levels by listing multipolarities of deexciting and feeding gamma transitions.
---

# Writing Spin-Parity Comments from Gamma Transitions

- ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`.
- Gamma-ray multipolarity selection rules: `.github/docs/gamma_selection_rules.md`.
- G-record data field notation: `.github/skills/ensdf-gamma-record-format/SKILL.md`.

Examples of using gamma properties in `cL J$` comments to deduce Jπ:

- `cL J$<G-energy>|g to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, M1+E2, to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, M1+E2, |DJ=1 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, E2, |DJ=2 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, D, |DJ=1 to <Jπ>, <L-energy> level`
- `cL J$<G-energy>|g, Q, |DJ=2 to <Jπ>, <L-energy> level`

Bracketed multipolarities, such as `[E1]`, `[M1,E2]`, or `[E2]`, are deduced solely from the level-scheme Jπ changes between the initial and final levels of a transition. They need no provenance comment and cannot be used to deduce the Jπ of either level.

---

## `cL J$` Comment Rules

When writing primary-transition lists in `cL J$` comments:

1. For transitions used to deduce a level's Jπ, exclude weak γ rays (Iγ < 5), γ rays with upper-limit intensity (`LT` in the `DRI` field), γ rays with questionable placement (`?` in column 80), and γ rays to final levels with uncertain or multi-valued Jπ. If the user requests a weak γ ray and it helps further constrain the Jπ deduction, include it with the other transitions.
2. List transitions in descending order of intensity, with the strongest first, to reflect the most probable deexcitation paths. If multiple transitions go to final levels with the same Jπ, include only the strongest transition to each Jπ; this is sufficient for Jπ deduction.
3. For one γ transition, use `cL J$<E_gamma1>|g to <Jπ1> g.s.` When wrapping, break between words and keep each level energy with its `level` designator.
4. For multiple γ transitions, use one list with semicolons between transitions and one final period. Do not use commas or `and` between transitions, and do not place a period before the last transition. Example: `cL J$<E_gamma1>|g to <Jπ1> g.s.; <E_gamma2>|g to <Jπ2>, <E_level2>; <E_gamma3>|g to <Jπ3>, <E_level3>.` With specified intensities: `cL J$transitions with I|g>10: <E_gamma1>|g to <Jπ1> <E_level1>; <E_gamma2>|g to <Jπ2>, <E_level2>.` With specified multipolarities: `cL J$<E_gamma1>|g, D(+Q), to <Jπ1>, <E_level1>; <E_gamma2>|g, D(+Q), to <Jπ2>, <E_level2>.`
5. Separate the γ-transition list from other existing Jπ arguments with a period. Example: `cL J$<E_gamma1>|g to <Jπ1>, <E_level1>; <E_gamma2>|g to <Jπ2> g.s.; <E_gamma3>|g to <Jπ3>, <E_level3>. spin=<J1:J2> from |g(|q) in <dataset>. L=<L-transfer> from <Jπ_target> in <dataset>.`
