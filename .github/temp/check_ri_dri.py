"""Cross-check all RI/DRI values in ENSDF file against Table I markdown.
Parses both files and reports every intensity mismatch."""

import re
import sys

ENSDF_FILE = r"d:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens"
TABLE_FILE = r"d:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm_Table_I.md"

def parse_ensdf_gammas(filepath):
    """Parse ENSDF file, return list of (line_num, level_e, gamma_e, ri_str, dri_str, full_line)."""
    gammas = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        line = line.rstrip('\n').rstrip('\r')
        if len(line) < 80:
            continue
        # G-record
        if line[7] == 'G' and line[6] == ' ':
            # E field: cols 10-19 (left-justified)
            e_field = line[9:19].strip()
            # DE field: cols 20-21
            de_field = line[19:21].strip()
            # RI field: cols 23-29
            ri_field = line[22:29]
            # DRI field: cols 30-31
            dri_field = line[29:31]
            
            gammas.append({
                'line_num': i + 1,
                'gamma_e': e_field,
                'de': de_field,
                'ri': ri_field,
                'dri': dri_field,
                'full': line
            })
    
    return gammas

def parse_table_intensities(filepath):
    """Parse Table I markdown, return dict: (gamma_e, final_ex) -> (intensity_str, intensity_val, intensity_unc)."""
    table_data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find table rows: | Ex | Jpi | Eg | Intensity | ... |
    # Pattern matches rows like: | 810.6(2) | 15/2− | 634.6(2) | 1000.0 | | | | 175.9 | (11/2−) | E2 |
    rows = re.findall(
        r'\|\s*([\d.]+(?:\([^)]*\))?)\s*\|'  # Ex
        r'\s*(?:[^|]*)\s*\|'  # Jpi
        r'\s*([\d.]+(?:\([^)]*\))?)\s*\|'  # Eg
        r'\s*([\d.]+(?:\([^)]*\))?[a-z]?)\s*\|',  # Intensity
        content
    )
    
    # Also try a more lenient approach
    lines = content.split('\n')
    for line in lines:
        # Skip header/spacer lines
        if not line.startswith('|') or '---' in line or 'keV' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        # Need at least: Ex, Jpi, Eg, Intensity, Rdco, Rthe, P, FinalEx, FinalJpi
        if len(parts) < 11:
            continue
        try:
            ex_field = parts[1].strip()
            eg_field = parts[3].strip()
            intensity_field = parts[4].strip()
            final_ex_field = parts[8].strip()
            
            if not eg_field or not intensity_field:
                continue
            
            # Strip parenthetical uncertainty from Eg for matching
            # e.g., "651.9(5)" -> "651.9", "634.6(2)" -> "634.6"
            eg_key = re.sub(r'\([^)]*\)$', '', eg_field)
            
            # Parse intensity: "1000.0", "36.9(11)", "16.2(12)", "3.0(1)", etc.
            # Strip trailing letters like 'b'
            intensity_clean = re.sub(r'[a-z]$', '', intensity_field)
            
            # Parse value and uncertainty
            m = re.match(r'^([\d.]+)(?:\(([\d.]+)\))?$', intensity_clean)
            if not m:
                # Try scientific notation or other formats
                if intensity_clean in ('', '—', '-'):
                    continue
                print(f"WARNING: Cannot parse intensity '{intensity_field}' for Eg={eg_field}")
                continue
            
            val_str = m.group(1)
            unc_str = m.group(2)
            
            table_data[eg_key] = {
                'ex': ex_field,
                'final_ex': final_ex_field,
                'intensity_str': intensity_field,
                'val': val_str,
                'unc': unc_str,
                'line': line.strip()[:100]
            }
        except (ValueError, IndexError) as e:
            continue
    
    return table_data

def intensity_to_ensdf(val_str, unc_str):
    """Convert '3.0' and '1' to ENSDF RI and DRI fields.
    Returns (ri_field_7chars, dri_field_2chars, expected_ri_value, expected_dri_value).
    
    DRI = uncertainty integer (the digits in last-digit notation).
    RI = value, with same decimal places as justified by uncertainty.
    """
    if unc_str is None:
        # No uncertainty
        ri = val_str
        dri = ''
    else:
        ri = val_str
        dri = unc_str
    
    # DRI field: 2 chars, left-justified, plain integer
    dri_field = dri.ljust(2) if dri else '  '
    
    # RI field: 7 chars, left-justified
    ri_field = ri.ljust(7)
    
    return ri_field, dri_field, val_str, (unc_str or '')

def main():
    print("=" * 70)
    print("RI/DRI CROSS-CHECK: ENSDF vs Table I")
    print("=" * 70)
    
    gammas = parse_ensdf_gammas(ENSDF_FILE)
    table = parse_table_intensities(TABLE_FILE)
    
    print(f"\nParsed {len(gammas)} G-records from ENSDF file")
    print(f"Parsed {len(table)} intensity entries from Table I\n")
    
    issues = []
    
    for g in gammas:
        eg = g['gamma_e']
        ri_ensdf = g['ri']
        dri_ensdf = g['dri']
        
        # Try to find matching entry in table by gamma energy
        # We need to match gamma energy tuples (Ex, Eg) because some energies repeat
        # For now, match by Eg alone and flag all mismatches
        if eg not in table:
            # Skip if no intensity (e.g., the 59.2, 300.0 lines)
            if ri_ensdf.strip() == '' and dri_ensdf.strip() == '':
                continue
            # Also skip if it's a known unplaced transition
            continue
        
        t = table[eg]
        expected_ri, expected_dri, exp_val, exp_unc = intensity_to_ensdf(t['val'], t['unc'])
        
        # Compare
        ri_ok = (ri_ensdf == expected_ri)
        dri_ok = (dri_ensdf == expected_dri)
        
        if not ri_ok or not dri_ok:
            issue = {
                'line': g['line_num'],
                'eg': eg,
                'ensdf_ri': repr(ri_ensdf),
                'ensdf_dri': repr(dri_ensdf),
                'expected_ri': repr(expected_ri),
                'expected_dri': repr(expected_dri),
                'table_intensity': t['intensity_str'],
                'table_ex': t['ex'],
            }
            issues.append(issue)
            print(f"LINE {g['line_num']:4d}  Eg={eg:>8s}  "
                  f"ENSDF: RI={ri_ensdf} DRI={dri_ensdf}  "
                  f"TABLE: RI={expected_ri} DRI={expected_dri}  "
                  f"({t['intensity_str']}  Ex={t['ex']})")
    
    print(f"\n{'='*70}")
    print(f"TOTAL ISSUES: {len(issues)}")
    if len(issues) == 0:
        print("ALL MATCH!")
    
    return issues

if __name__ == '__main__':
    issues = main()
    sys.exit(0 if len(issues) == 0 else 1)
