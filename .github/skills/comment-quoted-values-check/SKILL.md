---
name: comment-quoted-values-check
description: >
  Use this skill when cross-checking all quoted values in cL J$ comment
  lines against L-record and G-record data fields in ENSDF adopted files.
  Detects mismatches in gamma energies, multipolarities, level energies,
  J-π values, and energy conservation violations. Fixes comment text
  only — never edits data records. Skip ruler and column validation
  (comment-only workflow).
argument-hint: [adopted.ens]
---

# Comment Quoted Values Cross-Check

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Cross-check all quoted values in `cL J$` comments against corresponding L-record and G-record data fields. Detect discrepancies between comment text and data records.

**Scope:**
- **Checks:** Quoted energies, multipolarities, and J-π values within `cL J$` comment lines
- **Fixes:** Comment text only — do NOT edit data record fields (L, G)
- **Data-record issues** (e.g., multipolarity at wrong column): Flag for separate handling
- **Validation:** Skip ruler, column calibration, and gamma ordering checks (this workflow edits comments only)

---

## ENSDF Record Reference
Be sure to follow the **Integral Understanding of Continuation Records and Comments (Column 6)** specified in `.github/agents/ENSDF-Agent.agent.md`.

### L-Record Fields Used

| Field | Columns | Purpose           |
| :---- | :------ | :---------------- |
| E     | 10–19   | Level energy      |
| J     | 23–39   | Spin-parity (J-π) |

Column 22 may be a readability space (some evaluators use column 22 as start of J field, which is acceptable).

### G-Record Fields Used

| Field | Columns | Purpose          |
| :---- | :------ | :--------------- |
| E     | 10–19   | Gamma-ray energy |
| M     | 33–41   | Multipolarity    |

Column 32 may be part of M field (some evaluators do not use readability space at column 32, which is acceptable).

---

## Value Types Checked

### 1. Gamma Energy
Quoted gamma energy must match G-record energy character-for-character.
- **Pattern:** `energy|g` (e.g., `1824.7|g`)
- **Requirement:** Exact string match

### 2. Multipolarity
Quoted multipolarity must match the G-record M field character-for-character.
- **Pattern:** `energy|g MULT` (e.g., `1824.7|g M1+E2`)
- **Equivalence:** a measured `D`/`Q`/`D+Q`/`D(+Q)` form and the electromagnetic character derived from it describe the same transition, so quoting the measured form for a record whose M field holds the character form is accepted, e.g. `D, |DJ=1` quoted for an `(E1)` record. The character derived from the level scheme must not be quoted back as evidence for that same level's Jπ (circular); see `.github/skills/gamma-selection-rules/SKILL.md`.
- **Zero tolerance** on multipole order — quoted `D` against an `M1+E2` record, or quoted `E2` against a `D` record, is a mismatch

### 3. Level Energy
Quoted level energy must match L-record energy character-for-character.
- **Pattern:** `to J-π, ENERGY level` or `from J-π, ENERGY level`; the designator may also be `resonance`
- **Coverage:** Every quoted level energy in a `cL J$` block is checked, including comments that quote no γ energy
- **Special Convention:** Comments use `g.s.` for ground state; data records show `0.0` — these are semantically equivalent (no error flagged)

### 4. J-π Notation
Quoted J-π must match the L-record J field character-for-character. Parentheses encode distinct physical meaning:
- `1/2+` — definite J and π
- `1/2(+)` — definite J, tentative π
- `(1/2+)` — tentative J and π
- `(1/2)+` — tentative J, definite π
- `(11/2)-` — tentative J, definite negative π (minus OUTSIDE parentheses)
- `(11/2-)` — tentative J and π (minus INSIDE parentheses)

### 5. Energy Conservation

For transitions quoted as `E_gamma|g to/from E_level`, verify:
- **E_initial - E_final ≈ E_gamma** (within ±2 keV warning, ±5 keV error)
- `to` direction: E_gamma = E_initial - E_final (de-excitation)
- `from` direction: E_gamma = E_final - E_initial (feeding transition)

---

## Comment Patterns Detected

| Pattern Example                           | Checks Performed                                                                      |
| :---------------------------------------- | :------------------------------------------------------------------------------------ |
| `1824.7\|g M1+E2 to 7/2-, 1991 level`           | γ vs G-record, mult vs G-record, level E vs L-record, J-π vs L-record, E conservation |
| `2061.6\|g D, \|DJ=1 from (11/2+), 5877.7 level` | Same as above (`from` reverses energy conservation)                                   |
| `1986\|g to 1/2+, 1572 level`                   | γ vs G-record, level E vs L-record, J-π, E conservation                               |
| `3594.5\|g Q, \|DJ=2 to 3/2+, g.s.`       | Same as above (g.s. treated as 0.0 keV)                                               |

