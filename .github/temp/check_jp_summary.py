#!/usr/bin/env python3
"""Extract J-π validation summary from column_calibrate.py output."""
import subprocess
import sys

result = subprocess.run(
    ['python', '.github/column_calibrate.py', 'd:/X/ND/ENSDF/A35/Cl35/new/Cl35_34s_p_g.ens'],
    capture_output=True,
    text=True
)

lines = result.stdout.split('\n')
jp_section = False

print("=" * 80)
print("J-π FIELD VALIDATION SUMMARY")
print("=" * 80)

for line in lines:
    if 'J-π FIELD VALIDATION' in line:
        jp_section = True
    
    if jp_section:
        if 'J-π FIELD SUMMARY' in line:
            print(line)
            # Print next 5 lines for full summary
            idx = lines.index(line)
            for i in range(1, 6):
                if idx + i < len(lines):
                    print(lines[idx + i])
            break
        
        if '[ERROR]' in line:
            print(line)

print("\nExit code:", result.returncode)
