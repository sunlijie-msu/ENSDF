"""
Cross-check script: (p,d) dataset (XREF=K) vs adopted S35_adopted.ens
Checks for 48 Part-1 matched levels:
  1. Level energies considered (only for levels WITHOUT G records)
  2. XREF contains K
  3. cL J$ comment cites L-transfer from (p,d)
"""
import re

ADOPTED_FILE = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"
PD_FILE      = r"d:\X\ND\ENSDF\A35\S35\new\S35_36s_p_d.ens"

# Part-1 matched pairs: (p_d_E_keV, adopted_E_nominal, delta_keV)
# Format: (p_d energy, adopted energy label for lookup, energy tolerance)
MATCHED_LEVELS = [
    (0,    0.0,        1.0),
    (1569, 1572.370,   6.0),
    (1990, 1991.27,    3.0),
    (2348, 2347.779,   3.0),
    (2718, 2717.07,    3.0),
    (2937, 2938.62,    3.0),
    (3420, 3423.2,     5.0),
    (3558, 3558.079,   3.0),
    (3592, 3594.62,    5.0),
    (3800, 3801.952,   3.0),
    (3883, 3886.28,    5.0),
    (4023, 4027.2,     6.0),   # !! doublet concern
    (4107, 4105.6,     3.0),
    (4182, 4189.238,   10.0),
    (4300, 4302.6,     5.0),
    (4486, 4482,       6.0),
    (4574, 4576,       5.0),
    (4614, 4617,       5.0),
    (4838, 4839,       5.0),
    (4907, 4903.371,   6.0),   # !! doublet concern
    (4955, 4963.081,   10.0),  # !! probably wrong match
    (5121, 5127,       8.0),
    (5766, 5771,       7.0),
    (5844, 5841.482,   5.0),
    (6121, 6129,       10.0),
    (6338, 6334,       6.0),
    (6439, 6446,       9.0),
    (6550, 6545.1,     7.0),
    (6639, 6635.2,     6.0),
    (6682, 6684,       5.0),
    (7019, 7018.89,    3.0),   # !! doublet concern
    (7102, 7100.73,    3.0),
    (7151, 7143.27,    10.0),
    (7215, 7218.0,     5.0),
    (7249, 7253.2,     6.0),
    (7279, 7275.93,    5.0),
    (7326, 7331.00,    7.0),
    (7349, 7347.9,     3.0),
    (7441, 7442.14,    3.0),
    (7490, 7494.5,     7.0),
    (7753, 7749.7,     5.0),
    (7885, 7889.0,     6.0),
    (7980, 7974.19,    8.0),
    (8073, 8076.46,    6.0),
    (8103, 8093.0,     12.0),
    (8221, 8224.2,     5.0),
    (8270, 8273.3,     5.0),
    (8410, 8406.55,    6.0),
]

# p,d L-transfer values from source (from S35_36s_p_d.ens L-records)
PD_L_XFER = {
    0:    "2",
    1569: "0",
    1990: "3",
    2348: "1",
    2718: "2",
    2937: "2",
    3420: "2",
    3558: "(2)",
    3592: "(2)",
    3800: "1",
    3883: "3",
    4023: "(2)",
    4107: "(2)",
    4182: "1",
    4300: "(1)",
    4486: "3",
    4574: "2",
    4614: "2",
    4838: "(0)",
    4907: "0",
    4955: "2",
    5121: "0",
    5766: "2",
    5844: "(2)",
    6121: "(2)",
    6338: "0",
    6439: "(0)",
    6550: "2",
    6639: "2",
    6682: "0",
    7019: "(1)",
    7102: "(1)",
    7151: "(3)",
    7215: "2",     # inferred from 3/2+ Jp
    7249: "(2)",   # inferred from (3/2+) Jp
    7279: "2",     # inferred from 1/2+ Jp
    7326: "2",     # inferred from 1/2+ Jp
    7349: "(0)",   # inferred from (1/2+)
    7441: "2",     # inferred from 1/2+ Jp... wait no, 1/2+ is L=0 or L=2
    7490: "1",     # inferred from 1/2- Jp
    7753: "2",     # from 5/2+
    7885: "(2)",   # from (5/2+)
    7980: "1",     # from 3/2-
    8073: "(2)",   # from (5/2+)
    8103: "1",     # from 1/2-
    8221: "1",     # from 1/2-
    8270: "1",     # from 1/2-
    8410: "(2)",   # from (5/2+)
}

