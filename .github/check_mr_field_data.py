#!/usr/bin/env python3
"""
CRITICAL MR FIELD VERIFICATION: 1976SP09 Data
Check if MR field values in G-records match original δ values with sign conventions.
"""

def check_mr_field_data():
    """Verify MR field data against original 1976SP09 δ values."""
    
    print("="*100)
    print("CRITICAL MR FIELD VERIFICATION: 1976SP09 Data")
    print("="*100)
    
    # From original 1976SP09.ens file
    original_data = [
        {'eg': 7730, 'ei_initial': 8950, 'ei_final': 1220, 'A2': +0.12, 'A4': -0.02, 'delta': +0.34, 'alt_delta': +5.0},
        {'eg': 8950, 'ei_initial': 8950, 'ei_final': 0, 'A2': -0.19, 'A4': +0.02, 'delta': +0.39, 'alt_delta': +8.2}
    ]
    
    # From ENSDF file (user's example)
    ensdf_data = [
        {'eg': 7732.7, 'level': '8953.0', 'mr_field': -0.34, 'mr_comment_alt': +5.0, 'A2': +0.12, 'A4': -0.02},
        {'eg': 8951.8, 'level': '8953.0', 'mr_field': -0.39, 'mr_comment_alt': +8.2, 'A2': -0.19, 'A4': +0.02}
    ]
    
    print("Energy Correspondence and MR Field Analysis:")
    print("="*60)
    
    issues_found = []
    
    for i, (orig, ensdf) in enumerate(zip(original_data, ensdf_data)):
        print(f"\n[{i+1}] Energy Mapping:")
        print(f"    Original: {orig['eg']} keV → ENSDF: {ensdf['eg']} keV (Δ={abs(orig['eg']-ensdf['eg']):.1f} keV)")
        print(f"    Transition: {orig['ei_initial']}→{orig['ei_final']} keV")
        
        print(f"\n    Original δ values:")
        print(f"      Primary: δ = +{orig['delta']:.2f}")
        if 'alt_delta' in orig:
            print(f"      Alternative: δ = +{orig['alt_delta']:.1f}")
        
        print(f"\n    ENSDF MR field and comments:")
        print(f"      MR field: {ensdf['mr_field']:+.2f}")
        print(f"      cG MR comment alternative: +{ensdf['mr_comment_alt']:.1f}")
        
        # Check primary δ vs MR field (should have sign flip)
        expected_mr = -orig['delta']
        if abs(ensdf['mr_field'] - expected_mr) < 0.01:
            print(f"    ✅ MR field: {orig['delta']:+.2f} → {ensdf['mr_field']:+.2f} (correct sign flip)")
        else:
            print(f"    ❌ MR field: {orig['delta']:+.2f} → {ensdf['mr_field']:+.2f} (EXPECTED: {expected_mr:+.2f})")
            issues_found.append(f"MR field mismatch for {ensdf['eg']} keV")
        
        # Check alternative δ vs MR comment (should have sign flip)
        if 'alt_delta' in orig:
            expected_alt_mr = -orig['alt_delta']
            if abs(ensdf['mr_comment_alt'] - (-expected_alt_mr)) < 0.1:  # Comment shows +, but should be - of original
                print(f"    ❌ MR alternative: Original δ = +{orig['alt_delta']:.1f}, but ENSDF comment shows +{ensdf['mr_comment_alt']:.1f}")
                print(f"        Expected ENSDF comment: -{orig['alt_delta']:.1f} (with sign flip)")
                issues_found.append(f"Alternative MR sign error for {ensdf['eg']} keV")
            else:
                print(f"    ✅ MR alternative: Correct handling")
        
        # Check A2, A4 values (should match exactly)
        if abs(orig['A2'] - ensdf['A2']) < 0.01 and abs(orig['A4'] - ensdf['A4']) < 0.01:
            print(f"    ✅ A2, A4: Match perfectly ({orig['A2']:+.2f}, {orig['A4']:+.2f})")
        else:
            print(f"    ❌ A2, A4: Mismatch detected")
            issues_found.append(f"A2/A4 mismatch for {ensdf['eg']} keV")
    
    # Analysis of the sign convention issue
    print(f"\n{'='*100}")
    print("CRITICAL SIGN CONVENTION ANALYSIS")
    print("="*100)
    
    print("From original data:")
    print("  7730 keV: δ = +0.34(2) or +5.0(4)")
    print("  8950 keV: δ = +0.39(5) or +8.2(7)")
    
    print("\nExpected ENSDF with sign flip convention (+→-, -→+):")
    print("  7732.7 keV: MR = -0.34, MR comment alt = -5.0")
    print("  8951.8 keV: MR = -0.39, MR comment alt = -8.2")
    
    print("\nActual ENSDF (from user's example):")
    print("  7732.7 keV: MR = -0.34 ✓, MR comment alt = +5.0 ❌")
    print("  8951.8 keV: MR = -0.39 ✓, MR comment alt = +8.2 ❌")
    
    print(f"\n🔍 CRITICAL FINDING:")
    print("The MR field values are CORRECT (proper sign flip applied)")
    print("BUT the MR comment alternatives show WRONG signs (should be negative)")
    
    if issues_found:
        print(f"\n⚠️ ISSUES DETECTED:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False
    else:
        print(f"\n✅ ALL MR FIELD DATA VALIDATED")
        return True

if __name__ == "__main__":
    success = check_mr_field_data()
    print(f"\n{'='*100}")
    if success:
        print("✅ MR FIELD VALIDATION SUCCESSFUL")
    else:
        print("❌ MR FIELD VALIDATION ISSUES DETECTED")
    print("="*100)