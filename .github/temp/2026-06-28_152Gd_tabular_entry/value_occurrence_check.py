"""
Value Occurrence Check per SKILL.md:
Verify every level appearing as both Ei and Ef has identical
energy string, uncertainty, and J-pi across all occurrences.
"""
import re, os

md_path = r'd:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_I.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# ============================================================
# STEP 1: Build canonical level registry from Ei occurrences
# ============================================================
canonical = {}  # energy_float -> list of (energy_string, uncertainty, Jpi, line_numbers)
data_rows = []
current_ei_str = None
current_ei_de = None
current_jpi_i = None
row_num = 0

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
    jpi_i_raw = cells[1]
    eg_raw = cells[2]
    ef_raw = cells[4]
    jpi_f_raw = cells[5]
    
    row_num += 1
    
    # Update current Ei if provided
    if ei_raw:
        ei_clean = ei_raw.replace('\u2212','-')
        m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_clean)
        if m:
            current_ei_str = m.group(1)
            current_ei_de = m.group(2)
        else:
            current_ei_str = ei_clean
            current_ei_de = ''
        current_jpi_i = jpi_i_raw.replace('\u2212','-') if jpi_i_raw else ''
        
        # Register in canonical
        try:
            ei_f = float(current_ei_str)
            full_str = ei_raw  # keep original for comparison
            if ei_f not in canonical:
                canonical[ei_f] = []
            canonical[ei_f].append({
                'full_str': full_str,
                'energy': current_ei_str,
                'de': current_ei_de,
                'jpi': current_jpi_i,
                'line': ln,
                'role': 'Ei'
            })
        except ValueError:
            pass
    
    # Parse Ef
    ef_clean = ef_raw.replace('\u2212','-')
    m_ef = re.match(r'([\d.]+)\s*\((\d+)\)', ef_clean)
    if m_ef:
        ef_str = m_ef.group(1)
        ef_de = m_ef.group(2)
    else:
        ef_str = ef_clean
        ef_de = ''
    
    jpi_f = jpi_f_raw.replace('\u2212','-') if jpi_f_raw else ''
    
    data_rows.append({
        'row': row_num,
        'line': ln,
        'Ei_str': ei_raw,
        'Ei': current_ei_str,
        'DEi': current_ei_de,
        'Jpi_i': current_jpi_i,
        'Eg': eg_raw,
        'Ef_str': ef_raw,
        'Ef': ef_str,
        'DEf': ef_de,
        'Jpi_f': jpi_f,
    })

print('Canonical levels from Ei occurrences: {}'.format(len(canonical)))
print('Total data rows: {}'.format(len(data_rows)))
print()

# ============================================================
# STEP 2: Check Ef references against canonical registry
# ============================================================
errors = []
warnings = []

