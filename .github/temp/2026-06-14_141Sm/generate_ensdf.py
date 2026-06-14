"""
Generate complete ENSDF file for 141Sm from 2026MAAA table.
"""
import re, math

# Read source table
table_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()

rows = []
for line in table_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line and 'Excitation' not in line and 'Footnote' not in line and 'Asterisk' not in line and 'Superscript' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8:
            rows.append(parts)

def parse_val_unc(s):
    """Parse '810.6(2)' -> (810.6, '2') or '1000.0' -> ('1000.0', '')"""
    m = re.match(r'([\d.]+)(?:\((\d+)\))?', s)
    if m:
        return m.group(1), m.group(2) if m.group(2) else ''
    return s, ''

def fmt_dp(val_str):
    """Count decimal places in value string"""
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def fmt_e(val_str):
    """Format energy value left-justified in cols 10-19 (10 chars)"""
    return val_str.ljust(10)

def fmt_de(de_str):
    """Format DE in cols 20-21 (2 chars)"""
    if not de_str: return '  '
    return de_str.ljust(2)

def fmt_j(j_str):
    """Format J in cols 23-39 (17 chars)"""
    return j_str.ljust(17)

def fmt_ri(ri_str):
    """Format RI in cols 23-29 (7 chars)"""
    return ri_str.ljust(7)

def fmt_dri(dri_str):
    """Format DRI in cols 30-31 (2 chars)"""
    if not dri_str: return '  '
    return dri_str.ljust(2)

def fmt_m(m_str):
    """Format M in cols 33-41 (9 chars)"""
    if not m_str: return ' ' * 9
    return m_str.ljust(9)

# Group rows by level energy
levels = {}
for row in rows:
    ex = row[0]
    ex_val, ex_de = parse_val_unc(ex)
    ex_key = ex_val  # group by exact value string
    
    jpi = row[1]
    eg = row[2]
    eg_val, eg_de = parse_val_unc(eg.replace('*', ''))
    has_star = '*' in eg
    
    intensity = row[3]
    int_val, int_de = parse_val_unc(intensity.replace('b', ''))
    has_b = 'b' in intensity
    
    rdco = row[4]
    rado = row[5]
    pol = row[6]
    assign = row[7]
    
    if ex_key not in levels:
        levels[ex_key] = {
            'ex_val': ex_val,
            'ex_de': ex_de,
            'jpi': jpi,
            'gammas': []
        }
    
    levels[ex_key]['gammas'].append({
        'eg_val': eg_val,
        'eg_de': eg_de,
        'int_val': int_val,
        'int_de': int_de,
        'rdco': rdco,
        'rado': rado,
        'pol': pol,
        'assign': assign,
        'star': has_star,
        'b': has_b,
        'eg_raw': eg,
    })

# Sort levels by energy
def ex_sort_key(k):
    try: return float(k)
    except: return 0
sorted_ex = sorted(levels.keys(), key=ex_sort_key)

# Generate ENSDF lines
lines = []

def make_l_record(ex_val, ex_de, jpi):
    """Generate 80-char L record"""
    nucid = '141SM'
    # cols 1-5: NUCID (3-digit mass + 2-letter element)
    line = nucid  # 5 chars
    line += ' '   # col 6 blank
    line += ' '   # col 7 blank
    line += 'L'   # col 8
    line += ' '   # col 9 blank
    line += fmt_e(ex_val)  # cols 10-19
    line += fmt_de(ex_de)  # cols 20-21
    line += ' '   # col 22 space
    line += fmt_j(jpi)    # cols 23-39
    # rest blank
    line = line.ljust(80)
    return line

def make_g_record(eg_val, eg_de, int_val, int_de, m_str, flag=''):
    """Generate 80-char G record"""
    nucid = '141SM'
    line = nucid  # cols 1-5
    line += ' '   # col 6
    line += ' '   # col 7
    line += 'G'   # col 8
    line += ' '   # col 9
    line += fmt_e(eg_val)   # cols 10-19
    line += fmt_de(eg_de)   # cols 20-21
    line += ' '   # col 22
    line += fmt_ri(int_val) # cols 23-29
    line += fmt_dri(int_de) # cols 30-31
    line += ' '   # col 32
    line += fmt_m(m_str)    # cols 33-41
    # Flag in col 77
    line = line.ljust(77)
    if flag:
        line += flag
    else:
        line += ' '
    line = line.ljust(80)
    return line

# Map assignments to M field
def map_m(assign):
    m = assign.strip()
    # Handle special cases
    if '$' in m:
        m = re.sub(r'\$.*?\$', '', m).strip()
        m = re.sub(r'\\Delta I\s*=\s*0,\s*', '', m).strip()
        m = m.replace(',', '').strip()
    
    mapping = {
        'E2': 'E2',
        'E1': 'E1',
        'M1': 'M1',
        'Mixed M1+E2': 'M1+E2',
        'M1+E2': 'M1+E2',
        '(E2)': '(E2)',
        '(E1)': '(E1)',
        '(M1)': '(M1)',
        '(Mixed M1+E2)': '(M1+E2)',
    }
    
    # Handle 'ΔI = 0, E1' -> E1
    if 'E1' in m and ('0' in m or 'ΔI' in m):
        return 'E1', True  # True = needs ΔI=0 comment
    if 'M1' in m and ('0' in m or 'ΔI' in m):
        return 'M1', True
    
    return mapping.get(m, ''), False

# Track L-record lines (need E for GLSC)
l_lines = {}

# Process all levels
for ex_key in sorted_ex:
    lv = levels[ex_key]
    ex_val = lv['ex_val']
    ex_de = lv['ex_de']
    jpi = lv['jpi']
    gammas = lv['gammas']
    
    # Sort gammas by energy
    gammas_sorted = sorted(gammas, key=lambda g: float(g['eg_val']))
    
    # L record
    lrec = make_l_record(ex_val, ex_de, jpi)
    lines.append(('L', ex_val, lrec))
    
    # G records
    for g in gammas_sorted:
        m_val, needs_di0 = map_m(g['assign'])
        flag = 'X' if g['star'] else ''
        grec = make_g_record(g['eg_val'], g['eg_de'], g['int_val'], g['int_de'], m_val, flag)
        lines.append(('G', g['eg_val'], grec))

# Write generated data section to file
with open('.github/temp/2026-06-14_141Sm/generated_data.txt', 'w', encoding='utf-8') as f:
    for typ, val, line in lines:
        f.write(line + '\n')

print(f'Generated {len(lines)} lines ({sum(1 for t,_,_ in lines if t=="L")} L, {sum(1 for t,_,_ in lines if t=="G")} G)')

# Print first 20 lines for verification
for i, (typ, val, line) in enumerate(lines[:20]):
    print(f'{typ} {val}: {line[:60]}...')
