#!/usr/bin/env python3
"""
Cross-check Cl34_adopted.ens level energies (from L 7018.9 onwards) against
Cl34_33s_p_g.ens (dataset K) and Cl34_33s_p_p_resonances.ens (dataset L).

Column positions (1-based):
  L-record primary: col6=' ', col7=' ', col8='L'; E=cols10-19, DE=cols20-21
  XREF line:        col6='X', col7=' ', col8='L'
  cL comment:       col6=' ', col7='c', col8='L'; text=cols10+
  2cL continuation: col6='2', col7='c', col8='L'
"""

import re
import sys
import subprocess
import math

ADOPTED_FILE = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens"
K_FILE       = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens"
L_FILE       = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens"
JAVA_AVG     = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"


def parse_ensdf_value(e_str, de_str):
    """Parse energy and uncertainty; return (E_float, DE_float_absolute, E_str, DE_str)."""
    e_str = e_str.strip()
    de_str = de_str.strip()
    try:
        e_val = float(e_str)
    except ValueError:
        return None, None, e_str, de_str
    if not de_str or de_str in ('', '  '):
        return e_val, None, e_str, de_str
    if de_str in ('LT', 'GT'):
        return e_val, de_str, e_str, de_str
    try:
        de_int = int(de_str)
    except ValueError:
        return e_val, None, e_str, de_str
    # last-digit notation: count decimal places in e_str
    if '.' in e_str:
        decimal_places = len(e_str.rstrip('0').split('.')[1]) if '.' in e_str else 0
        # Handle trailing zeros: keep them
        decimal_places = len(e_str.split('.')[1])
    else:
        decimal_places = 0
    de_abs = de_int * (10 ** (-decimal_places))
    return e_val, de_abs, e_str, de_str


def parse_l_records(filepath):
    """Parse all L-records from an ENSDF file.
    Returns dict: {E_str: {'e': float, 'de': float, 'e_str': str, 'de_str': str}}
    Also returns list of (E_str, e_float, de_float, e_raw, de_raw) in order.
    """
    records = {}
    ordered = []
    with open(filepath, encoding='ascii', errors='replace') as f:
        lines = f.readlines()
    for line in lines:
        if len(line) < 21:
            continue
        # Check if it's an L-record (col 8 = 'L', col 7 = ' ')
        if len(line) >= 9 and line[7] == 'L' and line[6] == ' ':
            # Continuation check: col 6 should be blank for primary record
            if line[5] not in (' ', '\t'):
                continue
            e_raw = line[9:19]  # cols 10-19 (1-based), 0-based: 9-19
            de_raw = line[19:21]  # cols 20-21
            e_val, de_val, e_str, de_str = parse_ensdf_value(e_raw, de_raw)
            if e_val is not None:
                key = e_str.strip()
                records[key] = {'e': e_val, 'de': de_val, 'e_str': e_str.strip(), 'de_str': de_str.strip()}
                ordered.append((key, e_val, de_val, e_str.strip(), de_str.strip()))
    return records, ordered


