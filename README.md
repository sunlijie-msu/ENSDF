 # Evaluated Nuclear Structure Data File (ENSDF)

## Primary Purpose
This repository contains the datasets being evaluated by the FRIB Nuclear Data Group. 

## Core Components

### ENSDF Data Files
- **A=35 mass chain**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35.
- **A=34 mass chain**: Ne34, Na34, Mg34, Al34, Si34, P34, S34, Cl34, Ar34, K34.
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
├── A35/[Element]35/new/    # Current A=35 evaluation files (*.ens) - 83 datasets
├── A35/[Element]35/old/    # Reference files from previous evaluation rounds (*.old)
├── A35/[Element]35/raw/    # Provenance: original paper data, intermediate outputs
├── A35/A35_submission.ens  # Complete A=35 mass chain submission file
├── A34/[Element]34/        # A=34 mass chain evaluation files
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

## Raw / provenance data

- In order to make provenance clear, temporary and intermediate folders previously named `temp/` have been renamed to `raw/`.
- The `raw/` directories contain original data extracted from references (PDFs, extracted tables, per-paper ENSDF fragments) and intermediate processing outputs (ruler reports, .avg, .mrg, etc.) retained for traceability.
- A move log was created at `.github/raw_move_log.txt` listing all file moves performed during the workspace cleanup.

When producing finalized ENSDF evaluation files, copy or move verified outputs into the `new/` or `old/` trees as appropriate. Keep `raw/` as the immutable provenance store.

## Recent workspace cleanup

- **2025-10-06**: Renamed per-isotope `temp/` directories to `raw/` across the workspace to make file provenance explicit. See `.github/raw_move_log.txt` for details.
- **2025-10-25**: A35 mass chain evaluation nearing completion with 83 datasets across 11 nuclides (Ne through Ca). Submission file under final validation and formatting review.




## Statistics

**A=35 Mass Chain Evaluation (March 2025 - October 2025)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **98 datasets completed** across all nuclides
  - Ne35 (1), Na35 (3), Mg35 (4), Al35 (6), Si35 (7), P35 (13), S35 (15), Cl35 (29), Ar35 (12), K35 (4), Ca35 (4)
- **11 adopted levels datasets** (one per nuclide)
- **87 reaction/decay datasets** for non-adopted data

**XUNDL Compilation & Review (2025)**:
- **4 papers processed**: 
- **7 nuclear datasets**: isotopes A=99 to A=127
- **6 review rounds completed** across all papers

**AI-Assisted Workflow Development**:
- First AI agent for ENSDF 80-column formatting developed at FRIB Nuclear Data Center
- Custom GitHub Copilot integration with ENSDF-specific validation tools
- Presented at LECM2025 meeting


