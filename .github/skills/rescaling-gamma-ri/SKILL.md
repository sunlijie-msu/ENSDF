---
name: rescaling-gamma-ri
description: Rescales G-record relative intensities (RI) and their uncertainties within a single adopted level block when the contributing datasets use different RI=100 normalization references.
---

# Rescaling Relative Intensities (Adopted Dataset)

ENSDF record/field definitions, column positions, uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Rules and spot-check policy: `.github/copilot-instructions.md`.

**Problem** — within a single level block, different datasets may place RI=100 on a different γ. Adopted RI are normalized per level, with the strongest γ set to RI=100. Therefore, every dataset cited in a `cG RI$` comment must be anchored to the same γ at RI=100.

**Scope** — G-records under one L-record in an adopted dataset (e.g., `ElementA_adopted.ens`) whose RI come from datasets with different RI=100 references. *Fill in:* the adopted RI standard, whose RI/DRI enters the fields verbatim = `[dataset]`; the datasets to rescale into `cG RI$other` = `[datasets]`.

1. Adopt the RI standard: its reference γ has RI=100. Copy its RI and DRI verbatim into the G-record fields.
2. Transcribe each dataset's reference RI/DRI from its source record or supplied source table; do not reuse an adopted value as a source value.
3. Compute k = RI_ref(adopted) / RI_ref(other) at the same physical reference γ, then multiply each other RI and uncertainty by k.
4. Round value and σ together per `.github/skills/rounding/SKILL.md`; align decimal places and avoid over-rounding σ.
5. Add `cG RI$other: RI' {Iσ'} from REACTION.`; delete superseded average comments and continuations.
6. Never average RI values with different references; rescaling exposes the disagreement.

**Safeguards** — verify level/gamma identity and source normalization before arithmetic. After editing, assert adopted fields are unchanged, rescaled comments match the calculation, and old average text is absent.

**Validation** — check RI/DRI columns 23-31 and exact changed-line scope; run `.github/scripts/column_calibrate.py` and `.github/scripts/check_gamma_ordering.py`. Follow `.github/copilot-instructions.md` for full rules.
