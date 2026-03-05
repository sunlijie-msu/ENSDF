import sys

path = r'd:\X\ND\ENSDF\.github\copilot-instructions.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the start of section 5 and replace everything until the end.
start_marker = '## 5. Tabular Data Extraction and Quality Assurance'
end_marker = 'Order comments at the beginning of `Adopted.ens` files as follows:'

if start_marker in content:
    header_up_to_5 = content.split(start_marker)[0]
    
    new_sections = """## 5. Tabular Data Extraction and Data Entry Quality Assurance

**CRITICAL REQUIREMENT:** For ALL data entry tasks involving multiple numeric values (gamma transitions, level energies, intensities, half-lives, etc.), you MUST execute BOTH quality assurance checks before claiming task completion: Bidirectional Positional Check and Random Spot Check.

### Trigger Conditions

Execute these checks immediately when any of the following apply:
-   The task involves entering ≥50 numeric data points.
-   The request mentions "data entry," "extract data," or "format tabular data."
-   Bulk numeric input from source tables, figures, or publications is required.
-   Arithmetic-intensive work (calculations, conversions, averaging) is performed.

### Forbidden Behaviors

-   Claiming "task complete" without executing both checks.
-   Skipping checks because data "looks correct."
-   Performing checks mentally without documented evidence.
-   Using <100% verification rates (all sampled entries must pass).

---

### Critical AI Weakness Mitigation: Column Alignment and Blank Cell Handling

#### AI Frequent Failure Patterns to Avoid

-   Assuming column positions without explicit mapping.
-   Ignoring blank cells that shift subsequent data columns.
-   Single-direction counting (forward only) leading to off-by-one errors.
-   Mismatched header-to-data column associations.
-   Treating blank cells as non-existent rather than positional placeholders.

#### Mandatory Verification Protocol

1.  **Column alignment:** Explicitly map ALL columns, including blank ones. Never assume positions based on visible data alone.
2.  **Blank cells:** Count blank cells meticulously. Each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment.
3.  **Bidirectional verification:** Always cross-check both forward counting (header to data) and backward mapping (data to header) to ensure accurate alignment.

#### Critical Validation Steps for Tabular Data

-   **Step 1:** List all header columns explicitly, including blank column positions.
-   **Step 2:** Count blank cells between data columns as positional placeholders.
-   **Step 3:** Perform forward verification (match each header column to the corresponding data column).
-   **Step 4:** Perform backward verification (confirm each data column maps back to the correct header).
-   **Step 5:** Perform arithmetic validation (verify row/column calculations account for blank cell shifts).

#### Example Failure Prevention

```text
CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95
```

**CRITICAL COLUMN RULE:** When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).

### MANDATORY Random Spot-Check Protocol

**NON-NEGOTIABLE REQUIREMENT:** After ANY large-scale data entry task, you MUST perform random spot-check validation before claiming completion. This is NOT optional.

#### Execution Requirements

-   **Minimum sample size:** 5% of total entries (absolute minimum: 5 samples).
-   **Selection method:** Random sampling (neither sequential nor cherry-picked).
-   **Evidence required:** Generate a verification script showing:
    -   Total entry count.
    -   Sample size calculation (e.g., "200 entries → 5% = 10 samples").
    -   Randomly selected row or line numbers.
    -   Source data values for each sample.
    -   Verification results (PASS/FAIL per sample).

#### Verification Checklist (100% Pass Rate Required)

-   ✅ Arithmetic accuracy (no calculation errors).
-   ✅ Values match source data exactly (character-for-character).
-   ✅ Uncertainties match source data exactly.
-   ✅ Mapping accuracy (correct ENSDF fields used).
-   ✅ Positional alignment (no off-by-one errors).

#### Procedures for Error Discovery

If any errors are found:
1.  **Stop immediately** and do not claim completion.
2.  Identify the root cause (systematic vs. isolated error).
3.  Analyze the error pattern across all entries.
4.  Correct all instances of the identified error type.
5.  Re-run automated validation (`column_calibrate.py` and `check_gamma_ordering.py`).
6.  Perform a new random spot-check with different samples.
7.  Repeat until a 100% pass rate is achieved.

#### Workflow Integration

-   Execute after automated validation passes (`column_calibrate.py` and `check_gamma_ordering.py`).
-   Execute after the Bidirectional Positional Check confirms endpoints.
-   Execute before claiming "task completed successfully."
-   Document findings in the compliance checklist for user verification.

#### Zero-Tolerance Enforcement

-   Tasks are incomplete until the spot-check passes with zero errors.
-   No exceptions for "simple" or "small" data entry tasks.
-   Failure to execute constitutes failure to complete the assigned task.

---

## 6. Academic Standards

### Professional English Grammar

**Common corrections:**
-   **Spelling:** "other" (not "ohter"), "stopped" (not "stoped"), "using" (not "usign"), "coefficients" (not "coeffcients"), "deexciting" (not "deexiting"), "multipolarities" (not "multiporities"), "parentheses" (not "paretheses").
-   **Dittography:** Remove duplicated words (e.g., "the the").
-   **Hyphenation Rule:** [Number]-[Unit]-[Descriptor] [Noun]. Hyphenate compound adjectives occurring before a noun (e.g., "x-ray diffraction," "4-mm-long gas cell," "R-matrix theory"). Do not hyphenate when they are not adjectives before nouns (e.g., "emitted by x rays," "was 4 mm long").
-   **Consistency:** Always hyphenate "L-transfers" and "half-life."

### General Comment Ordering at the beginning of Adopted.ens Files

Order comments as follows:
1.  **Isotope Discovery:** Experimental details and references.
2.  **Production:** Methods and studies.
3.  **Decay Measurements:** Half-life and decay modes.
4.  **Radius Measurement:** Nuclear radius determinations.
5.  **Mass Measurements:** Mass spectrometry and Q-values.
6.  **Theoretical Calculations:** Models and predictions (always last).

---

## Document Structure

This document consists of six main sections:

1.  **ENSDF Comment Text Format Standards:** Superscripts, subscripts, Greek letters, mathematical symbols, and NSR citation format.
2.  **ENSDF 80-Column Format Standards:** NUCID field rules, L/G/DP/B/E record specifications, and critical formatting rules.
3.  **ENSDF Uncertainty Notation:** Data record fields (plain numbers) and comment lines ({In} notation).
4.  **ENSDF File Editing Workflow:** File protection, validation tools, and the Sacred Workflow method.
5.  **Tabular Data Processing and QA:** Bidirectional checks, random spot checks, and AI weakness mitigation.
6.  **Academic Standards:** Professional grammar and comment ordering for Adopted files.
"""
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header_up_to_5 + new_sections)
    print('Refinement applied.')
else:
    print('Start marker not found.')
