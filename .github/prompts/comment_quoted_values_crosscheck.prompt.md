# Comment Quoted Values Cross-Check

## Purpose

Cross-check all quoted values in `cL J$` comments against corresponding L-record and G-record data fields. Detect discrepancies between comment text and data records.

**Scope:**
- **Checks:** Quoted energies, multipolarities, and J-π values within `cL J$` comment lines
- **Fixes:** Comment text only — do NOT edit data record fields (L, G)
- **Data-record issues** (e.g., multipolarity at wrong column): Flag for separate handling
- **Validation:** Skip ruler, column calibration, and gamma ordering checks (this workflow edits comments only)

---

## Prerequisites

- Python 3.8+
- Detection script: `.github/scripts/check_quoted_values.py`

---

## ENSDF Record Reference

### L-Record Fields Used

| Field | Columns | Purpose |
|:------|:--------|:--------|
| E     | 10–19   | Level energy |
| J     | 23–39   | Spin-parity (J-π) |

### G-Record Fields Used

| Field | Columns | Purpose |
|:------|:--------|:--------|
| E     | 10–19   | Gamma-ray energy |
| M     | 33–41   | Multipolarity |

Column 32 is a readability space and must be blank.

### cL J$ Comment Format

- Column 7: `c` (comment indicator)
- Column 8: `L` (level comment type)
- Columns 10–80: Comment text
- `J$` identifier marks spin-parity discussion
- Continuation lines: `2cL`, `3cL`, etc.

Data-record identification requires col 6 = blank AND col 7 = blank. Comment records have col 7 = `c`. Continuation records have col 6 ≠ blank.

---

## Value Types Checked

### 1. Gamma Energy

Quoted gamma energy must correspond to a G-record energy.

- **Pattern:** `energy|g` (e.g., `1824.7|g`)
- **Match against:** G-record E field (columns 10–19)
- All energy differences are reported with exact values

### 2. Multipolarity

Quoted multipolarity must match the G-record M field character-for-character.

- **Pattern:** `energy|g MULT` (e.g., `1824.7|g M1+E2`)
- **Match against:** G-record M field (columns 33–41)
- Brackets and parentheses carry physical meaning: `D` ≠ `(M1)` ≠ `M1` ≠ `[E2]`
- Zero tolerance — exact string match required

### 3. Level Energy

Quoted level energy must correspond to an L-record energy.

- **Pattern:** `to ENERGY, J-π` or `from ENERGY, J-π` (e.g., `to 1991, 7/2-`)
- **Match against:** L-record E field (columns 10–19)
- Comments may use rounded integers (e.g., `1991` for L-record `1991.27`)
- All energy differences are reported; the evaluator determines appropriateness

### 4. J-π Notation

Quoted J-π must match the L-record J field character-for-character.

- **Pattern:** `level_energy, J-π` (e.g., `1991, 7/2-`)
- **Match against:** L-record J field (columns 23–39)
- Parentheses encode distinct physical meaning:
  - `1/2+` — definite J and π
  - `1/2(+)` — definite J, tentative π
  - `(1/2+)` — tentative J and π
  - `(1/2)+` — tentative J, definite π
  - `(11/2)-` — tentative J, definite negative π (minus OUTSIDE parentheses)
  - `(11/2-)` — tentative J and π (minus INSIDE parentheses)
- Zero tolerance — every character must match exactly

---

## Comment Patterns Detected

| Pattern Example | Components Extracted |
|:----------------|:---------------------|
| `1824.7\|g M1+E2 to 1991, 7/2-` | γ energy, multipolarity, direction, level energy, J-π |
| `2061.6\|g D, \|DJ=1 from 5877.7 (11/2+)` | γ energy, multipolarity, direction, level energy, J-π |
| `1986\|g to 1572, 1/2+` | γ energy, direction, level energy, J-π |
| `3594.5\|g Q, \|DJ=2 to g.s., 3/2+` | γ energy, multipolarity, direction, g.s., J-π |

---

## Error Classification

| Code | Severity | Description |
|:-----|:---------|:------------|
| `GAMMA_NOT_FOUND` | ERROR | No G-record matches quoted gamma energy within search window |
| `GAMMA_ENERGY_DIFF` | INFO | Gamma energy differs from G-record value (exact difference reported) |
| `MULTIPOLARITY_MISMATCH` | ERROR | Comment multipolarity ≠ G-record M field |
| `LEVEL_NOT_FOUND` | ERROR | No L-record matches quoted level energy within search window |
| `LEVEL_ENERGY_DIFF` | INFO | Level energy differs from L-record value (exact difference reported) |
| `JPI_MISMATCH` | ERROR | Comment J-π ≠ L-record J field |

**Exit codes:**
- `0` — No errors (INFO items may exist)
- `1` — One or more errors found

---

## Workflow

### Step 1: Run Detection

```bash
python .github/scripts/check_quoted_values.py "path/to/adopted.ens"
```

Optional flags:

| Flag | Default | Description |
|:-----|:--------|:------------|
| `--tolerance N` | `1.0` | Search window in keV for finding matching records |
| `--debug` | off | Verbose parser diagnostics |

### Step 2: Review Findings

- **ERROR:** Must be resolved — string mismatches or missing records
- **INFO:** Energy differences — evaluator reviews whether rounding is appropriate

### Step 3: Investigate Each Finding

For each reported discrepancy:

1. Read the comment line and its surrounding L/G-record context
2. Determine whether the comment or the data record is the source of truth
3. If the comment is wrong → proceed to Step 4
4. If the data record is wrong → flag for separate handling (do NOT fix in this workflow)

### Step 4: Correct Comments

Fix ONLY comment text (`cL`, `2cL`, `3cL` lines). Use `replace_string_in_file` with 3–5 lines of context.

**J-π correction** — match L-record J field exactly:
- `(7/2+)` → `7/2(+)` if L-record shows `7/2(+)`
- `(11/2-)` → `(11/2)-` if L-record shows `(11/2)-`

**Multipolarity correction** — match G-record M field exactly:
- `D` → `(M1)` if G-record shows `(M1)`

**Energy correction** — match L/G-record E field value:
- `1991` → `1991.3` if L-record shows `1991.3`

### Step 5: Re-verify

```bash
python .github/scripts/check_quoted_values.py "path/to/adopted.ens"
```

Confirm zero errors.

---

## Common Pitfalls

1. **J-π parentheses ignored:** `(11/2)-` (tentative J, definite π⁻) ≠ `(11/2-)` (both tentative)
2. **Multipolarity at column 32:** G-record multipolarity belongs at columns 33–41; column 32 is a readability space
3. **Multipolarity substitution:** `D` (dipole, unspecified) ≠ `(M1)` (tentative M1) ≠ `M1` (definite M1)
4. **Editing data records:** This workflow fixes comments only; data-record issues require separate validation with ruler and column tools
5. **Incorrect direction:** `from` (feeding gamma) vs. `to` (de-exciting gamma) reference different levels
6. **Arbitrary acceptance thresholds:** Do not declare energy differences as "acceptable" — report all differences and let the evaluator decide

---

## Success Criteria

- Detection script reports zero errors
- All quoted gamma energies correspond to existing G-records
- All quoted multipolarities match G-record M fields exactly
- All quoted level energies correspond to existing L-records
- All quoted J-π values match L-record J fields exactly
- All energy differences have been reviewed by the evaluator
