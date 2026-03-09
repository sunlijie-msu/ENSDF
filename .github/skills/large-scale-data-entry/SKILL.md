---
name: large-scale-data-entry
description: Bulk data entry from CSV tables into ENSDF L-records and G-records. Extracts level energies, gamma energies, intensities, DCO ratios (if available), and multipolarities (if available). Enforces bidirectional column mapping, blank-cell counting, ascending energy ordering, and random 5% spot-check validation. Use for large datasets of 50+ numeric data points from papers, tables, or CSV files.
argument-hint: [CSV file] [ENSDF file]
---

# Large-Scale Data Entry for ENSDF

## Overview
Use this skill for large-scale transfer of tabulated nuclear structure data from CSV files into ENSDF L-records and G-records.

## Core Task
Extract $E_i$ (excitation energy of the initial level) from the provided CSV file and populate the corresponding L-records in the ENSDF file.

A nuclear level may deexcite through multiple $\gamma$ transitions. Ensure that all transitions are converted to G-records under the correct L-record for the same $E_i$ value.

Extract $E_\gamma$ ($\approx E_i - E_f$) and $I_\gamma$ (gamma-ray intensity) for each $\gamma$-ray transition from the CSV file, and populate the `E` and `RI` fields in ENSDF G-records.

## Additional Column: Other Final Levels

When present, also process the `Other Ef` column, which contains $\gamma$ transitions to final levels not listed in the table header.

### Data Format
- Format: `Exf_value(Iγ_value)`
- Example: `6120(0.4)` indicates $E_f = 6120$ keV and $I_\gamma = 0.4$

### Processing Steps
1. **Unit conversion:** Convert MeV to keV when necessary. Example: `6.10 MeV -> 6102 keV`.
2. **Gamma-energy calculation:** Calculate $E_\gamma \approx E_i - E_f$.
3. **G-record creation:** Add a G-record with the calculated $E_\gamma$ and $I_\gamma$ value, maintaining ascending gamma-energy order within the level.

## Execution Notes
- Apply bidirectional column mapping before entering any data.
- Count blank cells explicitly; they affect column alignment.
- Preserve ascending order for both L-record energies and the G-record energies within each level block.
- Perform a reproducible random 5% spot-check before closing the task.

## Prompt Design Notes
- Keep prompt files concise and task-focused.
- Reuse repository instruction files and custom agents instead of duplicating detailed ENSDF rules in each prompt.
- Reference the relevant instruction or agent files when the skill depends on broader repository standards.
