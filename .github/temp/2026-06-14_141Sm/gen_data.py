"""
Generate ENSDF data section for 141Sm 116Cd(30Si,5ng).
Output: only L, G, and cG records (no header).
"""
import re

table_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()

rows = []
for line in table_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line \
       and 'Excitation' not in line and 'Footnote' not in line \
       and 'Asterisk' not in line and 'Superscript' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8:
            rows.append(parts)

def pvu(s):
    """Parse '810.6(2)' -> (810.6, '2', '810.6') or pure number"""
    s = s.strip()
    if not s: return '', '', ''
    # Remove trailing * (both ASCII and Unicode) or b
    clean = s.replace('\u2217','').replace('*','').replace('b','')
    m = re.match(r'^([+-]?\d+\.?\d*)\s*\((\d+)\)\s*$', clean)
    if m:
        return m.group(1), m.group(2), s
    m = re.match(r'^([+-]?\d+\.?\d*)\s*$', clean)
    if m:
        return m.group(1), '', s
    return clean, '', s

# Group by level
levels = {}
for row in rows:
    ex_val, ex_de, _ = pvu(row[0])
    ex_key = ex_val
    jpi = row[1]
    eg_val, eg_de, _ = pvu(row[2])
    has_star = '\u2217' in row[2] or '*' in row[2]
    int_val, int_de, _ = pvu(row[3])
    has_b = 'b' in row[3]
    # If intensity has no decimal (like 1000), keep as integer
    # Actually check: if it's a whole number like '1000.0', treat as '1000'
    if '.' in int_val and int_val.split('.')[1] == '0':
        int_val = int_val.split('.')[0]
    
    if ex_key not in levels:
        levels[ex_key] = {'ex_val': ex_val, 'ex_de': ex_de, 'jpi': jpi, 'gammas': []}
    levels[ex_key]['gammas'].append({
        'eg_val': eg_val, 'eg_de': eg_de, 'int_val': int_val, 'int_de': int_de,
        'rdco': row[4], 'rado': row[5], 'pol': row[6], 'assign': row[7],
        'star': has_star, 'b': has_b
    })

def map_m(assign):
    """Map assignment -> (M_field, needs_di0_comment)"""
    a = assign.strip()
    # ΔI=0 handling
    if 'Delta I' in a or '\\Delta I' in a:
        di0 = True
        if 'E1' in a: m = 'E1'
        elif 'M1' in a: m = 'M1'
        else: m = ''
        if '(' in a: m = f'({m})'
        return m, di0
    d = {
        'E2': ('E2', False), 'E1': ('E1', False), 'M1': ('M1', False),
        'Mixed M1+E2': ('M1+E2', False),
        '(E2)': ('(E2)', False), '(E1)': ('(E1)', False), '(M1)': ('(M1)', False),
        '(Mixed M1+E2)': ('(M1+E2)', False),
    }
    return d.get(a, ('', False))

lines = []

# Pre-existing levels
lines.append('141SM  L 0.0          1/2+'.ljust(80))
lines.append('141SM  L 175.9        11/2-'.ljust(80))

sorted_ex = sorted(levels.keys(), key=lambda k: float(k))

for ex_key in sorted_ex:
    lv = levels[ex_key]
    # L record
    lrec = f'141SM  L {lv["ex_val"].ljust(10)}{lv["ex_de"].ljust(2)} {lv["jpi"].ljust(17)}'.ljust(80)
    lines.append(lrec)
    
    gammas = sorted(lv['gammas'], key=lambda g: float(g['eg_val']))
    
    for g in gammas:
        m_val, needs_di0 = map_m(g['assign'])
        flag = 'X' if g['star'] else ' '
        
        # G record
        grec = f'141SM  G {g["eg_val"].ljust(10)}{g["eg_de"].ljust(2)} {g["int_val"].ljust(7)}{g["int_de"].ljust(2)} {m_val.ljust(9)}'
        grec = grec.ljust(76) + flag
        grec = grec.ljust(80)
        lines.append(grec)
        
        # cG comment
        parts = []
        if g['rdco']:
            rv, ru, _ = pvu(g['rdco'])
            parts.append(f'R{{-DCO}}={rv} {{I{ru}}}')
        if g['rado']:
            rv, ru, _ = pvu(g['rado'])
            parts.append(f'R{{-ADO}}={rv} {{I{ru}}}')
        if g['pol']:
            p = g['pol'].strip()
            rv, ru, _ = pvu(p)
            # pvu returns value with sign embedded; use directly
            parts.append(f'POL={rv} {{I{ru}}}')
        if needs_di0:
            parts.append('|DJ=0')
        if g['b']:
            parts.append('Composite intensity for 299.5- and 300.0-keV |g transitions')
        
        if parts:
            comment = '$' + ', '.join(parts) + '.'
            prefix = '141SM cG '
            max1 = 80 - len(prefix)
            
            # Try to fit on one line
            if len(comment) <= max1:
                lines.append((prefix + comment).ljust(80))
            else:
                # Find good break point before max1
                brk = max1
                # Look backward for comma+space
                for j in range(max1-1, max1-30, -1):
                    if j < len(comment) and comment[j] == ',' and comment[j-1] != ' ':
                        brk = j + 1
                        break
                if brk > max1 - 5: brk = max1  # not a good break found
                
                cpref = '141SM2cG '
                max2 = 80 - len(cpref)
                lines.append((prefix + comment[:brk]).ljust(80))
                rem = comment[brk:]
                
                if len(rem) <= max2:
                    lines.append((cpref + rem).ljust(80))
                else:
                    lines.append((cpref + rem[:max2]).ljust(80))
                    rem2 = rem[max2:]
                    cpref2 = '141SM3cG '
                    lines.append((cpref2 + rem2).ljust(80))

# Write
outpath = '.github/temp/2026-06-14_141Sm/data_section.txt'
with open(outpath, 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

l_cnt = sum(1 for l in lines if '  L ' in l and 'dL' not in l)
g_cnt = sum(1 for l in lines if '  G ' in l)
c_cnt = sum(1 for l in lines if 'cG ' in l)
print(f'Generated: L={l_cnt}, G={g_cnt}, cG={c_cnt}, Total={len(lines)}')

# Print a few samples
for i, line in enumerate(lines[2:12]):
    print(f'{i+2}: {line}')
