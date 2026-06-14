"""
Generate complete ENSDF file for 141Sm 116Cd(30Si,5ng) from 2026MAAA table.
Includes header, L-records, G-records, and cG comments.
"""
import re

# ===================== HEADER =====================
header = """141SM    116CD(30SI,5NG):XUNDL-3       2026MAAA                                 
141SM dL E$Least-squares fitting is done by GLSC (version 21-Apr-2026)          
141SM c  Compiled by L. J. Sun and J. Chen (FRIB, MSU), June 13, 2026.          
141SM c  Phys. Rev. C xxx, xxxxxx (2026).                                       
141SM c  2026MaAA: E{-lab}=149 MeV 30Si beam was impinged on a 2.4-mg/cm2 99%   
141SM2c  enriched 116Cd target backed by 10.8-mg/cm2 208Pb. States of 141Sm were
141SM3c  populated via the 116Cd(30Si,5n)141Sm fusion-evaporation reaction and  
141SM4c  the deexciting |g rays were detected by the Indian National Gamma Array
141SM5c  (INGA), consisting of 17 Compton-suppressed Clover HPGe detectors      
141SM6c  arranged in six angles 90|'|'(4), 40|'|'(3), 65|'|'(1), 115|'|'(3),   
141SM7c  140|'|'(3) and 157|'|'(3)] with respect to the beam axis (the number   
141SM8c  in the parenthesis indicates the detector numbers at each angles).     
141SM9c  Measured E|g, I|g, |g|g-coin, |g|g(|q), |g|g(|q)(DCO), |g|g(|q)(ADO),  
141SMAc  and linear polarization (POL). Deduced levels, J, |p, |g-ray           
141SMBc  multipolarities, and lifetimes using DSAM and transition strengths.     
141SMCc  Comparisons with large-scale shell-model calculations using the PBPKH   
141SMDc  interaction.                                                           
141SM cG E,RI$From 2026MaAA, unless otherwise noted.                            
141SM cG M$As given in 2026MaAA. Multipolarities for newly observed |g           
141SM2cG transitions are assigned based on measured DCO ratios. Expected R{-DCO}
141SM3cG values in a stretched quadrupole gate are R{-DCO}(Q)|?1.0 for stretched
141SM4cG quadrupole (|DJ=2) or unstretched dipole (|DJ=0) transitions;          
141SM5cG R{-DCO}(Q)|?0.5 for stretched dipole (|DJ=1) transitions. Expected     
141SM6cG R{-ADO} values are R{-ADO}|?1.6 for stretched quadrupole (|DJ=2);      
141SM7cG R{-ADO}|?0.65 for stretched dipole (|DJ=1) transitions. A positive POL 
141SM8cG indicates an electric type transition, and a negative POL indicates a  
141SM9cG magnetic type transition.                                              
141SM cG M(P)$Quoted multipolarities from 2000Po03, 1971Al31, and 1974Ja26 by   
141SM2cG 2026MaAA authors.                                                      
141SM cG M(S)$Deduced from spin difference between initial and final levels by  
141SM2cG 2026MaAA authors.                                                      
141SM cL E$From a least-squares fit to |g-ray energies (by compiler).           
141SM cL J$As given in 2026MaAA, unless otherwise noted.                        
141SM PN                                                                     5  
"""

# ===================== DATA =====================
# Read table
table_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()

rows = []
for line in table_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line and 'Excitation' not in line and 'Footnote' not in line and 'Asterisk' not in line and 'Superscript' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8:
            rows.append(parts)

def parse_val_unc(s):
    """Parse '810.6(2)' -> (810.6, '2')"""
    m = re.match(r'([\d.]+)(?:\((\d+)\))?', s)
    if m:
        return m.group(1), m.group(2) if m.group(2) else ''
    return s, ''

def mk_line(left, content):
    """Make an 80-char line: '141SM' + left-justified content padded to 80"""
    return f'141SM{left}{content}'.ljust(80)

# Group by level
levels = {}
for row in rows:
    ex_val, ex_de = parse_val_unc(row[0])
    ex_key = ex_val
    jpi = row[1]
    eg_raw = row[2]
    eg_val, eg_de = parse_val_unc(eg_raw.replace('*', ''))
    has_star = '*' in eg_raw
    int_raw = row[3]
    int_val, int_de = parse_val_unc(int_raw.replace('b', ''))
    has_b = 'b' in int_raw
    
    if ex_key not in levels:
        levels[ex_key] = {'ex_val': ex_val, 'ex_de': ex_de, 'jpi': jpi, 'gammas': []}
    levels[ex_key]['gammas'].append({
        'eg_val': eg_val, 'eg_de': eg_de, 'int_val': int_val, 'int_de': int_de,
        'rdco': row[4], 'rado': row[5], 'pol': row[6], 'assign': row[7],
        'star': has_star, 'b': has_b
    })

