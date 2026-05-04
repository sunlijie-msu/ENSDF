"""Search for 1330 and other key patterns in the file."""
with open(r'A34\Cl34\new\Cl34_adopted.ens', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')

# Search for 1330|g in comment lines
print('\n--- Lines containing 1330 ---')
for i, line in enumerate(lines, 1):
    if '1330' in line:
        print(f'{i:5d}: {repr(line.rstrip()[:70])}')

# Search for 5541 L-record
print('\n--- Lines containing 5541 ---')
for i, line in enumerate(lines, 1):
    if '5541' in line and len(line) > 9 and line[7] == 'L':
        print(f'{i:5d}: {repr(line.rstrip()[:70])}')
