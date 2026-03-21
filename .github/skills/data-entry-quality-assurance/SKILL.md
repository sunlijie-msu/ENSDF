---
name: data-entry-quality-assurance
description: >
  Use this skill when extracting 30 or more numeric data points from images,
  CSV files, or publication tables into ENSDF records. Enforces bidirectional
  column mapping, blank-cell counting, numerical exactness, and mandatory
  random 15% spot-check validation. Applies to any bulk data extraction or
  transcription task involving level energies, gamma energies, intensities,
  or uncertainties.
argument-hint: [source image/table] [extracted ENSDF data]
---

# Data Entry Quality Assurance

## Purpose

Validate accuracy and completeness of tabular data extraction for ENSDF data entry. This skill supplements the bidirectional positional check and random spot-check protocols defined in `copilot-instructions.md` Section 5 with ENSDF-specific extraction guidance.

## When to Use

ALL numerical data extraction/entry tasks

## Extraction Rules

- Output extracted data as a Markdown table; omit footnotes
- Focus on E_γ and relative intensity columns
- Match each E_γ to the correct L-record and G-record: E_γ ≈ E_i − E_f
- Preserve every decimal place, sign, and uncertainty exactly as in the source
- Keep the final extracted table at the end of the output; do not add content after it

## Workflow

### Step 1: Bidirectional Column Mapping

Follow the five-step bidirectional positional check defined in `copilot-instructions.md` Section 5

### Step 2: Numerical Exactness

Follow the Data Extraction Rules defined in `FIRBND.agent.md` Section 8.

### Step 3: Random Spot-Check

Follow the mandatory spot-check protocol in `copilot-instructions.md` Section 5

## Gotchas

- Blank cells shift all subsequent column positions — the most common cause of catastrophic misalignment
- AI models frequently fail at lower-right corners of large tables — apply extra scrutiny there
- When fixing column positions, adjust spacing only; never shift field data to wrong columns