---

## Error Classification

| Code                          | Severity | Description                               |
| :---------------------------- | :------- | :---------------------------------------- |
| `GAMMA_NOT_FOUND`             | ERROR    | No G-record matches quoted gamma energy   |
| `GAMMA_ENERGY_MISMATCH`       | ERROR    | Quoted gamma energy ≠ G-record E field    |
| `MULTIPOLARITY_MISMATCH`      | ERROR    | Comment multipolarity ≠ G-record M field  |
| `LEVEL_NOT_FOUND`             | ERROR    | No L-record matches quoted level energy   |
| `LEVEL_ENERGY_MISMATCH`       | ERROR    | Quoted level energy ≠ L-record E field    |
| `JPI_MISMATCH`                | ERROR    | Comment J-π ≠ L-record J field            |
| `MISSING_LEVEL_SUFFIX`        | ERROR    | Quoted level energy not followed by `level` |
| `ENERGY_CONSERVATION_WARNING` | WARNING  | \|E_initial - E_final - E_gamma\| > 2 keV |
| `ENERGY_CONSERVATION_ERROR`   | ERROR    | \|E_initial - E_final - E_gamma\| > 5 keV |

**Exit codes:** `0` = no errors; `1` = one or more errors found; `2` = file not found

---

## Workflow

### Step 1: Run Detection
```bash
python .github/scripts/check_quoted_values.py "path/to/adopted.ens"
```

Optional flags: `--tolerance N` (default 1.0 keV search window), `--debug` (verbose diagnostics)

### Step 2: Investigate Each Finding

For each discrepancy:
1. Read the comment line and its surrounding L/G-record context
2. Determine whether the comment or the data record is the source of truth
3. If comment is wrong → fix comment (Step 3)
4. If data record is wrong → flag for separate handling (do NOT fix in this workflow)
5. Update and debug the script only if needed to handle edge cases. Keep the script simple, straightforward, and robust.

### Step 3: Correct Comments

Fix ONLY comment text (`cL`, `2cL`, `3cL` lines) using `replace_string_in_file`.

- Rewrapped blocks: set `old_str` to the comment block plus the following record line, and `new_str` to the corrected block (every line padded to exactly 80 columns) plus that same record line. Content is then written verbatim; the final matched line keeps its own padding.
- A single-line `old_str` cannot fix line length: the original trailing padding survives after `new_str`, so a rewritten comment stays over-long or short.
- Length-neutral single-line fix: anchor on the line tail + its trailing pad + the opening token of the next line, and set `new_str` to the corrected fragment with `pad_new = pad_old − Δ` (Δ = character-count change of the fragment). No whole-block rewrite needed. If the line already ends at column 80 (pad 0), Δ must be 0 or the block must be rewrapped.
- The checker only parses `to/from J-π, ENERGY level` (comma required): normalize comma-less quotations by hand (e.g. `to 8+ 10650 level` → `to (8+), 10651.5 level`).
- Verify every touched line is exactly 80 columns (the checker ignores trailing padding, so it never reports these defects); retry with a corrected pad count where off.

### Step 4: Re-verify
```bash
python .github/scripts/check_quoted_values.py "path/to/adopted.ens"
```
Confirm zero errors.

Re-run the checker after any L-record J-π or level-energy edit: existing comment quotations immediately go stale and surface as `JPI_MISMATCH` or `LEVEL_ENERGY_MISMATCH`. Fix the comment text, never the L-record.

---

## Common Pitfalls

1. **J-π parentheses ignored:** `(11/2)-` ≠ `(11/2-)` — different physical meaning
2. **Multipolarity order substitution:** `D` ≠ `M1+E2`, `Q` ≠ `D+Q` — measured-to-character pairs (e.g. `D` and `(M1)`) are equivalent, but a different multipole order always is a mismatch
3. **Energy string mismatches:** `1991` ≠ `1991.27` — must match character-for-character
4. **Ground state notation:** `g.s.` in comments = `0.0` in data records (no error)
5. **Energy conservation not checked:** Always verify E_initial - E_final ≈ E_gamma

---

## Success Criteria

- All quoted values match data records character-for-character
- Every quoted level energy carries the `level` designator (`g.s.` exempt)
- All transitions satisfy energy conservation (|deviation| ≤ 2 keV)
- Zero errors returned by `check_quoted_values.py`
