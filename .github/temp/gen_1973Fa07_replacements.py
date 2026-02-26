import re, json, math

with open(r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens','r') as f:
    lines = f.readlines()

d_idx = None
for i, l in enumerate(lines):
    if 'Only edit data below this line' in l:
        d_idx = i
        break

factor = 2.21052631579

targets = []
for i, l in enumerate(lines):
    if i <= d_idx:
        continue
    if '1973Fa07' not in l or '|w|g' not in l:
        continue
    content = l.rstrip('\r\n')

    # Pattern 2 first (more specific): |w|g=(X.X) eV
    m2 = re.search(r'\|w\|g=\(([0-9.]+)\) eV \(1973Fa07\)', content)
    # Pattern 1: |w|g=X.X eV
    m1 = re.search(r'\|w\|g=([0-9.]+) eV \(1973Fa07\)', content)
    # Pattern 3: |w|g(X.X) eV (no equals)
    m3 = re.search(r'\|w\|g\(([0-9.]+)\) eV \(1973Fa07\)', content)

    if m2:
        val = float(m2.group(1))
        ptype = 'paren'
        old_substr = m2.group(0)
    elif m1:
        val = float(m1.group(1))
        ptype = 'normal'
        old_substr = m1.group(0)
    elif m3:
        val = float(m3.group(1))
        ptype = 'paren_no_eq'
        old_substr = m3.group(0)
    else:
        print(f'WARNING: unmatched line {i+1}: {content[:70]}')
        continue

    scaled = val / factor
    new_val = round(scaled, 2)
    new_val_str = '{:.2f}'.format(new_val)

    # Build new substring
    if ptype == 'normal':
        new_substr = '|w|g={} eV (1973Fa07)'.format(new_val_str)
    elif ptype == 'paren':
        new_substr = '|w|g=({}) eV (1973Fa07)'.format(new_val_str)
    elif ptype == 'paren_no_eq':
        new_substr = '|w|g({}) eV (1973Fa07)'.format(new_val_str)

    new_content = content.replace(old_substr, new_substr, 1)
    # Pad or trim to 80 chars
    new_content = new_content.rstrip()
    if len(new_content) < 80:
        new_content = new_content + ' ' * (80 - len(new_content))

    prev_line = lines[i-1].rstrip('\r\n') if i > 0 else ''

    targets.append({
        'line': i+1,
        'old_val': val,
        'new_val': new_val,
        'type': ptype,
        'old_block': prev_line + '\n' + content,
        'new_block': prev_line + '\n' + new_content,
        'new_len': len(new_content),
    })

print(f'Total targets: {len(targets)}')
print()
print(f'{"Line":<6} {"Type":<14} {"OldVal":<8} {"NewVal":<8} {"Len":<5}')
print('-'*45)
for t in targets:
    print(f'{t["line"]:<6} {t["type"]:<14} {t["old_val"]:<8} {t["new_val"]:<8} {t["new_len"]:<5}')

# Check for bad lengths
bad = [t for t in targets if t['new_len'] != 80]
if bad:
    print(f'\nERROR: {len(bad)} lines not 80 chars!')
    for t in bad:
        print(f'  Line {t["line"]}: {t["new_len"]} chars')
else:
    print(f'\nAll {len(targets)} lines exactly 80 chars: OK')

with open(r'd:\X\ND\ENSDF\.github\temp\1973Fa07_replacements.json', 'w') as f:
    json.dump(targets, f, indent=2)
print(f'Saved to .github/temp/1973Fa07_replacements.json')
