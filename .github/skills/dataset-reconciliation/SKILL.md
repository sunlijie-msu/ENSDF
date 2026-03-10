---
name: reconciling-data
description: Merge level and gamma-transition data from a source ENSDF file into a target ENSDF file while preserving existing spectroscopic metadata (multipolarities, mixing ratios, angular correlations). Use when updating ENSDF Adopted or Source datasets with experimental values from processed (.adp) files.
---

# Reconciling ENSDF Data

## Workflow: Merge Source Data into Target File

Track progress using this checklist:

```
Reconciliation Progress:
- [ ] Extract Level Energy and all Gamma records from source (.adp) file
- [ ] Capture existing Multipolarity (M) and Mixing Ratio (MR) from target (.ens) file
- [ ] Construct 80-column records combining source E/RI with target M/MR
- [ ] Execute atomic replacement of level block in target file
- [ ] Validate: 80-column compliance + ascending energy order
```

### Step 1: Extract Source Data

Locate the target level in the `.adp` file and extract:
- Level Energy and uncertainty
- All Gamma transitions: Energy, Intensity (RI), Uncertainty (DRI)
- All `cG RI` comment lines (weighted average notes, secondary source "Other" values)

### Step 2: Preserve Target Spectroscopy

From the `.ens` target file for each matching Gamma, capture:
- Multipolarity (`M`) in columns 33-41
- Mixing Ratio (`MR`) in columns 42-49
- Associated `cG M,MR$` or `cG $A{-2}=` comments

### Step 3: Build 80-Column Records

Merge source values with preserved metadata:
- Use `.adp` Level Energy, Gamma Energy, RI, DRI
- Keep `.ens` Multipolarity, Mixing Ratio, angular correlation comments
- Pad every line to exactly 80 characters

### Step 4: Replace and Validate

Use atomic string replacement (not sequential edits):
- Replace entire level block at once
- Run ruler validation: `python .github/scripts/ensdf_1line_ruler.py --file target.ens --show-only-wrong`
- Verify energy ordering: `python .github/scripts/check_gamma_ordering.py target.ens`

---

## Critical Rules

**Numerical Precision**
- Character-for-character transcription (no rounding)
- Copy uncertainty notation exactly: `{I51}`, `LT`, `GT`
- Leave blank fields blank

**80-Column Format**
- All inserted/modified lines must be exactly 80 characters
- For field column positions, see [.github/copilot-instructions.md](.github/copilot-instructions.md), section "2. ENSDF 80-Column Format Standards"

**Spectroscopic Integrity**
- Never overwrite existing M, MR, or angular correlation data
- Preserve associated comments (`cG M,MR$`, `cG $A{-2}=`)

---

## When to Use This Skill

✓ Synchronizing Adopted (`.ens`) file with source measurements from processed (`.adp`) file  
✓ Updating level/gamma energies and intensities while preserving multipolarities  
✗ Do NOT use if source and target isotopes differ  
✗ Do NOT use if target already has higher-quality data (verify intent first)

---

## Common Mistakes

| Mistake | Impact | Fix |
|---|---|---|
| Copy E/RI without `cG RI` comments | Lost traceability | Always extract and insert associated comments |
| Overwrite M/MR fields | Lost spectroscopy | Preserve target M/MR exactly |
| Misaligned decimal places | Parser failure | Use exact transcription; verify with ruler tool |
| Edit multiple records sequentially | Risk of file corruption | Use atomic replacement with surrounding context |
