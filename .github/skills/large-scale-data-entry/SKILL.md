---
name: large-scale-data-entry
description: Bulk data entry from CSV tables into ENSDF L-records and G-records. Extracts level energies, gamma energies, intensities, DCO ratios (if available), and multipolarities (if available). Enforces bidirectional column mapping, blank-cell counting, ascending energy ordering, and random 5% spot-check validation. Use for large datasets of 50+ numeric data points from papers, tables, or CSV files.
argument-hint: [CSV file] [ENSDF file]
---

# Large-Scale Data Entry for ENSDF

## Task Description
Extract Ei (Excitation energy of the initial level) from the provided CSV file and populate the corresponding L-records in the ENSDF file.
Extract Eg (Gamma energy), Iγ (Gamma intensity), Initial level for each γ-ray transition from the provided CSV file and populate the corresponding E and RI fields in ENSDF G-records.
DCO ratios should be added as comments following a G-record.


## Additional: "Other Final Levels" Column

When present, also process the "Other final levels" column containing γ transitions to final levels not listed in the table header.

### Column Format
- **Data Format**: `Exf_value(BR_value)` (e.g., `6.10(0.4)` indicates Exf = 6.10 MeV and BR = 0.4)

### Processing Steps
1. **Identify Final Level Energy**: Convert MeV to keV (e.g., 6.10 MeV → 6102 keV) and locate the exact energy in the ENSDF file.
2. **Calculate Gamma Energy**: Eγ = Exi - Exf.
3. **Create G-Record**: Add G-record with calculated Eγ and BR value, maintaining ascending energy order within the level.