# p,d Jp values from source
PD_JP = {
    0: "3/2+", 1569: "1/2+", 1990: "7/2-", 2348: "3/2-", 2718: "5/2+",
    2937: "3/2+", 3420: "5/2+", 3558: "(5/2+)", 3592: "(5/2+)", 3800: "3/2-",
    3883: "7/2-", 4023: "(3/2+)", 4107: "(3/2+)", 4182: "1/2-", 4300: "(1/2-,3/2-)",
    4486: "7/2-", 4574: "3/2+", 4614: "5/2+", 4838: "(1/2+)", 4907: "1/2+",
    4955: "5/2+", 5121: "1/2+", 5766: "5/2+", 5844: "(5/2+)", 6121: "(3/2+)",
    6338: "1/2+", 6439: "(1/2+)", 6550: "3/2+", 6639: "5/2+", 6682: "1/2+",
    7019: "(1/2-,3/2-)", 7102: "(1/2-,3/2-)", 7151: "(7/2-)", 7215: "3/2+",
    7249: "(3/2+)", 7279: "1/2+", 7326: "1/2+", 7349: "(1/2+)", 7441: "1/2+",
    7490: "1/2-", 7753: "5/2+", 7885: "(5/2+)", 7980: "3/2-", 8073: "(5/2+)",
    8103: "1/2-", 8221: "1/2-", 8270: "1/2-", 8410: "(5/2+)",
}

# Note on L-transfers: The p,d Lfield in the ENS file gives L directly
# Let me re-read the p,d ENS L-records to get exact L-field values

def parse_adopted_file(filepath):
    """Parse adopted file into level blocks."""
    levels = []
    current = None

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for i, lraw in enumerate(lines):
        line = lraw.rstrip('\n')
        if len(line) < 8:
            continue
        # Check NUCID field = " 35S" or "35S " or similar
        nucid = line[:5]
        if not ('35S' in nucid or '35s' in nucid):
            continue

        col6 = line[5] if len(line) > 5 else ' '
        col7 = line[6] if len(line) > 6 else ' '
        col8 = line[7] if len(line) > 7 else ' '
        col9 = line[8] if len(line) > 8 else ' '

        # L-record: col6=space or digit/letter (blank for first), col7=space, col8=L, col9=space
        if col7 == ' ' and col8 == 'L' and col9 == ' ' and col6 == ' ':
            # New L-record
            E_str = line[9:19].strip() if len(line) > 19 else ''
            J_str = line[22:39].strip() if len(line) > 39 else ''
            try:
                E_val = float(E_str) if E_str else None
            except ValueError:
                E_val = None
            current = {
                'E': E_val,
                'E_str': E_str,
                'J': J_str,
                'line': line,
                'lineno': i + 1,
                'xref': None,
                'has_G': False,
                'jpi_comments': [],
                'e_comments': [],
            }
            levels.append(current)

        elif col7 == ' ' and col8 == 'G' and col9 == ' ' and col6 == ' ':
            # G-record
            if current is not None:
                current['has_G'] = True

        elif col6 == ' ' and col7 == 'X' and col8 == ' ' and col9 == 'L':
            # XREF line
            if current is not None:
                xval = line[9:].rstrip()
                current['xref'] = xval

        elif col6.upper() in ('C','2','3','4','5','6','7','8','9') and line[5:8] in ('cL ', '2cL', '3cL', '4cL', '5cL', '6cL', '7cL', '8cL', '9cL'):
            # comment line for L
            comment_text = line[9:].rstrip() if len(line) > 9 else ''
            if 'J$' in comment_text or (current and current.get('_in_j_comment')):
                if current is not None:
                    current['jpi_comments'].append(comment_text)
            if 'E$' in comment_text or (current and current.get('_in_e_comment')):
                if current is not None:
                    current['e_comments'].append(comment_text)
        else:
            # more careful parsing
            # cL pattern: col5=c, col6=L, col7=space
            # In ENSDF: cols 1-5 = NUCID, col6=CONT, col7=type indicator, col8=record type
            # Wait let me recount: 0-indexed or 1-indexed?
            # In the file line[0:5] = NUCID (cols 1-5)
            # line[5] = CONT (col 6)
            # line[6] = 'c' means comment
            # line[7] = 'L' means L-record comment
            pass

    return levels


