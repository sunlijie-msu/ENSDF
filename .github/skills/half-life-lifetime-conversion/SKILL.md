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
- **Unit must match T$ exactly** — if T$ uses FS, write FS; if PS, write PS. Never convert.
- **Limits have no numeric DT** — `|t<V U` → T=`V U`, DT=`LT    `. Nothing else in DT.
- **E-notation** in the existing T field (e.g., `1.6E2 FS`) must be replaced when T$ gives plain digits.
- **DT can be 1–3 digits** — pad with trailing spaces to fill 6 chars; never truncate.
