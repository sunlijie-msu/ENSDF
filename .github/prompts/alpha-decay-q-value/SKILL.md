---
name: alpha-decay-q-value
description: >
  Use this skill when calculating Q-alpha values from measured alpha energies
  and updating the Q field (cols 65-74) and DQ field (cols 75-76) in ENSDF
  P records. Uses exact kinematic formula Q = E_alpha * A/(A-4). Applies to
  single files or chains of alpha-decay datasets.
---

# Alpha Decay Q-Value Calculation and P Record Update

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Compute $Q_\alpha$ from the measured alpha energy $E_\alpha$ and populate the Q and DQ fields in the parent P record of each ENSDF alpha-decay dataset.

## Formula

$$Q_\alpha = E_\alpha \times \frac{A_\text{parent}}{A_\text{parent} - 4}$$

$$\delta Q_\alpha = \delta E_\alpha \times \frac{A_\text{parent}}{A_\text{parent} - 4}$$

Round both to the nearest integer (keV precision).

## P Record Field Layout

| Field | Columns (1-based) | Width |
| :--- | :--- | :--- |
| Q (Q-value) | 65–74 | 10 chars, left-justified |
| DQ (uncertainty) | 75–76 | 2 chars, left-justified |

## Input Sources

- $E_\alpha$ and $\delta E_\alpha$: from the A record (cols 10–19, 20–21) **or** from the `QP$From E|a=` comment line.
- $A_\text{parent}$: mass number of the parent nuclide (from NUCID in the P record).

## Workflow

### Step 1: Read $E_\alpha$ and $\delta E_\alpha$

From the `cP QP$` comment line (preferred, as it identifies the g.s.-to-g.s. transition):
```
219NP cP QP$From E|a=9015 keV {I16} g.s. to g.s. transition ...
```
Extract 9015 and 16.

Or directly from the daughter A record (cols 10–19 and 20–21).

### Step 2: Identify $A_\text{parent}$

Read cols 1–3 of the P record NUCID. For `219NP  P ...`, $A = 219$.

### Step 3: Compute and Round

```python
Q  = round(Ea * A / (A - 4))
DQ = round(DEa * A / (A - 4))
```

### Step 4: Write into P Record

- Cols 65–74 (index 64–73): `str(Q).ljust(10)`
- Cols 75–76 (index 74–75): `str(DQ).ljust(2)`
- Verify total line length = 80 chars.

```python
new_line = s[:64] + str(Q).ljust(10) + str(DQ).ljust(2) + s[76:80] + '\n'
```

### Step 5: Validate

Run ruler on the modified P record line:
```
python .github/scripts/ensdf_1line_ruler.py --line "modified line here"
```

## Example

| Parent | $A$ | $E_\alpha$ (keV) | $\delta E_\alpha$ | $Q_\alpha$ | $\delta Q$ |
| :----- | :-: | :--------------: | :---------------: | :--------: | :--------: |
| 219NP  | 219 | 9015             | 16                | **9183**   | **16**     |
| 215PA  | 215 | 8087             | 12                | **8240**   | **12**     |
| 211AC  | 211 | 7451             | 9                 | **7595**   | **9**      |
| 207FR  | 207 | 6762             | 8                 | **6895**   | **8**      |

## Common Errors

| Error | Cause | Fix |
| :---- | :---- | :-- |
| Q copied from $E_\alpha$ directly | Forgot kinematic factor | Always apply $A/(A-4)$ |
| DQ wrong | Used wrong $A$ or forgot to round | Recompute with correct $A$ |
| Line length ≠ 80 | `s[76:80]` truncated | Ensure source line is `.ljust(80)` before slicing |

## Notes

- For an alpha-decay chain, process each file independently; each file has its own $A_\text{parent}$.
- The P record Q field represents $Q_\alpha$ for the **parent** decay (g.s. to g.s.).
- Do **not** confuse with the daughter L-record energy (always 0 for g.s.).
