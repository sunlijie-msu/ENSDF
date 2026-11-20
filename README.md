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
- **A=61 mass chain**: Ca61, Sc61, Ti61, V61, Cr61, Mn61, Fe61, Co61, Ni61, Cu61, Zn61, Ga61, Ge61.
- **Evaluation files**: `.ens` format with current evaluations
- **Reference files**: `.old` format from previous evaluations

### XUNDL Data Files
- **XUNDL submodule**: eXperimental Unevaluated Nuclear Data List (private repository)

### Publication Support
- **FRIENDS/**: Manuscripts and analysis material, including the 237Np Mössbauer-state linewidth paper.

## AI-Native Development Infrastructure (`.github/`)

Instructions, ENSDF-Agent, specialized skills, validation scripts, and edit-safety hooks live here.

## Repository Architecture

```
├── A34/[Element]34/        # A=34: submitted 2026-09-30; revisions ongoing
│   ├── new/                # Current evaluation files (*.ens)
│   ├── old/                # Reference files from 2012 NDS
│   ├── raw/                # Original paper data and intermediate outputs
│   └── pdf/                # PDF documentation
├── A35/[Element]35/        # A=35: published in NDS 211 (2026)
│   ├── new/                # Current evaluation files (*.ens)
│   ├── old/                # Reference files from 2011 NDS
│   ├── raw/                # Original paper data and intermediate outputs
│   └── pdf/                # PDF documentation
├── A36/[Element]36/        # A=36: chain assembled; not submitted
├── A60/[Element]60/        # A=60: active evaluation
├── A61/[Element]61/        # A=61: work started 2026-11-16
├── FRIENDS/                # Manuscripts and collaboration material
├── XUNDL/                  # Experimental Unevaluated Nuclear Data List (Git submodule)
├── .github/                # AI-Native Development Infrastructure
│   ├── agents/             # Custom Agents (ENSDF-Agent.agent.md)
│   ├── docs/               # Context Engineering (Theory & Manuals)
│   ├── hooks/scripts/      # Edit-safety hooks
│   ├── skills-dormant/     # Rare workflows, not auto-discovered by Copilot
│   ├── scripts/            # Tooling Infrastructure (Python validators)
│   ├── skills/             # Specialized Agent Skills
│   └── copilot-instructions.md   # Global Instructions & ENSDF Standards
└── .gitmodules             # Git submodule configuration
```

Skills in `.github/skills-dormant/` are excluded from Copilot discovery. To invoke one as a skill, move its folder into `.github/skills/`; `disable-model-invocation: true` keeps it manual-only.

The dormant `relative-gamma-intensity-scaling` workflow scales γ-ray RI comments; `resonance-strength-scaling` scales resonance ωγ values. Active `rescale-gamma-ri` reconciles adopted RI normalization within a level block.

## Evaluation Status

Four NDS baseline snapshots; statuses reflect current repository state.

| Mass Chain | Status | Nuclides | Baseline Datasets | Baseline L-Records | Baseline G-Records | Baseline Lines | NDS Year |
|---|---|---|---|---|---|---|---|
| **A=34** | Submitted 2026-09-30; revisions ongoing | 11 | 96 | 4,260 | 4,356 | 13,649 | 2012 |
| **A=35** | Published, NDS 211 (2026) | 11 | 74 | 3,890 | 4,007 | 11,240 | 2011 |
| **A=36** | Chain assembled; not submitted | 10 | 108 | 4,122 | 3,847 | 11,777 | 2012 |
| **A=60** | Active evaluation | 13 | 120 | 4,219 | 4,658 | 14,533 | 2013 |
| **A=61** | Work started 2026-11-16 | 13 | — | — | — | — | 2015 |
| **A=34–60 baseline total** | — | 45 | 398 | 16,491 | 16,868 | 51,199 | — |

### A=34 Mass Chain (2012 NDS baseline; submitted 2026-09-30, revisions ongoing)

**Baseline Statistics**: 11 nuclides, 96 datasets, 4,260 L-records, 4,356 G-records, 13,649 lines

**Current Work**: 126 `.ens` files; per-nuclide counts below.

| Nuclide | Baseline | Current `.ens` files | Status |
|---|---|---|---|
| Ne34 | 1 | 1 | In progress |
| Na34 | 2 | 2 | In progress |
| Mg34 | 6 | 6 | In progress |
| Al34 | 4 | 10 | In progress |
| Si34 | 11 | 16 | In progress |
| P34 | 13 | 18 | In progress |
| S34 | 28 | 34 | In progress |
| Cl34 | 21 | 24 | In progress |
| Ar34 | 6 | 12 | In progress |
| K34 | 1 | 2 | In progress |
| Ca34 | 1 | 1 | In progress |

### A=35 Mass Chain (published in NDS 211 (2026); 2011 NDS baseline)

**Baseline Statistics**: 11 nuclides, 74 datasets, 3,890 L-records, 4,007 G-records, 11,240 lines

**Current Evaluation**: 99 `.ens` files, 3,010 L-records, 3,583 G-records, 15,900 lines — **✓ Published**

| Nuclide | Baseline | Current `.ens` files | Status |
|---|---|---|---|
| Ne35 | 0 | 1 | ✓ Published |
| Na35 | 2 | 3 | ✓ Published |
| Mg35 | 4 | 4 | ✓ Published |
| Al35 | 4 | 6 | ✓ Published |
| Si35 | 5 | 7 | ✓ Published |
| P35 | 8 | 13 | ✓ Published |
| S35 | 11 | 16 | ✓ Published |
| Cl35 | 25 | 29 | ✓ Published |
| Ar35 | 10 | 12 | ✓ Published |
| K35 | 3 | 4 | ✓ Published |
| Ca35 | 1 | 4 | ✓ Published |

### A=36 Mass Chain (2012 NDS baseline; chain assembled 2026-09-30)

**Baseline Statistics**: 10 nuclides, 108 datasets, 4,122 L-records, 3,847 G-records, 11,777 lines

**Status**: Full chain is assembled in `A36_30September2026.ens`; per-dataset `.ens` files are present for S36 only.

**Nuclides**: Na36, Mg36, Al36, Si36, P36, S36, Cl36, Ar36, K36, Ca36

**Per-Nuclide Baseline Datasets**: Na36 (1), Mg36 (8), Al36 (2), Si36 (5), P36 (6), S36 (17), Cl36 (21), Ar36 (36), K36 (6), Ca36 (4)

### A=60 Mass Chain (2013 NDS baseline; active evaluation)

**Baseline Statistics**: 13 nuclides, 120 datasets, 4,219 L-records, 4,658 G-records, 14,533 lines

**Current Work**: 176 `.ens` files across all 13 nuclides.

**Nuclides**: Ca60, Sc60, Ti60, V60, Cr60, Mn60, Fe60, Co60, Ni60, Cu60, Zn60, Ga60, Ge60

### A=61 Mass Chain (2015 NDS baseline; work started 2026-11-16)

153 `.ens` files across 13 nuclides.

## Collaborative Work (2025–2026)

### XUNDL Compilation & Data Consistency Review

**Papers Processed**: 11 manuscripts
- 10 data consistency reviews
- 11 XUNDL compilations

**Coverage**: 23 nuclear datasets spanning mass numbers A=32 to A=220

**Review Completion**: 14 review rounds completed across 10 data consistency review papers

## AI-Enhanced Workflow Infrastructure

### ENSDF-Agent

**Overview**: The first AI Agent designed for ENSDF 80-column formatting and nuclear data evaluation, developed and refined through daily evaluation tasks at the FRIB Nuclear Data Group.
