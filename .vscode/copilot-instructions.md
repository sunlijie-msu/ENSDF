# Copilot Instructions

## Important Rules
- Never modify the first line or bottom line of any .ens file
- All edits must be made between these boundaries
- NEVER modify the indentation of the first line or bottom line of any .ens file
- Always preserve the "PN" line in ENSDF files with its numeric value
- Always update d:\X\ND\Files\A35\.vscode\change.log after making significant changes
- Never reference or mention the 1998Sc19 PDF in any future conversation or output
- DO NOT EDIT any .old files EVER! These are last round of evaluation ENSDF files that must be kept for reference
- Updated copilot-instructions.md with rule about not modifying first/last line indentation
- Fixed spelling and formatting errors in various reference comments
- DO NOT add extra spaces when adding Jπ values or other information to ENSDF records
- DO NOT shift existing numbers in each line when adding new information
- Focus primarily on K35 and P35 files - Ar35 files are already completed

## Spin-Parity (Jπ) Placement
- When adding spin-parity values to levels, place them exactly at column 23
- Example: `35K   L 4788      49 1/2+,3/2+`
  - Energy value (4788) remains at columns 11-15
  - Uncertainty (49) remains at columns 17-18  
  - Jπ (1/2+,3/2+) starts precisely at column 23
- Never add additional spaces that would shift uncertainty values

## Grammar and Spelling Fixes
- Common typos to watch for and fix:
  - "stoped" → "stopped"
  - "usign" → "using"
  - "coeffcients" → "coefficients"
  - "preocesses" → "processes"
  - "deduded" → "deduced"
  - "paticles" → "particles"
  - "mesured" → "measured"
- Add missing articles (a, an, the) and conjunctions (and, or) where appropriate
- Fix awkward sentence structures (e.g., "...but causing an IMME breakdown" → "...which caused an IMME breakdown")
- Maintain scientific accuracy while improving English readability

## Automatic Change Tracking
- Track all changes made to ENSDF files throughout each workday
- At the end of each workday, update the change.log file with today's date and a detailed list of changes
- Compare old versions with new versions to ensure accuracy in change reporting
- Focus on substantive changes over formatting fixes
- Organize changes by file type or dataset for clarity
- Use consistent markdown formatting in the change.log file

## Change.log Documentation Guidelines
- Begin each day's entry with the date in format: `## YYYY-MM-DD`
- Include specific details about:
  - Energy level changes and uncertainties
  - Spin-parity (J) assignment changes
  - Reference updates (e.g., 2012WA38 → 2021WA16)
  - Multipolarity assignments to gamma transitions
  - Level ordering corrections
  - Cross-reference (XREF) additions or updates
  - E(p) values and E(level) calculations
  - log ft value modifications
- Never hallucinate changes - verify all differences through direct comparison

## ENSDF N Record Column Positioning
- NR value: columns 11-15
- NR uncertainty: columns 20-21
- BR value: columns 32-36
- NB (uncertainty of BR): columns 42-43
- Strictly follow these column positions for all N records

## ENSDF Column Positioning Requirements
- BR (Branching Ratio) values must be positioned at column 32
- Strict adherence to column positions is critical for all ENSDF records
- When editing values, maintain proper spacing according to ENSDF format

## Formatting Guidelines for ENSDF Files

When editing Evaluated Nuclear Structure Data File (ENSDF) files, please adhere to the following structure rules:

### Column Position and Field Structure
- Each ENSDF record is 80 characters wide with strict column positioning
- Record identifiers in columns 1-5 contain the nucleus (e.g., `33F  `) with specific spacing
- Record continuation identifiers in columns 6-8 (e.g., `2 H` or `2c ` for line 2 of a comment)
- Record types in column 9 (`H`=header, `c`=comment, `cL`=level comment, `L`=level, `G`=gamma, etc.)
- Data fields in columns 10-80 with precise fixed-width column positions

### Record Types and Conventions
- Nucleus record (starting with nucleus symbol) begins each dataset section
- Header records (`H`) must follow specific syntax (e.g., `TYP=FUL$AUT=...`)
- Comment records (`c`) provide detailed documentation for the dataset
- Level records (`L`) define energy levels and properties
- Gamma records (`G`) define gamma transitions between levels
- Parent records (`P`) describe parent nucleus in decay datasets
- References to datasets (e.g., `XREF=ABCDEF`) follow specific formatting rules

### Specialized Notation
- Uncertainties are indicated with specific formatting (e.g., `90.3 MS   10` for 90.3 ± 1.0 ms)
- Special characters like `|g` (gamma), `|b` (beta), `|p` (parity), `|s` (sigma), etc.
- References indicated with year and author code (e.g., `2019Mo01`)
- Superscripts and subscripts denoted by `{+x}` and `{-x}` respectively
- Indicators like `%B-=100` for decay modes and percentages
- Specific notation for moments (`MOMM1`, `MOME2`), quantum numbers, etc.

### Content Guidelines
- Be concise when adding information to comment records
- Information should be scientifically precise yet compact
- When adding to existing comments, ensure the addition flows naturally with surrounding text
- Avoid redundancy with information already present in the file
- Maintain consistent terminology with the rest of the file
- If a change appears too long, consider if it can be shortened while preserving meaning

### Hierarchical Structure
- Maintain the proper sequence of records within each dataset
- Preserve parent-child relationships between levels and transitions
- Keep records for the same nucleus grouped together in the correct order
- Respect the formatting of cross-reference records (`XREF`) and dataset connections

### File Organization
- Each mass chain is organized by increasing Z (proton number)
- For each nuclide, ADOPTED dataset comes first, followed by individual datasets
- Dataset type is indicated in the title record (e.g., `ADOPTED LEVELS, GAMMAS`)

These instructions are designed to ensure strict compliance with the ENSDF format and maintain data integrity. Any changes must preserve both the scientific content and the precise formatting required for proper data processing.