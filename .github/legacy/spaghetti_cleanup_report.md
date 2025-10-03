ENSDF Spaghetti Code Cleanup Report
==================================================
**Last Updated: October 2, 2025**

## PROBLEM IDENTIFIED:
Found 95+ redundant scripts causing massive code duplication and maintenance nightmares.

## ACTIVE TOOLS IN .github/ (4 CORE SCRIPTS ONLY):
  ✓ column_calibrate.py - Comprehensive ENSDF field validation
  ✓ ensdf_1line_ruler.py - 80-column format validator
  ✓ check_gamma_ordering.py - Energy ordering validator
  ✓ ens2pdf.py - PDF conversion tool

## ARCHIVED TOOLS (ALL MOVED TO legacy/):
Previously in .github/ but moved to legacy archive:

### Cl-35 1976Me12 Dataset Scripts (cl35_1976me12_scripts/):
  ❌ fix_1976ME12_formatting.py
  ❌ generate_complete_resonances.py
  ❌ insert_1976ME12_gammas.py
  ❌ insert_resonances_1976ME12.py
  ❌ replace_resonances_1976ME12_CORRECTED.py
  ❌ update_main_file.py
  ❌ integrate_resonances.py (Oct 2, 2025)
  ❌ update_resonances_precise.py (Oct 2, 2025)
  ❌ verify_complete_file.py (Oct 2, 2025)

### Data Validation Scripts (validation_scripts/):
  ❌ final_mr_validation.py
  ❌ validate_1976sp09_data.py
  ❌ validate_wgamma_data.py
  ❌ verify_de_corrections.py
  ❌ verify_sp09_energy_mapping.py

### Format Check Scripts (check_scripts/):
  ❌ analyze_limits.py
  ❌ check_de_format.py
  ❌ check_level_energies.py
  ❌ check_missing_levels.py
  ❌ check_mr_field_data.py
  ❌ check_mul_positioning.py

### Debug/Test Scripts (debug_test_scripts/):
  ❌ debug_gamma_extraction.py
  ❌ test_line.py
  ❌ test_padding.py
  ❌ test_trailing_spaces.py

### Other Utilities:
  ❌ extract_wgamma_levels.py (extract_scripts/)
  ❌ fix_unicode.py (fix_scripts/)
  ❌ cleanup_spaghetti_scripts.py (cleanup_scripts/)

## REDUNDANT SCRIPTS (ORIGINAL SPAGHETTI - ALREADY IN legacy/):

### Verify Scripts:
  ❌ verify_49_gammas.py
  ❌ verify_all_14_evidence.py
  ❌ verify_constraints.py
  ❌ verify_corrected_json.py
  ❌ verify_ensdf_against_placement.py
  ❌ verify_gamma_assignments.py
  ❌ verify_gamma_placement.py
  ❌ verify_json_lifetimes.py
  ❌ verify_lifetimes.py
  ❌ verify_multipolarity.py
  ❌ verify_parentheses_correct.py
  ❌ verify_parentheses_final.py
  ❌ verify_parentheses_formatting.py
  ❌ verify_parentheses_jpi.py
  ❌ verify_parentheses_with_tolerance.py
  ❌ verify_parentheses_with_tolerance_fixed.py
  ❌ verify_png_data.py

### Check Scripts:
  ❌ check_averages.py
  ❌ check_current_json.py
  ❌ check_errors.py
  ❌ check_image_levels_parentheses.py
  ❌ check_jp_confusion.py
  ❌ check_jp_errors.py
  ❌ check_l_fields.py
  ❌ check_missing_simple.py
  ❌ check_subtle_differences.py

### Analyze Scripts:
  ❌ analyze_close_energies.py
  ❌ analyze_columns.py
  ❌ analyze_ensdf_gammas.py
  ❌ analyze_jp_assignments.py
  ❌ analyze_s_field.py
  ❌ analyze_uncertainties.py

