"""
Scan Cl34_33s_p_g.ens for:
1. Group A: G records with existing 2-source averages where 1969Gr29 is in "Other:"
2. Group C: D-flagged G records at L>6100 with numeric 1969Gr29 {I..}
"""
import re

fpath = r"A34/Cl34/new/Cl34_33s_p_g.ens"
lines = open(fpath, encoding='latin-1').readlines()

current_level = 0.0
results = []
group_a = []

def parse_comment_unc(val_str, unc_str):
    """Convert {INN} notation to float uncertainty given value string."""
    try:
        val = float(val_str)
        unc = float(unc_str)
        # determine decimal places of val
        if '.' in val_str:
            dec = len(val_str.split('.')[1])
        else:
            dec = 0
        actual_unc = unc * (10 ** (-dec))
        return val, actual_unc
    except:
        return None, None

def parse_dri_field(ri_str, dri_str):
    """Convert G record RI + DRI field values to float uncertainty."""
    try:
        ri = float(ri_str)
        dri = int(dri_str)
        if '.' in ri_str:
            dec = len(ri_str.rstrip('0').split('.')[1])
        else:
            dec = 0
        actual_unc = dri * (10 ** (-dec))
        return ri, actual_unc
    except:
        return None, None

i = 0
while i < len(lines):
    s = lines[i].rstrip()
    # Track current level energy
    if re.match(r' 34CL {2}L ', s):
        try:
            current_level = float(s[9:19].strip())
        except:
            pass

    # G record
    if re.match(r' 34CL {2}G ', s):
        padded = s.ljust(80)
        flag = padded[76]  # col 77 (1-based), index 76 (0-based)

        ri_str = s[22:29].strip() if len(s) > 22 else ''
        dri_str = s[29:31].strip() if len(s) > 31 else ''

        try:
            ri_val = float(ri_str)
        except:
            ri_val = None

        gamma_e = s[9:19].strip()

        # Read associated comment block (col 6 can be blank or continuation char)
        block_lines = []
        j = i + 1
        while j < len(lines):
            nxt = lines[j].rstrip()
            if re.match(r' 34CL[ 2-9A-Za-z]c[GL]', nxt):
                block_lines.append((j+1, nxt))
                j += 1
            else:
                break
        block = ' '.join(bl for _, bl in block_lines)

        # Search for 1969Gr29 with {I..} in comment block
        m_gr = re.search(r'(\d[\d.]*)\s*\{I(\d+)\}\s*\(1969Gr29\)', block)

        # ---------- GROUP C: D-flagged, L>6100, RI≠100, Gr29 present ----------
        if (flag == 'D' and ri_val is not None and ri_val != 100.0
                and current_level > 6100 and m_gr):
            gr29_val = float(m_gr.group(1))
            gr29_unc_code = int(m_gr.group(2))
            gr29_val_str = m_gr.group(1)
            # compute actual uncertainty from {I} notation
            _, gr29_unc = parse_comment_unc(gr29_val_str, m_gr.group(2))
            da02_ri, da02_unc = parse_dri_field(ri_str, dri_str)

            # Find Other: sources excluding 1969Gr29
            others = re.findall(r'(\d[\d.]*(?:\s*\{I\d+\})?)\s*\((\d{4}[A-Z][a-z]\d{2})\)', block)
            other_str = ', '.join(
                f"{val} ({src})" if '{I' not in val else val
                for val, src in others
                if '1969Gr29' not in src
            )

            results.append({
                'group': 'C',
                'level': current_level,
                'gamma': gamma_e,
                'da02_ri': da02_ri,
                'da02_unc': da02_unc,
                'da02_ri_str': ri_str,
                'da02_dri_str': dri_str,
                'gr29_val': gr29_val,
                'gr29_unc': gr29_unc,
                'gr29_val_str': gr29_val_str,
                'gr29_unc_code': gr29_unc_code,
                'other_str': other_str,
                'line': i+1,
                'block': block,
            })

        # ---------- GROUP A: two-source average in comments with Gr29 in Other: ----------
        m_avg = re.search(r'RI\$weighted average of ([\d.]+)\s*\{I(\d+)\}\s*\((\w+)\)\s+and\s+([\d.]+)\s*\{I(\d+)\}\s*\((\w+)\)', block)
        m_other_gr29 = re.search(r'[Oo]ther:.*?(\d[\d.]*)\s*\{I(\d+)\}\s*\(1969Gr29\)', block)
        if m_avg and m_other_gr29:
            v1 = float(m_avg.group(1)); u1_code = int(m_avg.group(2)); s1 = m_avg.group(3)
            v2 = float(m_avg.group(4)); u2_code = int(m_avg.group(5)); s2 = m_avg.group(6)
            gr29_val2 = float(m_other_gr29.group(1)); gr29_unc2_code = int(m_other_gr29.group(2))
            _, u1 = parse_comment_unc(m_avg.group(1), m_avg.group(2))
            _, u2 = parse_comment_unc(m_avg.group(4), m_avg.group(5))
            _, u_gr = parse_comment_unc(m_other_gr29.group(1), m_other_gr29.group(2))
            group_a.append({
                'group': 'A',
                'level': current_level,
                'gamma': gamma_e,
                'src1': s1, 'v1': v1, 'u1': u1, 'v1_str': m_avg.group(1), 'u1_code': u1_code,
                'src2': s2, 'v2': v2, 'u2': u2, 'v2_str': m_avg.group(4), 'u2_code': u2_code,
                'gr29_val': gr29_val2, 'gr29_unc': u_gr,
                'gr29_val_str': m_other_gr29.group(1),
                'gr29_unc_code': gr29_unc2_code,
                'line': i+1,
                'current_ri': ri_val,
                'ri_str': ri_str, 'dri_str': dri_str
            })

    i += 1

print("=" * 80)
print("GROUP A — Add 1969Gr29 to existing 2-source weighted averages")
print("=" * 80)
for case in group_a:
    print(f"\nL={case['level']:.2f}  G={case['gamma']}  line={case['line']}")
    print(f"  {case['v1_str']} {{I{case['u1_code']}}} ({case['src1']})")
    print(f"  {case['v2_str']} {{I{case['u2_code']}}} ({case['src2']})")
    print(f"  {case['gr29_val_str']} {{I{case['gr29_unc_code']}}} (1969Gr29)")
    print(f"  Java call: python .github/scripts/Java_Average.py {case['v1']} {case['u1']} {case['v2']} {case['u2']} {case['gr29_val']} {case['gr29_unc']}")

print("\n" + "=" * 80)
print("GROUP C — D-flagged gammas at L>6100, average 1977Da02 + 1969Gr29")
print("=" * 80)
for case in results:
    print(f"\nL={case['level']:.2f}  G={case['gamma']}  line={case['line']}")
    print(f"  1977Da02: {case['da02_ri_str']} (DRI={case['da02_dri_str']}) → unc={case['da02_unc']}")
    print(f"  1969Gr29: {case['gr29_val_str']} {{I{case['gr29_unc_code']}}} → unc={case['gr29_unc']}")
    print(f"  Java call: python .github/scripts/Java_Average.py {case['da02_ri']} {case['da02_unc']} {case['gr29_val']} {case['gr29_unc']}")

print(f"\nTotal Group A cases: {len(group_a)}")
print(f"Total Group C cases: {len(results)}")
