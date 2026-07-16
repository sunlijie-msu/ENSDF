import re, sys

# ---- Parse Table I ----
source_text = open(r'd:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm_Table_I_revised.md', 'r', encoding='utf-8').read()

source_rows = []
for line in source_text.split('\n'):
    line = line.strip()
    if not line.startswith('|'):
        continue
    if '---' in line or 'Assignment' in line:
        continue
    # Split keeping all columns (including empty)
    cols = [c.strip() for c in line.split('|')]
    # cols: ['', Ex, Jpi, Eg, Intensity, RDCO, Rtheta, P, Assignment, '']
    if len(cols) >= 10:
        Ex = cols[1]
        Jpi = cols[2]
        Eg = cols[3]
        RI = cols[4]
        RDCO = cols[5]
        Rtheta = cols[6]
        P = cols[7]
        Assign = cols[8]
        if Eg:  # data row
            source_rows.append([Ex, Jpi, Eg, RI, RDCO, Rtheta, P, Assign])

print(f'Parsed {len(source_rows)} table rows')

# ---- Parse ENS file ----
ens_lines = open(r'd:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()

records = []
current_level = None

for line in ens_lines:
    line_orig = line.rstrip('\n')
    if len(line_orig) < 9:
        continue
    if line_orig[7:8] == 'L':
        e_str = line_orig[9:19].strip()
        de_str = line_orig[19:21].strip()
        j_str = line_orig[22:39].strip()
        current_level = {'E': e_str, 'DE': de_str, 'J': j_str, 'gammas': [], 'line': line_orig}
        records.append(current_level)
    elif line_orig[7:8] == 'G' and current_level is not None:
        eg_str = line_orig[9:19].strip()
        ri_str = line_orig[22:29].strip()
        dri_str = line_orig[29:31].strip()
        m_str = line_orig[32:41].strip()
        current_level['gammas'].append({
            'Eg': eg_str, 'RI': ri_str, 'DRI': dri_str, 'M': m_str,
            'comments': [], 'line': line_orig
        })
    elif line_orig[6:8] == 'cG' and current_level is not None and current_level['gammas']:
        current_level['gammas'][-1]['comments'].append(line_orig[9:].strip())

print(f'Parsed {len(records)} levels')

# ---- Cross-Check ----
print('\n' + '='*80)
print('CROSS-CHECK RESULTS')
print('='*80)

mismatches = []

for i, src in enumerate(source_rows):
    Ex, Jpi, Eg, RI, RDCO, Rtheta, P, Assign = src
    
    try:
        src_Eg_val = float(Eg.split('(')[0].rstrip('*'))
    except:
        print(f'Row {i+1}: Cannot parse Eg={Eg}')
        continue

    found = False
    for rec in records:
        for g in rec['gammas']:
            try:
                ens_Eg_val = float(g['Eg'])
            except:
                continue
            if abs(ens_Eg_val - src_Eg_val) < 0.3:
                found = True
                all_comments = ' '.join(g['comments'])
                
                print(f'\n--- Row {i+1}: Eg={Eg} ---')
                print(f'  Level:  Table Ex={Ex} J={Jpi}')
                print(f'          ENS  Ex={rec["E"]}({rec["DE"]}) J={rec["J"]}')
                print(f'  Gamma:  Table RI={RI} M={Assign}')
                print(f'          ENS  RI={g["RI"]}({g["DRI"]}) M={g["M"]}')
                print(f'  Table:  RDCO={RDCO} Rtheta={Rtheta} P={P}')
                
                # --- Check M field ---
                table_M = Assign
                ens_M = g['M']
                m_ok = False
                if table_M == 'Q' and ens_M in ['Q', '(E2)', 'E2']:
                    m_ok = True
                elif table_M == 'D+Q' and ens_M in ['D+Q', '(M1+E2)', 'M1+E2']:
                    m_ok = True
                
                m_status = 'OK' if m_ok else '** MISMATCH **'
                print(f'  M check: {m_status}')
                if not m_ok:
                    mismatches.append((i+1, 'M', table_M, ens_M))
                
                # --- Check RDCO in cG comments ---
                if RDCO:
                    # Already matched - just confirm present
                    m = re.search(r'([\d.]+)\((\d+)\)', RDCO)
                    if m:
                        expected = f'R{{-DCO}}={m.group(1)}'
                        if expected in all_comments:
                            print(f'  RDCO OK: {RDCO}')
                        else:
                            print(f'  ** RDCO mismatch: expected {expected} in comments')
                            mismatches.append((i+1, 'RDCO', RDCO, all_comments[:100]))
                
                # --- Check Rtheta (RADO) in cG comments ---
                if Rtheta:
                    m = re.search(r'([\d.]+)\((\d+)\)', Rtheta)
                    if m:
                        expected = f'R{{-ADO}}={m.group(1)}'
                        if expected in all_comments:
                            print(f'  RADO OK: {Rtheta}')
                        else:
                            print(f'  ** RADO mismatch: expected {expected} in comments')
                            mismatches.append((i+1, 'RADO', Rtheta, all_comments[:100]))
                
                # --- Check RI value ---
                # Parse table RI
                try:
                    tbl_ri_val = float(RI.split('(')[0])
                except:
                    tbl_ri_val = None
                try:
                    ens_ri_val = float(g['RI'])
                except:
                    ens_ri_val = None
                if tbl_ri_val is not None and ens_ri_val is not None:
                    if abs(tbl_ri_val - ens_ri_val) < 0.05:
                        print(f'  RI OK: {RI} vs {g["RI"]}')
                    else:
                        print(f'  ** RI mismatch: table={RI} ens={g["RI"]}')
                        mismatches.append((i+1, 'RI', RI, g['RI']))
                
                break
        if found:
            break
    
    if not found:
        print(f'\n--- Row {i+1}: Eg={Eg} ** NOT FOUND ** ---')
        mismatches.append((i+1, 'MISSING', Eg, ''))

print(f'\n{"="*80}')
print(f'TOTAL MISMATCHES: {len(mismatches)}')
for m in mismatches:
    print(f'  Row {m[0]}: {m[1]} mismatch - table={m[2]} ens={m[3]}')
