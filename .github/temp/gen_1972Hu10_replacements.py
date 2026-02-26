import math, re, json

with open(r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

d_line_idx = None
for i, l in enumerate(lines):
    if 'Only edit data below this line' in l:
        d_line_idx = i
        break

factor = 2.21052631579
threshold_scaled = 1.0 / factor

targets = []
for i, line in enumerate(lines):
    if '1972Hu10' in line and '|w|g' in line and i > d_line_idx:
        match = re.search(r'\|w\|g=([0-9.]+)\s*eV\s*\{I(\d+)\}.*\(1972Hu10\)', line)
        if match:
            old_val = float(match.group(1))
            old_unc_str = match.group(2)
            targets.append({'idx': i, 'old_val': old_val, 'old_unc_str': old_unc_str})

print('Total targets:', len(targets))

replacements = []
for t in targets:
    old_val = t['old_val']
    scaled = old_val / factor

    rel_pct = 50 if scaled < threshold_scaled else 30
    unc = scaled * (rel_pct / 100.0)

    if unc == 0:
        val_str = '{:.1f}'.format(scaled)
        unc_int = 0
    else:
        mag = math.floor(math.log10(unc))
        leading_2 = int(round(unc / (10 ** (mag - 1))))

        if leading_2 < 35:
            round_to = mag - 1
        else:
            round_to = mag

        rounded_val = round(scaled, -round_to)
        rounded_unc = round(unc, -round_to)

        if round_to >= 0:
            val_str = '{:.0f}'.format(rounded_val)
            unc_int = int(round(rounded_unc))
        else:
            decimals = -round_to
            val_str = '{:.{}f}'.format(rounded_val, decimals)
            unc_int = int(round(rounded_unc * 10**decimals))

    idx = t['idx']
    old_line = lines[idx].rstrip('\r\n')

    # Extract exact old substring from line — just the |w|g=X eV {In} part
    m = re.search(r'\|w\|g=[0-9.]+ eV \{I\d+\}', old_line)
    if m:
        exact_old = m.group(0)
    else:
        print(f'ERROR: Cannot find pattern in line {idx+1}')
        continue

    new_substr = '|w|g={} eV {{I{}}}'.format(val_str, unc_int)
    new_line = old_line.replace(exact_old, new_substr, 1)

    # Strip trailing spaces then pad/trim to exactly 80 chars
    new_line = new_line.rstrip()
    if len(new_line) < 80:
        new_line = new_line + ' ' * (80 - len(new_line))
    elif len(new_line) > 80:
        print(f'ERROR: Line {idx+1} content exceeds 80 chars even after rstrip: {len(new_line)}')

    # Context: use prev line for unique matching
    prev_line = lines[idx-1].rstrip('\r\n') if idx > 0 else ''

    old_block = prev_line + '\n' + old_line
    new_block = prev_line + '\n' + new_line

    replacements.append({
        'line': idx + 1,
        'old_block': old_block,
        'new_block': new_block,
        'old_val': t['old_val'],
        'new_val': val_str,
        'new_unc': unc_int,
        'new_line_len': len(new_line),
    })

print()
for r in replacements:
    print(f"Line {r['line']}: {r['old_val']} -> {r['new_val']} {{I{r['new_unc']}}}, len={r['new_line_len']}")

with open(r'd:\X\ND\ENSDF\.github\temp\1972Hu10_replacements.json', 'w') as f:
    json.dump(replacements, f, indent=2)
print(f'\nSaved {len(replacements)} replacements to .github/temp/1972Hu10_replacements.json')
