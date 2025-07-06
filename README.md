 # Nuclear Data Evaluation System (ENSDF)

## Primary Purpose
Evaluation and processing of nuclear structure data for the **A=35 mass chain** using the Evaluated Nuclear Structure Data File (ENSDF) format for international nuclear structure databases.

## Core Components

### ENSDF Data Files (A35 Directory Structure)
- **Nuclear isotope data**: A=35 chain covering Al35, Ar35, Ca35, Cl35, K35, Mg35, Na35, Ne35, P35, S35, Si35
- **Evaluation files**: `.ens` format with nuclear level schemes, gamma transitions, decay data
- **Reference files**: `.old` format from previous evaluation rounds

### Processing Tools
- **`ens2pdf.py`**: Converts ENSDF files to PDF format using Java conversion tool
- **`column_calibrate.py`**: Validates ENSDF column formatting (critical for 80-column fixed-width format)
- **`check_averages.py`**: Verifies weighted vs unweighted average calculations in nuclear data

### Additional Mass Chains
- **A34 and A60** evaluation projects
- **XUNDL** (eXperimental Unevaluated Nuclear Data List) processing

## Technical Stack
- **Python scripts** for data processing and validation
- **Java-based conversion tools** (McMaster-MSU-Java-NDS)
- **ENSDF format compliance** (strict 80-column formatting)
- **Git version control** for tracking nuclear data changes

## Key Features
- **Column-precise formatting validation** for nuclear databases
- **Statistical analysis** of nuclear measurements (weighted/unweighted averages)
- **PDF generation** from ENSDF source files
- **Cross-platform compatibility** (Windows/Linux/macOS)

## File Structure
```
├── A35/finished/[Element]35/new/    # Primary ENSDF evaluation files (*.ens)
├── A35/finished/[Element]35/old/    # Reference files from previous rounds (*.old)
├── A34/, A60/                      # Additional mass chain evaluations
├── XUNDL/                          # Experimental unevaluated data processing
├── ens2pdf.py                      # PDF conversion tool
└── .vscode/                        # Validation scripts & development tools
```

## Domain
Nuclear physics data evaluation and curation for international nuclear structure databases.

---

**For detailed usage instructions and workflows, see `.github/copilot-instructions.md`**

### Configuration
The workspace is configured for ENSDF development with:
- File associations: `*.ens` → log format for syntax highlighting
- 80-column rulers for ENSDF format compliance
- Specialized validation tools

## Usage

### PDF Generation
Convert ENSDF files to publication-ready PDFs:

```bash
# Convert single file
python ens2pdf.py Si35_adopted

# Convert with pattern matching
python ens2pdf.py "Si35_*"

# Convert all files for an element
python ens2pdf.py Si

# Convert and open in VS Code
python ens2pdf.py Si35_adopted --open
```

### Data Validation
Ensure ENSDF format compliance:

```bash
# Validate column alignment
python .vscode/column_calibrate.py "filename.ens"

# Check header formatting
python .vscode/column_calibrate.py "filename.ens" --header

# Detailed character mapping
python .vscode/column_calibrate.py "filename.ens" --detailed
```

### Change Tracking
Document modifications systematically:

```bash
# Check current status
git status

# Review specific changes
git diff HEAD~1 "filename.ens"

# Update change log (maintained in .vscode/change.log)
```

## ENSDF Format Standards

### Critical Requirements
- **80-column fixed format** with exact field positioning
- **Left-justified values** in all data fields
- **Strict column alignment** for automated parsing
- **Standardized record types** (L, G, N, P, etc.)

### Example Record Format
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
L-Record: 35P   L 1572.0    1  1/2+             2.29 PS  14        2        1.23     45
G-Record: 35P   G 1572.0    1  100.0  4   [E2]     1.23   0.45  0.0368 8   1.23     45
```

## Scientific Context

### Data Sources
- **International experimental facilities**: FRIB, RIKEN, GANIL, NSCL, ORNL, MSU, etc.
- **Multiple experimental techniques**: In-beam spectroscopy, decay studies, transfer reactions
- **Comprehensive literature review**: Published and unpublished experimental data

### Quality Assurance
- **Multi-level validation**: Automated format checking, scientific consistency review
- **Peer review integration**: Data consistency checking for journal submissions
- **Version control**: Complete change tracking and documentation

### Professional Standards
- **USNDP compliance**: U.S. Nuclear Data Program standards
- **NSDD integration**: International Network of Nuclear Structure and Decay Data
- **Publication readiness**: Professional PDF output for scientific publications

## Statistics

As of current evaluation:
- **126 adopted levels** across all nuclides
- **93 adopted gamma transitions**
- **1300+ L records** (energy levels)
- **1669+ G records** (gamma transitions)
- **7869 total lines** of ENSDF data
- **63 non-adopted datasets** for comparison

## Contributing

### Development Workflow
1. Follow ENSDF manual specifications exactly
2. Use provided validation tools before committing
3. Update change.log with evidence-based entries
4. Generate PDFs to verify formatting
5. Commit with comprehensive messages

### Quality Standards
- **No format violations**: All ENSDF records must pass validation
- **Scientific accuracy**: Cross-reference with experimental publications
- **Complete documentation**: Every change must be tracked and justified

## License & Attribution

This work is conducted under the **FRIB Laboratory** nuclear data evaluation program in collaboration with the **U.S. Nuclear Data Program (USNDP)** and **International Network of Nuclear Structure and Decay Data (NSDD)**.

**Evaluator**: FRIB Nuclear Data Group  
**Period**: March 2025 - September 2025  
**Scope**: Professional nuclear data evaluation for scientific publication

---

*For technical issues with ENSDF formatting or validation tools, consult the .vscode/ directory for specialized development tools and documentation.*
