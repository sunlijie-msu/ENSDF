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

## Workflow

**Progress:**
- [ ] Step 1: Build replacement table from all T$ comments
- [ ] Step 2: Edit each L-record T/DT field (one at a time, validate after each)
- [ ] Step 3: Run final file validation

---

## Step 1 — Extract adopted value from T$ comment

**Source:** First occurrence after `|t=`, `|t>`, or `|t<` — stop at colon, `Others:`, or `Other:`.

| T$ pattern | T field content | DT field content |
|---|---|---|
| `\|t=V U {In}` | `V U` | `n` |
| `\|t>V U` | `V U` | `GT` |
| `\|t<V U` | `V U` | `LT` |

## Step 2 — Format and edit

**T field:** cols 40–49, 10 chars, `VALUE UNIT` left-justified, trailing spaces to fill.
**DT field:** cols 50–55, 6 chars, digits or `GT`/`LT` left-justified, trailing spaces.

After each edit, validate immediately:
```
python .github/scripts/ensdf_1line_ruler.py --line "<exact 80-char line>"
```
Confirm exit code 0 before proceeding.

## Step 3 — Final file validation

```
python .github/scripts/column_calibrate.py "file.ens"
```

---

## Gotchas

- **Skip** L records with no following cL T$ comment — leave T/DT untouched.
- **Unit conversion rule** — If the half-life value in the T field exceeds 200, convert to the bigger unit (value divide by 1000); otherwise use the smaller unit. cL T$ comment lifetime units match the source literature as it is and may not be converted; T field units are uppercase `FS`/`PS`/`NS`/`US` and must be converted if the value exceeds 200.
  - Example: `|t=286 fs {I45}` → T field `0.286 PS  `, DT `45    ` (digits unchanged).
  - The DT uncertainty digits are invariant under FS↔PS conversion.
- **Limits have no numeric DT** — `|t<V U` → T=`V U`, DT=`LT    `. Nothing else in DT.
- **E-notation** in the existing T field (e.g., `1.6E2 FS`) must be replaced when T$ gives plain digits.
