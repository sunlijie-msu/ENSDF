---
name: large-scale-data-entry
description: Bulk data entry from CSV tables into ENSDF L-records and G-records. Extracts level energies, gamma energies, intensities, DCO ratios (if available), and multipolarities (if available). Enforces bidirectional column mapping, blank-cell counting, ascending energy ordering, and random 5% spot-check validation. Use for large datasets of 50+ numeric data points from papers, tables, or CSV files.
argument-hint: [CSV file] [ENSDF file]
---

# Large-Scale Data Entry for ENSDF

## Task Description
Extract Ei (Excitation energy of the initial level) from the provided CSV file and populate the corresponding L-records in the ENSDF file.

A nuclear level may deexcite by multiple gamma transitions, so ensure that all gamma transitions are converted to G-records under the correct L-record with the same Ei value.

Extract Eg (Gamma energy ≈ Ei - Ef) and Iγ (Gamma intensity) for each γ-ray transition from the provided CSV file and populate the corresponding E and RI fields in ENSDF G-records.


## Additional: "Other Final Levels" Column

When present, also process the "Other Ef" column containing γ transitions to final levels not listed in the table header.

### Column Format
- **Data Format**: `Exf_value(Iγ_value)` (e.g., `6120(0.4)` indicates Ef = 6120 keV and Iγ = 0.4)

### Processing Steps
1. **Unit Conversion**: Convert MeV to keV (e.g., 6.10 MeV → 6102 keV) if necessary.
2. **Calculate Gamma Energy**: Eγ ≈ Ei - Ef.
3. **Create G-Record**: Add G-record with calculated Eγ and Iγ value, maintaining ascending energy order within the level.
