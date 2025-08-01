 # Evaluated Nuclear Structure Data File (ENSDF)

## Primary Purpose
This repository contains as the datasets being evaluated by the FRIB Nuclear Data Group. 

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
- **`.github/column_calibrate.py`**: Validates ENSDF column formatting (critical for 80-column fixed-width format)
- **`.github/check_averages.py`**: Verifies weighted vs unweighted average calculations in nuclear data




## Repository Architecture
```
├── A35/[Element]35/new/    # Primary ENSDF evaluation files (*.ens)
├── A35/[Element]35/old/    # Reference files from previous rounds (*.old)
├── A34/[Element]34/        # A=34 mass chain evaluation files
├── A60/[Element]60/        # A=60 mass chain evaluation files
├── XUNDL/                  # Unevaluated data (Git submodule → private repository)
├── ens2pdf.py              # PDF conversion tool
├── .github/                # Development tools and validation scripts
│   ├── column_calibrate.py
│   ├── check_averages.py
│   └── copilot-instructions.md
└── .gitmodules             # Git submodule configuration
```



## Statistics

As of current evaluation:
- **126 adopted levels** across all nuclides
- **93 adopted gamma transitions**
- **1300+ L records** (energy levels)
- **1669+ G records** (gamma transitions)
- **7869 total lines** of ENSDF data
- **63 non-adopted datasets** for comparison


