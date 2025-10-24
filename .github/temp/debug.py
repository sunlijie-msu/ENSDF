import re

filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Test L 9081.5 at line 2821
print("Testing L 9081.5 (line 2821):")
print(f"Line 2821: {lines[2820][:50]}")
print(f"Line 2823: {lines[2822][:50]}")
print(f"Line 2826: {lines[2825][:50]}")
print(f"Line 2828: {lines[2827][:50]}")
print()

# Check if lines match cL pattern
for i in [2822, 2825, 2827]:
    line = lines[i]
    match = re.match(r'^ \d{1,3}[A-Z][a-z]? cL ', line)
    has_T = ' T$' in line
    has_E = ' E$' in line
    has_J = ' J$' in line
    print(f"Line {i+1}: match={match is not None}, T$={has_T}, E$={has_E}, J$={has_J}")
    if match:
        print(f"  Text: {line[:60]}")
print()

# Test L 8844.3 at line 2606
print("Testing L 8844.3 (line 2606):")
print(f"Line 2606: {lines[2605][:50]}")
print(f"Line 2607: {lines[2606][:50]}")
print(f"Line 2610: {lines[2609][:50]}")
print(f"Line 2613: {lines[2612][:50]}")
print()

for i in [2606, 2609, 2612]:
    line = lines[i]
    match = re.match(r'^ \d{1,3}[A-Z][a-z]? cL ', line)
    has_T = ' T$' in line
    has_E = ' E$' in line
    has_J = ' J$' in line
    print(f"Line {i+1}: match={match is not None}, T$={has_T}, E$={has_E}, J$={has_J}")
    if match:
        print(f"  Text: {line[:60]}")
