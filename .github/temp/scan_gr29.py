import re

lines = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').readlines()

cases = []
i = 0
while i < len(lines):
    s = lines[i].rstrip()
    if re.match(r' 34CL[2-9A-Z]?cG', s):
        block_lines = [s]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].rstrip()
            if re.match(r' 34CL[2-9A-Z]cG', nxt):
                block_lines.append(nxt)
                j += 1
            else:
                break
        block = ' '.join(bl.strip() for bl in block_lines)
        if 'cG RI' in block and '1969Gr29' in block:
            m_gr = re.search(r'([<>]?\d[\d.]*\s*(?:\{I[^}]+\})?)\s*\(1969Gr29\)', block)
            if m_gr:
                gr29_str = m_gr.group(1).strip()
                is_limit = gr29_str.startswith('<') or gr29_str.startswith('>')
                if not is_limit:
                    level_e, gamma_e, adopted_ri = '', '', ''
                    for k in range(i-1, max(0,i-40), -1):
                        lk = lines[k].rstrip()
                        if re.match(r' 34CL  L ', lk) and not level_e:
                            level_e = lk[9:19].strip()
                        if re.match(r' 34CL  G ', lk) and not gamma_e:
                            gamma_e = lk[9:19].strip()
                            adopted_ri = lk[22:29].strip()
                        if level_e and gamma_e:
                            break
                    has_average = 'average' in block.lower()
                    src_pattern = re.findall(r'\((\d{4}[A-Za-z]{2}\d{2})\)', block)
                    cases.append({
                        'lineno': i+1, 'level': level_e, 'gamma': gamma_e,
                        'adopted_ri': adopted_ri, 'gr29_val': gr29_str,
                        'has_avg': has_average, 'sources': src_pattern,
                        'block': '\n  '.join(block_lines)
                    })
    i += 1

# Separate into categories
avg_cases = [c for c in cases if c['has_avg']]
single_cases = [c for c in cases if not c['has_avg']]

print(f'Total cases with numeric 1969Gr29 RI: {len(cases)}')
print(f'  Already in average: {len(avg_cases)}')
print(f'  NOT in average yet: {len(single_cases)}')
print()
print('=== ALREADY HAS AVERAGE + numeric 1969Gr29 as Other: ===')
for c in avg_cases:
    print(f"  line {c['lineno']:4d}  L={c['level']:10s}  G={c['gamma']:8s}  adopted={c['adopted_ri']:8s}  1969Gr29={c['gr29_val']}")
    print(f"    {c['block'][:130]}")

print()
print('=== NO AVERAGE YET — single or multi source + numeric 1969Gr29 ===')
for c in single_cases:
    print(f"  line {c['lineno']:4d}  L={c['level']:10s}  G={c['gamma']:8s}  adopted={c['adopted_ri']:8s}  1969Gr29={c['gr29_val']:15s}  srcs={c['sources']}")
