---
name: rescaling-gamma-ri
description: Rescales G-record relative intensities and uncertainties within one adopted level block when its individual datasets report different normalization references (G with RI=100), adopting the reference dataset's RI/DRI into the G-record fields and quoting the rescaled values in cG RI$other comments.
---

# Rescaling Relative Intensities (Adopted Dataset)

ENSDF record/field definitions, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Rules and spot-check policy: `.github/copilot-instructions.md`.

**Scope / task setup** — G records under one L record in an Adopted dataset (ElementA_adopted.ens)whose RI come from datasets with different 100-references. *Fill in:* adopted RI standard (its RI/DRI goes verbatim into the fields) = `[dataset]`; datasets to rescale into `cG RI$other` = `[datasets]`.

1. Take the reference dataset as adopted: its reference γ is RI=100. Adopt its RI and DRI verbatim into the G-record fields.
2. For every other dataset, k = RI_ref(adopted) / RI_ref(other) at that reference γ.
3. Scale each other RI and its uncertainty by the same k; round value and σ together per `.github/skills/rounding/SKILL.md`, aligning decimals and not over-rounding σ.
4. Add `cG RI$other: RI' {Iσ'} from REACTION.` to each affected γ; delete the superseded average comments and their continuations.
5. Never average RI resting on different references; rescaling exposes the disagreement.

Validate: 80 columns, RI at 23-29, DRI at 30-31, then `.github/scripts/column_calibrate.py` and `.github/scripts/check_gamma_ordering.py`.
