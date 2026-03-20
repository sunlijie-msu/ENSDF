---
name: flag-expansion
description: >
  Use this skill when expanding FLAG= shorthand continuation records in
  ENSDF files into individual cG or cL comment lines. Maps each flag
  character (uppercase for energy source, lowercase for intensity source)
  to its defined description in the dataset header. Clears column 77 flag
  characters from data records and deletes original FLAG= continuation
  lines after expansion.
argument-hint: [ENSDF file]
---

# ENSDF Flag Expansion (Generalized)

## 1. Objective
Systematically expand shorthand `FLAG=` continuation records into individual `cG` or `cL` comments to improve human readability and convenience in data evaluation.

## 2. Character Mapping Pattern
Map characters within a `FLAG=` string to their respective comment lines defined in the dataset header.

### Energy Flags (Uppercase)
- **Mapping**: `[NUCID] cG E$E|g [Source description]`
- **Format**: Left-justify energy source starting at column 10.

### Intensity Flags (Lowercase)
- **Mapping**: `[NUCID] cG RI$[Source description]`
- **Format**: Left-justify intensity source starting at column 10.

## 3. Execution Procedure

### Step 1: Identification
- Locate all data records (L, G, B, E) and check **column 77** for a flag character.
- Locate continuation lines matching the pattern: `[NUCID]F G FLAG=[String]` or `[NUCID]F L FLAG=[String]`.
- Identify the parent record associated with these flags.

### Step 2: Expansion & Replacement
- Iterate through each flag character (either from column 77 or the `FLAG=` string).
- Generate a new `cL` or `cG` record for **each** character.
- **Requirement**: Use the `$` separator (standard ENSDF comment delimiter, e.g., `RI$`, `E$`, `J$`).
- **Placement**: Insert new lines immediately after the parent data record (and its existing comments).
- **Cleanup**: 
  - Clear the flag character from column 77 of the data record.
  - Delete the original `FLAG=` continuation line.

### Step 3: 80-Column Integrity
- Pad every generated comment line with trailing spaces to reach exactly 80 characters.
- Maintain field boundaries as defined in the 80-column manual.
