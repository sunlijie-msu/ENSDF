import re

f = open('A34/Cl34/new/Cl34_32s_3he_pg.ens', 'r')
lines = f.readlines()
f.close()

# Find all T$ lines
print("=== LIFETIME COMMENTS ===\n")
for j, line in enumerate(lines):
    if ' cL T$' in line:
        # Extract the lifetime comment
        lifetime_comment = line.rstrip()
        print(f"Line {j+1}:")
        print(f"  {lifetime_comment}")
        
        # Show continuation lines if any
        k = j + 1
        while k < len(lines) and (lines[k].startswith(' 34CL2cL') or lines[k].startswith(' 34CL3cL') or lines[k].startswith(' 34CL4cL') or lines[k].startswith(' 34CL5cL')):
            print(f"  {lines[k].rstrip()}")
            k += 1
        print()
