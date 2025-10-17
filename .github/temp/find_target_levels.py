#!/usr/bin/env python3
"""Find exact line numbers of target Exi levels"""

targets = [7178.6, 7548.9, 7837.2, 8208.2, 8216.3, 8381.8, 8484.4, 8893.3, 8906.8, 9081.4]

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

print("Current L-record positions for target Exi levels:")
for line_num, line in enumerate(lines, 1):
    if len(line) > 8 and line[7:8] == 'L':
        try:
            e_str = line[9:19].strip()
            if e_str:
                e_val = float(e_str)
                for te in targets:
                    if abs(e_val - te) < 1:
                        print(f"Line {line_num}: Exi {e_val:.1f} (target {te})")
        except:
            pass