for row in data_rows:
    ef_str = row['Ef']
    jpi_f = row['Jpi_f']
    ef_raw = row['Ef_str']
    
    if not ef_str or ef_str == '0':
        # Ground state - special case, always 0+
        if jpi_f and jpi_f != '0+':
            errors.append('Row {} Ln {}: Ground state Ef Jpi={} expected 0+'.format(row['row'], row['line']))
        continue
    
    try:
        ef_f = float(ef_str)
    except ValueError:
        continue
    
    # Find matching canonical level (within 0.02 keV tolerance)
    matches = []
    for can_ei, entries in canonical.items():
        if abs(can_ei - ef_f) < 0.02:
            matches.extend(entries)
    
    if not matches:
        # Try wider tolerance
        for can_ei, entries in canonical.items():
            if abs(can_ei - ef_f) < 1.0:
                matches.extend(entries)
        if matches:
            warnings.append('Row {} Ln {}: Ef={} matched canonical {} (tolerance {:.2f} keV > 0.02)'.format(
                row['row'], row['line'], ef_str, matches[0]['energy'],
                abs(float(matches[0]['energy']) - ef_f)))
    
    if not matches:
        errors.append('Row {} Ln {}: Ef={} NOT FOUND in canonical registry (Ei={}, Eg={})'.format(
            row['row'], row['line'], ef_str, row['Ei'], row['Eg']))
        continue
    
    # Get canonical Jpi
    can_jpis = set(m['jpi'] for m in matches)
    can_energies = set(m['full_str'] for m in matches)
    
    # Check Jpi consistency
    if jpi_f:
        if jpi_f not in can_jpis and '' not in can_jpis:
            # Jpi_f doesn't match any canonical Jpi
            errors.append('Row {} Ln {}: Ef={} Jpi_f={} but canonical Jpi={} (Ei={}, Eg={})'.format(
                row['row'], row['line'], ef_str, jpi_f, can_jpis, row['Ei'], row['Eg']))
    
    # Check energy string (if Ef has uncertainty)
    if row['DEf']:
        # Ef has explicit uncertainty - check character match
        ef_full = ef_raw.replace('\u2212','-')
        found_match = False
        for m in matches:
            can_full = m['full_str'].replace('\u2212','-')
            if ef_full == can_full:
                found_match = True
                break
        if not found_match:
            warnings.append('Row {} Ln {}: Ef={} string differs from canonical {} (Ei={})'.format(
                row['row'], row['line'], ef_raw, can_energies, row['Ei']))

print('=== ERRORS ({} found) ==='.format(len(errors)))
for e in errors:
    print('  ' + e)

print()
print('=== WARNINGS ({} found) ==='.format(len(warnings)))
for w in warnings:
    print('  ' + w)

# ============================================================
# STEP 3: Check canonical registry internal consistency
# ============================================================
print()
print('=== CANONICAL REGISTRY INTERNAL CHECK ===')
reg_errors = []
for ei_f, entries in canonical.items():
    if len(entries) > 1:
        jpis = set(e['jpi'] for e in entries)
        strs = set(e['full_str'].replace('\u2212','-') for e in entries)
        des = set(e['de'] for e in entries)
        if len(jpis) > 1:
            reg_errors.append('Level {} keV: Jpi inconsistency across Ei rows: {}'.format(
                ei_f, [(e['jpi'], e['line']) for e in entries]))
        if len(strs) > 1:
            reg_errors.append('Level {} keV: energy string differs across Ei rows: {}'.format(
                ei_f, [(e['full_str'], e['line']) for e in entries]))
        if len(des) > 1:
            reg_errors.append('Level {} keV: DE differs across Ei rows: {}'.format(
                ei_f, [(e['de'], e['line']) for e in entries]))

if reg_errors:
    print('{} internal inconsistencies:'.format(len(reg_errors)))
    for e in reg_errors:
        print('  ' + e)
else:
    print('All canonical levels internally consistent.')

# ============================================================
# STEP 4: Check levels appearing only as Ef (never as Ei)
# ============================================================
print()
print('=== LEVELS APPEARING ONLY AS Ef ===')
unique_ef = set()
for row in data_rows:
    try:
        ef_f = float(row['Ef'])
        if ef_f > 0:
            unique_ef.add((ef_f, row['Ef_str'], row['Jpi_f']))
    except:
        pass

only_ef = []
for ef_f, ef_str, jpi_f in sorted(unique_ef):
    if ef_f not in canonical:
        only_ef.append((ef_f, ef_str, jpi_f))

if only_ef:
    print('{} level(s) appear only as Ef (never as Ei):'.format(len(only_ef)))
    for ef_f, ef_str, jpi_f in only_ef:
        print('  {} keV, Jpi={}'.format(ef_str, jpi_f))
else:
    print('None - all levels appear at least once as Ei.')

# Final summary
total_issues = len(errors) + len(reg_errors)
print()
print('=' * 60)
if total_issues == 0:
    print('PASS: No value occurrence errors found.')
else:
    print('FAIL: {} error(s) found.'.format(total_issues))
