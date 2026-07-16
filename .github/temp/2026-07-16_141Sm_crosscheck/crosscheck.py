import re, sys

# ---- Parse Table I (source) ----
source_text = open(r'd:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm_Table_I_revised.md', 'r', encoding='utf-8').read()

source_rows = []
for line in source_text.split('\n'):
    line = line.strip()
    if line.startswith('|') and 'keV' not in line and '---' not in line and 'Assignment' not in line and 'Intensity' not in line:
        cols = [c.strip() for c in line.split('|')]
        cols = [c for c in cols if c]
        if len(cols) >= 7:
            source_rows.append(cols)

print('=== Source Table I entries ===')
for i, row in enumerate(source_rows):
    print(f'{i+1}: Ex={row[0]} Jpi={row[1]} Eg={row[2]} RI={row[3]} RDCO={row[4] if len(row)>4 else ""} Rth={row[5] if len(row)>5 else ""} P={row[6] if len(row)>6 else ""} M={row[7] if len(row)>7 else ""}')

# ---- Parse ENS file ----
ens_lines = open(r'd:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()

records = []
current_level = None

for line in ens_lines:
    line = line.rstrip('\n')
    if len(line) < 9:
        continue
    if line[7:8] == 'L':
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        j_str = line[22:39].strip()
        current_level = {'E': e_str, 'DE': de_str, 'J': j_str, 'gammas': []}
        records.append(current_level)
    elif line[7:8] == 'G' and current_level is not None:
        eg_str = line[9:19].strip()
        deg_str = line[19:21].strip()
        ri_str = line[22:29].strip()
        dri_str = line[29:31].strip()
        m_str = line[32:41].strip()
        current_level['gammas'].append({
            'Eg': eg_str, 'DEg': deg_str, 'RI': ri_str, 'DRI': dri_str, 'M': m_str,
            'comments': [], 'line': line
        })
    elif line[6:8] == 'cG' and current_level is not None and current_level['gammas']:
        current_level['gammas'][-1]['comments'].append(line[9:].strip())

print('\n=== Cross-Check Results ===')
mismatches = []

for i, src in enumerate(source_rows):
    src_Ex, src_Jpi = src[0], src[1]
    src_Eg = src[2]
    src_RI = src[3]
    src_rdco = src[4] if len(src) > 4 else ''
    src_rtheta = src[5] if len(src) > 5 else ''
    src_pol = src[6] if len(src) > 6 else ''
    src_assign = src[7] if len(src) > 7 else ''

    src_Eg_val = float(src_Eg.split('(')[0].rstrip('*'))

    found = False
    for rec in records:
        for g in rec['gammas']:
            try:
                ens_Eg_val = float(g['Eg'])
            except:
                continue
            if abs(ens_Eg_val - src_Eg_val) < 0.2:
                found = True
                all_comments = ' '.join(g['comments'])
                
                print(f'\nRow {i+1}: Eg={src_Eg} (Level: Table Ex={src_Ex} | ENS Ex={rec["E"]})')
                
                # Check M field
                table_M = src_assign
                ens_M = g['M']
                m_ok = False
                if table_M == 'Q' and ens_M in ['Q', '(E2)', 'E2']:
                    m_ok = True
                elif table_M == 'D+Q' and ens_M in ['D+Q', '(M1+E2)', 'M1+E2']:
                    m_ok = True
                
                if not m_ok:
                    print(f'  ** M MISMATCH: table="{table_M}"  ens="{ens_M}"')
                    mismatches.append((i+1, 'M', table_M, ens_M, g['line']))
                else:
                    print(f'  M OK: {table_M} -> {ens_M}')
                
                # Check RDCO
                if src_rdco:
                    m = re.search(r'([\d.]+)\((\d+)\)', src_rdco)
                    if m:
                        val, unc = m.group(1), m.group(2)
                        # Check if both value and uncertainty match
                        expected = f'R{{-DCO}}={val}'
                        if expected not in all_comments:
                            print(f'  ** RDCO value mismatch: expected {expected}')
                            mismatches.append((i+1, 'RDCO_val', f'{val}({unc})', all_comments[:80], g['line']))
                        else:
                            # Check uncertainty
                            # Look for {Iunc} after the value
                            expected_full = f'R{{-DCO}}={val} {{I{unc}}}'
                            if expected_full in all_comments:
                                print(f'  RDCO OK: {val}({unc})')
                            else:
                                print(f'  ** RDCO unc check: table={src_rdco}, looking for {val} {{I{unc}}}')
                                print(f'     Found in comments: {all_comments[:120]}')
                        # Check uncertainty format
                        expected_iunc = f'R{{-DCO}}={val}'
                        if expected_iunc in all_comments:
                            pass  # value present
                        else:
                            mismatches.append((i+1, 'RDCO_val', f'{val}({unc})', 'not found', g['line']))
                
                # Check Rtheta (RADO)
                if src_rtheta:
                    m = re.search(r'([\d.]+)\((\d+)\)', src_rtheta)
                    if m:
                        val, unc = m.group(1), m.group(2)
                        expected_full = f'R{{-ADO}}={val}'
                        if expected_full not in all_comments:
                            print(f'  ** RADO value mismatch: expected R{{-ADO}}={val}')
                            mismatches.append((i+1, 'RADO_val', f'{val}({unc})', all_comments[:80], g['line']))
                        else:
                            print(f'  RADO OK: {val}({unc})')
                
                # Check POL if present in table
                if src_pol:
                    print(f'  POL: table={src_pol} (check manually)')
                
                break
        if found:
            break
    if not found:
        print(f'\nRow {i+1}: Eg={src_Eg} ** NOT FOUND in ENS!')
        mismatches.append((i+1, 'MISSING', src_Eg, '', ''))

print(f'\n=== Summary: {len(mismatches)} mismatches found ===')
for m in mismatches:
    print(f'  Row {m[0]}: {m[1]} mismatch')
