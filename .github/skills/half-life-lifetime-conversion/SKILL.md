---
name: half-life-lifetime-conversion
description: >
  Update L-record half-life value
  T and uncertainty DT from adopted cL T$ lifetime values by converting |t to T{-1/2}
  with ln(2), applying ENSDF uncertainty notation, unit scaling, and validation.
argument-hint: "[ENSDF file path]"
---

# Sync cL T$ Lifetime to L-Record T/DT Fields

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Recommended Operating Procedure

1. Read the adopted lifetime from the first `|t=`, `|t>`, or `|t<` in cL T$.
2. Decode comment uncertainty (`{In}` or `{I+n-m}`) in value units.
3. Convert with `T{-1/2}=|t|*ln(2)`; scale uncertainty by `ln(2)`.
4. Choose a natural unit (`FS`, `PS`, `NS`, ...): keep stored value not `>100`; if converted value is `<0.1`, scale down when the smaller unit gives `<=100`.
5. Round value/uncertainty together so DT is valid ENSDF data-field content.
6. Update one L-record at a time, then validate immediately.

## Core Rule

`cL T$` stores lifetime (`|t`), but L-record `T` stores half-life (`T{-1/2}`).

- Numeric: `T{-1/2}=|t|*ln(2)`.
- Symmetric uncertainty: `DT{-1/2}=D|t|*ln(2)`.
- Asymmetric uncertainty: Min and max are converted separately and then combined.
- Limits preserve direction: `|t>...` -> `T>...`, `|t<...` -> `T<...`.

- Follow uncertainty-in-last-digits notation.
See `.github/copilot-instructions.md` § ENSDF Uncertainty Notation Rules.

- Round the T value and DT uncertainty together so DT is a valid 1- or 2-digit.
- Example: `|t=649 fs {I190}` → `T{-1/2}=0.45 PS`, `DT=13`.

- Choose a natural T-field unit by scaling between `FS`, `PS`, `NS`, `US`, etc. so the stored final value is not `>100` or `<0.1`; if the converted value is `>100` or `<0.1`, scale up or down to the nearest appropriate unit.
- Example: 
  - `T{-1/2}=650 FS {I80}` should be converted to `T{-1/2}=0.65 PS {I8}`
  - `T{-1/2}=650 PS {I10}` should be converted to `T{-1/2}=0.650 NS {I10}`.

- Avoid introducing unjustified or misleading extra digits.
- Do not over-truncate digits; keep physically faithful bounds.
- Example: `|t<2 fs` → `T{-1/2}<1.4 FS`, not `T{-1/2}<1 FS`, which would change the original value by 40%.

## Validation

- Run a reproducible random spot-check focused on transformation correctness (`|t` -> `T{-1/2}`, decoded uncertainty -> `DT`).
- After each edit: `python .github/scripts/ensdf_1line_ruler.py --line "<exact 80-char line>"`
- After all edits:
  - `python .github/scripts/column_calibrate.py "file.ens"`
  - `python .github/scripts/check_gamma_ordering.py "file.ens"`

