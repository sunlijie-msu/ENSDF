import re

with open(r'D:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Build level blocks
level_blocks = []
current_block = None

for i, line in enumerate(lines):
    raw = line.rstrip('\n')
    if len(raw) < 8:
        continue
    cont = raw[5]      # col 6: continuation label
    char6 = raw[6]     # col 7: 'c' for comment, ' ' for data
    rtype = raw[7]     # col 8: record type
    
    # G data record: col7=' ', col8='G'
    # cG comment: col7='c', col8='G'
    # L data record: col7=' ', col8='L'
    # cL comment: col7='c', col8='L'
    
    if cont == ' ' and char6 == ' ' and rtype == 'L':
        if current_block:
            level_blocks.append(current_block)
        E_str = raw[9:19].strip()
        try:
            E_lev = float(E_str)
            current_block = {'E': E_lev, 'line': i+1, 'gammas': []}
        except:
            current_block = None
    elif current_block is not None and cont == ' ' and char6 == ' ' and rtype == 'G':
        eg_str = raw[9:19].strip()
        ri_str = raw[22:29].strip()
        dri_str = raw[29:31].strip()
        flag = raw[76] if len(raw) > 76 else ' '
        try:
            eg = float(eg_str)
            ri = float(ri_str) if ri_str and ri_str not in ['LT','GT'] else None
            current_block['gammas'].append({
                'eg': eg, 'ri': ri, 'dri': dri_str,
                'flag': flag, 'line': i+1, 'cg_lines': []
            })
        except:
            pass
    elif current_block is not None and char6 == 'c' and rtype == 'G':
        # cG comment line - attach to last gamma
        content = raw[9:].strip()
        if current_block['gammas'] and 'RI$' in content:
            current_block['gammas'][-1]['cg_lines'].append(content)
    elif current_block is not None and cont in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk23456789' and char6 == 'c' and rtype == 'G':
        # continuation cG comment line
        content = raw[9:].strip()
        if current_block['gammas']:
            current_block['gammas'][-1]['cg_lines'].append(content)

if current_block:
    level_blocks.append(current_block)

# For each level, find normalization gamma (RI=100)
# and check if any NON-normalization gamma has a source that reported 100
print('=== Normalization Audit: Gammas with RI!=100 but some source reported 100 ===')
print()
issues = []

for block in level_blocks:
    E = block['E']
    gammas = block['gammas']
    if not gammas:
        continue
    
    # Find normalization gamma (RI=100)
    norm_gammas = [g for g in gammas if g['ri'] is not None and abs(g['ri']-100.0) < 0.1]
    non_norm_gammas = [g for g in gammas if g['ri'] is not None and abs(g['ri']-100.0) >= 0.1]
    
    if not norm_gammas:
        continue  # no normalization standard
    
    # For each non-normalization gamma, check if any cG line contains '100' as a value
    for g in non_norm_gammas:
        for cg in g['cg_lines']:
            if 'RI$' in cg or 'RI(' in cg:
                # Look for patterns like '100 {I' or 'RI=100' or '100 ('
                if re.search(r'\b100\b', cg):
                    issues.append((E, g['eg'], g['ri'], g['line'], cg))
                    break

print(f'Levels with potential normalization issues: {len(issues)}')
print()
for E, eg, ri, lineno, cg in issues:
    print(f'Level E={E} keV, Line {lineno}: G {eg} keV, RI={ri}')
    print(f'  cG: {cg[:100]}')
    print()
