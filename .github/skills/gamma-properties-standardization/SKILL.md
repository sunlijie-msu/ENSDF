---
name: gamma-properties-standardization
description: >
  Use this skill when standardizing multipolarity (M), mixing ratio (MR),
  angular correlation coefficients (A2, A4, A6), and polarization (POL) in
  ENSDF G-records. Extracts data from messy raw comment text, populates
  G-record fields, and adds standardized cG comment lines with proper
  subscript notation and {I} uncertainties.
argument-hint: [ENSDF file path]
---

# ENSDF Gamma Properties Standardization

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Extract M, MR, A2/A4/A6, and POL data from source/raw data and create properly formatted G-records with standardized `cG` comment lines.

## cG Comment Templates

**Multipolarity and mixing ratio:**

 `NUCID cG M,MR$from |g(|q) in NSR_keynumber or Reaction_Dataset.`
 `NUCID cG M,MR$from |g|g(|q)(DCO) in NSR_keynumber or Reaction_Dataset.`
 `NUCID cG M,MR$from |g|g(|q)(ADO) in NSR_keynumber or Reaction_Dataset.`

**Polarization:**

 `NUCID cG $POL=+/-value {Iunc} (NSR_keynumber).`
 `NUCID cG $Electric/Magnetic character from POL=+/-value {Iunc} (NSR_keynumber).`

**Angular correlation coefficients:**
 `NUCID cG $R{-ADO}=value {Iunc} (NSR_keynumber).`
 `NUCID cG $R{-DCO}=value {Iunc} (NSR_keynumber).`
 `NUCID cG $A{-2}=value {Iunc}, A{-4}=value {Iunc}, A{-6}=value {Iunc} (NSR_keynumber).`


## Formatting Rules

- Subscripts: `A{-2}`, `A{-4}`, `A{-6}` — never `A2`, `A4`, `A6`
- Uncertainties: `{Iunc}` integer format — never parentheses
- End statements with period


## Workflow

### 1. Understand the Data Landscape

Read the target file. Identify levels with M, MR, A2/A4, or POL data in comments. Create an inventory table.

### 2. Extract

- M, MR, DMR from cL/cG lines or inline text
- A2, A4, A6 coefficients and uncertainties
- POL values and uncertainties
- NSR references for each measurement

### 3. Update G-Records

- Create missing G-records or update existing ones
- Position M at column 33, MR at column 42, DMR at column 50
- Ensure every line is exactly 80 characters

### 4. Add Standardized cG Comments

- Add `M,MR$` line referencing NSR key and method
- Add `$A{-2}=...` line with subscript notation
- Add `$POL=...` line if polarization data exists

## Gotchas

