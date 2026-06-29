"""Full analysis of asterisk-marked gamma rays with intensity comparison."""
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
            # Also check if Eg has asterisk
            eg_has_ast = '*' in eg_raw or '\u2217' in eg_raw
            
            # Parse Ig value and uncertainty
            ig_clean = ig_raw.replace('\u2217','').replace('*','').strip()
            m_ig = re.match(r'([\d.]+)\s*\((\d+)\)', ig_clean) if ig_clean else None
            ig_val = m_ig.group(1) if m_ig else ig_clean
            ig_unc = m_ig.group(2) if m_ig else ''
            
            # Parse Eg
            m_eg = re.match(r'([\d.]+)\s*\((\d+)\)', eg_raw) if eg_raw else None
            eg_val = m_eg.group(1) if m_eg else eg_raw
            eg_unc = m_eg.group(2) if m_eg else ''
            
            asterisk_rows.append({
                'file': sf.replace('2026OSAA_CT11035_152Gd_Table_I_','').replace('.md',''),
                'line': ln,
                'Ei': current_ei, 'Jpi': current_jpi,
                'Eg': eg_val, 'DEg': eg_unc,
                'Ig': ig_val, 'DIg': ig_unc,
                'Ig_raw': ig_raw,
                'Ef': ef_raw,
                'Mult': mult_raw,
                'Eg_ast': eg_has_ast,
            })

# Print full markdown table
print('| # | File | Ei (keV) | Jpi | Eg (keV) | Ig | Ef (keV) | Mult | Eg*? |')
print('|---|------|----------|-----|----------|-----|---------|------|------|')
for i, r in enumerate(asterisk_rows, 1):
    eg_ast_mark = 'YES' if r['Eg_ast'] else ''
    ig_str = '{}({})*'.format(r['Ig'], r['DIg']) if r['DIg'] else r['Ig_raw']
    print('| {} | {} | {} | {} | {}({}) | {} | {} | {} | {} |'.format(
        i, r['file'], r['Ei'], r['Jpi'],
        r['Eg'], r['DEg'],
        ig_str,
        r['Ef'], r['Mult'], eg_ast_mark))

print()
print('Total: {} asterisk-marked gammas'.format(len(asterisk_rows)))

# Check for same-Eg multiplets with intensity comparison
from collections import defaultdict
by_eg = defaultdict(list)
for r in asterisk_rows:
    try:
        egf = float(r['Eg'])
        by_eg[egf].append(r)
    except: pass

print()
print('=== Same-Eg groups ===')
for egf in sorted(by_eg.keys()):
    items = by_eg[egf]
    if len(items) > 1:
        print('Eg = {} keV: {} occurrences'.format(egf, len(items)))
        for it in items:
            print('  {} -> {} : Ig = {}({})*  [{}]'.format(
                it['Ei'], it['Ef'], it['Ig'], it['DIg'], it['file']))
        # Check if intensities match
        igs = [(it['Ig'], it['DIg']) for it in items]
        if all(ig == igs[0] for ig in igs):
            print('  ** INTENSITIES MATCH **')
        else:
            print('  ** INTENSITIES DIFFER **')
            for it in items:
                print('      {} -> {} : Ig={}({})*'.format(it['Ei'], it['Ef'], it['Ig'], it['DIg']))
        print()

# Count Eg with asterisks
eg_ast_count = sum(1 for r in asterisk_rows if r['Eg_ast'])
print('Entries with asterisk on Eg: {}'.format(eg_ast_count))
