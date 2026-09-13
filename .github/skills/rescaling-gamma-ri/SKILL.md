---
name: rescaling-gamma-ri
description: Rescales G-record relative intensities (RI) and their uncertainties within a single adopted level block when the contributing datasets use different RI=100 normalization references. Adopts the reference dataset's RI/DRI into the G-record fields and quotes the rescaled values in cG RI$other comments.
---

# Rescaling Relative Intensities (Adopted Dataset)

ENSDF record/field definitions, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Rules and spot-check policy: `.github/copilot-instructions.md`.

**Problem** — within a single level block, different datasets may place RI=100 on a different γ. Adopted RI are normalized per level, with the strongest γ set to RI=100. Therefore, every dataset cited in a `cG RI$` comment must be anchored to the same γ at RI=100.

**Scope** — G-records under one L-record in an adopted dataset (e.g., `ElementA_adopted.ens`) whose RI come from datasets with different RI=100 references. *Fill in:* the adopted RI standard, whose RI/DRI enters the fields verbatim = `[dataset]`; the datasets to rescale into `cG RI$other` = `[datasets]`.

1. Adopt the RI standard: its reference γ has RI=100. Copy its RI and DRI verbatim into the G-record fields.
2. For every other dataset, compute k = RI_ref(adopted) / RI_ref(other) at that reference γ.
3. Multiply each other RI and its uncertainty by k. Round value and σ together as described in `.github/skills/rounding/SKILL.md`, keeping decimal places aligned and avoiding over-rounding of σ.
4. For each affected γ, add `cG RI$other: RI' {Iσ'} from REACTION.`; delete the superseded average comments and their continuation lines.
5. Never average RI values that rest on different references — rescaling exposes the disagreement.

**Validation** — check the 80-column format, with RI in columns 23-29 and DRI in columns 30-31; then run `.github/scripts/column_calibrate.py` and `.github/scripts/check_gamma_ordering.py`.
