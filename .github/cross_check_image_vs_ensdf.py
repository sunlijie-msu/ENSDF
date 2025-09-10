#!/usr/bin/env python3
"""
Cross-check the image J-π assignments with both ENSDF and XUNDL data.
"""

def main():
    # Levels from the user's image (extracted manually)
    image_levels = [
        (3958.7, "27/2-"),  # NO parentheses in image
        (2976.6, "23/2-"),  # NO parentheses in image
        (2545.4, "19/2-"),  # NO parentheses in image  
        (1893.9, "15/2-"),  # NO parentheses in image
        (1235.2, "11/2-"),  # NO parentheses in image
        (2356.7, "19/2+"),  # NO parentheses in image
        (1876.2, "17/2+"),  # NO parentheses in image
        (1479.7, "15/2+"),  # NO parentheses in image
        (716.4, "11/2+"),   # NO parentheses in image
        (744.9, "9/2+")     # NO parentheses in image
    ]
    
    # ENSDF levels (from the file we just analyzed)
    ensdf_levels = [
        (0.00, "5/2+"),
        (57.46, "7/2+"),
        (628.51, "7/2+"),
        (650.79, "9/2+"),
        (716.48, "11/2+"),
        (744.76, "9/2+"),
        (1235.13, "11/2-"),
        (1266.29, "13/2+"),
        (1306.54, "11/2+"),
        (1479.75, "15/2+"),
        (1550.68, "13/2+"),
        (1876.02, "17/2+"),
        (1893.64, "15/2-"),
        (1973.80, "15/2+"),
        (2356.75, "19/2+"),
        (2357.10, "17/2+"),
        (2545.13, "19/2-"),
        (2788.42, "21/2+"),
        (2829.60, "(19/2+)"),    # PARENTHESES in ENSDF
        (2976.10, "23/2-"),
        (3207.30, "(23/2+)"),    # PARENTHESES in ENSDF  
        (3442.60, "(21/2+)"),    # PARENTHESES in ENSDF
        (3557.20, "27/2+"),
        (3600.80, "(25/2+)"),    # PARENTHESES in ENSDF
        (3957.90, "(27/2-)"),    # PARENTHESES in ENSDF
        (3988.50, "(27/2-)"),    # PARENTHESES in ENSDF
        (4367.40, "(29/2-)"),    # PARENTHESES in ENSDF
        (4641.60, "(31/2-)"),    # PARENTHESES in ENSDF
        (5242.60, "(35/2-)"),    # PARENTHESES in ENSDF
    ]
    
    print("CROSS-CHECK: IMAGE vs ENSDF J-π ASSIGNMENTS")
    print("=" * 60)
    print("Checking if image levels match ENSDF parentheses formatting")
    print()
    
    def find_closest_level(target_energy, levels, tolerance=1.0):
        """Find the closest level within tolerance."""
        best_match = None
        best_diff = float('inf')
        
        for energy, jpi in levels:
            diff = abs(energy - target_energy)
            if diff <= tolerance and diff < best_diff:
                best_diff = diff
                best_match = (energy, jpi)
        
        return best_match
    
    print(f"{'Image Energy':<12} {'Image J-π':<10} {'ENSDF Energy':<12} {'ENSDF J-π':<12} {'Status':<20}")
    print("-" * 70)
    
    parentheses_issues = []
    
    for img_energy, img_jpi in image_levels:
        match = find_closest_level(img_energy, ensdf_levels, tolerance=1.0)
        
        if match:
            ensdf_energy, ensdf_jpi = match
            
            # Check if J-π values match (ignoring parentheses)
            img_core = img_jpi.strip('()')
            ensdf_core = ensdf_jpi.strip('()')
            
            if img_core == ensdf_core:
                if img_jpi == ensdf_jpi:
                    status = "✅ PERFECT MATCH"
                else:
                    status = "⚠️ PARENTHESES DIFF"
                    parentheses_issues.append((img_energy, img_jpi, ensdf_energy, ensdf_jpi))
            else:
                status = "❌ J-π MISMATCH"
            
            print(f"{img_energy:<12.1f} {img_jpi:<10} {ensdf_energy:<12.2f} {ensdf_jpi:<12} {status:<20}")
        else:
            print(f"{img_energy:<12.1f} {img_jpi:<10} {'---':<12} {'---':<12} {'❌ NOT FOUND':<20}")
    
    print("-" * 70)
    print()
    
    if parentheses_issues:
        print("PARENTHESES FORMATTING ISSUES DETECTED:")
        print("=" * 50)
        print("The following levels show different parentheses formatting between image and ENSDF:")
        print()
        for img_energy, img_jpi, ensdf_energy, ensdf_jpi in parentheses_issues:
            print(f"Energy {img_energy:.1f} keV:")
            print(f"  Image shows: {img_jpi} (NO parentheses)")
            print(f"  ENSDF shows: {ensdf_jpi} (WITH parentheses)")
            print(f"  Energy difference: {abs(img_energy - ensdf_energy):.2f} keV")
            print()
        
        print("❗ CRITICAL FINDING:")
        print(f"Found {len(parentheses_issues)} levels where image shows NO parentheses")
        print("but ENSDF file has parentheses (tentative assignments).")
        print()
        print("This suggests the ENSDF parentheses may need to be REMOVED")
        print("to match the definitive assignments shown in the image.")
    else:
        print("✅ All parentheses formatting is consistent between image and ENSDF")
    
    print()
    print("SUMMARY:")
    print("=" * 30)
    print(f"Total image levels checked: {len(image_levels)}")
    print(f"Parentheses issues found: {len(parentheses_issues)}")
    
    if parentheses_issues:
        print()
        print("🚨 ACTION REQUIRED:")
        print("The image appears to show definitive J-π assignments")
        print("(without parentheses) for levels that ENSDF marks as tentative")
        print("(with parentheses). Consider updating ENSDF to match image.")

if __name__ == "__main__":
    main()
