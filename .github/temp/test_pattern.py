filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check line 2823 character by character
line = lines[2822]
print(f"Line 2823 (index 2822):")
print(f"Length: {len(line)}")
print(f"First 10 chars: {repr(line[:10])}")
print(f"Columns 1-9: {repr(line[:9])}")
print()

# Check if it's " 35CL cL " or something else
import re
patterns = [
    r'^ \d{1,3}[A-Z][a-z]? cL ',  # My current pattern
    r'^ 35CL cL ',                # Simpler pattern
    r' 35CL cL ',                 # Starting with space
]

for p in patterns:
    match = re.match(p, line)
    print(f"Pattern {repr(p):40s}: {match is not None}")
