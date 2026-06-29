"""Find asterisk-marked gamma rays in all source markdown files."""
import re, os

src_dir = r'd:\X\ND\ENSDF\XUNDL'
src_files = [
    '2026OSAA_CT11035_152Gd_Table_I_4-6.md',
    '2026OSAA_CT11035_152Gd_Table_I_7-9.md',
    '2026OSAA_CT11035_152Gd_Table_I_10-12.md',
    '2026OSAA_CT11035_152Gd_Table_I_13-15.md',
    '2026OSAA_CT11035_152Gd_Table_I_16-18.md',
]

asterisk_rows = []
current_ei = ''
current_jpi = ''
for sf in src_files:
    fpath = os.path.join(src_dir, sf)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith('|'): continue
        if '$E_i$' in s and '$J^\\pi_i$' in s: continue
        if s.count(':---') >= 3: continue
        parts = s.split('|')
        if parts and parts[0]=='': parts=parts[1:]
        if parts and parts[-1]=='': parts=parts[:-1]
        cells = [c.strip() for c in parts]
        while len(cells) < 9: cells.append('')
        ei_raw = cells[0]
        jpi_raw = cells[1]
        eg_raw = cells[2]
        ig_raw = cells[3]
        ef_raw = cells[4]
        mult_raw = cells[6]

        if ei_raw:
            m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_raw)
            current_ei = m.group(1) if m else ei_raw
            current_jpi = jpi_raw if jpi_raw else ''

        # Check for asterisk in Ig (Unicode or ASCII)
        if '*' in ig_raw or '\u2217' in ig_raw:
            asterisk_rows.append({
                'file': sf, 'line': ln,
                'Ei': current_ei, 'Jpi': current_jpi,
                'Eg': eg_raw, 'Ig': ig_raw, 'Ef': ef_raw,
                'Mult': mult_raw
            })

print('Found {} asterisk-marked gamma rays:'.format(len(asterisk_rows)))
print()
for r in asterisk_rows:
    print('  {}:{}'.format(r['file'], r['line']))
    print('    Level {} ({}) -> {}'.format(r['Ei'], r['Jpi'], r['Ef']))
    print('    Eg={}, Ig={}, Mult={}'.format(r['Eg'], r['Ig'], r['Mult']))
    print()

# Group by gamma energy to identify multiplets
from collections import defaultdict
by_eg = defaultdict(list)
for r in asterisk_rows:
    m = re.match(r'([\d.]+)\s*\((\d+)\)', r['Eg'])
    eg_val = m.group(1) if m else r['Eg']
    try:
        egf = float(eg_val)
        by_eg[egf].append(r)
    except:
        pass

print('=== Grouped by gamma energy (potential multiplets) ===')
for egf in sorted(by_eg.keys()):
    items = by_eg[egf]
    if len(items) > 1:
        print('  Eg={}: {} occurrences'.format(egf, len(items)))
        for it in items:
            print('    Level {} -> {}'.format(it['Ei'], it['Ef']))