def parse_adopted_from_7018(filepath):
    """Parse adopted file starting from L 7018.9 line.
    Returns list of level dicts with XREF, comment info etc.
    """
    with open(filepath, encoding='ascii', errors='replace') as f:
        lines = f.readlines()
    
    # Find start line
    start_idx = None
    for i, line in enumerate(lines):
        if '  L 7018.9' in line and line[7] == 'L':
            start_idx = i
            break
    if start_idx is None:
        print("ERROR: Could not find L 7018.9 in adopted file")
        sys.exit(1)
    
    levels = []
    current_level = None
    
    for line in lines[start_idx:]:
        if len(line) < 9:
            continue
        
        record_type = line[7] if len(line) > 7 else ' '
        cont_marker = line[5] if len(line) > 5 else ' '
        
        # Primary L-record
        if record_type == 'L' and line[6] == ' ' and cont_marker == ' ':
            if current_level is not None:
                levels.append(current_level)
            e_raw = line[9:19]
            de_raw = line[19:21]
            e_val, de_val, e_str, de_str = parse_ensdf_value(e_raw, de_raw)
            current_level = {
                'e_str': e_str.strip(),
                'de_str': de_str.strip(),
                'e': e_val,
                'de': de_val,
                'line': line.rstrip('\n'),
                'xref': None,
                'cl_e_comments': [],
                'has_K': False,
                'has_L': False,
                'K_ambiguous': False,  # K(*) notation
                'L_ambiguous': False,  # L(*) notation
            }
        
        # XREF line
        elif record_type == 'L' and line[4:6] == 'X ':
            if current_level is not None:
                xref_str = line[9:].rstrip('\n').strip()
                if xref_str.startswith('XREF='):
                    xref_str = xref_str[5:]
                current_level['xref'] = xref_str
                # Parse K and L presence
                # K(*) means K has ambiguous match
                # L(*) means L has ambiguous match
                xref_raw = xref_str
                
                # Check for K(*) - K with asterisk
                if re.search(r'K\(\*\)', xref_raw):
                    current_level['has_K'] = True
                    current_level['K_ambiguous'] = True
                elif re.search(r'(?<![A-Za-z])K(?!\()', xref_raw) or re.search(r'(?<![A-Za-z])K\([^*]', xref_raw):
                    # K appears but not K(*) - also handle K at end of string
                    # Simple check: K is in XREF but not with (*)
                    if 'K' in xref_raw and 'K(*)' not in xref_raw:
                        current_level['has_K'] = True
                
                if re.search(r'L\(\*\)', xref_raw):
                    current_level['has_L'] = True
                    current_level['L_ambiguous'] = True
                elif 'L' in xref_raw and 'L(*)' not in xref_raw:
                    current_level['has_L'] = True
                
                # More careful parsing for K and L with and without (*)
                # Re-parse carefully
                current_level['has_K'] = False
                current_level['has_L'] = False
                current_level['K_ambiguous'] = False
                current_level['L_ambiguous'] = False
                
                # Find all dataset letters and their modifiers
                # Pattern: letter possibly followed by (...) or (*) or (energy) etc.
                tokens = re.findall(r'([A-Z])(\([^)]*\))?', xref_raw)
                for letter, modifier in tokens:
                    is_ambiguous = modifier == '(*)'
                    if letter == 'K':
                        current_level['has_K'] = True
                        current_level['K_ambiguous'] = is_ambiguous
                    elif letter == 'L':
                        current_level['has_L'] = True
                        current_level['L_ambiguous'] = is_ambiguous
        
        # cL E$ comment line
        elif line[6:8] == 'cL' and cont_marker == ' ' and record_type == 'c':
            # Actually check col 6-7 for 'cL'
            pass
        
        # Check for cL E$ comment
        if len(line) >= 12:
            # Col 6-7 is the comment type, col 8 is 'L' for level
            # Format: ' 34CL cL E$...' -> positions [5:7]='cL', [7]='L'... wait
            # Actually in ENSDF: col 6 = 'c', col 7 = 'L', col 8 = ' ', col 9 = 'E$...'
            if line[5] == 'c' and line[6] == 'L' and line[7] == ' ':
                comment_text = line[9:].rstrip('\n')
                if current_level is not None:
                    current_level['cl_e_comments'].append(comment_text.strip())
            # Continuation comment: col 5 is digit (2-9)
            elif line[5].isdigit() and line[6] == 'c' and line[7] == 'L':
                comment_text = line[9:].rstrip('\n')
                if current_level is not None and current_level['cl_e_comments']:
                    # Append to last comment (continuation)
                    current_level['cl_e_comments'][-1] += ' ' + comment_text.strip()
    
    if current_level is not None:
        levels.append(current_level)
    
    return levels


