---
name: resonance-strength-scaling
description: >
  Use this skill to scale relative intensity comments in ENSDF datasets by
  normalizing the strongest line to 100, then append the scaled RI values with
  the source citation while preserving ENSDF formatting.
argument-hint: "[SOURCE_CITATION NORMALIZATION_ENERGY]"
---

# Resonance strength scaling

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Principle
Scale the strongest RI to 100.
- Reference transition: highest original intensity.
- Scale factor: `SF = 100 / RI_reference`.
- Apply `SF × original RI` to each entry, then round to 2 significant figures.

## Steps
1. Locate the target `G` record by matching `E_gamma` to the closest adopted level.
2. Read the existing `cG RI$other` comment and append the new scaled value.
3. Use `cG RI$other: [existing values], [new value] ([source NSR])`.
4. Omit entries where the original RI is unknown or absent.
5. Validate with `ensdf_1line_ruler.py` and `check_gamma_ordering.py`.

## Calculation table
| Final level `E_f` | `E_gamma = E_i - E_f` | Original RI | `SF × RI` | Scaled RI |
|---|---:|---:|---:|---:|
| [target] | [calculated] | [value] | [result] | [rounded] |

## Done when
- The strongest transition is normalized to exactly 100.
- Each appended value includes the correct citation.
- ENSDF comment formatting and 80-column layout remain valid.
