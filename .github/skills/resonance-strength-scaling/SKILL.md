---
name: resonance-strength-scaling
description: Scale resonance strengths (ωγ) in ENSDF cL comment lines by a given factor and apply specified relative uncertainties. Handles dual-threshold uncertainty (e.g., 30% above cutoff, 50% below cutoff). Uses PDG sig-fig convention for ENSDF {In} formatting. Comment-only workflow — skip ruler and column validation.
argument-hint: [REFERENCE FACTOR UNCERTAINTY_PERCENT THRESHOLD_EV UNCERTAINTY_BELOW_PERCENT]
---

# Resonance Strength Scaling in ENSDF Comment Lines

## Purpose

Scale `|w|g` (ωγ) resonance strength values from a specific NSR reference in `cL` comment lines by a constant factor, then assign relative uncertainties using the ENSDF `{In}` notation.

## When to Use

- A reference's resonance strengths need renormalization (e.g., updated standard)
- Relative uncertainties must be assigned or revised
- Bulk scaling of comment-line values from one NSR reference

## Prerequisites

- Target file: `*.ens` ENSDF file with cL comment lines containing `|w|g=X.X eV {In} (NSR_REF).`
- Know: scaling factor, relative uncertainty (%), any dual-threshold rules
- Know: which levels are in scope (e.g., above a certain energy, below the d-line)

## Workflow

### Step 1: Identify Targets

```python
# Find all target lines: cL comments with |w|g and the specific NSR reference
# Only below the d-line and above the minimum level energy
with open('file.ens', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'NSR_REF' in line and '|w|g' in line and i >= d_line_index:
        # This is a target
```

### Step 2: Extract Parent Level Energy

For each target cL line, walk backwards to find the parent L-record:
```python
for j in range(i-1, -1, -1):
    if lines[j][5:8] == '  L':
        level_energy = lines[j][9:19].strip()
        break
```

### Step 3: Compute Scaled Value and Uncertainty

```python
import math

factor = 2.21052631579  # example scaling factor
rel_unc_high = 0.30     # 30% for values >= threshold
rel_unc_low = 0.50      # 50% for values < threshold
threshold = 1.0 / factor  # threshold AFTER scaling (e.g., 0.4524 eV)

scaled = old_value / factor
rel_unc = rel_unc_low if scaled < threshold else rel_unc_high
unc = scaled * rel_unc
```

### Step 4: Apply PDG Significant Figure Convention

Per copilot-instructions.md Section 3:
- Leading digit of uncertainty 1, 2, or <35 → **2 significant figures**
- Leading digit ≥35, or 4-9 → **1 significant figure**

```python
mag = math.floor(math.log10(unc))
# Get leading digits
leading = int(round(unc / (10 ** (mag - 1))))
sig_figs = 2 if leading < 35 else 1
round_to = mag - 1 if sig_figs == 2 else mag

rounded_val = round(scaled, -round_to)
rounded_unc = round(unc, -round_to)

if round_to >= 0:
    val_str = '{:.0f}'.format(rounded_val)
    unc_int = int(round(rounded_unc))
else:
    decimals = -round_to
    val_str = '{:.{}f}'.format(rounded_val, decimals)
    unc_int = int(round(rounded_unc * 10**decimals))
```

### Step 5: Format ENSDF Comment Line

```
 35CL cL $|w|g=<val_str> eV {I<unc_int>} (NSR_REF).
```
- Pad to exactly 80 characters with trailing spaces
- Preserve any suffix text (e.g., `, possible doublet.`)

### Step 6: Apply Edits

Use `replace_string_in_file` or `multi_replace_string_in_file` with 3-line context blocks (prev + target + next) to ensure unique matching.

### Step 7: Validate

Since this is a **comment-only** task, skip ruler/column validation per FRIBND.agent.md.

Run verification:
- Count all target lines matches expected total
- All lines are exactly 80 characters
- All targets are below d-line
- Bidirectional positional check (first and last entries)
- Random 5% spot check with forward computation from original values

## Special Cases

### No Original Uncertainty
If the original value has no `{In}` (e.g., `|w|g=4.8 eV (1976Me12)`), apply the relative uncertainty to the scaled value normally.

### Dual-Threshold Uncertainty
Some references state different relative uncertainties for weak vs strong resonances:
- Example: 30% for ≥1 eV original (≥0.452 eV scaled), 50% for <1 eV original (<0.452 eV scaled)
- The threshold applies to the **pre-scaling** value or equivalently to the **post-scaling** value divided back

### Suffix Text Preservation
Lines with extra text after the NSR reference (e.g., `, possible doublet.`) must preserve that text exactly.

### Skip Specific Resonances
User may exclude specific resonances (e.g., "1213 resonance already cleaned"). Verify by checking the parent level's resonance energy in the S-field or via the level energy.

## PDG Convention Quick Reference

| Uncertainty Leading Digits | Sig Figs | Example |
|---|---|---|
| 10-34 | 2 | 0.0286 → {I29}, 0.132 → {I13} |
| 35-99 | 1 | 0.042 → {I4}, 0.38 → {I4} |
| Borderline 29.86→30 | 2→1 after rounding | Check after rounding |

## Common Pitfalls

1. **False positives in verification**: New scaled values may coincidentally match old value patterns from other entries (e.g., old 2.8→new 1.3, which looks like old 1.3)
2. **Line count changes**: Monitor file line count before/after edits to detect accidental line deletions
3. **Duplicate content lines**: Many targets have identical content; use 3-line context blocks for unique matching
4. **Reverse-computation round trips**: Verifying by back-computing may fail at rounding boundaries; always verify forward from original values
