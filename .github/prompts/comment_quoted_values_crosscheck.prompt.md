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

Quoted gamma energy must match G-record energy character-for-character.

- **Pattern:** `energy|g` (e.g., `1824.7|g`)
- **Match against:** G-record E field (columns 10–19)
- **Tolerance:** Search window for finding matching record only
- **Requirement:** Exact string match (e.g., `1824.7` must match `1824.7`, not `1824.70` or `1825`)

### 2. Multipolarity

Quoted multipolarity must match the G-record M field character-for-character.

- **Pattern:** `energy|g MULT` (e.g., `1824.7|g M1+E2`)
- **Match against:** G-record M field (columns 33–41)
- Brackets and parentheses carry physical meaning: `D` ≠ `(M1)` ≠ `M1` ≠ `[E2]`
- Zero tolerance — exact string match required

### 3. Level Energy

Quoted level energy must match L-record energy character-for-character.

- **Pattern:** `to ENERGY, J-π` or `from ENERGY, J-π` (e.g., `to 1991.27, 7/2-`)
- **Match against:** L-record E field (columns 10–19)
- **Tolerance:** Search window for finding matching record only
- **Requirement:** Exact string match (e.g., `1991.27` must match `1991.27`, not `1991` or `1991.3`)

**Special Convention — Ground State (g.s.):**
- Comments use `g.s.` notation for ground state transitions
- Data records store ground state energy as `0.0` keV
- These are semantically equivalent per ENSDF convention: `g.s.` in comments = `0.0` in L-record
- No error flagged for this valid mismatch

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
| `GAMMA_ENERGY_MISMATCH` | ERROR | Quoted gamma energy string ≠ G-record E field string |
| `MULTIPOLARITY_MISMATCH` | ERROR | Comment multipolarity ≠ G-record M field |
| `LEVEL_NOT_FOUND` | ERROR | No L-record matches quoted level energy within search window |
| `LEVEL_ENERGY_MISMATCH` | ERROR | Quoted level energy string ≠ L-record E field string |
| `JPI_MISMATCH` | ERROR | Comment J-π ≠ L-record J field |

**Exit codes:**
- `0` — No errors (all quoted values match exactly)
- `1` — One or more errors found (any mismatch)

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

All findings are errors that must be fixed:
- **String mismatches:** Quoted value differs from data record field
- **Not found:** No matching record exists within search window

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
exactly:
- `1991` → `1991.27` if L-record shows `1991.27`
- `1824.7` → `1824.70` if G-record shows `1824.70eld value:
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
4. **Energy string mismatches:** `1991` ≠ `1991.27` even if numerically close; must match character-for-character
5. **Incorrect direction:** `from` (feeding gamma) vs. `to` (de-exciting gamma) reference different levels
6. **Ground state notation:** Comments use `g.s.`, data records show `0.0` — these are equivalent per ENSDF convention (no error)
7. **Arbitrary acceptance thresholds:** Do not declare energy differences as "acceptable" — report all differences and let the evaluator decide

---

## Success Criteria

- All quoted gamma energies match G-record E fields character-for-character
- All quoted multipolarities match G-record M fields character-for-character
- All quoted level energies match L-record E fields character-for-character (or `g.s.` ↔ `0.0`)
- All quoted J-π values match L-record J fields exactly
- Zero errors returned by check_quoted_values.py