### Compare Scripts:
  ❌ compare_files.py
  ❌ compare_gamma_sets.py
  ❌ compare_jp_assignments.py
  ❌ compare_jp_corrected.py
  ❌ compare_jpi_assignments.py
  ❌ compare_l_records.py
  ❌ compare_with_original.py

### Fix Scripts:
  ❌ fix_cg_spacing.py
  ❌ fix_column_alignment.py
  ❌ fix_ev_widths.py
  ❌ fix_gamma_ordering.py
  ❌ fix_jp_confusion.py
  ❌ fix_ri_alignment.py

### Extract Scripts:
  ❌ extract_2025laaa_gammas.py
  ❌ extract_close_gammas.py
  ❌ extract_eli_energies.py
  ❌ extract_ensdf_jp.py
  ❌ extract_json_jp.py

### Debug Scripts:
  ❌ debug_association.py
  ❌ debug_lifetimes.py

### Test Scripts:
  ❌ simple_test.py
  ❌ simple_verification.py
  ❌ test_g_record_detection.py
  ❌ test_regex.py

### Final Scripts:
  ❌ final_check.py
  ❌ final_comparison.py
  ❌ final_extraction.py
  ❌ final_lifetime_verification.py
  ❌ final_table_generator.py
  ❌ final_verification.py
  ❌ ultimate_verification.py

### Other Redundant:
  ❌ add_missing_gammas.py
  ❌ basic_debug.py
  ❌ cleanup_ensdf_file.py
  ❌ column_calibrate_old.py
  ❌ column_validate_ascii.py
  ❌ corrected_comparison.py
  ❌ corrected_extraction.py
  ❌ corrected_verification.py
  ❌ create_accurate_placement.py
  ❌ create_l_mapping.py
  ❌ create_update_plan.py
  ❌ cross_check_image_vs_ensdf.py
  ❌ delete_d_lines.py
  ❌ detailed_comparison.py
  ❌ detailed_jpi_comparison_list.py
  ❌ determine_gamma_placements.py
  ❌ enhanced_column_calibrate.py
  ❌ ensdf_json_comparison.py
  ❌ ensdf_json_detailed_comparison.py
  ❌ find_long_line.py
  ❌ fixed_ensdf_comparison.py
  ❌ json_ensdf_comparison.py
  ❌ json_ensdf_comparison_fixed.py
  ❌ json_ensdf_comparison_v2.py
  ❌ l_update_plan.py
  ❌ match_2012_2025_gammas.py
  ❌ multipolarity_summary.py
  ❌ png_final_verification.py
  ❌ png_full_reextraction.py
  ❌ remove_extra_l_records.py
  ❌ remove_widths.py
  ❌ step2_match_energies.py

## SUMMARY:
  - **ACTIVE in .github/: 4 core validation tools**
  - **Archived in legacy/: 27 task-specific scripts** (organized by category)
  - **Original spaghetti: 95 redundant scripts** (from previous cleanup)
  - **Total archived: 122 scripts** properly categorized

## WORKSPACE ORGANIZATION STATUS:
  ✅ .github/ - CLEAN (4 core tools only)
  ✅ temp/ - CLEAN (data files only, trash removed)
  ✅ legacy/ - ORGANIZED (7 categories, 122 scripts)

## ANTI-SPAGHETTI RULES ENFORCED:
  ❌ NO creating verify_*, check_*, analyze_*, compare_* scripts in .github/
  ❌ NO creating test_*, debug_*, fix_* scripts in .github/
  ❌ NO creating scripts in temp/ folders (temp is for DATA only)
  ❌ NO creating scripts in ENSDF dataset folders
  ✅ ONLY core validation tools in .github/
  ✅ Task-specific scripts go to legacy/ immediately after use
  ✅ Professional workspace organization maintained

## APPROVED CORE TOOLS (.github/):
  1. column_calibrate.py - Field position and line length validation
  2. ensdf_1line_ruler.py - Single-line 80-column format checker
  3. check_gamma_ordering.py - L-record and G-record energy ordering
  4. ens2pdf.py - ENSDF to PDF conversion utility

**All other scripts belong in legacy/ archive!**