def map_m(assign):
    """Map assignment to M field + special flags"""
    a = assign.strip()
    # ΔI=0 cases
    if '\\Delta I' in a or ('0' in a and ('E1' in a or 'M1' in a)):
        di0 = True
        if 'E1' in a: m = 'E1'
        elif 'M1' in a: m = 'M1'
        else: m = ''
        if '(' in a: m = f'({m})'
        return m, di0
    
    mapping = {
        'E2': ('E2', False), 'E1': ('E1', False), 'M1': ('M1', False),
        'Mixed M1+E2': ('M1+E2', False),
        '(E2)': ('(E2)', False), '(E1)': ('(E1)', False), '(M1)': ('(M1)', False),
        '(Mixed M1+E2)': ('(M1+E2)', False),
    }
    return mapping.get(a, ('', False))

def fmt_col(val, width, left=True):
    """Format value in fixed-width column"""
    s = str(val)
    if left: return s.ljust(width)
    return s.rjust(width)

# Generate output
output_lines = []
output_lines.append(header.rstrip())

# Pre-existing levels not in table
output_lines.append(f'141SM  L 0.0          1/2+'.ljust(80))
output_lines.append(f'141SM  L 175.9        11/2-'.ljust(80))

sorted_ex = sorted(levels.keys(), key=lambda k: float(k))

for ex_key in sorted_ex:
    lv = levels[ex_key]
    ex_v = lv['ex_val']
    ex_d = lv['ex_de']
    jpi = lv['jpi']
    
    # L record: cols 1-5=NUCID, 6=' ', 7=' ', 8='L', 9=' ', 10-19=E(left), 20-21=DE, 22=' ', 23-39=J(left)
    lrec = f'141SM  L {ex_v.ljust(10)}{ex_d.ljust(2)} {jpi.ljust(17)}'.ljust(80)
    output_lines.append(lrec)
    
    # Sort gammas by energy
    gammas = sorted(lv['gammas'], key=lambda g: float(g['eg_val']))
    
    for g in gammas:
        eg_v = g['eg_val']
        eg_d = g['eg_de']
        int_v = g['int_val']
        int_d = g['int_de']
        m_val, needs_di0 = map_m(g['assign'])
        flag = 'X' if g['star'] else ' '
        
        # G record: cols 1-5=NUCID, 10-19=Eg, 20-21=DEg, 22=' ', 23-29=RI, 30-31=DRI, 32=' ', 33-41=M, 77=flag
        grec = f'141SM  G {eg_v.ljust(10)}{eg_d.ljust(2)} {int_v.ljust(7)}{int_d.ljust(2)} {m_val.ljust(9)}'
        grec = grec.ljust(77) + flag
        grec = grec.ljust(80)
        output_lines.append(grec)
        
        # Build cG comment
        parts = []
        if g['rdco']:
            rv, ru = parse_val_unc(g['rdco'])
            parts.append(f'R{{-DCO}}={rv} {{I{ru}}}')
        if g['rado']:
            rv, ru = parse_val_unc(g['rado'])
            parts.append(f'R{{-ADO}}={rv} {{I{ru}}}')
        if g['pol']:
            pol_str = g['pol']
            if not pol_str.startswith('+') and not pol_str.startswith('-'):
                pol_str = '+' + pol_str
            rv, ru = parse_val_unc(pol_str.replace('+','').replace('-',''))
            parts.append(f'POL={pol_str} {{I{ru}}}')
        if needs_di0:
            parts.append('|DJ=0')
        if g['b']:
            parts.append('Composite intensity for 299.5- and 300.0-keV |g transitions')
        
        if parts:
            comment = '$' + ', '.join(parts) + '.'
            # Fit into 80-char lines with continuation
            prefix = '141SM cG '
            cpref = '141SM2cG '
            cpref2 = '141SM3cG '
            max1 = 80 - len(prefix)
            maxN = 80 - len(cpref)
            if len(comment) <= max1:
                output_lines.append((prefix + comment).ljust(80))
            elif len(comment) <= max1 + maxN:
                # Split into 2 lines
                output_lines.append((prefix + comment[:max1]).ljust(80))
                output_lines.append((cpref + comment[max1:]).ljust(80))
            else:
                output_lines.append((prefix + comment[:max1]).ljust(80))
                rem = comment[max1:]
                output_lines.append((cpref + rem[:maxN]).ljust(80))
                rem2 = rem[maxN:]
                output_lines.append((cpref2 + rem2).ljust(80))

# Write
with open('.github/temp/2026-06-14_141Sm/141Sm_generated.ens', 'w', encoding='utf-8') as f:
    for line in output_lines:
        f.write(line + '\n')

print(f'Generated {len(output_lines)} lines')
print(f'First few lines:')
for i, line in enumerate(output_lines[:30]):
    print(f'{i}: {line[:70]}')

# Also count
l_count = sum(1 for l in output_lines if '  L ' in l and 'dL' not in l)
g_count = sum(1 for l in output_lines if '  G ' in l)
cg_count = sum(1 for l in output_lines if 'cG ' in l)
print(f'\nCounts: L={l_count}, G={g_count}, cG={cg_count}, Total={len(output_lines)}')