def parse_adopted_file_v2(filepath):
    """Parse adopted file: extract L-blocks with XREF, G presence, J$ comments, E$ comments."""
    levels = []
    current = None
    in_j_comment = False
    in_e_comment = False

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for i, lraw in enumerate(lines):
        line = lraw.rstrip('\n')
        if len(line) < 8:
            continue

        nucid = line[:5]
        if '35S' not in nucid and '35s' not in nucid:
            continue

        col6 = line[5] if len(line) > 5 else ' '  # continuation
        col7 = line[6] if len(line) > 6 else ' '  # ' ' or 'c' or 'X'
        col8 = line[7] if len(line) > 7 else ' '  # record type: L G X c etc.
        col9 = line[8] if len(line) > 8 else ' '  # usually space

        # L-record: CONT=' ', col7=' ', col8='L', col9=' '
        if col6 == ' ' and col7 == ' ' and col8 == 'L' and col9 == ' ':
            E_str = line[9:19].strip() if len(line) > 19 else ''
            J_str = line[22:39].strip() if len(line) > 39 else ''
            try:
                E_val = float(E_str) if E_str else None
            except ValueError:
                E_val = None
            current = {
                'E': E_val, 'E_str': E_str, 'J': J_str,
                'line': line, 'lineno': i + 1,
                'xref': None, 'has_G': False,
                'j_comment_lines': [], 'e_comment_lines': [],
            }
            levels.append(current)
            in_j_comment = False
            in_e_comment = False

        # G-record: CONT=' ', col7=' ', col8='G', col9=' '
        elif col6 == ' ' and col7 == ' ' and col8 == 'G' and col9 == ' ':
            if current is not None:
                current['has_G'] = True
            in_j_comment = False
            in_e_comment = False

        # XREF line: CONT='X' at line[5], col7=' ', col8='L', col9=' '
        # Format: " 35S X L XREF=..." => line[5]='X', line[6]=' ', line[7]='L', line[8]=' '
        elif col6 == 'X' and col7 == ' ' and col8 == 'L' and col9 == ' ':
            if current is not None:
                xval = line[9:].rstrip()
                current['xref'] = xval

        # cL comment: CONT=' ' (col6), col7='c', col8='L', col9=' '  (first comment only)
        elif col6 == ' ' and col7 == 'c' and col8 == 'L' and col9 == ' ':
            if current is not None:
                comment_text = line[9:].rstrip() if len(line) > 9 else ''
                if 'J$' in comment_text:
                    in_j_comment = True
                    in_e_comment = False
                    current['j_comment_lines'].append(comment_text)
                elif 'E$' in comment_text:
                    in_e_comment = True
                    in_j_comment = False
                    current['e_comment_lines'].append(comment_text)
                else:
                    # continuation of previous comment type
                    if in_j_comment:
                        current['j_comment_lines'].append(comment_text)
                    elif in_e_comment:
                        current['e_comment_lines'].append(comment_text)
                    else:
                        pass  # unrelated comment, ignore

        # 2cL, 3cL etc: CONT='2','3',... col7='c', col8='L'
        elif col6 in '23456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' and col7 == 'c' and col8 == 'L':
            if current is not None:
                comment_text = line[9:].rstrip() if len(line) > 9 else ''
                if in_j_comment:
                    current['j_comment_lines'].append(comment_text)
                elif in_e_comment:
                    current['e_comment_lines'].append(comment_text)

        # New L-type continuation (2 L, F L) resets comments  
        elif col6 != ' ' and col7 == ' ' and col8 == 'L' and col9 == ' ':
            in_j_comment = False
            in_e_comment = False

        # Next level starts: any unrelated type
        elif col6 == ' ' and col7 not in ('c', 'X', ' ', 'x'):
            pass

    return levels


def parse_pd_l_values(filepath):
    """Read p,d L-transfer from L field (cols 56-64, 0-indexed 55:64) of L-records."""
    pd_levels = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if len(line) < 20:
            continue
        # Only first L-records (CONT=' ')
        if line[5] != ' ' or line[6] != ' ' or line[7] != 'L' or line[8] != ' ':
            continue
        E_str = line[9:19].strip()
        try:
            E = float(E_str) if E_str else None
        except ValueError:
            continue
        if E is None:
            continue
        # L field cols 56-64 (0-indexed 55:64)
        L_str = line[55:64].strip() if len(line) > 55 else ''
        Jp_str = line[22:39].strip() if len(line) > 39 else ''
        pd_levels[int(round(E))] = {'E': E, 'L': L_str, 'Jp': Jp_str}
    return pd_levels


