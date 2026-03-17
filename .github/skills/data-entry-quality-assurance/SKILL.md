---
name: data-entry-quality-assurance
description: Comprehensive validation protocol for tabular data extraction and ENSDF data entry. Enforces bidirectional column mapping, blank-cell counting, numerical exactness, and mandatory random 5% spot-check validation. Use when extracting ≥30 numeric data points from images, CSV files, or tables.
argument-hint: [source image/table] [extracted ENSDF data]
---

# Data Entry Quality Assurance Protocol
Task: Tabular Data Extraction and Data Entry Quality Assurance.
Meticulous data extraction from the image and output table as a markdown file.
Omit the "Method of observation" column.
Omit footnotes.
Focus on Eγ, Relative intensity columns.
Carefully identify Eγ should match which L record's which G record.
Eγ≈Ei-Ef. Ei indicates the energy of the initial level, and Ef indicates the energy of the final level.

Ensure that every +/- sign absolutely matches the original image.
Keep the final extracted table at the end of the markdown. Do not add any extra content after the table!

Extract all numerical data and uncertainties with absolute fidelity to the source image. Preserve every decimal place exactly—do not round, omit, alter, or add digits. Example: 10.0 is 10.0, not 10 or 10.00!
Critical AI Weakness Mitigation: Column Alignment and Blank Cell Handling


Mandatory Bidirectional Positional Check


Column alignment: Explicitly map ALL columns, including blank ones. Never assume positions based on visible data alone.

Blank cells: Count blank cells meticulously. Each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment.

Bidirectional verification: Always cross-check both forward counting (header to data) and backward mapping (data to header) to ensure accurate alignment.


Critical Validation Steps for Tabular Data


Step 1: List all header columns explicitly, including blank column positions.

Step 2: Count blank cells between data columns as positional placeholders.

Step 3: Perform forward verification (match each header column to the corresponding data column).

Step 4: Perform backward verification (confirm each data column maps back to the correct header).

Step 5: Perform arithmetic validation (verify row/column calculations account for blank cell shifts).


Example Failure Prevention

CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95

CRITICAL COLUMN RULE: When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).


Mandatory Random Spot-Check Protocol

NON-NEGOTIABLE REQUIREMENT: After ANY large-scale data entry task, you MUST perform random spot-check validation before claiming completion. This is NOT optional.


Execution Requirements


Minimum sample size: 5% of total entries (absolute minimum: 5 samples).

Selection method: Random sampling (neither sequential nor cherry-picked).

Evidence required: Generate a verification script showing:

Total entry count.

Sample size calculation (e.g., "200 entries → 5% = 10 samples").

Randomly selected row or line numbers.

Source data values for each sample.

Verification results (PASS/FAIL per sample).