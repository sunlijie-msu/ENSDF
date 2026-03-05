---
name: comment-cleanup
description: Clean up and standardize cG E$ and cG RI$ comment lines in ENSDF files. Establishes a single default-source general comment and adds individual exceptions only where needed. Covers weighted averages, non-default dataset sources, and enforces ENSDF comment ordering (E$ → RI$ → M$ → MR$). Use when reviewing or writing gamma-ray source comments for a dataset.
argument-hint: [ENSDF file or dataset name]
---

# ENSDF Comment Cleanup Instructions

## General cG E,RI Comment Strategy

**Principle:** Establish the most common data source as default in a general comment, then document exceptions individually.

### General Comment Format
```
 NUCID cG E,RI$From {DOMINANT_DATASET} unless otherwise noted. E|g values 
 NUCID2cG without uncertainties are deduced from level-energy differences.       
```

### Individual Comment Rules

| Scenario | Action |
|----------|--------|
| E or RI from default dataset only | No individual comment needed |
| E|g without uncertainty | No comment needed (deduced from level difference) |
| Weighted/unweighted average from multiple datasets | Add cG E$ or cG RI$ with average details |
| Value from non-default dataset | Add cG E$ or cG RI$ stating source |
| Other values exist but not used for averaging | Add "other: VALUE from DATASET" |

### Comment Ordering (per ENSDF rules)
```
cG E$ → cG RI$ → cG M$ → cG MR$ → other identifiers
```

### Examples

**Weighted average:**
```
 34AR cG E$weighted average of 1197.5 {I4} from {+12}C({+24}Mg,{+34}Ar|g) and   
 34AR2cG 1196.5 {I4} from {+32}S({+3}He,n|g)                                    
```

**Non-default source with other value:**
```
 34AR cG RI$from {+32}S({+3}He,n|g). Other: 100 from {+12}C({+24}Mg,{+34}Ar|g)  
```

**Non-default source only:**
```
 34AR cG RI$from {+32}S({+3}He,n|g)                                             
```

### What to Avoid

- ❌ Redundant comments restating the default source
- ❌ Individual cG E,RI$ for gammas that match the general comment default
- ❌ Comments for deduced energies (no uncertainty = level difference)

## Execution Checklist

1. Identify dominant dataset for E,RI and set it in the general `cG E,RI$` comment.
2. For each gamma with quoted uncertainty:
	- From default only → no individual `cG E$`/`cG RI$` comment
	- From multiple datasets → add weighted/unweighted average comment
	- From non-default dataset → add source comment, with `Other:` values when applicable
3. Remove redundant individual comments that merely restate the default source.
4. Preserve ENSDF ordering for each gamma comment block:
	- `cG E$` → `cG RI$` → `cG M$` → `cG MR$` → other identifiers
5. Keep deduced E|g values (no uncertainty) undocumented at per-gamma level unless an explicit exception is required.

## Completion Criteria

- One clear default-source general comment exists for E,RI.
- Exception comments exist only where source differs from default or averaging is required.
- No redundant per-gamma default-source comments remain.
- Comment ordering follows ENSDF sequence rules.



### General Comment Ordering at the beginning of Adopted.ens Files

Order comments at the beginning of `Adopted.ens` files as follows:
1.  **Isotope Discovery:** Experimental details and references.
2.  **Production:** Methods and studies.
3.  **Decay Measurements:** Half-life and decay modes.
4.  **Radius Measurement:** Nuclear radius determinations.
5.  **Mass Measurements:** Mass spectrometry and Q-values.
6.  **Theoretical Calculations:** Models and predictions (always last).
