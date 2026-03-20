---
name: reconciling-data
description: >
  Use this skill when merging level and gamma-transition data from a source
  ENSDF file (.adp or .mrg or .csv) into a target ENSDF file while preserving
  existing spectroscopic metadata (multipolarities, mixing ratios, angular
  correlations). Suitable for synchronizing Adopted files with processed
  source measurements or updating energies and intensities across datasets.
argument-hint: [source file, target file]
---

# Reconciling ENSDF Data

## Purpose

Merge source-file level and gamma data into a target file, combining updated E/RI values with preserved M/MR spectroscopy.

## When to Use

- Synchronizing an Adopted `.ens` file with processed `.adp` measurements
- Updating level/gamma energies and intensities while preserving multipolarities
- Merging RI data from multiple sources with provenance tracking

## When NOT to Use

- Source and target isotopes differ
- Target already has higher-quality data (verify intent first)

## Workflow

### Step 1: Extract Source Data

From the source file, extract for each level:

- Level energy and uncertainty
- All gamma transitions: energy, RI, DRI
- All `cG RI` comment lines (weighted averages, secondary "Other" values)

### Step 2: Preserve Target Spectroscopy

From the target file, capture for each matching gamma:

- Multipolarity (M, columns 33-41)
- Mixing ratio (MR, columns 42-49) and uncertainty (DMR, columns 50-55)
- Associated `cG M,MR$` and `cG $A{-2}=` comments

### Step 3: Gamma Matching

Match source gammas to target gammas by energy within a tolerance window (typically 1-2 keV, depending on dataset precision):

- If target gamma energy already has a credible match, keep the existing target E; update only RI, DRI, flags, and comments
- If no credible match exists, treat as possible wrong assignment — revise E only when the correct match is unambiguous; report the case explicitly
- Do not replace a credible existing energy merely to shift it toward one source value

### Step 4: RI Provenance Rules

When multiple sources contribute RI values, apply these precedence rules consistently. The user must specify the dataset-specific RI convention — the general pattern is:

| Scenario | G-Record RI/DRI | Column 77 | cG Comment |
|---|---|---|---|
| Only default-source RI exists | Default RI, DRI | (blank) | None needed |
| Only alternate-source RI exists | Alternate RI, DRI | Source flag | None needed |
| One finite, one upper limit | Finite RI, DRI | As appropriate | `cG RI$other:` with the limit |
| Both upper limits | Smaller limit | As appropriate | `cG RI$other:` with larger limit |
| Both finite RI values | Preferred source RI, DRI | Source flag | `cG RI$other:` with the other |

### Step 5: Build 80-Column Records

- Combine source E/RI with preserved target M/MR
- Pad every line to exactly 80 characters
- Apply field positions per `copilot-instructions.md` Section 2

### Step 6: Replace and Validate

Use atomic string replacement (entire level block at once):

```bash
python .github/scripts/ensdf_1line_ruler.py --file target.ens --show-only-wrong
python .github/scripts/check_gamma_ordering.py target.ens
```

Both must return exit code 0.

## Gotchas

| Mistake | Impact | Fix |
|---|---|---|
| Overwrite M/MR fields | Lost spectroscopy | Preserve target M/MR exactly |
| Match gammas by exact energy only | Missed transitions | Allow tolerance window appropriate to dataset |
| Replace credible existing E with nearby source value | Unnecessary churn | Keep existing E when match is credible |
| Add per-gamma RI comments for default source | Redundant clutter | Use file-level general comment for default source |
| Omit source flag for non-default RI | Provenance lost | Apply column 77 flag per established convention |
| Edit records sequentially | File corruption risk | Use atomic replacement for entire level block |
| Misaligned decimal places | Parser failure | Character-for-character transcription; verify with ruler |