def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print("Cross-check: (p,d) XREF=K vs S35_adopted.ens — 48 Part-1 Matched Levels")
    print("=" * 80)

    # Parse files
    adopted_levels = parse_adopted_file_v2(ADOPTED_FILE)
    pd_levels = parse_pd_l_values(PD_FILE)

    print(f"\n  Parsed {len(adopted_levels)} adopted levels")
    print(f"  Parsed {len(pd_levels)} p,d levels")
    print(f"\n  p,d L-transfer values read:")
    for e, d in sorted(pd_levels.items()):
        print(f"    E={d['E']}, L={d['L']!r}, Jp={d['Jp']!r}")

    # Build lookup table for adopted levels by energy
    def find_adopted(target_E, tol):
        best = None
        best_delta = tol + 1
        for lv in adopted_levels:
            if lv['E'] is None:
                continue
            delta = abs(lv['E'] - target_E)
            if delta <= tol and delta < best_delta:
                best_delta = delta
                best = lv
        return best

    print("\n" + "=" * 80)
    print("CHECK 1 — XREF contains K")
    print("CHECK 2 — Level energy source (for levels WITHOUT G records)")  
    print("CHECK 3 — J$ comment cites (p,d) / L-transfer")
    print("=" * 80)

    # Issues found
    xref_missing_k = []
    energy_not_sourced = []
    j_comment_missing = []

    for pd_e, adopted_e, tol in MATCHED_LEVELS:
        lv = find_adopted(adopted_e, tol)
        if lv is None:
            print(f"\n  [NOT FOUND] p_d E={pd_e} → adopted E={adopted_e} (no match within {tol} keV)")
            continue

        # Get p,d data
        pd_key = int(round(pd_e))
        pd_data = pd_levels.get(pd_key, None)
        pd_L = pd_data['L'] if pd_data else 'N/A'
        pd_Jp = pd_data['Jp'] if pd_data else 'N/A'

        print(f"\n  Level: adopted E={lv['E']} keV (line {lv['lineno']}), p_d E={pd_e} keV")
        print(f"    p_d Jp={pd_Jp}, L={pd_L}")
        print(f"    Adopted J={lv['J']!r}")

        # CHECK 1: XREF contains K
        xref = lv.get('xref', None)
        if xref is None:
            print(f"    XREF: MISSING (no XREF line found)")
            xref_missing_k.append((lv['E'], 'No XREF line'))
        elif 'K' not in xref:
            print(f"    XREF: '{xref}' -- MISSING K [ERROR]")
            xref_missing_k.append((lv['E'], xref))
        else:
            # Check if K has a parenthetical energy annotation (delta > 5 keV)
            delta = abs(pd_e - lv['E']) if lv['E'] is not None else 0
            k_match = re.search(r'K(\([^)]*\))?', xref)
            k_notation = k_match.group(0) if k_match else 'K'
            if delta > 5:
                print(f"    XREF: '{xref}' -- K present OK, delta={delta:.0f} keV (needs K({pd_e})? current={k_notation})")
            else:
                print(f"    XREF: '{xref}' -- K={k_notation} OK (delta={delta:.1f} keV)")

        # CHECK 2: Level energy source (only for levels WITHOUT G records)
        print(f"    Has G records: {lv['has_G']}")
        if not lv['has_G']:
            e_comments = ' '.join(lv['e_comment_lines'])
            if 'p,d' in e_comments or '36S(p,d)' in e_comments or '2026Jo01' in e_comments or 'Jo01' in e_comments or 'transfer' in e_comments.lower():
                print(f"    E$ comment: cites p,d ✓")
            else:
                if lv['e_comment_lines']:
                    print(f"    E$ comment: {lv['e_comment_lines']} — does not explicitly cite p,d ⚠")
                else:
                    print(f"    E$ comment: none — adopted E from where? (level has no G records) ⚠")
                energy_not_sourced.append(lv['E'])

        # CHECK 3: J$ comment cites L-transfer from (p,d)
        j_text = ' '.join(lv['j_comment_lines'])
        # Look for mentions of (p,d), p,d, 36S, 2026Jo01, L=N from p,d context
        pd_cited = any(kw in j_text for kw in [
            'p,d', '36S(p', '(p,d)', '2026Jo01', 'Jo01',
            '{+36}S(p', '36S)(p', '36)(p',
        ])
        if j_text:
            print(f"    J$ comment: {j_text[:120]}...")
            if pd_cited:
                print(f"    J$ cites p,d contribution: ✓")
            else:
                print(f"    J$ cites p,d/L: NOT FOUND ⚠")
                j_comment_missing.append((lv['E'], pd_L, pd_Jp, j_text[:80]))
        else:
            print(f"    J$ comment: (none)")
            if pd_L and pd_L != 'N/A':
                j_comment_missing.append((lv['E'], pd_L, pd_Jp, '(no J$ comment)'))

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nXREF missing K ({len(xref_missing_k)}):")
    for e, x in xref_missing_k:
        print(f"  E={e} keV: {x}")

    print(f"\nLevel energy not sourced to p,d ({len(energy_not_sourced)}) — levels w/o G records:")
    for e in energy_not_sourced:
        print(f"  E={e} keV")

    print(f"\nJ$ comment missing p,d citation ({len(j_comment_missing)}):")
    for e, L, Jp, txt in j_comment_missing:
        print(f"  E={e} keV (p,d L={L}, Jp={Jp}): {txt}")

    print(f"\nTotal issues: {len(xref_missing_k) + len(energy_not_sourced) + len(j_comment_missing)}")


if __name__ == '__main__':
    main()