def run_java_average(e1, de1, e2, de2):
    """Run Java_Average.py with two values and return (avg, unc_str, full_output)."""
    result = subprocess.run(
        [sys.executable, JAVA_AVG, str(e1), str(de1), str(e2), str(de2)],
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    return output


def extract_java_avg_result(output):
    """Extract the suggested average and uncertainty from Java_Average output."""
    # Look for "Suggested Adopted Result:" line
    for line in output.split('\n'):
        if 'Suggested Adopted Result' in line or 'suggested' in line.lower():
            # Try to parse value and uncertainty
            m = re.search(r'([\d.]+)\s*\{I([^\}]+)\}', line)
            if m:
                val_str = m.group(1)
                unc_str = m.group(2)
                return val_str, unc_str
    # Fallback: look for the numeric result line
    for line in output.split('\n'):
        m = re.search(r'Average\s*=\s*([\d.]+)\s*[+\-]\s*([\d.]+)', line, re.IGNORECASE)
        if m:
            return m.group(1), m.group(2)
    return None, None


def parse_comment_energy(comment_text):
    """Extract quoted energy value and uncertainty from cL E$ comment.
    Returns list of (value_str, unc_str, source) tuples.
    Example: 'weighted average of 7059.04 {I30} from {+33}S(p,|g) and 7057.7 {I20} from...'
    """
    results = []
    # Pattern: number {Innn} from source
    # Find all occurrences of value {Innn}
    pattern = r'([\d.]+)\s*\{I([\d+\-]+)\}'
    matches = re.findall(pattern, comment_text)
    for val, unc in matches:
        results.append((val, unc))
    return results


def format_for_comparison(e_str, de_str):
    """Format E and DE as they would appear in the ENSDF L-record."""
    return f"E={e_str}, DE={de_str}"


def main():
    print("=" * 80)
    print("Cl34 Adopted File Level Energy Cross-Check (from L 7018.9)")
    print("=" * 80)
    print()
    
    # Parse source datasets
    print("Parsing dataset K (Cl34_33s_p_g.ens)...")
    k_records, k_ordered = parse_l_records(K_FILE)
    print(f"  Found {len(k_ordered)} L-records in K")
    
    print("Parsing dataset L (Cl34_33s_p_p_resonances.ens)...")
    l_records, l_ordered = parse_l_records(L_FILE)
    print(f"  Found {len(l_ordered)} L-records in L")
    
    print("Parsing adopted file from L 7018.9...")
    adopted_levels = parse_adopted_from_7018(ADOPTED_FILE)
    print(f"  Found {len(adopted_levels)} L-records from 7018.9 onwards")
    print()
    
    # Build quick lookup by energy value (rounded to reasonable precision)
    def make_lookup(records_list):
        """Build lookup dict: key = rounded energy for fuzzy matching."""
        d = {}
        for key, e, de, e_str, de_str in records_list:
            d[round(e, 3)] = (key, e, de, e_str, de_str)
        return d
    
    k_lookup = make_lookup(k_ordered)
    l_lookup = make_lookup(l_ordered)
    
    def find_in_dataset(e_val, lookup, tolerance=0.15):
        """Find closest level in dataset within tolerance."""
        best = None
        best_diff = tolerance
        for key_e in lookup:
            diff = abs(key_e - e_val)
            if diff <= best_diff:
                best_diff = diff
                best = lookup[key_e]
        return best
    
    mismatches = []
    warnings = []
    
    for level in adopted_levels:
        e_adopted = level['e']
        de_adopted_str = level['de_str']
        e_str_adopted = level['e_str']
        xref = level['xref']
        has_K = level['has_K']
        has_L = level['has_L']
        K_amb = level['K_ambiguous']
        L_amb = level['L_ambiguous']
        
        if e_adopted is None:
            continue
        
        # Determine which datasets should contribute
        # If K(*): K is ambiguous, only use L
        # If L(*): L is ambiguous, only use K
        use_K = has_K and not K_amb
        use_L = has_L and not L_amb
        
        label = f"L {e_str_adopted} (XREF={xref})"
        
        if use_K and not use_L:
            # Should match K exactly
            k_match = find_in_dataset(e_adopted, k_lookup, tolerance=1.0)
            if k_match is None:
                mismatches.append({
                    'level': label,
                    'type': 'MISSING_IN_K',
                    'detail': f"Adopted E={e_str_adopted} not found in K dataset"
                })
            else:
                k_key, k_e, k_de, k_e_str, k_de_str = k_match
                # Check E
                if k_e_str != e_str_adopted:
                    mismatches.append({
                        'level': label,
                        'type': 'E_MISMATCH (K-only)',
                        'detail': f"Adopted E={e_str_adopted}, K has E={k_e_str}"
                    })
                # Check DE
                if k_de_str != de_adopted_str:
                    mismatches.append({
                        'level': label,
                        'type': 'DE_MISMATCH (K-only)',
                        'detail': f"Adopted DE={de_adopted_str!r}, K has DE={k_de_str!r}"
                    })
        
        elif use_L and not use_K:
            # Should match L exactly
            l_match = find_in_dataset(e_adopted, l_lookup, tolerance=1.0)
            if l_match is None:
                mismatches.append({
                    'level': label,
                    'type': 'MISSING_IN_L',
                    'detail': f"Adopted E={e_str_adopted} not found in L dataset"
                })
            else:
                l_key, l_e, l_de, l_e_str, l_de_str = l_match
                # Check E
                if l_e_str != e_str_adopted:
                    mismatches.append({
                        'level': label,
                        'type': 'E_MISMATCH (L-only)',
                        'detail': f"Adopted E={e_str_adopted}, L has E={l_e_str}"
                    })
                # Check DE
                if l_de_str != de_adopted_str:
                    mismatches.append({
                        'level': label,
                        'type': 'DE_MISMATCH (L-only)',
                        'detail': f"Adopted DE={de_adopted_str!r}, L has DE={l_de_str!r}"
                    })
        
        elif use_K and use_L:
            # Should be weighted average of K and L
            k_match = find_in_dataset(e_adopted, k_lookup, tolerance=5.0)
            l_match = find_in_dataset(e_adopted, l_lookup, tolerance=5.0)
            
            if k_match is None:
                mismatches.append({
                    'level': label,
                    'type': 'MISSING_IN_K (KL avg)',
                    'detail': f"Adopted E={e_str_adopted} not found in K dataset"
                })
                continue
            if l_match is None:
                mismatches.append({
                    'level': label,
                    'type': 'MISSING_IN_L (KL avg)',
                    'detail': f"Adopted E={e_str_adopted} not found in L dataset"
                })
                continue
            
            k_key, k_e, k_de, k_e_str, k_de_str = k_match
            l_key, l_e, l_de, l_e_str, l_de_str = l_match
            
            # 1. Check cL E$ comment quoted values match source
            cl_comments = ' '.join(level['cl_e_comments'])
            comment_values = parse_comment_energy(cl_comments)
            
            if len(comment_values) >= 2:
                # First value should be K, second should be L (or reverse - check by order in comment)
                # The comment format is usually "weighted average of K_val {Iunc} from {+33}S(p,g) and L_val {Iunc} from ..."
                # Determine which is K and which is L from comment context
                # K source: {+33}S(p,g) or {+33}S(p,|g)
                # L source: {+33}S(p,p) or resonances
                
                # Find positions of K and L mentions
                k_pos = min(
                    cl_comments.find('p,|g)') if 'p,|g)' in cl_comments else 99999,
                    cl_comments.find('p,g)') if 'p,g)' in cl_comments else 99999,
                )
                l_pos = min(
                    cl_comments.find('p,p)') if 'p,p)' in cl_comments else 99999,
                    cl_comments.find('resonances') if 'resonances' in cl_comments else 99999,
                )
                
                # Find positions of the value matches in the comment
                val_positions = []
                for val, unc in comment_values:
                    pos = cl_comments.find(val)
                    val_positions.append((pos, val, unc))
                val_positions.sort()
                
                if len(val_positions) >= 2:
                    # First value is the one appearing earlier in comment
                    v1_pos, v1_val, v1_unc = val_positions[0]
                    v2_pos, v2_val, v2_unc = val_positions[1]
                    
                    # Determine which is K and which is L based on source mention after value
                    # Default assumption: in most comments, K (p,g) is mentioned first
                    comment_v_K = None
                    comment_v_L = None
                    comment_unc_K = None
                    comment_unc_L = None
                    
                    # Check which value is closer to K and which to L
                    v1_diff_K = abs(float(v1_val) - k_e) if k_e else 999
                    v1_diff_L = abs(float(v1_val) - l_e) if l_e else 999
                    v2_diff_K = abs(float(v2_val) - k_e) if k_e else 999
                    v2_diff_L = abs(float(v2_val) - l_e) if l_e else 999
                    
                    # Assign based on proximity
                    if v1_diff_K <= v1_diff_L and v2_diff_L <= v2_diff_K:
                        comment_v_K, comment_unc_K = v1_val, v1_unc
                        comment_v_L, comment_unc_L = v2_val, v2_unc
                    elif v1_diff_L <= v1_diff_K and v2_diff_K <= v2_diff_L:
                        comment_v_L, comment_unc_L = v1_val, v1_unc
                        comment_v_K, comment_unc_K = v2_val, v2_unc
                    else:
                        # Ambiguous - just take order
                        comment_v_K, comment_unc_K = v1_val, v1_unc
                        comment_v_L, comment_unc_L = v2_val, v2_unc
                    
                    # Check comment K value against actual K
                    if comment_v_K and k_e_str:
                        if comment_v_K != k_e_str:
                            mismatches.append({
                                'level': label,
                                'type': 'COMMENT_K_VALUE_MISMATCH',
                                'detail': f"Comment quotes K={comment_v_K}, but K file has E={k_e_str}"
                            })
                        if comment_unc_K and k_de_str and comment_unc_K != k_de_str:
                            mismatches.append({
                                'level': label,
                                'type': 'COMMENT_K_UNC_MISMATCH',
                                'detail': f"Comment quotes K uncertainty={{I{comment_unc_K}}}, but K file has DE={k_de_str}"
                            })
                    
                    # Check comment L value against actual L
                    if comment_v_L and l_e_str:
                        if comment_v_L != l_e_str:
                            mismatches.append({
                                'level': label,
                                'type': 'COMMENT_L_VALUE_MISMATCH',
                                'detail': f"Comment quotes L={comment_v_L}, but L file has E={l_e_str}"
                            })
                        if comment_unc_L and l_de_str and comment_unc_L != l_de_str:
                            mismatches.append({
                                'level': label,
                                'type': 'COMMENT_L_UNC_MISMATCH',
                                'detail': f"Comment quotes L uncertainty={{I{comment_unc_L}}}, but L file has DE={l_de_str}"
                            })
            
            # 2. Run Java_Average.py to get expected adopted value
            if k_de is not None and l_de is not None:
                java_out = run_java_average(k_e, k_de, l_e, l_de)
                
                # Extract suggested result
                avg_val_str, avg_unc_str = extract_java_avg_result(java_out)
                
                if avg_val_str and avg_unc_str:
                    # Compare with adopted
                    try:
                        avg_val = float(avg_val_str)
                        avg_unc_int = int(avg_unc_str.strip('+').split('-')[0])
                        
                        # Count decimal places in adopted E
                        if '.' in e_str_adopted:
                            adp_dec = len(e_str_adopted.split('.')[1])
                        else:
                            adp_dec = 0
                        
                        # Count decimal places in avg result
                        if '.' in avg_val_str:
                            avg_dec = len(avg_val_str.split('.')[1])
                        else:
                            avg_dec = 0
                        
                        # Check if adopted E matches avg within rounding
                        diff = abs(e_adopted - avg_val)
                        tolerance_e = 0.5 * 10**(-avg_dec)
                        
                        if diff > tolerance_e:
                            mismatches.append({
                                'level': label,
                                'type': 'AVG_VALUE_MISMATCH',
                                'detail': (f"Adopted E={e_str_adopted}, Java_Average gives {avg_val_str} "
                                          f"(K={k_e_str}±{k_de_str}, L={l_e_str}±{l_de_str})")
                            })
                        
                        # Check uncertainty
                        if de_adopted_str and avg_unc_str.strip():
                            if de_adopted_str.strip() != avg_unc_str.strip():
                                mismatches.append({
                                    'level': label,
                                    'type': 'AVG_UNC_MISMATCH',
                                    'detail': (f"Adopted DE={de_adopted_str!r}, Java_Average gives DE={avg_unc_str!r} "
                                              f"(K={k_e_str}±{k_de_str}, L={l_e_str}±{l_de_str})")
                                })
                    except (ValueError, IndexError):
                        warnings.append(f"{label}: Could not parse Java_Average output: {avg_val_str}, {avg_unc_str}")
                else:
                    warnings.append(f"{label}: Java_Average gave no parseable output:\n{java_out[:300]}")
        
        elif not has_K and not has_L:
            # Level doesn't use K or L - skip (e.g., XREF=EF, XREF=GK is partially K)
            # Special handling: XREF=GK means G and K, so has_K should be True
            pass
        
        elif K_amb and not has_L and not use_L:
            # K(*) only - energy should be blank or something
            pass
        elif L_amb and not has_K and not use_K:
            pass
    
    # Print results
    print(f"MISMATCHES FOUND: {len(mismatches)}")
    print(f"WARNINGS: {len(warnings)}")
    print()
    
    if mismatches:
        print("=" * 80)
        print("MISMATCHES:")
        print("=" * 80)
        for i, m in enumerate(mismatches, 1):
            print(f"\n[{i}] {m['level']}")
            print(f"    Type: {m['type']}")
            print(f"    {m['detail']}")
    
    if warnings:
        print()
        print("=" * 80)
        print("WARNINGS (non-critical):")
        print("=" * 80)
        for w in warnings:
            print(f"  {w}")
    
    print()
    print("Done.")


if __name__ == '__main__':
    main()
