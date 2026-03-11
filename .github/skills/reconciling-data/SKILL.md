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
- For this Cl34 reconciliation workflow, gamma energies that differ by about 1 to 2 keV between source and target are normally considered acceptable matches when the level context and transition pattern agree.

### Step 3: Build 80-Column Records

Merge source values with preserved metadata:
- Use `.adp` Level Energy, Gamma Energy, RI, DRI
- Keep `.ens` Multipolarity, Mixing Ratio, angular correlation comments
- Respect dataset-specific RI conventions already established in the target file:
- In this case, the 1983Wa27 RI data does not have uncertainty while the 1977Da02 RI data does.
	- If only a 1983Wa27 RI value/limit exists for a gamma, place that RI directly in the G-record RI and DRI fields and add no per-gamma RI provenance comment, because 1983Wa27 is already the file-level default RI source.
	- If only a 1977Da02 RI value/limit exists for a gamma, place that RI directly in the G-record RI and DRI fields and put `D` in column 77 of that G-record to indicate the 1977Da02 source.
	- If one source gives a finite RI value and the other gives only an upper limit, place the finite RI value in the G-record RI and DRI fields. Put the upper-limit value in a `cG RI$other: RI (19XXXxNN)` comment.
	- If both 1977Da02 and 1983Wa27 give upper limits, place the smaller upper limit in the G-record RI and DRI fields and put the larger upper limit in a `cG RI$other:` comment.
	- If both 1977Da02 and 1983Wa27 give finite RI values, place the 1977Da02 RI and DRI in the G-record fields, put `D` in column 77, and record the 1983Wa27 RI in a `cG RI$other:` comment.
	- If an ENSDF gamma energy does not have a credible source match within about 1 to 2 keV for that level, treat it as a possible wrong gamma-energy assignment: revise the G-record E field only when the correct source match is clear, and report that case explicitly.
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
| Copy E/RI without preserving the target file's RI provenance convention | Lost traceability or redundant source labeling | Preserve the established RI convention: use file-level default-source comments, column-77 RI flags when defined, and per-gamma RI comments only where needed |
| Match gammas only by exact energy equality | Wrong source-to-target mapping or missed transitions | For this workflow, allow about 1 to 2 keV EG differences when the level context and transition pattern support the match |
| Prefer 1983 finite RI over 1977 finite RI when both exist | Less-preferred RI source ends up in the adopted field | When both sources are finite, use 1977Da02 RI and DRI in the G-record with flag D, and put the 1983Wa27 RI in `cG RI$other:` |
| Keep a looser upper limit in the RI field when both sources only give limits | Adopted RI field becomes less informative | Put the smaller upper limit in the RI field and move the larger upper limit to `cG RI$other:` |
| Add per-gamma RI comments for a file-wide default source | Redundant clutter and inconsistent source labeling | Use the file-level RI general comment for default-source-only gammas |
| Omit a defined RI source flag for non-default single-source RI | Source provenance lost in the G record | Put the defined flag, such as `D` or `F`, in column 77 |
| Overwrite M/MR fields | Lost spectroscopy | Preserve target M/MR exactly |
| Misaligned decimal places | Parser failure | Use exact transcription; verify with ruler tool |
| Edit multiple records sequentially | Risk of file corruption | Use atomic replacement with surrounding context |
