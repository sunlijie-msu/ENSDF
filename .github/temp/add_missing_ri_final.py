#!/usr/bin/env python3
"""
Add missing RI$ cG comments to 34 gammas in Cl35_34s_p_g.ens
This script will insert new cG RI$ lines after the G-records
"""

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Mapping: (line_number_of_G_record (0-indexed), RI_value_to_add)
additions = [
    (2042-1, 1),   # After G 3446.3
    (2229-1, 1),   # After G 3611.7
    (2252-1, 34),  # After G 6618.1
    (2258-1, 2),   # After G 8380.7
    (2330-1, 7),   # After G 3603.2
    (2331-1, 1),   # After G 3859.8
    (2332-1, 1),   # After G 4516.8
    (2333-1, 5),   # After G 4565.6
    (2334-1, 7),   # After G 5481.2
    (2335-1, 20),  # After G 5790.0
    (2336-1, 3),   # After G 5838.2
    (2337-1, 46),  # After G 6720.7
    (2338-1, 4),   # After G 8483.3
    (2653-1, 1),   # After G 3293.4
    (2655-1, 9),   # After G 4779.3
    (2656-1, 4),   # After G 4950.0
    (2657-1, 29),  # After G 5729.8
    (2658-1, 37),  # After G 6198.8
    (2659-1, 19),  # After G 7129.5
    (2660-1, 1),   # After G 8892.1
    (2680-1, 2),   # After G 3261.0
    (2682-1, 4),   # After G 3321.0
    (2685-1, 6),   # After G 4136.7
    (2686-1, 15),  # After G 4963.5
    (2757-1, 1),   # After G 3357.7
    (2758-1, 1),   # After G 4200.2
    (2762-1, 2),   # After G 4903.1
    (2763-1, 2),   # After G 4907.6
    (2764-1, 9),   # After G 5162.5
    (2767-1, 6),   # After G 5917.9
    (2768-1, 2),   # After G 6386.9
    (2769-1, 1),   # After G 6435.1
    (2770-1, 16),  # After G 7317.6
    (2773-1, 60),  # After G 9080.1
]

print(f"This script will add {len(additions)} cG RI$ lines to Cl35_34s_p_g.ens")
print(f"Current file: {len(lines)} lines")
print("\nInserting lines from BOTTOM to TOP (to preserve line number accuracy):")

# Sort additions by line number in REVERSE order
additions_sorted = sorted(additions, key=lambda x: x[0], reverse=True)

failed = 0
success = 0

# Insert from bottom to top
for line_idx, ri_val in additions_sorted:
    # Verify this is a G-record
    if line_idx < len(lines):
        g_line = lines[line_idx]
        if len(g_line) > 7 and g_line[7:8] == 'G':
            # Create cG line (exactly 80 chars with newline)
            cg_template = " 35CL cG RI${} {{2001Vo24}}".format(ri_val)
            cg_line_padded = cg_template + ' ' * (80 - len(cg_template)) + '\n'
            
            # Verify it's exactly 80 chars (not counting newline)
            if len(cg_line_padded) - 1 != 80:
                cg_line_padded = cg_line_padded[:80] + '\n'
            
            # Insert the cG line AFTER this G-record
            lines.insert(line_idx + 1, cg_line_padded)
            success += 1
            if success <= 5 or success > len(additions_sorted) - 5:
                eg_str = g_line[9:19].strip() if len(g_line) > 19 else '?'
                print(f"  ✓ Line {line_idx+1}: G {eg_str} → Added cG RI${ri_val} {{2001Vo24}}")
            elif success == 6:
                print(f"  ... (inserting {len(additions_sorted)-10} more lines) ...")
        else:
            print(f"  ✗ Line {line_idx+1}: NOT a G-record!")
            failed += 1

if failed == 0:
    # Write back
    with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'w') as f:
        f.writelines(lines)
    
    print(f"\n✅ SUCCESS!")
    print(f"   Updated file: now {len(lines)} lines (was {len(lines)-success} lines)")
    print(f"   Added {success} cG RI$ lines successfully")
else:
    print(f"\n❌ FAILED - {failed} verification errors, file NOT modified")
