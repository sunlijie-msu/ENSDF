# Evaluated Nuclear Structure Data File (ENSDF)
Core nuclear structure and decay database containing evaluated (recommended) data for 3,171 nuclides, organized in over 17,269 individual datasets.

It serves as principal source of data for nuclear structure research, nuclear spectroscopy applications, Medical Internal Radiation Dose (MIRD), Nuclear structure and decay data (NuDat), and publications such as Nuclear Data Sheets and Table of Isotopes.

Nuclear data scientists from around the world contribute to this collaborative effort.

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

## AI & Validation Infrastructure (.github/)

This repository hosts the FRIB Nuclear Data Center's advanced AI-assisted evaluation workflow. The `.github` directory contains the core infrastructure for this system.

### 1. Validation Scripts (`.github/scripts/`)
Python-based tools for ensuring strict adherence to ENSDF formatting rules.
- **`column_calibrate.py`**: The primary validator for ENSDF 80-column format (L/G/E/B/DP records).
- **`check_gamma_ordering.py`**: Enforces ascending energy ordering for levels and gammas.
- **`ensdf_1line_ruler.py`**: A visual debugging tool for checking single-line alignment.
- **`angular_momentum_coupling.py`**: Calculates allowed final spins/parities based on conservation laws.
- **`ens2pdf.py`**: Wrapper for the Java-based ENSDF-to-PDF converter.
- **`Java_FormatCheck.py`**: Wrapper for the Java-based format checker.
- **`update_headers.py`**: Utility for batch updating ENSDF headers.

### 2. AI Custom Agents (`.github/agents/`)
Definitions for specialized AI agents designed to assist evaluators.
- **`FRIBND.agent.md`**: The master definition for the FRIB Nuclear Data agent, encoding the "Sacred Workflow" and expert knowledge.

### 3. Task Prompts (`.github/prompts/`)
Specialized prompt templates for specific, repeatable end-to-end tasks.
- **`average.prompt.md`**: For calculating weighted/unweighted averages.
- **`spin_parity.prompt.md`**: For J-pi assignment arguments.
- **`reaction_equations.prompt.md`**: For formatting nuclear reaction strings.
- **`large_scale_data_entry.prompt.md`**: For bulk data extraction and formatting.

### 4. Documentation (`.github/docs/`)
- **`copilot-instructions.md`**: The core rulebook for AI interactions (located in root of .github).
- **`angular_momentum_coupling.md`**: Theoretical background for the coupling tool.

## Repository Architecture
```
├── A34/[Element]34/        # A=34 mass chain evaluation files (New work in progress)
├── A35/[Element]35/new/    # Current A=35 evaluation files (*.ens) - 99 datasets
├── A35/[Element]35/old/    # Reference files from previous evaluation rounds (*.old)
├── A35/[Element]35/raw/    # Provenance: original paper data, intermediate outputs
├── A35/A35_submission.ens  # Complete A=35 mass chain submission file
├── A36/[Element]36/        # A=36 mass chain evaluation files
├── A60/[Element]60/        # A=60 mass chain evaluation files
├── XUNDL/                  # Unevaluated data (Git submodule → private repository)
├── .github/                # AI & Validation Infrastructure
│   ├── agents/             # AI Agent definitions (FRIBND.agent.md)
│   ├── docs/               # Documentation (PDFs, Guides)
│   ├── prompts/            # Task-specific prompt templates
│   ├── scripts/            # Python validation tools
│   └── copilot-instructions.md   # Core AI instructions
└── .gitmodules             # Git submodule configuration
```


## Statistics

**A=34 Mass Chain (2012 NDS)**:
- **11 nuclides**: Ne34, Na34, Mg34, Al34, Si34, P34, S34, Cl34, Ar34, K34, Ca34
- **96 datasets**: 4260 L-records, 4356 G-records, 13649 lines
- **Per-nuclide datasets**: Ne34 (1), Na34 (2), Mg34 (6), Al34 (4), Si34 (11), P34 (13), S34 (28), Cl34 (21), Ar34 (6), K34 (1), Ca34 (1)
- **Current status**: Evaluation in progress (145 datasets completed/in-progress)
- **New work**: Ne34 (1), Na34 (3), Mg34 (12), Al34 (11), Si34 (21), P34 (22), S34 (31), Cl34 (30), Ar34 (11), K34 (2), Ca34 (1)

**A=35 Mass Chain (2011 NDS)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **74 datasets**: 3890 L-records, 4007 G-records, 11240 lines
- **Per-nuclide datasets**: Ne35 (0), Na35 (2), Mg35 (4), Al35 (4), Si35 (5), P35 (8), S35 (11), Cl35 (25), Ar35 (10), K35 (3), Ca35 (1)

**A=35 Mass Chain (submitted)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **99 datasets**: 4288 L-records, 4680 G-records, 15248 lines
- **Per-nuclide datasets**: Ne35 (1), Na35 (3), Mg35 (4), Al35 (6), Si35 (7), P35 (13), S35 (15), Cl35 (29), Ar35 (12), K35 (4), Ca35 (4)

**A=36 Mass Chain (2012 NDS)**:
- **10 nuclides**: Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36
- **108 datasets**: 4122 L-records, 3847 G-records, 11777 lines
- **Per-nuclide datasets**: Na36 (1), Mg36 (8), Al36 (2), Si36 (5), P36 (6), S36 (17), Cl36 (21), Ar36 (36), K36 (6), Ca36 (4)
- **Current status**: Not yet started (all new/ folders empty)

**A=60 Mass Chain (2013 NDS)**:
- **13 nuclides**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60
- **120 datasets**: 4219 L-records, 4658 G-records, 14533 lines
- **Current status**: Evaluation in plan (10 datasets completed: Zn60)

**XUNDL Compilation & Review (2025)**:
- **7 papers processed**
- **12 nuclear datasets**: isotopes A=92 to A=127
- **Paper codes**: 2012DI06, 2025ABAA, 2025DEAA, 2025HEAA, 2025LAAA, 2025LIAA, 2025SHAA
- **7 review rounds completed** across all papers

**AI-Assisted Workflow Development**:
- First AI agent for ENSDF 80-column formatting developed at FRIB Nuclear Data Center
- Custom GitHub Copilot integration with ENSDF-specific validation tools
- Introduced at the LECM2025 and USNDP2025 meetings


