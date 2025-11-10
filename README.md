 # Evaluated Nuclear Structure Data File (ENSDF)

## Primary Purpose
This repository contains the datasets being evaluated by the FRIB Nuclear Data Group. 

## Core Components

### ENSDF Data Files
- **A=34 mass chain**: Ne34, Na34, Mg34, Al34, Si34, P34, S34, Cl34, Ar34, K34, Ca34.
- **A=35 mass chain**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35.
- **A=36 mass chain**: Ne36, Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36.
- **A=60 mass chain**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60.
- **Evaluation files**: `.ens` format with current evaluations
- **Reference files**: `.old` format from previous evaluations

### XUNDL Data Files
- **XUNDL submodule**: eXperimental Unevaluated Nuclear Data List (private repository)

### Processing Tools
- **`ens2pdf.py`**: Converts ENSDF files to PDF format using Java conversion tool
- **`.github/column_calibrate.py`**: Validates ENSDF 80-column format (L/G/E/B/DP records)
- **`.github/check_gamma_ordering.py`**: Verifies ascending energy order for L-records and G-records
- **`.github/check_averages.py`**: Verifies weighted vs unweighted average calculations
- **`.github/ensdf_1line_ruler.py`**: Quick single-line or file validation with visual ruler display
- **`.github/copilot-instructions.md`**: AI agent instructions for ENSDF formatting compliance




## Repository Architecture
```
├── A34/[Element]34/        # A=34 mass chain evaluation files
├── A35/[Element]35/new/    # Current A=35 evaluation files (*.ens) - 87 datasets
├── A35/[Element]35/old/    # Reference files from previous evaluation rounds (*.old)
├── A35/[Element]35/raw/    # Provenance: original paper data, intermediate outputs
├── A35/A35_submission.ens  # Complete A=35 mass chain submission file
├── A36/[Element]36/        # A=36 mass chain evaluation files
├── A60/[Element]60/        # A=60 mass chain evaluation files
├── XUNDL/                  # Unevaluated data (Git submodule → private repository)
├── ens2pdf.py              # PDF conversion tool (Java-based)
├── .github/                # Validation scripts and AI agent instructions
│   ├── column_calibrate.py       # 80-column format validator
│   ├── check_gamma_ordering.py   # Energy ordering validator
│   ├── ensdf_1line_ruler.py      # Quick format checker with visual ruler
│   ├── check_averages.py         # Average calculation verifier
│   └── copilot-instructions.md   # ENSDF AI agent rules and workflows
└── .gitmodules             # Git submodule configuration
```


## Statistics

**A=34 Mass Chain (2012 NDS)**:
- **11 nuclides**: Ne34, Na34, Mg34, Al34, Si34, P34, S34, Cl34, Ar34, K34, Ca34
- **83 datasets**: 2108 L-records, 3171 G-records, 13101 lines
- **Per-nuclide datasets**: Ne34 (1), Na34 (1), Mg34 (5), Al34 (3), Si34 (10), P34 (12), S34 (27), Cl34 (20), Ar34 (5), K34 (0), Ca34 (0)
- **Current status**: Evaluation in progress (1 dataset completed: Ar34)

**A=35 Mass Chain (2011 NDS)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **63 datasets**: 1793 L-records, 2941 G-records, 11068 lines
- **Per-nuclide datasets**: Ne35 (0), Na35 (1), Mg35 (3), Al35 (3), Si35 (4), P35 (7), S35 (10), Cl35 (24), Ar35 (9), K35 (2), Ca35 (0)

**A=35 Mass Chain (submitted)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **87 datasets**: 2065 L-records, 3003 G-records, 15081 lines
- **Per-nuclide datasets**: Ne35 (1), Na35 (2), Mg35 (3), Al35 (5), Si35 (6), P35 (12), S35 (14), Cl35 (28), Ar35 (11), K35 (3), Ca35 (3)

**A=36 Mass Chain (2012 NDS)**:
- **10 nuclides**: Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36
- **95 datasets**: 2267 L-records, 3340 G-records, 11212 lines
- **Per-nuclide datasets**: Na36 (0), Mg36 (6), Al36 (1), Si36 (4), P36 (5), S36 (16), Cl36 (20), Ar36 (35), K36 (5), Ca36 (3)
- **Current status**: Not yet started (all new/ folders empty)

**A=60 Mass Chain (2013 NDS)**:
- **13 nuclides**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60
- **Current status**: Evaluation in plan (1 dataset completed: Zn60)

**XUNDL Compilation & Review (2025)**:
- **6 papers processed**
- **9 nuclear datasets**: isotopes A=92 to A=127
- **7 review rounds completed** across all papers

**AI-Assisted Workflow Development**:
- First AI agent for ENSDF 80-column formatting developed at FRIB Nuclear Data Center
- Custom GitHub Copilot integration with ENSDF-specific validation tools
- Presented at the LECM2025 and USNDP2025 meetings


