#!/usr/bin/env python3
"""
Apply all gamma energy corrections to cL J$ comments in Cl35_adopted.ens.
Uses surgical string replacement with validation.
"""

import sys
from pathlib import Path

# Remaining corrections: (line_num, old_value, new_value)
corrections = [
    (522, "2437.4|g", "2433.5|g"),
    (781, "4886.4|g", "4886.5|g"),
    (781, "4342.9|g", "4347.8|g"),
    (781, "6106.2|g", "6105.6|g"),
    (1027, "6142.0|g", "6141.9|g"),
    (1049, "4232.7|g", "4233.3|g"),
    (1074, "4498.0|g", "4500.3|g"),
    (1179, "3689.1|g", "3688.8|g"),
    (1193, "4668.8|g", "4667.6|g"),
    (1229, "3634.5|g", "3634.8|g"),
    (1229, "4690.8|g", "4690.9|g"),
    (1257, "4581.5|g", "4578.4|g"),
    (1280, "4613.8|g", "4613.9|g"),
    (1297, "6561.7|g", "6557.1|g"),
    (1362, "6618.9|g", "6617.2|g"),
    (1362, "3895.9|g", "3892.0|g"),
    (1378, "2652.8|g", "2652.0|g"),
    (1389, "1946.35|g", "1943.43|g"),
    (1389, "1786.2|g", "1783.21|g"),
    (1429, "3018.1|g", "3016.6|g"),
    (1429, "3721.1|g", "3717.8|g"),
    (1467, "3622.3|g", "3619.52|g"),
    (1497, "2592.0|g", "2592.2|g"),
    (1497, "2832.1|g", "2830.8|g"),
    (1588, "3897.8|g", "3894.1|g"),
    (1588, "3962.0|g", "3960.13|g"),
    (1605, "5449.9|g", "5450.0|g"),
    (1605, "3918.0|g", "3918.24|g"),
    (1644, "2897.4|g", "2892.6|g"),
    (1644, "4145.7|g", "4145.4|g"),
    (1679, "3978.7|g", "3976.4|g"),
    (1697, "5016.0|g", "5016.1|g"),
    (1697, "5485.0|g", "5484.9|g"),
    (1789, "3118.9|g", "3117.4|g"),
    (1789, "4104.2|g", "4100.5|g"),
    (1837, "4350.5|g", "4347.8|g"),
    (1837, "5154.7|g", "5153.8|g"),
    (1858, "2911.9|g", "2912.4|g"),
    (1858, "2232.7|g", "2235.21|g"),
    (1870, "4209.1|g", "4213.6|g"),
    (1870, "7102.9|g", "7102.6|g"),
    (1949, "4496.7|g", "4500.3|g"),
    (1949, "3248.3|g", "3245.8|g"),
    (2001, "3080.0|g", "3075.81|g"),
    (2001, "2399.8|g", "2400.6|g"),
    (2113, "4282.1|g", "4286.1|g"),
    (2113, "6866.4|g", "6866.2|g"),
    (2259, "5817.6|g", "5817.7|g"),
    (2278, "6183.0|g", "6180.0|g"),
    (2294, "3617.1|g", "3619.52|g"),
    (2294, "4063.0|g", "4058.9|g"),
    (2294, "4719.1|g", "4722.6|g"),
    (2321, "971.38|g", "971.0|g"),
    (2361, "3722.6|g", "3717.8|g"),
    (2361, "6239.8|g", "6237.3|g"),
    (2361, "4707.9|g", "4703.4|g"),
    (2376, "4950.0|g", "4954.8|g"),
    (2376, "6198.8|g", "6198.7|g"),
    (2386, "4726.6|g", "4722.6|g"),
    (2386, "6210.3|g", "6206.6|g"),
    (2386, "7684.5|g", "7684.6|g"),
    (2412, "4571.7|g", "4572.7|g"),
    (2412, "7156.0|g", "7155.9|g"),
    (2535, "5993.6|g", "5991.7|g"),
    (2755, "2069.8|g", "2073.4|g"),
    (2755, "2014.7|g", "2010.9|g"),
    (2834, "2614.5|g", "2613.7|g"),
    (2878, "2390.8|g", "2393.8|g"),
]

def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_corrections.py <path_to_Cl35_adopted.ens>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    corrections_applied = []
    corrections_failed = []
    
    # Apply corrections
    for line_num, old_value, new_value in corrections:
        idx = line_num - 1  # Convert to 0-based index
        if idx < len(lines):
            original_line = lines[idx]
            if old_value in original_line:
                # Perform replacement
                lines[idx] = original_line.replace(old_value, new_value)
                corrections_applied.append((line_num, old_value, new_value))
                print(f"[OK] Line {line_num}: {old_value} -> {new_value}")
            else:
                corrections_failed.append((line_num, old_value, "Not found in line"))
                print(f"[FAIL] Line {line_num}: '{old_value}' not found")
                print(f"       Actual line: {original_line.rstrip()[:80]}")
        else:
            corrections_failed.append((line_num, old_value, "Line number out of range"))
            print(f"[FAIL] Line {line_num}: Out of range (file has {len(lines)} lines)")
    
    # Write back if any corrections were applied
    if corrections_applied:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        print(f"\n[SUCCESS] Applied {len(corrections_applied)} corrections to {file_path}")
    
    if corrections_failed:
        print(f"\n[WARNING] {len(corrections_failed)} corrections failed:")
        for line_num, old_value, reason in corrections_failed:
            print(f"  Line {line_num}: {old_value} - {reason}")
    
    print(f"\nSummary: {len(corrections_applied)} applied, {len(corrections_failed)} failed")
    sys.exit(0 if not corrections_failed else 1)

if __name__ == '__main__':
    main()
