# Index for 2025-10-28 cleanup

This index records what was consolidated into this dated folder.

## Top-level
- logs/
- reports/
- scripts/
- script_groups/

## script_groups (preserved sets)
- 2025-10-03_ep_data_scripts/
- 2025-10-06_1976sp08_formatting/
- 2025-10-06_analysis_scripts/
- 2025-10-06_RI_field_alignment/
- 2025-10-06_ri_field_attempts/
- 2025-10-16_2001VO24_verification_report/
- 2025-10-16_cleanup/
- 2025-10-16_cleanup_misplaced_root_files/
- 2025-10-16_misplaced_scripts/
- check_scripts/
- cl35_1976me12_scripts/
- cleanup_scripts/
- debug_test_scripts/
- extract_scripts/
- fix_scripts/
- validation_scripts/

## reports (high level)
- 1972HU10_COMPREHENSIVE_VERIFICATION_STATUS.md
- 1972HU10_RI_VERIFICATION_SUMMARY.md
- L7066_VERIFICATION.md
- L7103_VERIFICATION.md
- L7178_L7272_VERIFICATION.md
- L7362_L7503_VERIFICATION.md
- copilot-instructions-backup.md
- missing_ri.txt, missing_ri2.txt, ri_verify_output.txt
- 1972hu10_final/correct/verifications (see files)

## logs
- change.log
- errors.txt

## scripts (single utilities)
Representative examples:
- add_missing_ri.py, add_ri_to_comments.py
- fix_ensdf_uncertainty_notation.py
- scan_* and find_* analyzers
- verify_* and validate_* checks

For a full machine-readable listing:

```powershell
Get-ChildItem -Path 'd:\X\ND\ENSDF\.github\temp\2025-10-28_cleanup' -Recurse |
  Select-Object FullName | Out-File 'd:\X\ND\ENSDF\.github\temp\2025-10-28_cleanup\MANIFEST.txt'
```