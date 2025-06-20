# Git Commit Message for ENSDF Tools and Ar35 Data Improvements

## Title
Enhance ENSDF column calibration tools and improve Ar35 scientific content

## Summary
- Enhanced Python column calibration script with complete 80-column ENSDF format support
- Improved scientific content and formatting in Ar35 ENSDF files
- Completed comprehensive change tracking and documentation

## Changes in detail:

### Enhanced Python ENSDF Tools
- **column_calibrate.py**: Extended from 41-column to complete 80-column ENSDF support
  - Added all missing G-record fields: mixing ratio, conversion coefficients, flags
  - Fixed L-record L field extraction (Angular momentum transfer, cols 56-64)
  - Enhanced documentation and field reference guides
  - Validated with 35.adp (134 L-records, 37 G-records)
- **check_averages.py**: Completed and tested average calculation verification tool
  - Robust parsing of weighted/unweighted averages in ENSDF comments
  - Successfully validated against real ENSDF files

### ENSDF Scientific Content Improvements
- **Ar35_36ar_p_d.ens**: Fixed grammar in L=3 vs L=2 comparison (line 77)
- **Ar35_adopted.ens**: Multiple scientific and formatting enhancements:
  - Cleaned up comment structure and orphaned continuation lines
  - Enhanced level energy determination descriptions
  - Added 1973Be26 experimental context for L=2 assignment
  - Documented negative search results for T=3/2 levels
  - Fixed evaluator notes and improved scientific rationale
  - Corrected typo: "5992" → "5994" keV level reference

### Processing Artifacts
- **PDF files**: Regenerated Ar35_36ar_3he_a.pdf, Ar35_36ar_p_d.pdf, Ar35_adopted.pdf
- **Temp files**: Updated all analysis outputs (35.err, 35.fed, 35.fmt, etc.)
- **Untracked files**: Added Java_GTOL.out and Java_GTOL.rpt

### Documentation and Change Tracking
- **change.log**: Updated with comprehensive session documentation
- **Workflow improvements**: Established systematic change detection using git + what-changed.ps1
- **Evidence-based logging**: All changes verified with detailed file diffs

### Files changed: 15 files modified, 2 untracked
- Core ENSDF: finished/Ar35/new/Ar35_36ar_p_d.ens, finished/Ar35/new/Ar35_adopted.ens  
- PDFs: finished/Ar35/pdf/*.pdf (3 files)
- Tools: .vscode/change.log, .vscode/column_calibrate_fixed.py
- Processing: finished/Ar35/temp/*.* (9 files)

This commit represents the completion of comprehensive ENSDF column calibration tooling and systematic improvement of Ar35 nuclear data content, with full change tracking and documentation.
