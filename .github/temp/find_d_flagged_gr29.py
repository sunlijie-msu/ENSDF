import re

lines = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').readlines()

current_level = 0.0
results = []

i = 0
while i < len(lines):
    s = lines[i].rstrip()

    # Track current level energy
    if re.match(r' 34CL  L ', s):
        try:
            current_level = float(s[9:19].strip())
        except:
            pass

    # G record: check for D flag at col 77 (0-indexed col 76)
    if re.match(r' 34CL  G ', s):
        flag = s[76] if len(s) > 76 else ' '
        ri_str = s[22:29].strip()
        dri_str = s[29:31].strip()

        if flag == 'D' and ri_str and ri_str != 'LT' and ri_str != 'GT':
            try:
                ri_val = float(ri_str)
            except:
                ri_val = None

            if ri_val is not None and ri_val != 100.0 and current_level > 6100:
                gamma_e = s[9:19].strip()
                # Now look ahead in the cG block for 1969Gr29 with {I..}
                block_lines = []
                j = i + 1
                while j < len(lines):
                    nxt = lines[j].rstrip()
                    if re.match(r' 34CL[2-9A-Z]?cG', nxt):
                        block_lines.append((j+1, nxt))
                        j += 1
                    else:
                        break
                block = ' '.join(bl for _, bl in block_lines)

                # Look for numeric 1969Gr29 RI with uncertainty
                m_gr = re.search(r'(\d[\d.]*)\s*\{I([^}]+)\}\s*\(1969Gr29\)', block)
                if m_gr:
                    gr29_val = m_gr.group(1)
                    gr29_unc = m_gr.group(2)
                    is_limit = False  # Already excluded < > by regex
                    
                    # Get DRI properly
                    dri_val = dri_str if dri_str not in ('LT','GT','') else ''

                    print(f"L={current_level:<10}  G={gamma_e:<10}  "
                          f"Da02_RI={ri_val:<8}  Da02_DRI={dri_val:<5}  "
                          f"Gr29={gr29_val}{{I{gr29_unc}}}  "
                          f"line={i+1}")
                    # Print the cG RI line
                    for lineno, bl in block_lines:
                        if 'cG RI' in bl and '1969Gr29' in bl:
                            print(f"  cG: {bl.strip()}")
    i += 1
