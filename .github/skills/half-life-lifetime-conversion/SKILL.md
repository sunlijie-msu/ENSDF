---
name: half-life-lifetime-conversion
description: >
  Use this skill when updating L-record T (half-life) and DT (uncertainty) fields to match
  the adopted lifetime values already verified in cL T$ comment lines. Transfers VALUE, UNIT,
  and uncertainty from each T$ comment into the corresponding L-record T field (cols 40–49)
  and DT field (cols 50–55). Applies to individual datasets and adopted ENSDF files.
argument-hint: "[ENSDF file path]"
---

# Sync cL T$ Lifetime to L-Record T/DT Fields

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Workflow

1. Extract the adopted `|t` value from the first `|t=`, `|t>`, or `|t<` in the cL T$ comment.
2. Convert lifetime to half-life with `T{-1/2}=|t|*ln(2)`.
3. Format T/DT using ENSDF data-field uncertainty rules from `.github/copilot-instructions.md`.
4. Edit one L record at a time and validate immediately.

## Core Rule

**cL T$ gives lifetime `|t`, but the L-record T field stores half-life.**

- Numeric value: `T{-1/2}=|t|*ln(2)`.
- Symmetric uncertainty: `DT{-1/2}=D|t|*ln(2)`.
- Limits keep their sense after scaling: `|t>...` → `T>...`, `|t<...` → `T<...`.

## Comment Decoding

- Decode comment uncertainties in `{In}` notation before applying `ln(2)`.
- Use the last-digits rule from `.github/copilot-instructions.md`.
- Examples:
  - `|t=3.0 fs {I25}` means `|t=3.0 fs`, `D|t=2.5 fs`.
  - `|t=7.7 fs {I17}` means `D|t=1.7 fs`.

## Formatting

- Choose a natural T-field unit by scaling between `FS`, `PS`, `NS`, `US`, ... so the stored value is not `>200`; if the converted value is `<0.2`, scale down when that yields a value `<=200` in the smaller unit.
- T field: cols 40–49, `VALUE UNIT`, left-justified.
- DT field: cols 50–55, digits or `GT`/`LT`, left-justified.
- After `ln(2)` conversion and unit selection, round the value and uncertainty together so DT is a valid 1- or 2-digit ENSDF last-digits field.
- For GT/LT limits, convert the bound with `ln(2)` and preserve enough precision that rounding does not materially change the bound.
- Do not introduce finer displayed precision than the source lifetime already has unless it is needed to avoid a materially distorted converted half-life.
- If the source `|t` is quoted as an integer in `fs` and the converted half-life remains in `FS`, integer-fs display is usually preferred for numeric values, but do not force it for converted limits or any case where dropping the decimal would significantly change the converted bound.
- Example: `|t<2 fs` → `T{-1/2}<1.4 FS`, not `1 FS`.
- Example: `|t=649 fs {I190}` → `T{-1/2}=0.45 PS`, `DT=13`.

## Validation

After each edit:
```
python .github/scripts/ensdf_1line_ruler.py --line "<exact 80-char line>"
```

After all edits:
```
python .github/scripts/column_calibrate.py "file.ens"
python .github/scripts/check_gamma_ordering.py "file.ens"
```

## Lessons

- Do **not** copy lifetime directly into the T field; always apply `ln(2)` first.
- Do **not** treat comment `{In}` as a literal uncertainty in units; decode it from the value’s decimal places first.
- Do **not** let `ln(2)` create a misleading extra decimal place in the same unit when the source value was quoted as an integer.
- Do **not** remove a decimal place if that would materially change the converted value or limit.
- Random spot-checks must test the transformation logic (`|t` → `T{-1/2}` and decoded uncertainty → DT), not just text transcription.
- Skip L records with no following cL T$ comment.
