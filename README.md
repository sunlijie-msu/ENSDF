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

## AI-Native Development Infrastructure (`.github/`)

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
├── .github/                # AI-Native Development Infrastructure
│   ├── agents/             # Custom Agents (FRIBND.agent.md)
│   ├── docs/               # Context Engineering (Theory & Manuals)
│   ├── prompts/            # Agentic Workflows (.prompt.md)
│   ├── scripts/            # Tooling Infrastructure (Python validators)
│   └── copilot-instructions.md   # Global Instructions
└── .gitmodules             # Git submodule configuration
```


## Statistics

**A=34 Mass Chain (2012 NDS)**:
- **11 nuclides**: Ne34, Na34, Mg34, Al34, Si34, P34, S34, Cl34, Ar34, K34, Ca34
- **96 datasets**: 4260 L-records, 4356 G-records, 13649 lines
- **Per-nuclide datasets**: Ne34 (1), Na34 (2), Mg34 (6), Al34 (4), Si34 (11), P34 (13), S34 (28), Cl34 (21), Ar34 (6), K34 (1), Ca34 (1)
- **Current status**: Evaluation in progress (137 datasets in new/)
- **New work**: Ne34 (1), Na34 (3), Mg34 (12), Al34 (11), Si34 (21), P34 (22), S34 (31), Cl34 (21), Ar34 (12), K34 (2), Ca34 (1)

**A=35 Mass Chain (2011 NDS)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **74 datasets**: 3890 L-records, 4007 G-records, 11240 lines
- **Per-nuclide datasets**: Ne35 (0), Na35 (2), Mg35 (4), Al35 (4), Si35 (5), P35 (8), S35 (11), Cl35 (25), Ar35 (10), K35 (3), Ca35 (1)

**A=35 Mass Chain (submitted, under revision)**:
- **11 nuclides**: Ne35, Na35, Mg35, Al35, Si35, P35, S35, Cl35, Ar35, K35, Ca35
- **97 datasets**: 6162 L-records, 5903 G-records, 15516 lines
- **Per-nuclide datasets**: Ne35 (1), Na35 (3), Mg35 (4), Al35 (6), Si35 (7), P35 (12), S35 (15), Cl35 (29), Ar35 (12), K35 (4), Ca35 (4)

**A=36 Mass Chain (2012 NDS)**:
- **10 nuclides**: Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36
- **108 datasets**: 4122 L-records, 3847 G-records, 11777 lines
- **Per-nuclide datasets**: Na36 (1), Mg36 (8), Al36 (2), Si36 (5), P36 (6), S36 (17), Cl36 (21), Ar36 (36), K36 (6), Ca36 (4)
- **Current status**: Not yet started (all new/ folders empty)

**A=60 Mass Chain (2013 NDS)**:
- **13 nuclides**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60
- **120 datasets**: 4219 L-records, 4658 G-records, 14533 lines
- **Current status**: Evaluation in plan (10 datasets completed: Zn60)

**XUNDL Compilation & Review (2025–2026)**:
- **11 manuscripts processed** (10 data consistency reviews + 1 XUNDL compilation only)
- **23 nuclear datasets**: isotopes A=32 to A=220
- **NSR key numbers**: Confidential
- **14 review rounds completed** across 10 papers (data consistency reviews)

**AI-Enhanced Workflow Development**:
- FRIB ND AI Agent: The first AI Agent designed for ENSDF 80-column formatting has been developed and refined through daily evaluation tasks at the FRIB Nuclear Data Group.
- Introduced at the LECM2025 and USNDP2025 meetings


