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
├── A34/[Element]34/        # A=34 mass chain evaluation (137 datasets, in progress)
│   ├── new/                # Current evaluation files (*.ens)
│   ├── old/                # Reference files from 2012 NDS
│   ├── raw/                # Original paper data and intermediate outputs
│   └── pdf/                # PDF documentation
├── A35/[Element]35/        # A=35 mass chain submission (97 datasets, submitted)
│   ├── new/                # Current evaluation files (*.ens)
│   ├── old/                # Reference files from 2011 NDS
│   ├── raw/                # Original paper data and intermediate outputs
│   └── pdf/                # PDF documentation
├── A36/[Element]36/        # A=36 mass chain (10 nuclides, planning phase)
├── A60/[Element]60/        # A=60 mass chain (13 nuclides, planning phase)
├── XUNDL/                  # Experimental Unevaluated Nuclear Data List (Git submodule)
├── .github/                # AI-Native Development Infrastructure
│   ├── agents/             # Custom Agents (FRIBND.agent.md)
│   ├── docs/               # Context Engineering (Theory & Manuals)
│   ├── prompts/            # Agentic Workflows (.prompt.md)
│   ├── scripts/            # Tooling Infrastructure (Python validators)
│   ├── skills/             # Specialized Agent Skills
│   └── copilot-instructions.md   # Global Instructions & ENSDF Standards
└── .gitmodules             # Git submodule configuration
```


## Evaluation Status

Overview of mass-chain evaluation progress across four baseline evaluations (2011–2013 NDS):

| Mass Chain | Status | Nuclides | Datasets (Baseline) | L-Records | G-Records | Lines | NDS Year |
|---|---|---|---|---|---|---|---|
| **A=34** | In Progress | 11 | 96 | 4,260 | 4,356 | 13,649 | 2012 |
| **A=35** | ✓ Submitted/Under Revision | 11 | 97 | 6,162 | 5,903 | 15,516 | 2011 |
| **A=36** | Planning | 10 | 108 | 4,122 | 3,847 | 11,777 | 2012 |
| **A=60** | Planning (Zn60 pilot) | 13 | 120 | 4,219 | 4,658 | 14,533 | 2013 |
| **Total** | — | 45 | 421 | 18,763 | 18,918 | 55,475 | — |

### A=34 Mass Chain (2012 NDS, Evaluation In Progress)

**Baseline Statistics**: 11 nuclides, 96 datasets, 4,260 L-records, 4,356 G-records, 13,649 lines

**Current Work**: 137 datasets in evaluation

| Nuclide | Baseline | Current | Status |
|---|---|---|---|
| Ne34 | 1 | 1 | In progress |
| Na34 | 2 | 3 | In progress |
| Mg34 | 6 | 12 | In progress |
| Al34 | 4 | 11 | In progress |
| Si34 | 11 | 21 | In progress |
| P34 | 13 | 22 | In progress |
| S34 | 28 | 31 | In progress |
| Cl34 | 21 | 21 | In progress |
| Ar34 | 6 | 12 | In progress |
| K34 | 1 | 2 | In progress |
| Ca34 | 1 | 1 | In progress |

### A=35 Mass Chain (2011 NDS, Submitted For Publication)

**Baseline Statistics**: 11 nuclides, 74 datasets, 3,890 L-records, 4,007 G-records, 11,240 lines

**Current Submission**: 97 datasets, 6,162 L-records, 5,903 G-records, 15,516 lines — **✓ Submitted/Under Revision**

| Nuclide | Baseline | Submitted | Status |
|---|---|---|---|
| Ne35 | 0 | 1 | ✓ Submitted |
| Na35 | 2 | 3 | ✓ Submitted |
| Mg35 | 4 | 4 | ✓ Submitted |
| Al35 | 4 | 6 | ✓ Submitted |
| Si35 | 5 | 7 | ✓ Submitted |
| P35 | 8 | 12 | ✓ Submitted |
| S35 | 11 | 15 | ✓ Submitted |
| Cl35 | 25 | 29 | ✓ Submitted |
| Ar35 | 10 | 12 | ✓ Submitted |
| K35 | 3 | 4 | ✓ Submitted |
| Ca35 | 1 | 4 | ✓ Submitted |

### A=36 Mass Chain (2012 NDS, Planning Phase)

**Baseline Statistics**: 10 nuclides, 108 datasets, 4,122 L-records, 3,847 G-records, 11,777 lines

**Status**: Planning phase; evaluation to commence

**Nuclides**: Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36

**Per-Nuclide Baseline Datasets**: Na36 (1), Mg36 (8), Al36 (2), Si36 (5), P36 (6), S36 (17), Cl36 (21), Ar36 (36), K36 (6), Ca36 (4)

### A=60 Mass Chain (2013 NDS, Planning Phase)

**Baseline Statistics**: 13 nuclides, 120 datasets, 4,219 L-records, 4,658 G-records, 14,533 lines

**Status**: Planning phase; Zn60 pilot evaluation completed (10 datasets)

**Nuclides**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60

## Collaborative Work (2025–2026)

### XUNDL Compilation & Data Consistency Review

**Papers Processed**: 11 manuscripts
- 10 data consistency reviews
- 11 XUNDL compilations

**Coverage**: 23 nuclear datasets spanning mass numbers A=32 to A=220

**Review Completion**: 14 review rounds completed across 10 data consistency review papers

## AI-Enhanced Workflow Infrastructure

### FRIBND AI Agent

**Overview**: The first AI Agent designed for ENSDF 80-column formatting and nuclear data evaluation, developed and refined through daily evaluation tasks at the FRIB Nuclear Data Group.

**Presentations**:
- LECM2025 (Low Energy Community Meeting 2025)
- USNDP2025 (U.S. Nuclear Data Program Meeting 2025)


