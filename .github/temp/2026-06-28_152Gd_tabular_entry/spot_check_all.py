"""
Spot-check: 15% random sample across all 5 source files vs ENSDF output.
"""
import re, os, random

src_dir = r'd:\X\ND\ENSDF\XUNDL'
src_files = [
    '2026OSAA_CT11035_152Gd_Table_I_4-6.md',
    '2026OSAA_CT11035_152Gd_Table_I_7-9.md',
    '2026OSAA_CT11035_152Gd_Table_I_10-12.md',
    '2026OSAA_CT11035_152Gd_Table_I_13-15.md',
    '2026OSAA_CT11035_152Gd_Table_I_16-18.md',
]

def fix_unicode(s):
    return s.replace('\u2212','-').replace('\u2013','-').replace('\u2014','-')

# Parse all source
all_src = []
for sf in src_files:
    fpath = os.path.join(src_dir, sf)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    current_ei = ''
    current_jpi = ''
    for line in lines:
        line = line.strip()
        if not line.startswith('|'): continue
        if '$E_i$' in line or ':---' in line: continue
        parts = line.split('|')
        if parts and parts[0]=='': parts=parts[1:]
        if parts and parts[-1]=='': parts=parts[:-1]
        cells = [c.strip() for c in parts]
        while len(cells) < 9: cells.append('')
        ei_raw = fix_unicode(cells[0])
        jpi_raw = fix_unicode(cells[1])
        eg_raw = fix_unicode(cells[2])
        ig_raw = cells[3]
        mult_raw = fix_unicode(cells[6])
        delta_raw = fix_unicode(cells[7]) if len(cells)>7 else ''
        alpha_raw = cells[8] if len(cells)>8 else ''
        if ei_raw:
            m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_raw)
            current_ei = m.group(1) if m else ei_raw
            current_jpi = jpi_raw if jpi_raw else ''
        m_eg = re.match(r'([\d.]+)\s*\((\d+)\)', eg_raw) if eg_raw else None
        eg_val = m_eg.group(1) if m_eg else eg_raw
        eg_unc = m_eg.group(2) if m_eg else ''
        ig_clean = ig_raw.replace('\u2217','').replace('*','').strip()
        m_ig = re.match(r'([\d.]+)\s*\((\d+)\)', ig_clean) if ig_clean else None
        ig_val = m_ig.group(1) if m_ig else ig_clean
        ig_unc = m_ig.group(2) if m_ig else ''
        all_src.append({
            'Ei':current_ei,'Jpi':current_jpi,'Eg':eg_val,'DEg':eg_unc,
            'Ig':ig_val,'DIg':ig_unc,'Mult':mult_raw,'Delta':delta_raw,'Alpha':alpha_raw
        })

print(f'Source entries: {len(all_src)}')

# Parse ENSDF
ens_path = r'd:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens'
with open(ens_path, 'r') as f:
    ens = f.readlines()

ens_data = []
current_ei = None
for line in ens:
    s = line.rstrip('\n')
    if len(s) < 9: continue
    if s[7] == 'L':
        current_ei = s[9:19].strip()
    elif s[7] == 'G' and current_ei:
        eg = s[9:19].strip()
        de = s[19:21].strip()
        ri = s[22:29].strip()
        dri = s[29:31].strip()
        mult = s[32:41].strip()
        mr = s[41:49].strip()
        dmr = s[49:55].strip()
        cc = s[55:62].strip()
        dcc = s[62:64].strip()
        ens_data.append({
            'Ei':current_ei,'Eg':eg,'DEg':de,'Ig':ri,'DIg':dri,
            'Mult':mult,'MR':mr,'DMR':dmr,'CC':cc,'DCC':dcc
        })

print(f'ENSDF entries: {len(ens_data)}')

# Spot check 15%
random.seed(42)
sample_size = max(1, int(len(all_src) * 0.15))
sample = random.sample(range(len(all_src)), sample_size)
errors = []
checked = 0

for idx in sample:
    src = all_src[idx]
    # Find matching ENSDF entry
    match = None
    for e in ens_data:
        try:
            if abs(float(e['Ei'])-float(src['Ei'])) < 0.01 and abs(float(e['Eg'])-float(src['Eg'])) < 0.01:
                match = e
                break
        except:
            pass
    
    if match is None:
        errors.append('NOT FOUND: L={} Eg={}'.format(src['Ei'], src['Eg']))
        continue
    
    checked += 1
    
    if src['DEg'] != match['DEg']:
        errors.append('L={} Eg={}: DEg mismatch src={} ens={}'.format(src['Ei'], src['Eg'], src['DEg'], match['DEg']))
    
    # Ig: E0 with Ig=0 in source should have blank in ENSDF
    src_ig = src['Ig']
    ens_ig = match['Ig']
    if src['Mult'] == 'E0' and src_ig == '0':
        src_ig = ''  # E0 transitions should have blank RI
    if src_ig != ens_ig:
        errors.append('L={} Eg={}: Ig mismatch src={} ens={}'.format(src['Ei'], src['Eg'], src_ig, ens_ig))
    
    if src['DIg'] != match['DIg']:
        errors.append('L={} Eg={}: DIg mismatch src={} ens={}'.format(src['Ei'], src['Eg'], src['DIg'], match['DIg']))
    
    if src['Mult'] != match['Mult']:
        errors.append('L={} Eg={}: Mult mismatch src={} ens={}'.format(src['Ei'], src['Eg'], src['Mult'], match['Mult']))

print('\nChecked {} entries ({}% sample), {} errors'.format(checked, int(100*checked/len(all_src)), len(errors)))
for e in errors[:30]:
    print('  {}'.format(e))
if len(errors) > 30:
    print('  ... and {} more'.format(len(errors)-30))

# Also check level count
ens_levels = set()
for e in ens_data:
    ens_levels.add(e['Ei'])
print('\nUnique ENSDF levels: {}'.format(len(ens_levels)))

src_levels = set()
for s in all_src:
    src_levels.add(s['Ei'])
print('Unique source levels: {}'.format(len(src_levels)))
