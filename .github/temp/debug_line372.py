import re, math

with open(r'A35/Cl35/new/Cl35_adopted.ens', 'r') as f:
    lines = f.readlines()

# Line 372 (index 371)
line = lines[371]
print(f'Line 372: {repr(line[:80])}')
print(f'Col 7 (0-indexed): [{line[7]}]')
print(f'Col 0-5: [{line[0:6]}]')
print(f'Col 6: [{line[6]}]')
print(f'Is L-record? {line[7] == "L" and "35CL" in line[0:6]}')
print(f'T field (cols 40-49): [{line[39:49]}]')

# Check for T$ comment
for j in range(372, min(382, len(lines))):
    if 'T$' in lines[j]:
        print(f'\nLine {j+1} has T$: {repr(lines[j][:60])}')
        match = re.search(r'\|t=([0-9.]+)\s*([a-z]+)', lines[j])
        if match:
            print(f'  Lifetime: {match.group(1)} {match.group(2).upper()}')
            lifetime_value = float(match.group(1))
            lifetime_unit = match.group(2).upper()
            unit_conv = {'FS': 1, 'PS': 1e3, 'NS': 1e6, 'US': 1e9, 'MS': 1e12, 'S': 1e15}
            lifetime_fs = lifetime_value * unit_conv.get(lifetime_unit, 1)
            expected_t_fs = lifetime_fs * math.log(2)
            t_value = float(line[39:49].split()[0])
            t_fs = t_value * 1  # FS
            print(f'  Expected T: {expected_t_fs:.2f} FS')
            print(f'  Actual T: {t_fs} FS')
            print(f'  Error: {t_fs - expected_t_fs:+.2f} FS ({(t_fs - expected_t_fs) / expected_t_fs * 100:+.1f}%)')
            print(f'  Tolerance check: abs({t_fs - expected_t_fs:.2f}) > max(0.5, {expected_t_fs * 0.01:.2f})?')
            tolerance = max(0.5, expected_t_fs * 0.01)
            print(f'  {abs(t_fs - expected_t_fs):.2f} > {tolerance:.2f}? {abs(t_fs - expected_t_fs) > tolerance}')
